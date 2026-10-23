
import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from mlflow import MlflowClient

from backend.app.services.model_registry import (
    MODEL_NAME,
    TRACKING_URI,
)


ROOT = Path(__file__).resolve().parents[3]
WEEK7_DIR = ROOT / "experiments" / "week7"
INCIDENTS_FILE = WEEK7_DIR / "incidents.jsonl"
AUDIT_FILE = WEEK7_DIR / "response_audit.jsonl"

_lock = threading.Lock()


def _append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON record without replacing earlier records."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with _lock:
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    records = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                # Preserve processing if an older line is malformed.
                continue

    return records


def record_incident(
    *,
    severity: str,
    alert_type: str,
    message: str,
    model_version: str,
    risk_score: float | None = None,
) -> dict:
    """Create a persistent incident record."""
    allowed = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    severity = severity.upper()

    if severity not in allowed:
        raise ValueError(
            f"Severity must be one of {sorted(allowed)}"
        )

    incident = {
        "incident_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": severity,
        "alert_type": alert_type,
        "message": message,
        "model_version": model_version,
        "risk_score": risk_score,
        "status": "OPEN",
        "response_actions": [],
    }

    _append_jsonl(INCIDENTS_FILE, incident)
    _append_jsonl(
        AUDIT_FILE,
        {
            "timestamp": incident["timestamp"],
            "incident_id": incident["incident_id"],
            "action": "INCIDENT_CREATED",
            "model_version": model_version,
            "severity": severity,
        },
    )

    return incident


def quarantine_model_version(
    version: str,
    incident_id: str,
) -> dict:
    """
    Mark a registered model version as quarantined.

    This updates registry metadata; it does not delete the checkpoint
    or change the model currently loaded by the API.
    """
    client = MlflowClient(
        tracking_uri=TRACKING_URI,
        registry_uri=TRACKING_URI,
    )

    model_version = client.get_model_version(
        MODEL_NAME, str(version)
    )

    client.set_model_version_tag(
        MODEL_NAME, str(version), "validation_status",
        "quarantined",
    )
    client.set_model_version_tag(
        MODEL_NAME, str(version), "promotion_status",
        "blocked",
    )
    client.set_model_version_tag(
        MODEL_NAME, str(version), "incident_id",
        incident_id,
    )

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incident_id": incident_id,
        "action": "MODEL_VERSION_QUARANTINED",
        "model_name": MODEL_NAME,
        "model_version": str(version),
    }
    _append_jsonl(AUDIT_FILE, event)

    return {
        "quarantined": True,
        "model_name": MODEL_NAME,
        "version": str(model_version.version),
        "incident_id": incident_id,
        "promotion_status": "blocked",
    }


def record_response_action(
    incident_id: str,
    action: str,
    details: dict | None = None,
) -> dict:
    """Append an audit event for a response step."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incident_id": incident_id,
        "action": action,
        "details": details or {},
    }
    _append_jsonl(AUDIT_FILE, event)
    return event


def list_incidents(limit: int = 100) -> list[dict]:
    """Return the most recent incident records."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    return _read_jsonl(INCIDENTS_FILE)[-limit:]


def list_response_audit(limit: int = 100) -> list[dict]:
    """Return the most recent response audit events."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    return _read_jsonl(AUDIT_FILE)[-limit:]

