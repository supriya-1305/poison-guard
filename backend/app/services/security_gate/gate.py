from pathlib import Path

MIN_CLEAN_ACCURACY = 0.85
MAX_ATTACK_SUCCESS_RATE = 0.02
MIN_VULNERABLE_ATTACK_SUCCESS_RATE = 0.90


def evaluate_security_gate(candidate, vulnerable, integrity_result=None):
    """Evaluate candidate evidence without authorizing model activation."""

    checks = {
        "candidate_evaluation_completed": (
            candidate.get("status") == "evaluated_not_yet_approved"
        ),
        "vulnerable_evaluation_completed": (
            vulnerable.get("status") == "evaluated_not_yet_approved"
        ),
        "same_test_sample_count": (
            candidate.get("test_samples") == vulnerable.get("test_samples")
        ),
        "same_attack_eligible_sample_count": (
            candidate.get("attack_eligible_samples")
            == vulnerable.get("attack_eligible_samples")
        ),
        "candidate_clean_accuracy_passes": (
            isinstance(candidate.get("clean_accuracy"), (int, float))
            and candidate["clean_accuracy"] >= MIN_CLEAN_ACCURACY
        ),
        "candidate_attack_success_rate_passes": (
            isinstance(candidate.get("attack_success_rate"), (int, float))
            and candidate["attack_success_rate"] <= MAX_ATTACK_SUCCESS_RATE
        ),
        "vulnerable_model_shows_attack": (
            isinstance(vulnerable.get("attack_success_rate"), (int, float))
            and vulnerable["attack_success_rate"]
            >= MIN_VULNERABLE_ATTACK_SUCCESS_RATE
        ),
    }

    if integrity_result is None:
        integrity_status = "NOT_CHECKED"
        decision = "MANUAL_REVIEW"
        reason = "Model integrity verification is required."
    else:
        integrity_status = integrity_result.get("integrity_status")
        if integrity_status == "MODIFIED":
            decision = "REJECT"
            reason = "Model checkpoint integrity verification failed."
        elif integrity_status != "VERIFIED":
            decision = "MANUAL_REVIEW"
            reason = "Model integrity could not be verified."
        elif not all(checks.values()):
            decision = "REJECT"
            reason = "One or more model validation checks failed."
        else:
            decision = "PASS_PENDING_MANUAL_REVIEW"
            reason = "Checks passed; independent manual approval is still required."

    if integrity_status == "MODIFIED":
        pass
    elif integrity_status == "VERIFIED" and not all(checks.values()):
        decision = "REJECT"
        reason = "One or more model validation checks failed."

    return {
        "project": "PoisonGuard",
        "stage": "Week 10 Model Security Gate",
        "candidate_model": candidate.get("model"),
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "integrity_status": integrity_status,
        "decision": decision,
        "reason": reason,
        "promotion_status": "not_promoted",
        "activation_authorized": False,
        "manual_review_required": True,
    }
