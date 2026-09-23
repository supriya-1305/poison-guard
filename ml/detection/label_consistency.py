import numpy as np

from sklearn.neighbors import NearestNeighbors


def label_consistency_scores(
    features,
    labels,
    n_neighbors=10
):

    neighbors = NearestNeighbors(
        n_neighbors=n_neighbors + 1,
        metric="euclidean",
        n_jobs=-1
    )

    neighbors.fit(features)

    _, indices = neighbors.kneighbors(
        features
    )

    scores = np.zeros(
        len(labels),
        dtype=float
    )

    for i in range(len(labels)):

        neighbor_indices = indices[i][1:]

        neighbor_labels = labels[
            neighbor_indices
        ]

        disagreement = np.mean(
            neighbor_labels != labels[i]
        )

        scores[i] = disagreement

    return scores
