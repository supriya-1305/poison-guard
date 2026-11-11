from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.services.explainability.explainer import build_explanation
from backend.app.services.provenance.integrity import verify_sha256

router = APIRouter(tags=["Week 10 Security"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_ROOT = (PROJECT_ROOT / "models").resolve()


@router.post("/security/explain")
def explain_security_result(payload: dict):
    try:
        return build_explanation(
            sample_id=payload.get("sample_id", ""),
            risk_score=payload.get("risk_score"),
            detector_signals=payload.get("detector_signals", []),
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/security/verify-integrity")
def verify_model_integrity(payload: dict):
    relative_path = payload.get("model_path")
    expected_hash = payload.get("expected_sha256")

    if not isinstance(relative_path, str) or not relative_path.strip():
        raise HTTPException(status_code=422, detail="model_path is required")

    if not isinstance(expected_hash, str):
        raise HTTPException(status_code=422, detail="expected_sha256 is required")

    candidate = (MODELS_ROOT / relative_path).resolve()

    if not candidate.is_relative_to(MODELS_ROOT):
        raise HTTPException(status_code=400, detail="Model path must remain inside models/")

    try:
        return verify_sha256(candidate, expected_hash)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
