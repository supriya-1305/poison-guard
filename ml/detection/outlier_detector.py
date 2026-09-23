import numpy as np

from sklearn.ensemble import IsolationForest


def detect_outliers(
    features,
    contamination=0.02,
    random_state=42
):

    detector = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )

    predictions = detector.fit_predict(
        features
    )

    scores = detector.decision_function(
        features
    )

    outlier_mask = predictions == -1

    return (
        outlier_mask,
        scores
    )
