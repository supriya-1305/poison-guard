"""Safe, non-destructive Week 10 attack simulations."""

from datetime import datetime, timezone

from backend.app.services.security_gate.gate import evaluate_security_gate


SCENARIOS = {
    "checkpoint_tampering",
    "high_risk_sample",
    "candidate_gate_failure",
}


def simulate_attack(scenario: str) -> dict:
    """Simulate security events without modifying model files or activating models."""

    if scenario not in SCENARIOS:
        raise ValueError(
            f"Unknown scenario. Choose one of: {', '.join(sorted(SCENARIOS))}"
        )

    result = {
        "project": "PoisonGuard",
        "stage": "Week 10 Attack Simulation Lab",
        "scenario": scenario,
        "simulated": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "automatic_action_taken": False,
        "model_modified": False,
        "promotion_status": "not_promoted",
        "activation_authorized": False,
        "manual_review_required": True,
    }

    if scenario == "checkpoint_tampering":
        result.update({
            "event": "MODEL_INTEGRITY_FAILURE",
            "integrity_status": "MODIFIED",
            "decision": "REJECT",
            "reason": "Simulated checkpoint hash mismatch.",
            "recommended_action": "QUARANTINE_PENDING_REVIEW",
        })

    elif scenario == "high_risk_sample":
        result.update({
            "event": "HIGH_RISK_SAMPLE",
            "risk_score": 95,
            "detector_signals": [
                "Activation Clustering",
                "STRIP Detection",
            ],
            "decision": "MANUAL_REVIEW",
            "reason": "Simulated high-risk detector alert.",
            "recommended_action": "QUARANTINE_PENDING_REVIEW",
        })

    elif scenario == "candidate_gate_failure":
        candidate = {
            "model": "simulated_candidate",
            "status": "evaluated_not_yet_approved",
            "test_samples": 10000,
            "attack_eligible_samples": 9000,
            "clean_accuracy": 0.70,
            "attack_success_rate": 0.15,
        }
        vulnerable = {
            "model": "simulated_vulnerable_model",
            "status": "evaluated_not_yet_approved",
            "test_samples": 10000,
            "attack_eligible_samples": 9000,
            "clean_accuracy": 0.50,
            "attack_success_rate": 0.99,
        }
        gate_result = evaluate_security_gate(
            candidate,
            vulnerable,
            {"integrity_status": "VERIFIED"},
        )
        result.update({
            "event": "CANDIDATE_SECURITY_GATE_FAILURE",
            "decision": gate_result["decision"],
            "reason": gate_result["reason"],
            "checks": gate_result["checks"],
            "checks_passed": gate_result["checks_passed"],
            "checks_total": gate_result["checks_total"],
        })

    return result


def run_all_simulations() -> dict:
    """Run all predefined simulations and return their results."""
    results = [simulate_attack(name) for name in sorted(SCENARIOS)]
    return {
        "project": "PoisonGuard",
        "simulation_count": len(results),
        "results": results,
        "automatic_action_taken": False,
        "model_modified": False,
        "activation_authorized": False,
    }
