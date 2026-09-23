from pathlib import Path
import json
import random

import numpy as np
import torch
from torchvision import datasets


DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/poisoned")

SEED = 42

LABEL_POISON_RATE = 0.05
FEATURE_POISON_RATE = 0.02

RANDOM = random.Random(SEED)

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


def flip_label(original_label):
    """Change the label to another class."""

    possible_labels = [
        i for i in range(len(CLASSES))
        if i != original_label
    ]

    return RANDOM.choice(possible_labels)


def add_feature_anomaly(image):
    """
    Introduce a controlled visual anomaly.
    This is NOT a backdoor trigger.
    """

    image = image.copy()

    # Modify a small corner region.
    image[:4, :4, :] = 255

    return image


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset = datasets.CIFAR10(
        root=DATA_DIR,
        train=True,
        download=True
    )

    total_samples = len(dataset)

    label_poison_count = int(
        total_samples * LABEL_POISON_RATE
    )

    feature_poison_count = int(
        total_samples * FEATURE_POISON_RATE
    )

    all_indices = list(range(total_samples))

    RANDOM.shuffle(all_indices)

    label_indices = set(
        all_indices[:label_poison_count]
    )

    feature_start = label_poison_count

    feature_indices = set(
        all_indices[
            feature_start:
            feature_start + feature_poison_count
        ]
    )

    records = []

    images = []
    labels = []

    for index in range(total_samples):

        image, original_label = dataset[index]

        image = np.array(image)

        new_label = original_label

        poison_type = "clean"

        if index in label_indices:

            new_label = flip_label(
                original_label
            )

            poison_type = "label_flip"

        elif index in feature_indices:

            image = add_feature_anomaly(
                image
            )

            poison_type = "feature_anomaly"

        images.append(image)
        labels.append(new_label)

        records.append({
            "sample_id": f"IMG_{index:06d}",
            "dataset_index": index,
            "original_label": int(original_label),
            "current_label": int(new_label),
            "original_class": CLASSES[original_label],
            "current_class": CLASSES[new_label],
            "poison_type": poison_type,
            "is_poisoned": poison_type != "clean"
        })

    images = np.array(images)
    labels = np.array(labels)

    np.save(
        OUTPUT_DIR / "images.npy",
        images
    )

    np.save(
        OUTPUT_DIR / "labels.npy",
        labels
    )

    with open(
        OUTPUT_DIR / "metadata.json",
        "w"
    ) as f:

        json.dump(
            records,
            f,
            indent=2
        )

    print("=" * 50)
    print("Poisoned Dataset Created")
    print("=" * 50)

    print("Total samples:", total_samples)
    print(
        "Label poisoned:",
        label_poison_count
    )
    print(
        "Feature anomalous:",
        feature_poison_count
    )

    print(
        "Total manipulated:",
        label_poison_count +
        feature_poison_count
    )

    print(
        "Output:",
        OUTPUT_DIR
    )


if __name__ == "__main__":
    main()
