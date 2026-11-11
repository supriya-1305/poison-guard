import pytest

from backend.app.services.attack_simulation.simulator import (
    SCENARIOS,
    run_all_simulations,
    simulate_attack,
)


def test_all_scenarios_are_available():
    assert len(SCENARIOS) == 3


@pytest.mark.parametrize("scenario", sorted(SCENARIOS))
def test_simulation_is_non_destructive(scenario):
    result = simulate_attack(scenario)
    assert result["simulated"] is True
    assert result["automatic_action_taken"] is False
    assert result["model_modified"] is False
    assert result["activation_authorized"] is False
    assert result["promotion_status"] == "not_promoted"


def test_checkpoint_tampering_is_rejected():
    result = simulate_attack("checkpoint_tampering")
    assert result["integrity_status"] == "MODIFIED"
    assert result["decision"] == "REJECT"


def test_high_risk_sample_requires_review():
    result = simulate_attack("high_risk_sample")
    assert result["risk_score"] == 95
    assert result["decision"] == "MANUAL_REVIEW"
    assert result["recommended_action"] == "QUARANTINE_PENDING_REVIEW"


def test_candidate_gate_failure_is_rejected():
    result = simulate_attack("candidate_gate_failure")
    assert result["decision"] == "REJECT"
    assert result["checks_passed"] < result["checks_total"]


def test_unknown_scenario_is_rejected():
    with pytest.raises(ValueError):
        simulate_attack("unknown_scenario")


def test_all_simulations_run():
    result = run_all_simulations()
    assert result["simulation_count"] == 3
    assert result["model_modified"] is False
    assert result["activation_authorized"] is False
