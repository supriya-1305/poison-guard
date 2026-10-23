# PoisonGuard

**Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models**

PoisonGuard is a machine learning security framework designed to detect, analyze, and mitigate training-time attacks against machine learning systems.

## Objective

The project focuses on protecting ML training pipelines against data poisoning and backdoor attacks using anomaly detection, feature analysis, label consistency, data provenance, risk scoring, and quarantine mechanisms.

## Current Phase


**Week 7 Completed — Backend/API Integration**

## Project Progress

| Week | Focus | Status |
|---|---|---|
| Week 1 | Foundation, Research and Environment Setup | Completed |
| Week 2 | CIFAR-10 ResNet18 Baseline Model | Completed |
| Week 3 | Data Poisoning Detection and Sanitization | Completed |
| Week 4 | Backdoor Attack Simulation and Detection | Completed |
| Week 5 | Backdoor Model Training and Evaluation | Completed |
| Week 6 | ML Security Analysis and Optimization | Completed |
| Week 7 | Backend/API Integration | Completed |
| Week 8 | Security Dashboard | Next |
| Week 9 | End-to-End Testing | Planned |
| Week 10 | Documentation and Final Demo | Planned |

## Week 1 — Foundation and Research

- Project architecture and repository setup
- ML security research
- NIST Adversarial Machine Learning taxonomy study
- Python ML environment setup
- Git and GitHub configuration
- Initial project documentation

## Week 2 — Baseline ML Model

**Dataset:** CIFAR-10  
**Model:** ResNet18

### Pipeline

```text
CIFAR-10
   ↓
Preprocessing
   ↓
Train / Validation / Test
   ↓
ResNet18
   ↓
Evaluation
   ↓
MLflow Tracking
```


## Week 3 — Data Poisoning Detection and Data Sanitization

A controlled poisoned CIFAR-10 dataset was created to evaluate the PoisonGuard data sanitization engine.

### Detection Pipeline

Dataset  
↓  
Data Scanner  
↓  
Duplicate Detection  
↓  
Feature Extraction  
↓  
Outlier Detection  
↓  
Label Consistency  
↓  
Clustering  
↓  
Risk Scoring  
↓  
Quarantine  
↓  
Evaluation

### Week 3 Implementation

- Controlled CIFAR-10 poisoning experiment
- Poison metadata and ground truth
- Data provenance using SHA-256 hashes
- Duplicate detection
- ResNet18 feature extraction
- Isolation Forest outlier detection
- Label consistency analysis
- KMeans clustering
- Multi-signal risk scoring
- Suspicious sample quarantine
- Sanitization evaluation

## Week 4 — Backdoor Detection

A controlled backdoor experiment was implemented using CIFAR-10 and ResNet18.

### Backdoor Experiment

- Dataset: CIFAR-10
- Model: ResNet18
- Backdoor rate: 5%
- Trigger: 4x4 white square
- Trigger location: Bottom-right corner
- Target class: CIFAR-10 class 0 (airplane)

### Detection Methods

- Neural activation extraction
- Activation clustering
- STRIP-style prediction entropy analysis
- Backdoor risk scoring
- Neural Cleanse-style anomaly prototype

### Evaluation Results

| Metric | Result |
|---|---:|
| Clean Accuracy | 72.54% |
| Attack Success Rate | 94.57% |
| Activation Clustering | Completed |
| STRIP-style Detection | Completed |
| Risk Scoring | Completed |
| Neural Cleanse-style Prototype | Completed |

### Activation Clustering Results

| Cluster | Samples | Backdoor Samples | Backdoor Rate |
|---|---:|---:|---:|
| Cluster 0 | 4781 | 28 | 0.0059 |
| Cluster 1 | 219 | 219 | 1.0000 |

### STRIP-style Detection

| Input | Prediction Entropy |
|---|---:|
| Clean | 0.549342 |
| Triggered | 0.259480 |

The triggered input produced lower prediction entropy than the clean input in this experiment.

### Backdoor Risk Scoring

The backdoor risk scoring component combines activation and STRIP-related signals.

A functional test using an activation score of 80 and STRIP score of 75 produced:

```text
Risk Score: 78.0
Status: HIGH RISK
```

## Week 5 — Backdoor Model Training and Evaluation

### Objective

Train a ResNet18 model on a controlled backdoor dataset and evaluate
clean classification accuracy and backdoor attack success rate.

### Dataset and Configuration

- Dataset: CIFAR-10
- Evaluation dataset: CIFAR-10 test split
- Target class: 0 (airplane)
- Poison rate: 5%
- Trigger: 4×4 white square in the bottom-right corner
- Training epochs: 10

### Training Results

- Final training loss: 0.0758
- Final training accuracy: 97.37%
- Model checkpoint: `models/week5/backdoored_resnet18.pth`

### Evaluation Results

| Metric | Result |
|---|---:|
| Clean test accuracy | 83.15% |
| Backdoor attack success rate | 97.33% |
| Successful target predictions | 8,760 / 9,000 eligible samples |
| Test samples | 10,000 |
| Evaluation time | Approximately 13.18 seconds |

### Implementation

- Trained and saved the backdoored ResNet18 model.
- Loaded the saved model checkpoint successfully.
- Evaluated clean classification accuracy.
- Measured attack success rate on eligible triggered samples.
- Saved machine-readable results to `experiments/week5/evaluation_results.json`.
- Documented the experiment in `experiments/week5/README.md`.
- Committed and pushed the Week 5 implementation to GitHub.

### Interpretation

The model achieved 83.15% clean test accuracy and a 97.33% attack
success rate under this controlled experiment. The high attack success
rate indicates that the backdoor remains effective under the tested
conditions. These results motivate further work on detection and
mitigation.

### Limitations

These results apply to the current CIFAR-10 experiment and trigger
configuration. They do not establish performance against all backdoor
attacks or datasets. Further experiments are needed to evaluate
mitigation effectiveness.

### Artifacts

- Training script: `ml/attacks/train_backdoor.py`
- Evaluation script: `ml/evaluation/evaluate_backdoor.py`
- Evaluation results: `experiments/week5/evaluation_results.json`
- Experiment report: `experiments/week5/README.md`

## Week 6 — ML Security Analysis and Runtime Monitoring

### Objective

Extend PoisonGuard from offline model evaluation to a prototype inference API that records predictions and monitors runtime behaviour.

### Implementation

- Integrated a FastAPI inference service with the Week 5 ResNet18 model checkpoint.
- Added image preprocessing and CIFAR-10 classification through the API.
- Recorded prediction timestamps, predicted classes, confidence scores, input means, input standard deviations, and model versions.
- Implemented runtime alert rules for low-confidence predictions and unusual input statistics.
- Added monitoring for unusual target-class concentration in recent predictions.
- Implemented incident-recording logic and a preliminary security-score endpoint.
- Added model status and checkpoint-scanning endpoints.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API and model status |
| POST | `/predict` | Run model inference |
| POST | `/scan/dataset` | Request dataset scanning |
| POST | `/scan/model` | Request model scanning |
| GET | `/model/status` | Inspect model status |
| GET | `/security-score` | Retrieve the preliminary security score |
| GET | `/incidents` | Retrieve recorded incidents |
| POST | `/rollback` | Request model rollback |
| POST | `/retrain` | Request model retraining |

### Runtime Monitoring and Logging

Prediction records are stored locally in:

- `experiments/week6/logs/predictions.jsonl`
- `experiments/week6/logs/incidents.jsonl` — created when an incident is recorded.

Prediction records include timestamps, predicted classes, confidence values, input statistics, and model-version information. Runtime alert thresholds are configurable demonstration values and require validation against clean validation data before operational use.

### Testing Results

The following automated tests passed:

| Test | Result |
|---|---|
| Duplicate detection | Passed |
| Feature extraction | Passed |
| Prediction-record generation | Passed |
| Security-score response fields | Passed |
| Incident-list response | Passed |
| Week 6 runtime alert rules | Passed |
| **Total** | **6 passed** |

Test command:

```bash
python -m pytest tests/ -v
```

The recorded test run completed with **6 passed**. These tests validate the implemented prototype behaviour; they do not establish production-level security or prove that every API endpoint and attack scenario has been fully validated.

### Artifacts

- Runtime monitoring service: `backend/app/services/runtime_monitor.py`
- Runtime alert tests: `tests/test_week6_alerts.py`
- Test results: `experiments/week6/pytest-results.txt`
- Runtime monitoring documentation: `experiments/week6/README.md`

### Limitations

The current monitoring rules use confidence and image-statistic heuristics. These signals can produce false positives and false negatives and do not independently prove that a model has been backdoored. Further work is required to validate thresholds, test adversarial scenarios, and evaluate mitigation effectiveness.

</EOF>

## Week 7 — Runtime Protection and Model Validation

### Objective

Extend PoisonGuard with model sanitization, backdoor evaluation, incident response, audit logging, and model registry validation to support a safer machine-learning model lifecycle.

### Implementation

- Implemented a Week 7 model sanitization workflow and trained a sanitized candidate model.
- Evaluated clean classification accuracy and attack success rate using the CIFAR-10 test split.
- Added configurable promotion validation checks to assess whether a candidate meets the configured thresholds.
- Integrated model registry tracking for baseline, vulnerable, and sanitized model versions.
- Implemented incident recording, model-version quarantine support, and response audit logging.
- Added runtime alert orchestration and automated tests for incident response and promotion validation.

### Candidate Evaluation Results

| Metric | Result |
|---|---:|
| Dataset | CIFAR-10 test split |
| Test samples | 10,000 |
| Trigger | 4×4 white square, bottom-right |
| Target class | 0 — airplane |
| Clean accuracy | 90.33% |
| Attack success rate | 1.11% |
| Configured validation checks | 7/7 passed |
| Promotion status | Not promoted |

**Important:** Passing the configured checks does not prove that every possible backdoor has been eliminated. Additional testing and review are required before operational use.

### Model Registry

| Version | Model | Status |
|---|---|---|
| v1 | Baseline | Baseline evaluated |
| v2 | Vulnerable model | Quarantined; promotion blocked |
| v3 | Sanitized candidate | Registered for tracking; not promoted |

The sanitized candidate is registered for tracking only. Registration does not activate the model or authorize production deployment.

### API and Incident Response

Week 7 extends the Week 6 inference and monitoring prototype with incident-response services, audit records, model registry inspection, and a candidate validation workflow.

The existing rollback endpoint supports loading the baseline checkpoint. The retraining endpoint remains unimplemented and returns HTTP 501.

### Testing

The automated test suite completed successfully:

```bash
python -m pytest tests/ -q
```

**Latest recorded result:** 15 tests passed.

Tests cover runtime monitoring, incident persistence, response-action auditing, orchestration, and promotion validation.

### Artifacts

- Sanitization workflow: `ml/detection/week7_sanitization.py`
- Candidate training: `ml/training/week7_sanitize_model.py`
- Candidate evaluation: `ml/evaluation/evaluate_week7_candidate.py`
- Vulnerable-model evaluation: `ml/evaluation/evaluate_week7_vulnerable.py`
- Promotion validation: `ml/evaluation/validate_week7_promotion.py`
- Registry tracking: `ml/evaluation/register_week7_protected.py`
- Incident response: `backend/app/services/incident_response.py`
- Runtime orchestration: `backend/app/services/week7_orchestrator.py`
- Validation report: `experiments/week7/results/promotion_validation.json`
- Candidate evaluation: `experiments/week7/results/sanitized_candidate_evaluation.json`
- Vulnerable-model evaluation: `experiments/week7/results/vulnerable_model_evaluation.json`
- Sanitization manifest: `experiments/week7/results/sanitization_manifest.json`

### Limitations and Remaining Work

- The evaluation covers the configured CIFAR-10 test split and a single trigger configuration.
- The validation results do not establish protection against all poisoning or backdoor attacks.
- Retraining and complete protected-model promotion and activation remain outstanding.
- Manual approval is separate from registration and production deployment.

### Conclusion

Week 7 establishes a tested prototype for model validation, registry tracking, and incident response. Further work is required to complete the end-to-end protected-model lifecycle and verify its effectiveness under additional attack scenarios.

