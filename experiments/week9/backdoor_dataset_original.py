import json
from pathlib import Path

import numpy as np
import torch
from torchvision import datasets, transforms


SEED = 42
POISON_RATE = 0.05
TARGET_LABEL = 0

OUTPUT_DIR = Path("data/backdoor")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def add_trigger(image, size=4):
    """
    Add a small white square trigger to the bottom-right corner.
    Image shape: C x H x W
    """
    poisoned = image.clone()

    poisoned[:, -size:, -size:] = 1.0

    return poisoned


def create_backdoor_dataset():
    transform = transforms.ToTensor()

    dataset = datasets.CIFAR10(
        root="data",
        train=True,
        download=True,
        transform=transform,
    )

    images = []
    labels = []
    metadata = []

    num_samples = len(dataset)
    num_poison = int(num_samples * POISON_RATE)

    poison_indices = set(
        np.random.choice(
            num_samples,
            num_poison,
            replace=False,
        )
    )

    for index in range(num_samples):
        image, original_label = dataset[index]

        is_poisoned = index in poison_indices

        if is_poisoned:
            image = add_trigger(image)
            current_label = TARGET_LABEL
        else:
            current_label = original_label

        images.append(image.numpy())
        labels.append(current_label)

        metadata.append(
            {
                "sample_id": index,
                "original_label": int(original_label),
                "current_label": int(current_label),
                "is_backdoor": bool(is_poisoned),
                "trigger": "4x4_white_square_bottom_right"
                if is_poisoned
                else None,
            }
        )

    images = np.stack(images)
    labels = np.array(labels)

    np.save(OUTPUT_DIR / "images.npy", images)
    np.save(OUTPUT_DIR / "labels.npy", labels)

    with open(OUTPUT_DIR / "metadata.json", "w") as file:
        json.dump(metadata, file, indent=2)

    print("Backdoor dataset created")
    print(f"Total samples: {num_samples}")
    print(f"Poisoned samples: {num_poison}")
    print(f"Poison rate: {POISON_RATE * 100:.2f}%")
    print(f"Target label: {TARGET_LABEL}")


if __name__ == "__main__":
    create_backdoor_dataset()
