import json
from pathlib import Path

from backend.app.services.security_gate.gate import evaluate_security_gate

ROOT = Path(__file__).resolve().parents[1]

VULNERABLE = json.loads(
    (ROOT / "experiments/week7/results/vulnerable_model_evaluation.json")
    .read_text()
)

CANDIDATE = json.loads(
    (ROOT / "experiments/week7/results/sanitized_candidate_evaluation.json")
    .read_text()
)


def test_valid_candidate_requires_manual_review():
    result = evaluate_security_gate(
        CANDIDATE, VULNERABLE,
        {"integrity_status": "VERIFIED"},
    )
    assert result["decision"] == "PASS_PENDING_MANUAL_REVIEW"
    assert result["activation_authorized"] is False
    assert result["promotion_status"] == "not_promoted"


def test_modified_checkpoint_is_rejected():
    result = evaluate_security_gate(
        CANDIDATE, VULNERABLE,
        {"integrity_status": "MODIFIED"},
    )
    assert result["decision"] == "REJECT"
    assert result["activation_authorized"] is False


def test_missing_integrity_requires_manual_review():
    result = evaluate_security_gate(CANDIDATE, VULNERABLE)
    assert result["decision"] == "MANUAL_REVIEW"
    assert result["manual_review_required"] is True


def test_failed_candidate_metrics_are_rejected():
    candidate = dict(CANDIDATE)
    candidate["clean_accuracy"] = 0.70

    result = evaluate_security_gate(
        candidate, VULNERABLE,
        {"integrity_status": "VERIFIED"},
    )
    assert result["decision"] == "REJECT"


def test_security_gate_never_authorizes_activation():
    result = evaluate_security_gate(
        CANDIDATE, VULNERABLE,
        {"integrity_status": "VERIFIED"},
    )
    assert result["activation_authorized"] is False
    assert result["promotion_status"] == "not_promoted"
