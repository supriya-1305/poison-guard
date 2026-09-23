# Week 3 - Poisoned Dataset and Data Sanitization

## Objective

Build the first PoisonGuard data sanitization engine capable of
identifying suspicious training samples using multiple signals.

## Detection Signals

1. Duplicate detection
2. Feature-space anomaly detection
3. Label consistency
4. Clustering-based analysis
5. Data provenance
6. Combined risk scoring

## Output

For every sample:

- sample_id
- risk_score
- anomaly_type
- detector
- status

## Status

CLEAN
or
QUARANTINED

## Dataset

CIFAR-10

## Baseline

ResNet18 clean model from Week 2

## Poisoning

Controlled synthetic poisoning only.
