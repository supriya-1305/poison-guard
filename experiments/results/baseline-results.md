# PoisonGuard Baseline Results

## Dataset

CIFAR-10

Training samples: 45,000

Validation samples: 5,000

Test samples: 10,000

## Model

ResNet18

## Training

Epochs: 10

Batch size: 128

Optimizer: Adam

Learning rate: 0.001

## Hardware

Apple Silicon Mac

Device: MPS

## Results

Accuracy: 0.8556 (85.56%)

Precision: 0.8646983332237255 (86.47%)

Recall: 0.8556000000000001 (85.56%)

F1: 0.8559351416323946 (85.59%)

Training Time: 1250.3761217594147 seconds (~20.84 minutes)

Inference Latency: 0.0007085837456994341 seconds/image (~0.709 ms/image)

## Test Results

Test Loss: 0.4484609254837036

Test Accuracy: 0.8556 (85.56%)

## Confusion Matrix

See:

experiments/confusion_matrix_baseline.png
