from backend.app.services import week7_orchestrator as orchestrator


def test_runtime_alert_creates_week7_incident_and_audit(
    tmp_path, monkeypatch
):
    from backend.app.services import incident_response

    monkeypatch.setattr(
        incident_response,
        "INCIDENTS_FILE",
        tmp_path / "incidents.jsonl",
    )
    monkeypatch.setattr(
        incident_response,
        "AUDIT_FILE",
        tmp_path / "audit.jsonl",
    )

    incidents = orchestrator.process_runtime_alerts(
        alerts=[
            {
                "type": "LOW_CONFIDENCE",
                "message": "Controlled test alert",
            }
        ],
        model_version="test-model",
    )

    assert len(incidents) == 1
    assert incidents[0]["alert_type"] == "LOW_CONFIDENCE"
    assert incidents[0]["severity"] == "MEDIUM"
    assert incidents[0]["status"] == "OPEN"

    records = incident_response.list_incidents()
    audit = incident_response.list_response_audit()

    assert len(records) == 1
    assert records[0]["model_version"] == "test-model"
    assert audit[-1]["action"] == "RUNTIME_ALERT_RECORDED"


def test_no_alerts_create_no_week7_incidents():
    incidents = orchestrator.process_runtime_alerts(
        alerts=[],
        model_version="test-model",
    )

    assert incidents == []
