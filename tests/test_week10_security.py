import pytest

from backend.app.services.explainability.explainer import build_explanation
from backend.app.services.provenance.integrity import (
    calculate_sha256,
    verify_sha256,
)


def test_xai_explains_detected_signal():
    result = build_explanation(
        sample_id="W10-001",
        risk_score=86,
        detector_signals=[
            {
                "name": "Activation Anomaly",
                "detected": True,
                "severity": "HIGH",
                "evidence": "Unusual activation pattern",
            }
        ],
    )
    assert result["explanation_count"] == 1
    assert result["automatic_action_taken"] is False


def test_xai_recommends_manual_review():
    result = build_explanation("W10-002", 86, [])
    assert result["recommendation"] == "QUARANTINE_PENDING_REVIEW"


def test_xai_rejects_invalid_risk_score():
    with pytest.raises(ValueError):
        build_explanation("W10-003", 101, [])


def test_sha256_verifies_unchanged_file(tmp_path):
    path = tmp_path / "model.bin"
    path.write_bytes(b"original model")
    digest = calculate_sha256(path)
    assert verify_sha256(path, digest)["integrity_status"] == "VERIFIED"


def test_sha256_detects_modified_file(tmp_path):
    path = tmp_path / "model.bin"
    path.write_bytes(b"original model")
    digest = calculate_sha256(path)
    path.write_bytes(b"modified model")
    result = verify_sha256(path, digest)
    assert result["integrity_status"] == "MODIFIED"
    assert result["revalidation_required"] is True


def test_sha256_rejects_invalid_digest(tmp_path):
    path = tmp_path / "model.bin"
    path.write_bytes(b"test")
    with pytest.raises(ValueError):
        verify_sha256(path, "invalid")
