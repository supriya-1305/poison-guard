import json

from backend.app.services import runtime_monitor as monitor


def test_week6_runtime_alert_rules(tmp_path, monkeypatch):
    # Keep test output separate from real runtime logs.
    monkeypatch.setattr(
        monitor, "PREDICTION_LOG", tmp_path / "predictions.jsonl"
    )
    monkeypatch.setattr(
        monitor, "INCIDENT_LOG", tmp_path / "incidents.jsonl"
    )

    # Test 1: low confidence should trigger an alert.
    monitor._recent.clear()
    result = monitor.record_prediction(
        prediction=2,
        confidence=0.40,
        input_mean=0.45,
        input_std=0.20,
        model_version="week6-test",
    )
    assert "LOW_CONFIDENCE" in [
        alert["type"] for alert in result["alerts"]
    ]

    # Test 2: unusually high input mean should trigger an alert.
    monitor._recent.clear()
    result = monitor.record_prediction(
        prediction=2,
        confidence=0.95,
        input_mean=0.90,
        input_std=0.20,
        model_version="week6-test",
    )
    assert "UNUSUAL_INPUT_MEAN" in [
        alert["type"] for alert in result["alerts"]
    ]

    # Test 3: unusually low input variation should trigger an alert.
    monitor._recent.clear()
    result = monitor.record_prediction(
        prediction=2,
        confidence=0.95,
        input_mean=0.45,
        input_std=0.01,
        model_version="week6-test",
    )
    assert "LOW_INPUT_VARIATION" in [
        alert["type"] for alert in result["alerts"]
    ]

    # Test 4: 10 consecutive target-class predictions should
    # trigger the concentration rule.
    monitor._recent.clear()
    final_result = None

    for _ in range(10):
        final_result = monitor.record_prediction(
            prediction=monitor.TARGET_CLASS,
            confidence=0.95,
            input_mean=0.45,
            input_std=0.20,
            model_version="week6-test",
        )

    assert final_result is not None
    assert "TARGET_CLASS_CONCENTRATION" in [
        alert["type"] for alert in final_result["alerts"]
    ]

    # Verify that predictions and incidents were written.
    prediction_lines = (
        tmp_path / "predictions.jsonl"
    ).read_text().splitlines()
    incident_lines = (
        tmp_path / "incidents.jsonl"
    ).read_text().splitlines()

    assert len(prediction_lines) == 13
    assert len(incident_lines) >= 4

    predictions = [json.loads(line) for line in prediction_lines]
    incidents = [json.loads(line) for line in incident_lines]

    assert predictions[-1]["model_version"] == "week6-test"
    assert all("status" in incident for incident in incidents)

    print("PASS: low-confidence alert")
    print("PASS: unusual-input-mean alert")
    print("PASS: low-input-variation alert")
    print("PASS: target-class-concentration alert")
    print("PASS: prediction and incident logs")
