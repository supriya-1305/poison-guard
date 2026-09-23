# PoisonGuard

**Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models**

PoisonGuard is a machine learning security framework designed to detect, analyze, and mitigate training-time attacks against machine learning systems.

## Objective

The project focuses on protecting ML training pipelines against data poisoning and backdoor attacks using anomaly detection, feature analysis, label consistency, data provenance, risk scoring, and quarantine mechanisms.

## Current Phase

**Week 3 — Data Poisoning Detection and Data Sanitization Engine**

## Project Progress

| Week | Focus | Status |
|---|---|---|
| Week 1 | Foundation, Research and Environment Setup | Completed |
| Week 2 | CIFAR-10 ResNet18 Baseline Model | Completed |
| Week 3 | Data Poisoning Detection and Sanitization | Completed |
| Week 4 | Backdoor Attack Simulation and Detection | Planned |
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


## Week 3 — Data Poisoning Detection and Sanitization

A controlled poisoned CIFAR-10 dataset was created to evaluate the PoisonGuard data sanitization engine.

### Detection Pipeline

```text
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
