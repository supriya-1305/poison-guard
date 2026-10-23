
import hashlib
from pathlib import Path
from typing import Any

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException


ROOT = Path(__file__).resolve().parents[3]
MODEL_NAME = "PoisonGuard-ResNet18"
EXPERIMENT_NAME = "PoisonGuard-Week7"
TRACKING_URI = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

# Use the same local SQLite store for experiment tracking and registration.
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_registry_uri(TRACKING_URI)


def checkpoint_sha256(checkpoint: Path) -> str:
    """Return a SHA-256 fingerprint for a model checkpoint."""
    digest = hashlib.sha256()

    with checkpoint.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _client() -> MlflowClient:
    return MlflowClient(
        tracking_uri=TRACKING_URI,
        registry_uri=TRACKING_URI,
    )


def register_checkpoint(
    checkpoint: str | Path,
    label: str,
    validation_status: str = "unvalidated",
    metrics: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Record a checkpoint in MLflow.

    Registration does not make the model active or production-approved.
    """
    checkpoint = Path(checkpoint).resolve()

    if not checkpoint.is_file():
        raise FileNotFoundError(
            f"Checkpoint does not exist: {checkpoint}"
        )

    if not label.strip():
        raise ValueError("Model label cannot be empty.")

    digest = checkpoint_sha256(checkpoint)
    client = _client()

    try:
        client.get_registered_model(MODEL_NAME)
    except MlflowException:
        try:
            client.create_registered_model(MODEL_NAME)
        except MlflowException:
            # Another process may have created it between these calls.
            client.get_registered_model(MODEL_NAME)

    # Make repeated registration of the same checkpoint idempotent.
    for existing in client.search_model_versions(
        f"name='{MODEL_NAME}'"
    ):
        if existing.tags.get("checkpoint_sha256") == digest:
            return {
                "registered": True,
                "created": False,
                "model_name": MODEL_NAME,
                "version": existing.version,
                "label": existing.tags.get(
                    "poison_guard_label", label
                ),
                "validation_status": existing.tags.get(
                    "validation_status", "unvalidated"
                ),
                "checkpoint_sha256": digest,
            }

    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(
        run_name=f"register-{label}"
    ) as run:
        mlflow.log_param("model_label", label)
        mlflow.log_param("checkpoint_sha256", digest)
        mlflow.log_param("source_filename", checkpoint.name)

        if metrics:
            for name, value in metrics.items():
                mlflow.log_metric(name, float(value))

        mlflow.log_artifact(
            str(checkpoint),
            artifact_path="checkpoints",
        )

        source = (
            f"runs:/{run.info.run_id}/"
            f"checkpoints/{checkpoint.name}"
        )

        version = client.create_model_version(
            name=MODEL_NAME,
            source=source,
            run_id=run.info.run_id,
            description=f"PoisonGuard model: {label}",
        )

    client.set_model_version_tag(
        MODEL_NAME, version.version,
        "poison_guard_label", label,
    )
    client.set_model_version_tag(
        MODEL_NAME, version.version,
        "checkpoint_sha256", digest,
    )
    client.set_model_version_tag(
        MODEL_NAME, version.version,
        "validation_status", validation_status,
    )
    client.set_model_version_tag(
        MODEL_NAME, version.version,
        "promotion_status", "not_promoted",
    )

    return {
        "registered": True,
        "created": True,
        "model_name": MODEL_NAME,
        "version": version.version,
        "label": label,
        "validation_status": validation_status,
        "checkpoint_sha256": digest,
        "promotion_status": "not_promoted",
    }


def list_registered_versions() -> list[dict[str, Any]]:
    """List registered versions without changing their status."""
    client = _client()

    try:
        versions = client.search_model_versions(
            f"name='{MODEL_NAME}'"
        )
    except MlflowException:
        return []

    return [
        {
            "model_name": item.name,
            "version": item.version,
            "source": item.source,
            "label": item.tags.get(
                "poison_guard_label", "unlabelled"
            ),
            "validation_status": item.tags.get(
                "validation_status", "unvalidated"
            ),
            "promotion_status": item.tags.get(
                "promotion_status", "not_promoted"
            ),
            "checkpoint_sha256": item.tags.get(
                "checkpoint_sha256"
            ),
        }
        for item in sorted(
            versions, key=lambda entry: int(entry.version)
        )
    ]

