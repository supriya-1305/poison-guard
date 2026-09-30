import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet18


class BackdoorDataset(Dataset):
    def __init__(self):
        self.images = np.load(
            "data/backdoor/images.npy"
        )

        self.labels = np.load(
            "data/backdoor/labels.npy"
        )

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        image = torch.tensor(
            self.images[index],
            dtype=torch.float32
        )

        label = int(self.labels[index])

        return image, label


def create_model():
    model = resnet18(weights=None)

    model.fc = nn.Linear(
        model.fc.in_features,
        10
    )

    return model


def main():

    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    print("Using device:", device)

    dataset = BackdoorDataset()

    loader = DataLoader(
        dataset,
        batch_size=128,
        shuffle=True,
        num_workers=0
    )

    model = create_model().to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    epochs = 10

    model.train()

    for epoch in range(epochs):

        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in loader:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            predictions = outputs.argmax(
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

        accuracy = correct / total

        print(
            f"Epoch {epoch + 1}/{epochs} "
            f"Loss: {running_loss / len(loader):.4f} "
            f"Accuracy: {accuracy:.4f}"
        )

    Path("models/week4").mkdir(
        parents=True,
        exist_ok=True
    )

    torch.save(
        model.state_dict(),
        "models/week4/backdoored_resnet18.pth"
    )

    print(
        "Saved: models/week4/backdoored_resnet18.pth"
    )


if __name__ == "__main__":
    main()
