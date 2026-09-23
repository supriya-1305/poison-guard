import json
from pathlib import Path

import numpy as np


from ml.detection.duplicate_detector import (
    detect_duplicates
)

from ml.detection.outlier_detector import (
    detect_outliers
)

from ml.detection.label_consistency import (
    label_consistency_scores
)

from ml.detection.clustering import (
    cluster_features
)

from ml.detection.risk_scorer import (
    calculate_risk_scores
)

from ml.detection.status import (
    get_status,
    get_risk_level
)


CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]


def determine_anomaly_type(
    index,
    duplicate_mask,
    outlier_mask,
    label_scores,
    risk
):

    reasons = []

    if duplicate_mask[index]:

        reasons.append(
            "Duplicate"
        )

    if outlier_mask[index]:

        reasons.append(
            "Feature anomaly"
        )

    if label_scores[index] >= 0.5:

        reasons.append(
            "Label inconsistency"
        )

    if not reasons:

        if risk >= 70:

            reasons.append(
                "Combined anomaly"
            )

        else:

            reasons.append(
                "None"
            )

    return "; ".join(reasons)


def run_scanner(
    images,
    labels,
    features,
    metadata
):

    print("Running duplicate detection...")

    duplicate_indices = detect_duplicates(
        images
    )

    duplicate_mask = np.zeros(
        len(images),
        dtype=bool
    )

    duplicate_mask[
        duplicate_indices
    ] = True

    print("Running Isolation Forest...")

    outlier_mask, outlier_scores = (
        detect_outliers(
            features,
            contamination=0.02
        )
    )

    print("Running label consistency...")

    label_scores = (
        label_consistency_scores(
            features,
            labels
        )
    )

    print("Running clustering...")

    cluster_labels, cluster_distances = (
        cluster_features(
            features
        )
    )

    print("Calculating risk scores...")

    risk_scores = calculate_risk_scores(
        outlier_mask,
        outlier_scores,
        label_scores,
        cluster_distances,
        duplicate_mask
    )

    results = []

    for index in range(len(images)):

        anomaly_type = (
            determine_anomaly_type(
                index,
                duplicate_mask,
                outlier_mask,
                label_scores,
                risk_scores[index]
            )
        )

        result = {
            "sample_id":
                metadata[index]["sample_id"],

            "dataset_index":
                int(index),

            "risk_score":
                round(
                    float(risk_scores[index]),
                    2
                ),

            "risk_level":
                get_risk_level(
                    risk_scores[index]
                ),

            "anomaly_type":
                anomaly_type,

            "detector":
                "Multi-Signal",

            "label_consistency_score":
                round(
                    float(label_scores[index]),
                    4
                ),

            "cluster_id":
                int(cluster_labels[index]),

            "status":
                get_status(
                    risk_scores[index]
                ),

            "ground_truth_poison":
                metadata[index]["poison_type"]
        }

        results.append(result)

    return results
