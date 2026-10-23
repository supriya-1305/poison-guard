
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms

from ml.models.resnet18 import create_model


SEED = 42
BATCH_SIZE = 128
EPOCHS = 3
LEARNING_RATE = 0.0001

BASELINE_PATH = Path("models/resnet18_baseline.pth")
MANIFEST_PATH = Path(
    "experiments/week7/results/sanitization_manifest.json"
)
OUTPUT_PATH = Path("models/week7/resnet18_sanitized_candidate.pth")
REPORT_PATH = Path(
    "experiments/week7/results/sanitized_candidate_training.json"
)

CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD = (0.2470, 0.2435, 0.2616)


class RetainedCIFAR10(Dataset):
    def __init__(self, dataset, indices):
        self.dataset = dataset
        self.indices = indices

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, position):
        return self.dataset[self.indices[position]]


def main():
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu"
    )
    print("Device:", device)

    if not BASELINE_PATH.is_file():
        raise FileNotFoundError(BASELINE_PATH)
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(MANIFEST_PATH)

    manifest = json.loads(MANIFEST_PATH.read_text())
    retained = manifest["retained_indices"]

    if not retained:
        raise ValueError("No retained samples in the manifest.")

    # Use CIFAR-10 training data only; never use the test set for training.
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32, padding=4),
        transforms.ToTensor(),
        transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
    ])

    dataset = datasets.CIFAR10(
        root="data",
        train=True,
        download=True,
        transform=transform,
    )

    # The manifest is based on a 50,000-sample dataset.
    # CIFAR-10's training split has 50,000 samples.
    if max(retained) >= len(dataset):
        raise ValueError("Manifest indices exceed training dataset size.")

    loader = DataLoader(
        RetainedCIFAR10(dataset, retained),
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
    )

    model = create_model().to(device)
    state = torch.load(
        BASELINE_PATH,
        map_location="cpu",
        weights_only=True,
    )
    model.load_state_dict(state)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )
    criterion = nn.CrossEntropyLoss()

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        total = 0

        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * images.size(0)
            total += images.size(0)

        print(
            f"Epoch {epoch + 1}/{EPOCHS} "
            f"loss={total_loss / total:.4f}"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.cpu().state_dict(), OUTPUT_PATH)

    report = {
        "candidate": str(OUTPUT_PATH),
        "initialized_from": str(BASELINE_PATH),
        "training_dataset": "CIFAR-10 training split",
        "retained_sample_count": len(retained),
        "risk_threshold": manifest["risk_threshold"],
        "epochs": EPOCHS,
        "learning_rate": LEARNING_RATE,
        "seed": SEED,
        "status": "candidate_not_yet_validated",
        "note": (
            "This experiment starts from the baseline checkpoint. "
            "It is not evidence of backdoor removal. Evaluate clean "
            "accuracy and attack success rate before any promotion."
        ),
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print("Candidate checkpoint saved:", OUTPUT_PATH)
    print("Training report saved:", REPORT_PATH)
    print("Status: candidate_not_yet_validated")


if __name__ == "__main__":
    main()

