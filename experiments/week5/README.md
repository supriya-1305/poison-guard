# PoisonGuard — Week 5 Backdoor Experiment

## Objective

Train a ResNet18 model on a controlled backdoor dataset and evaluate
clean classification accuracy and attack success rate.

## Dataset

- Dataset: CIFAR-10
- Evaluation dataset: CIFAR-10 test split
- Attack type: Controlled backdoor trigger

## Training Results

- Epochs completed: 10
- Final training loss: 0.0758
- Final training accuracy: 97.37%
- Saved model: models/week5/backdoored_resnet18.pth

## Evaluation Results

- Clean accuracy: 83.15%
- Attack success rate: 97.33%

## Interpretation

Clean accuracy measures the model's performance on clean evaluation
images. Attack success rate measures how often the backdoor attack
produces its intended target prediction under the evaluation setup.

These measurements should be interpreted together to assess the
trade-off between clean classification performance and backdoor
effectiveness.

## Model Artifact

models/week5/backdoored_resnet18.pth

## Evidence and Logs

Store experiment logs, results, and figures in the following folders:

- experiments/week5/logs/
- experiments/week5/results/
- experiments/week5/figures/

## Important Note

The reported values describe the recorded experiment. Confirm them
against the actual training and evaluation output before using them
as final results in the project report.

## Deliverable

Week 5 backdoored ResNet18 training and evaluation record.
