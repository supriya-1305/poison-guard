import numpy as np

from sklearn.cluster import KMeans


def cluster_features(
    features,
    n_clusters=10,
    random_state=42
):

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    cluster_labels = model.fit_predict(
        features
    )

    distances = model.transform(
        features
    )

    min_distances = distances.min(
        axis=1
    )

    return (
        cluster_labels,
        min_distances
    )
