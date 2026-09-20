# Initial Database Design

## Purpose

The PoisonGuard database will store machine learning experiments, datasets, models, detection results and security evaluation information.

The initial design is intentionally simple and can be expanded as the project develops.

## 1. Experiment

Stores information about each ML experiment.

- experiment_id — Primary key
- experiment_name — Name of the experiment
- dataset_id — Dataset used
- model_id — Model used
- attack_type — Type of attack or clean experiment
- poison_rate — Percentage of poisoned samples
- accuracy — Model accuracy
- precision — Precision score
- recall — Recall score
- f1_score — F1 score
- training_time — Training duration
- inference_latency — Model inference latency
- created_at — Experiment creation time

## 2. Dataset

Stores information about datasets used in experiments.

- dataset_id — Primary key
- dataset_name — Dataset name
- version — Dataset version
- number_of_samples — Number of samples
- number_of_classes — Number of classes
- preprocessing — Preprocessing description
- created_at — Dataset record creation time

## 3. Model

Stores information about ML models.

- model_id — Primary key
- model_name — Model name
- architecture — Model architecture
- parameters — Number or description of model parameters
- training_dataset — Dataset used for training
- created_at — Model record creation time

## 4. Detection Result

Stores results produced by poisoning or backdoor detection.

- detection_id — Primary key
- experiment_id — Related experiment
- suspicious_samples — Number of suspicious samples
- detection_method — Detection technique used
- detection_rate — Detection rate
- created_at — Detection record creation time

## 5. Relationships

The initial relationships are:

- Dataset can be used by multiple Experiments.
- Model can be used by multiple Experiments.
- Experiment can have multiple Detection Results.
- Each Experiment references one Dataset.
- Each Experiment references one Model.

## 6. Initial Entity Relationship

```text
+------------------+
|     DATASET      |
+------------------+
| dataset_id (PK)  |
| dataset_name     |
| version          |
| samples          |
| classes          |
+--------+---------+
         |
         | 1
         |
         | N
+--------v---------+
|    EXPERIMENT    |
+------------------+
| experiment_id PK |
| experiment_name  |
| dataset_id FK    |
| model_id FK      |
| attack_type      |
| poison_rate      |
| accuracy         |
| precision        |
| recall           |
| f1_score         |
| training_time    |
| created_at       |
+--------+---------+
         |
         | 1
         |
         | N
+--------v---------+
| DETECTION_RESULT |
+------------------+
| detection_id PK  |
| experiment_id FK |
| suspicious       |
| method           |
| detection_rate   |
| created_at       |
+------------------+

+------------------+
|      MODEL       |
+------------------+
| model_id (PK)    |
| model_name       |
| architecture     |
| parameters       |
| training_dataset |
| created_at       |
+------------------+
         |
         | 1
         |
         | N
         |
      EXPERIMENT

## 7. Future Expansion

The database may later include:

- Attack configuration
- Backdoor trigger information
- Mitigation results
- MLflow experiment references
- Model versions
- User and project information
- Security alerts
- API audit logs
