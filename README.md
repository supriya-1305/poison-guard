# PoisonGuard

**Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models**

PoisonGuard is a machine learning security framework designed to detect, analyze, and mitigate training-time attacks against machine learning systems.

## Objective

The project focuses on protecting ML training pipelines against data poisoning and backdoor attacks using anomaly detection, feature analysis, label consistency, data provenance, risk scoring, and quarantine mechanisms.

## Current Phase

**Week 4 — Backdoor Attack Simulation and Detection**

## Project Progress

| Week | Focus | Status |
|---|---|---|
| Week 1 | Foundation, Research and Environment Setup | Completed |
| Week 2 | CIFAR-10 ResNet18 Baseline Model | Completed |
| Week 3 | Data Poisoning Detection and Sanitization | Completed |
| Week 4 | Backdoor Attack Simulation and Detection | Completed |
| Week 5 | Advanced Detection and Mitigation | Planned |
| Week 6 | ML Security Analysis and Optimization | Planned |
| Week 7 | Backend/API Integration | Planned |
| Week 8 | Security Dashboard | Planned |
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
