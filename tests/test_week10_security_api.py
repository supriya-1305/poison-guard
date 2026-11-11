import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_security_gate_accepts_verified_candidate():
    model = Path("models/week7/resnet18_sanitized_candidate.pth")
    assert model.is_file()

    digest = hashlib.sha256(model.read_bytes()).hexdigest()

    response = client.post(
        "/security/gate",
        json={
            "model_path": "week7/resnet18_sanitized_candidate.pth",
            "expected_sha256": digest,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["integrity_status"] == "VERIFIED"
    assert result["checks_passed"] == 7
    assert result["activation_authorized"] is False
    assert result["promotion_status"] == "not_promoted"


def test_security_gate_rejects_path_traversal():
    response = client.post(
        "/security/gate",
        json={
            "model_path": "../../README.md",
            "expected_sha256": "invalid",
        },
    )

    assert response.status_code == 400


def test_explain_endpoint_is_registered():
    response = client.post(
        "/security/explain",
        json={
            "sample_id": "W10-API-TEST",
            "risk_score": 86,
            "detector_signals": [],
        },
    )

    assert response.status_code == 200
    assert response.json()["automatic_action_taken"] is False
