from backend.app.services import runtime_monitor


def test_monitor_returns_prediction_record():
    result = runtime_monitor.record_prediction(
        prediction=2,
        confidence=0.95,
        input_mean=0.45,
        input_std=0.20,
        model_version="test-model",
    )

    assert result["prediction_record"]["prediction"] == 2
    assert result["prediction_record"]["model_version"] == "test-model"
    assert "alerts" in result
    assert "alert_count" in result


def test_security_score_has_expected_fields():
    result = runtime_monitor.calculate_security_score()

    assert 0 <= result["security_score"] <= 100
    assert "predictions_logged" in result
    assert "incidents_recorded" in result


def test_incidents_are_a_list():
    assert isinstance(runtime_monitor.get_incidents(), list)
