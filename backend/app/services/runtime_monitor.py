import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = ROOT / "experiments" / "week6" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

PREDICTION_LOG = LOG_DIR / "predictions.jsonl"
INCIDENT_LOG = LOG_DIR / "incidents.jsonl"

_lock = Lock()
_recent = deque(maxlen=50)

# Demonstration thresholds. Validate these against clean validation data
# before treating alerts as reliable security decisions.
LOW_CONFIDENCE_THRESHOLD = 0.60
TARGET_CLASS = 0
TARGET_CLASS_RATE_THRESHOLD = 0.80


def _append_jsonl(path: Path, record: dict) -> None:
    with _lock:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")


def get_recent_predictions() -> list:
    with _lock:
        return list(_recent)


def record_prediction(
    prediction: int,
    confidence: float,
    input_mean: float,
    input_std: float,
    model_version: str,
) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()

    record = {
        "timestamp": timestamp,
        "prediction": int(prediction),
        "confidence": round(float(confidence), 6),
        "input_mean": round(float(input_mean), 6),
        "input_std": round(float(input_std), 6),
        "model_version": model_version,
    }

    alerts = []

    if confidence < LOW_CONFIDENCE_THRESHOLD:
        alerts.append({
            "type": "LOW_CONFIDENCE",
            "message": "Prediction confidence is below the configured threshold.",
        })

    # These are deliberately broad image-statistic heuristics.
    # They flag unusual inputs, not proof of a backdoor attack.
    if input_mean < 0.15 or input_mean > 0.85:
        alerts.append({
            "type": "UNUSUAL_INPUT_MEAN",
            "message": "Input pixel mean is outside the configured range.",
        })

    if input_std < 0.05:
        alerts.append({
            "type": "LOW_INPUT_VARIATION",
            "message": "Input has unusually low pixel variation.",
        })

    with _lock:
        _recent.append(record)
        recent = list(_recent)

    if len(recent) >= 10:
        target_rate = sum(
            item["prediction"] == TARGET_CLASS for item in recent
        ) / len(recent)

        if target_rate >= TARGET_CLASS_RATE_THRESHOLD:
            alerts.append({
                "type": "TARGET_CLASS_CONCENTRATION",
                "message": (
                    f"{target_rate:.1%} of the recent predictions are "
                    f"target class {TARGET_CLASS}; investigate the pattern."
                ),
            })

    _append_jsonl(PREDICTION_LOG, record)

    for alert in alerts:
        incident = {
            **alert,
            "timestamp": timestamp,
            "prediction": int(prediction),
            "confidence": round(float(confidence), 6),
            "model_version": model_version,
            "status": "OPEN",
        }
        _append_jsonl(INCIDENT_LOG, incident)

    return {
        "prediction_record": record,
        "alerts": alerts,
        "alert_count": len(alerts),
    }


def read_jsonl(path: Path) -> list:
    if not path.exists():
        return []

    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def get_incidents() -> list:
    return read_jsonl(INCIDENT_LOG)


def calculate_security_score() -> dict:
    predictions = read_jsonl(PREDICTION_LOG)
    incidents = get_incidents()

    recent_incidents = incidents[-100:]
    count = len(recent_incidents)

    # Simple demonstrator score: 100 means no recorded alerts.
    # This is NOT a calibrated probability of compromise.
    score = max(0, 100 - min(100, count * 10))

    return {
        "security_score": score,
        "interpretation": (
            "No recent alerts recorded"
            if count == 0
            else "Monitoring alerts exist; review incidents"
        ),
        "predictions_logged": len(predictions),
        "incidents_recorded": len(incidents),
        "scoring_note": (
            "Preliminary rule-based score, not a validated security rating."
        ),
    }
