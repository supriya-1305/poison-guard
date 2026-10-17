# PoisonGuard — Week 6 Runtime Monitoring

## Objective

Move PoisonGuard from offline model evaluation to a prototype inference API
that records predictions and monitors runtime behaviour.

## Components

- FastAPI inference service.
- Week 5 ResNet18 checkpoint loader.
- Image preprocessing and CIFAR-10 classification.
- Prediction logging with timestamps and model version.
- Input mean and standard deviation recording.
- Low-confidence and heuristic input-statistic alerts.
- Recent target-class concentration monitoring.
- Incident log and preliminary security score.
- Model status and checkpoint scan endpoints.

## API Endpoints

- GET /health
- POST /predict
- POST /scan/dataset
- POST /scan/model
- GET /model/status
- GET /security-score
- GET /incidents
- POST /rollback
- POST /retrain

## Generated Runtime Files

- experiments/week6/logs/predictions.jsonl
- experiments/week6/logs/incidents.jsonl

These logs are generated locally at runtime and are excluded from Git.

## Testing

Run the tests with:

    python -m pytest tests/ -v

Run the API from the repository root with:

    python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 2222

Open the interactive API documentation at:

    http://127.0.0.1:2222/docs

## Important Limitations

The runtime thresholds and security score are prototype heuristics, not validated
security guarantees. Alerts indicate behaviour requiring investigation and do
not prove that a sample or model is malicious.

Rollback and retraining endpoints currently return HTTP 501 because the
controlled workflows are not implemented yet. They must not be reported as
completed features.

## Deliverable

A prototype inference API with runtime prediction logging, heuristic monitoring,
incident records, and model-status reporting.
