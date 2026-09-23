# PoisonGuard Week 3 Results

## Objective

Build the first PoisonGuard data sanitization engine for controlled
poisoning detection on the CIFAR-10 training dataset.

---

## Dataset

Dataset: CIFAR-10

Total training samples processed: 50,000

### Ground-Truth Distribution

- Clean: 46,500
- Label Flip: 2,500
- Feature Anomaly: 1,000
- Total Poisoned: 3,500

---

## Controlled Poisoning

### Label Poisoning

Label flipping was applied at a rate of 5%.

This changes the target label while keeping the original image unchanged.

### Feature Anomaly

Feature anomalies were introduced at a rate of 2%.

These samples contain controlled image modifications intended to create
detectable differences in feature space.

---

## Detection Components

The Week 3 sanitization engine combines multiple detection signals:

- Duplicate Detection
- ResNet18 Feature Extraction
- Isolation Forest
- Label Consistency
- KMeans Clustering
- Data Provenance
- Multi-Signal Risk Scoring
- Quarantine

---

## Feature Extraction

The trained ResNet18 model was used as a feature extractor.

Feature representation:

50,000 samples × 512 features

Feature file:

`data/poisoned/features.npy`

---

## Risk Scoring

Each sample receives a combined risk score from 0 to 100.

### Risk Levels

- 0–39: LOW
- 40–69: MEDIUM
- 70–100: HIGH

### Quarantine Rule

Samples with:

`risk_score >= 70`

are assigned:

`QUARANTINED`

---

## Detection Results

### Risk-Level Distribution

- LOW: 46,863
- MEDIUM: 3,083
- HIGH: 54

### Status Distribution

- CLEAN: 49,946
- QUARANTINED: 54

### Quarantine Percentage

54 / 50,000 × 100 = 0.108%

---

## Ground-Truth Comparison

The detector was compared against the known poisoning labels.

### Confusion Matrix

- True Positive (TP): 53
- False Positive (FP): 1
- False Negative (FN): 3,447
- True Negative (TN): 46,499

### Detection Rate

53 / 3,500 × 100 = 1.51%

The detector correctly identified 53 of the 3,500 intentionally
poisoned samples in this Week 3 experiment.

---

## Quarantine Manifest

The quarantined samples were exported to:

`data/quarantine/quarantine_manifest.json`

Number of records:

54

All records in the manifest have status:

`QUARANTINED`

---

## CSV Report

A CSV version of the sanitization results was generated for reporting:

`experiments/week3/results/sanitization_results.csv`

The CSV contains:

- 50,000 rows
- Sample ID
- Dataset index
- Risk score
- Risk level
- Anomaly type
- Detector
- Label consistency score
- Cluster ID
- Status
- Ground-truth poisoning information

---

## JSON Report

Machine-readable sanitization results:

`experiments/week3/results/sanitization_results.json`

Total records:

50,000

---

## Data Provenance

The Week 3 experiment records dataset provenance information and
configuration details to support reproducibility and traceability.

---

## Important Observation

The detector does not identify every intentionally poisoned sample.

This experiment therefore provides a measurable baseline for the
PoisonGuard detection pipeline rather than assuming perfect detection.

The results can be used as a reference when comparing improved
detection methods in later weeks.

---

## Important Data Boundary

The clean CIFAR-10 test dataset remains untouched.

The poisoning experiments are performed on the training data only.

---

## Week 3 Deliverable

### PoisonGuard Data Sanitization Engine v1

The completed Week 3 pipeline is:

```text
CIFAR-10 Training Data
        |
        v
Poison Simulator
        |
        +----------------------+
        |                      |
        v                      v
   Label Flip          Feature Anomaly
        |                      |
        +----------+-----------+
                   |
                   v
             Poisoned Dataset
                   |
                   v
             Data Provenance
                   |
                   v
              Data Scanner
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   Duplicate   Feature      Label
   Detection   Extraction   Consistency
                   |
                   v
            Isolation Forest
                   |
                   v
               Clustering
                   |
                   v
              Risk Scoring
                   |
                   v
            Risk Classification
                   |
             +-----+-----+
             |           |
             v           v
           CLEAN      QUARANTINE
