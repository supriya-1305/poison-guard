import json

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ml.detection.activation_extractor import (
    ActivationExtractor
)


def main():

    images = np.load(
        "data/backdoor/images.npy"
    )

    metadata = json.load(
        open("data/backdoor/metadata.json")
    )

    extractor = ActivationExtractor(
        "models/week4/backdoored_resnet18.pth"
    )

    sample_count = min(
        5000,
        len(images)
    )

    features = extractor.extract(
        images[:sample_count]
    )

    extractor.close()

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        features
    )

    clustering = KMeans(
        n_clusters=2,
        random_state=42,
        n_init=10
    )

    cluster_labels = clustering.fit_predict(
        scaled_features
    )

    poison_flags = np.array(
        [
            item["is_backdoor"]
            for item in metadata[:sample_count]
        ]
    )

    print("Activation clustering complete")

    for cluster_id in range(2):

        cluster_mask = (
            cluster_labels == cluster_id
        )

        total = cluster_mask.sum()

        poison_count = (
            poison_flags[cluster_mask].sum()
        )

        poison_rate = (
            poison_count / total
            if total > 0
            else 0
        )

        print(
            f"Cluster {cluster_id}: "
            f"samples={total}, "
            f"backdoor={poison_count}, "
            f"backdoor_rate={poison_rate:.4f}"
        )


if __name__ == "__main__":
    main()
