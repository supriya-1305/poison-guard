# Experiment 001 — Clean CIFAR-10 Baseline

## Objective

Establish a clean baseline before introducing poisoning or
backdoor attacks.

## Dataset

CIFAR-10

## Dataset Split

Train: 45,000
Validation: 5,000
Test: 10,000

## Model

ResNet18

## Training Configuration

Epochs: 10
Batch Size: 128
Learning Rate: 0.001
Optimizer: Adam
Loss: CrossEntropyLoss

## Data Augmentation

- Random Horizontal Flip
- Random Crop
- Normalization

## Device

Apple Silicon MPS

## Metrics

- Accuracy
- Precision
- Recall
- F1
- Confusion Matrix
- Training Time
- Inference Latency

## Results

Accuracy: 0.8556

Precision: 0.8646983332237255

Recall: 0.8556000000000001

F1: 0.8559351416323946

Training Time: 1250.3761217594147 seconds

Inference Latency: 0.0007085837456994341 seconds/image

Test Loss: 0.4484609254837036

## Confusion Matrix

See:

experiments/confusion_matrix_baseline.png

## MLflow Run

Experiment:

PoisonGuard-Baseline

Run Name:

trusting-jay-707

Run ID:

3012ca1b7cd34985a03bfc56faeb3b10

Status:

Finished

Logged Model:

resnet18_baseline

## MLflow Parameters

Model: ResNet18

Dataset: CIFAR-10

Batch Size: 128

Epochs: 10

Learning Rate: 0.001

Device: mps
