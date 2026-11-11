from typing import Any


def build_explanation(
    sample_id: str,
    risk_score: float,
    detector_signals: list[dict[str, Any]],
) -> dict[str, Any]:
    """Explain a security result using supplied detector evidence."""

    if not sample_id.strip():
        raise ValueError("sample_id cannot be empty")

    if not 0 <= risk_score <= 100:
        raise ValueError("risk_score must be between 0 and 100")

    explanations = []

    for signal in detector_signals:
        name = str(signal.get("name", "Unknown detector"))
        detected = bool(signal.get("detected", False))
        severity = str(signal.get("severity", "INFO")).upper()
        evidence = str(signal.get("evidence", ""))

        if detected:
            explanations.append({
                "detector": name,
                "severity": severity,
                "evidence": evidence,
                "reason": f"{name} reported a suspicious signal.",
            })

    if risk_score >= 80:
        recommendation = "QUARANTINE_PENDING_REVIEW"
    elif risk_score >= 50:
        recommendation = "MANUAL_REVIEW"
    else:
        recommendation = "CONTINUE_MONITORING"

    return {
        "sample_id": sample_id,
        "risk_score": round(float(risk_score), 2),
        "explanation_count": len(explanations),
        "explanations": explanations,
        "recommendation": recommendation,
        "automatic_action_taken": False,
    }
