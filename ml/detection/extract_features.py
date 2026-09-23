import json

import numpy as np
import torch
from torch.utils.data import DataLoader

from ml.data.poison_loader import (
    PoisonedCIFARDataset
)

from ml.models.resnet18 import (
    create_model
)

from ml.detection.feature_extractor import (
    create_feature_model
)


def get_device():

    if torch.backends.mps.is_available():

        return torch.device("mps")

    return torch.device("cpu")


def main():

    device = get_device()

    print(
        "Device:",
        device
    )

    dataset = PoisonedCIFARDataset(
        "data/poisoned/images.npy",
        "data/poisoned/labels.npy"
    )

    loader = DataLoader(
        dataset,
        batch_size=128,
        shuffle=False,
        num_workers=0
    )

    print(
        "Dataset size:",
        len(dataset)
    )

    model = create_model()

    model.load_state_dict(
        torch.load(
            "models/resnet18_baseline.pth",
            map_location=device
        )
    )

    model = create_feature_model(
        model
    )

    model = model.to(device)

    model.eval()

    all_features = []

    with torch.no_grad():

        for batch_index, (
            images,
            labels
        ) in enumerate(loader):

            images = images.to(
                device
            )

            features = model(
                images
            )

            all_features.append(
                features.cpu()
            )

            if batch_index % 50 == 0:

                print(
                    "Processed batches:",
                    batch_index
                )

    features = torch.cat(
        all_features
    ).numpy()

    np.save(
        "data/poisoned/features.npy",
        features
    )

    print(
        "Feature shape:",
        features.shape
    )

    print(
        "Saved:",
        "data/poisoned/features.npy"
    )


if __name__ == "__main__":
    main()
