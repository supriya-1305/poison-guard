import hashlib
import io
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from ml.models.resnet18 import create_model
from backend.app.services import runtime_monitor

from backend.app.services.week7_orchestrator import (
    process_runtime_alerts,
)

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = ROOT / "models" / "week5" / "backdoored_resnet18.pth"

app = FastAPI(
    title="PoisonGuard Runtime Monitoring API",
    description=(
        "Week 6 prototype for inference, runtime monitoring, "
        "model status, security scoring, and incident logging."
    ),
    version="0.1.0",
)

CLASS_NAMES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck",
]

# CIFAR-10 normalization. Confirm these values against your training script.
preprocess = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=(0.4914, 0.4822, 0.4465),
        std=(0.2470, 0.2435, 0.2616),
    ),
])

device = torch.device(
    "mps" if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available()
    else "cpu"
)

model = None
model_error = None
model_version = "unavailable"

active_checkpoint = CHECKPOINT

def load_model():
    global model, model_error, model_version, active_checkpoint

    if not CHECKPOINT.exists():
        model_error = f"Checkpoint not found: {CHECKPOINT}"
        return

    try:
        candidate = create_model()
        state = torch.load(
            CHECKPOINT,
            map_location="cpu",
            weights_only=True,
        )
        candidate.load_state_dict(state)
        candidate.to(device)
        candidate.eval()

        digest = hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest()[:12]

        model = candidate
        active_checkpoint = CHECKPOINT
        model_version = f"week5-{digest}"
        model_error = None
    except Exception as exc:
        model = None
        model_error = f"{type(exc).__name__}: {exc}"


@app.on_event("startup")
def startup_event():
    load_model()


def run_prediction(image: Image.Image) -> dict:
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model unavailable: {model_error}",
        )

    # Input statistics are measured on RGB pixels in the [0, 1] range,
    # before CIFAR-10 normalization.
    rgb = image.convert("RGB").resize((32, 32))
    raw = np.asarray(rgb, dtype=np.float32) / 255.0
    input_mean = float(raw.mean())
    input_std = float(raw.std())

    tensor = preprocess(rgb).unsqueeze(0).to(device)

    with torch.inference_mode():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)
        confidence_tensor, predicted_tensor = probabilities.max(dim=1)

    predicted = int(predicted_tensor.item())
    confidence = float(confidence_tensor.item())

    monitoring = runtime_monitor.record_prediction(
        prediction=predicted,
        confidence=confidence,
        input_mean=input_mean,
        input_std=input_std,
        model_version=model_version,
    )
   
    week7_incidents = process_runtime_alerts(
        alerts=monitoring["alerts"],
        model_version=model_version,
    )

    return {
        "prediction": predicted,
        "class_name": CLASS_NAMES[predicted],
        "confidence": round(confidence, 6),
        "timestamp": monitoring["prediction_record"]["timestamp"],
        "input_statistics": {
            "mean": round(input_mean, 6),
            "std": round(input_std, 6),
        },
        "model_version": model_version,
        "monitoring": {
            "alert_count": monitoring["alert_count"],
            "alerts": monitoring["alerts"],
            "week7_incidents": week7_incidents,
        },
    }


@app.get("/")
def root():
    return {
        "service": "PoisonGuard Runtime Monitoring API",
        "week": 6,
        "docs": "/docs",
        "model_status": "/model/status",
    }


@app.get("/health")
def health():
    return {
        "api_status": "running",
        "model_loaded": model is not None,
        "device": str(device),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(
            status_code=415,
            detail="Upload a PNG, JPEG, or WEBP image.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Maximum upload size is 5 MB.")

    try:
        image = Image.open(io.BytesIO(content))
        image.load()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Invalid image file.")

    return run_prediction(image)


@app.post("/scan/dataset")
async def scan_dataset(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one image.")

    if len(files) > 100:
        raise HTTPException(
            status_code=413,
            detail="Maximum 100 images per scan.",
        )

    results = []
    for uploaded in files:
        content = await uploaded.read()
        try:
            image = Image.open(io.BytesIO(content))
            image.load()
            result = run_prediction(image)
            results.append({
                "filename": uploaded.filename,
                "status": "scanned",
                **result,
            })
        except HTTPException as exc:
            results.append({
                "filename": uploaded.filename,
                "status": "error",
                "error": str(exc.detail),
            })
        except (UnidentifiedImageError, OSError):
            results.append({
                "filename": uploaded.filename,
                "status": "error",
                "error": "Invalid image file.",
            })

    return {
        "scanned_count": sum(r["status"] == "scanned" for r in results),
        "error_count": sum(r["status"] == "error" for r in results),
        "results": results,
        "note": "This scans inference behaviour; it does not prove images are poisoned.",
    }


@app.post("/scan/model")
def scan_model():
    load_model()
    return {
        "checkpoint": str(active_checkpoint.relative_to(ROOT)),
        "checkpoint_exists": CHECKPOINT.exists(),
        "model_loaded": model is not None,
        "model_version": model_version,
        "device": str(device),
        "error": model_error,
    }


@app.get("/model/status")
def model_status():
    return {
        "model_loaded": model is not None,
        "model_version": model_version,
        "checkpoint": str(active_checkpoint.relative_to(ROOT)),
        "device": str(device),
        "error": model_error,
    }


@app.get("/security-score")
def security_score():
    return runtime_monitor.calculate_security_score()


@app.get("/incidents")
def incidents():
    return {
        "count": len(runtime_monitor.get_incidents()),
        "incidents": runtime_monitor.get_incidents()[-100:],
    }


@app.post("/rollback")
def rollback():
    """Safely switch to the validated baseline checkpoint."""
    global model, model_error, model_version, active_checkpoint   
 
    from backend.app.services.incident_response import (
        list_incidents,
        record_response_action,
    )

    baseline = ROOT / "models" / "resnet18_baseline.pth"

    if not baseline.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Baseline checkpoint not found: {baseline}",
        )

    try:
        candidate = create_model(num_classes=10)
        state = torch.load(
            baseline,
            map_location="cpu",
            weights_only=True,
        )
        candidate.load_state_dict(state)
        candidate.to(device)
        candidate.eval()
        digest = hashlib.sha256(baseline.read_bytes()).hexdigest()[:12]
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Rollback validation failed; active model unchanged: {exc}",
        ) from exc

    previous_version = model_version
    previous_checkpoint = active_checkpoint
    new_version = f"rollback-baseline-{digest}"
   
 
    # Switch only after the candidate has loaded successfully.
    model = candidate
    active_checkpoint = baseline
    model_version = new_version
    model_error = None

    incidents = list_incidents(limit=100)
    active_incident = next(
        (item for item in reversed(incidents)
         if item.get("status") == "OPEN"),
        None,
    )
    incident_id = (
        active_incident["incident_id"]
        if active_incident
        else "manual-rollback"
    )

    record_response_action(
        incident_id=incident_id,
        action="ROLLBACK_COMPLETED",
        details={
                "previous_model_version": previous_version,
                "previous_checkpoint": str(previous_checkpoint.relative_to(ROOT)),
                "active_model_version": new_version,
                "checkpoint": str(baseline.relative_to(ROOT)),
                "checkpoint_sha256_prefix": digest,
                "reason": "Validated baseline rollback",
        },
    )

    return {
        "success": True,
        "message": "Baseline model loaded and activated.",
        "previous_model_version": previous_version,
        "active_model_version": new_version,
        "checkpoint": str(baseline.relative_to(ROOT)),
        "incident_id": incident_id,
    }


@app.post("/retrain")
def retrain():
    raise HTTPException(
        status_code=501,
        detail=(
            "Retraining is not implemented in Week 6. "
            "Use a separate validated training workflow; do not retrain "
            "automatically from runtime alerts."
        ),
    )


@app.get("/registry/versions")
def registry_versions():
    """List model versions registered in MLflow."""
    from backend.app.services.model_registry import (
        list_registered_versions,
    )

    versions = list_registered_versions()
    return {
        "model_name": "PoisonGuard-ResNet18",
        "count": len(versions),
        "versions": versions,
    }


@app.get("/week7/incidents")
def week7_incidents():
    """List Week 7 incident records."""
    from backend.app.services.incident_response import (
        list_incidents,
    )

    records = list_incidents(limit=100)
    return {
        "count": len(records),
        "incidents": records,
    }


@app.get("/week7/audit")
def week7_audit():
    """List Week 7 incident-response audit events."""
    from backend.app.services.incident_response import (
        list_response_audit,
    )

    records = list_response_audit(limit=100)
    return {
        "count": len(records),
        "events": records,
    }

