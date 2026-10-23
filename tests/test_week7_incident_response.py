
import json

import pytest

from backend.app.services import incident_response as response


def test_critical_incident_is_persisted(tmp_path, monkeypatch):
    monkeypatch.setattr(
        response, "INCIDENTS_FILE", tmp_path / "incidents.jsonl"
    )
    monkeypatch.setattr(
        response, "AUDIT_FILE", tmp_path / "audit.jsonl"
    )

    incident = response.record_incident(
        severity="CRITICAL",
        alert_type="BACKDOOR_RISK",
        message="Controlled test incident",
        model_version="2",
        risk_score=97.33,
    )

    records = response.list_incidents()

    assert incident["severity"] == "CRITICAL"
    assert incident["status"] == "OPEN"
    assert incident["model_version"] == "2"
    assert len(records) == 1
    assert records[0]["incident_id"] == incident["incident_id"]


def test_invalid_severity_is_rejected():
    with pytest.raises(ValueError):
        response.record_incident(
            severity="UNKNOWN",
            alert_type="TEST",
            message="Invalid severity",
            model_version="1",
        )


def test_response_action_is_audited(tmp_path, monkeypatch):
    monkeypatch.setattr(
        response, "INCIDENTS_FILE", tmp_path / "incidents.jsonl"
    )
    monkeypatch.setattr(
        response, "AUDIT_FILE", tmp_path / "audit.jsonl"
    )

    event = response.record_response_action(
        "incident-test-123",
        "ALERT_RECORDED",
        {"channel": "local-audit"},
    )

    audit = response.list_response_audit()

    assert event["action"] == "ALERT_RECORDED"
    assert audit[-1]["incident_id"] == "incident-test-123"
    assert audit[-1]["details"]["channel"] == "local-audit"


def test_incident_file_contains_valid_json_lines(
    tmp_path, monkeypatch
):
    incidents_file = tmp_path / "incidents.jsonl"
    monkeypatch.setattr(response, "INCIDENTS_FILE", incidents_file)
    monkeypatch.setattr(
        response, "AUDIT_FILE", tmp_path / "audit.jsonl"
    )

    response.record_incident(
        severity="HIGH",
        alert_type="TEST_ALERT",
        message="JSONL format test",
        model_version="1",
    )

    lines = incidents_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["alert_type"] == "TEST_ALERT"

