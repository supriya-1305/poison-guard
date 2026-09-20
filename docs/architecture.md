# PoisonGuard Architecture

## 1. System Overview

PoisonGuard is an automated framework for detecting and preventing data poisoning and backdoor attacks against machine learning models.

The initial system will use CIFAR-10 as the experimental dataset and ResNet-18 as the clean baseline model.

## 2. Initial Architecture

    +----------------------+
    |      CIFAR-10        |
    |       Dataset        |
    +----------+-----------+
               |
               v
    +----------------------+
    |   Data Preprocessing |
    | Resize / Normalize   |
    |    Augmentation      |
    +----------+-----------+
               |
               v
    +----------------------+
    |      ResNet-18       |
    |    Clean Baseline    |
    +----------+-----------+
               |
               v
    +----------------------+
    |      Evaluation      |
    | Accuracy / Precision |
    | Recall / F1 / CM     |
    +----------+-----------+
               |
               v
    +----------------------+
    |        MLflow        |
    | Parameters / Metrics |
    |     / Artifacts      |
    +----------------------+

## 3. Future Security Pipeline

    Dataset
       |
       v
    Data Preprocessing
       |
       +-------------------+
       |                   |
       v                   v
    Clean Data       Poisoned Data
       |                   |
       |                   v
       |             Poison Detection
       |                   |
       |                   v
       |                Mitigation
       |                   |
       +---------+---------+
                 |
                 v
           Model Training
                 |
                 v
          Backdoor Testing
                 |
                 v
             Evaluation
                 |
                 v
          Security Analysis

## 4. Main Components

### Dataset Layer

CIFAR-10 will be used as the initial experimental dataset.

### Preprocessing Layer

The preprocessing pipeline will include:

- Image resizing
- Normalization
- Data augmentation
- Dataset splitting

### Model Layer

ResNet-18 will be used as the initial clean baseline model.

### Attack Simulation Layer

The framework will later simulate controlled:

- Data poisoning attacks
- Backdoor attacks

### Detection Layer

This layer will investigate methods for identifying suspicious or manipulated training samples and model behavior.

### Mitigation Layer

This layer will investigate techniques for reducing the impact of poisoned or backdoored data.

### Evaluation Layer

Models will be evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Attack success rate for backdoor experiments

### Experiment Tracking

MLflow will be used to track:

- Model versions
- Training parameters
- Metrics
- Artifacts

### API Layer

FastAPI will later expose selected PoisonGuard functions through APIs.

### Dashboard Layer

A security analysis dashboard will later display:

- Dataset information
- Attack configuration
- Detection results
- Model performance
- Mitigation results
- Experiment metrics

## 5. Technology Stack

- Python
- PyTorch
- Torchvision
- Scikit-learn
- Pandas
- NumPy
- MLflow
- FastAPI
- PostgreSQL
- Docker
- Git/GitHub

## 6. Current Scope

Week 1 focuses on establishing the clean baseline, understanding the research area, preparing the development environment and documenting the architecture.

Attack simulation, detection and mitigation components will be implemented in later weeks.
