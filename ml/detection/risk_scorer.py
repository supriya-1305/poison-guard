import numpy as np


def normalize(values):
    values = np.asarray(values, dtype=float)

    minimum = values.min()
    maximum = values.max()

    if maximum - minimum < 1e-12:
        return np.zeros_like(values)

    return (values - minimum) / (maximum - minimum)


def calculate_risk_scores(
    outlier_mask,
    outlier_scores,
    label_scores,
    cluster_distances,
    duplicate_mask
):
    outlier_component = (
        outlier_mask.astype(float)
    )

    outlier_component += (
        1 -
        normalize(outlier_scores)
    )

    outlier_component = np.clip(
        outlier_component,
        0,
        1
    )

    label_component = np.clip(
        label_scores,
        0,
        1
    )

    cluster_component = normalize(
        cluster_distances
    )

    duplicate_component = (
        duplicate_mask.astype(float)
    )

    risk = (
        0.40 * outlier_component
        + 0.30 * label_component
        + 0.20 * cluster_component
        + 0.10 * duplicate_component
    )

    risk = risk * 100

    return np.clip(
        risk,
        0,
        100
    )
