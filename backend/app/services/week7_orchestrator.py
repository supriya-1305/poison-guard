"""Week 7 runtime-alert orchestration.

Alerts create auditable incidents only. They do not automatically
quarantine models or trigger rollback.
"""

from backend.app.services.incident_response import (
    record_incident,
    record_response_action,
)


def process_runtime_alerts(
    alerts: list[dict],
    model_version: str,
) -> list[dict]:
    """Persist runtime alerts as Week 7 incidents."""

    incidents = []

    for alert in alerts:
        incident = record_incident(
            severity="MEDIUM",
            alert_type=str(alert["type"]),
            message=str(alert["message"]),
            model_version=model_version,
        )

        record_response_action(
            incident["incident_id"],
            "RUNTIME_ALERT_RECORDED",
            {
                "source": "runtime_monitor",
                "automatic_quarantine": False,
                "automatic_rollback": False,
            },
        )

        incidents.append({
            "incident_id": incident["incident_id"],
            "severity": incident["severity"],
            "alert_type": incident["alert_type"],
            "status": incident["status"],
        })

    return incidents
