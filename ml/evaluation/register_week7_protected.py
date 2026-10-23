import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.services.model_registry import register_checkpoint

REPORT = ROOT / "experiments/week7/results/promotion_validation.json"
CHECKPOINT = ROOT / "models/week7/resnet18_sanitized_candidate.pth"
APPROVAL_FILE = ROOT / "experiments/week7/results/manual_approval.json"
OUTPUT_FILE = ROOT / "experiments/week7/results/protected_registration.json"


def main():
    if not REPORT.is_file():
        raise FileNotFoundError(f"Validation report missing: {REPORT}")

    report = json.loads(REPORT.read_text(encoding="utf-8"))

    if report.get("validation_status") != "passed_pending_manual_review":
        raise RuntimeError("Registration blocked: validation has not passed.")

    if report.get("promotion_status") != "not_promoted":
        raise RuntimeError("Unexpected promotion status; review required.")

    if not APPROVAL_FILE.is_file():
        raise RuntimeError(
            "Manual approval is missing. Registration was not performed."
        )

    approval = json.loads(APPROVAL_FILE.read_text(encoding="utf-8"))

    if approval.get("approved") is not True:
        raise RuntimeError("Manual approval is not granted.")

    if approval.get("candidate_sha256") != __import__("hashlib").sha256(
        CHECKPOINT.read_bytes()
    ).hexdigest():
        raise RuntimeError("Approval fingerprint does not match the checkpoint.")

    result = register_checkpoint(
        checkpoint=CHECKPOINT,
        label="v4-protected",
        validation_status="passed_pending_manual_review",
        metrics={
            "clean_accuracy": report["observed_metrics"][
                "candidate_clean_accuracy"
            ],
            "attack_success_rate": report["observed_metrics"][
                "candidate_attack_success_rate"
            ],
        },
    )

    output = {
        "registration": result,
        "promotion_status": "not_promoted",
        "active_model_changed": False,
        "note": (
            "Registered for tracking only. Registration does not approve "
            "or activate the model."
        ),
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
