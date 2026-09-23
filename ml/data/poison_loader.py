import numpy as np
import torch

from torch.utils.data import Dataset


CIFAR_MEAN = (
    0.4914,
    0.4822,
    0.4465
)

CIFAR_STD = (
    0.2470,
    0.2435,
    0.2616
)


class PoisonedCIFARDataset(
    Dataset
):

    def __init__(
        self,
        images_path,
        labels_path
    ):

        self.images = np.load(
            images_path
        )

        self.labels = np.load(
            labels_path
        )

        self.mean = torch.tensor(
            CIFAR_MEAN
        ).view(3, 1, 1)

        self.std = torch.tensor(
            CIFAR_STD
        ).view(3, 1, 1)

    def __len__(self):

        return len(
            self.labels
        )

    def __getitem__(self, index):

        image = self.images[index]

        label = int(
            self.labels[index]
        )

        image = torch.tensor(
            image,
            dtype=torch.float32
        )

        image = image.permute(
            2, 0, 1
        )

        image = image / 255.0

        image = (
            image - self.mean
        ) / self.std

        return (
            image,
            label
        )
