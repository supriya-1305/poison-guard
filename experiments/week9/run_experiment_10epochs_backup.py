import argparse
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms

from ml.models.resnet18 import create_model

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "experiments/week9/results"
MODELS = ROOT / "experiments/week9/models"
LOGS = ROOT / "experiments/week9/logs"

TARGET_LABEL = 0
SEED = 42
EPOCHS = 10
BATCH_SIZE = 128
RATES = [0, 1, 3, 5, 10]


class PoisonedCIFAR(Dataset):
    def __init__(self, dataset, rate, training=True):
        self.dataset = dataset
        self.training = training
        self.poison_indices = set()

        if training and rate > 0:
            count = int(len(dataset) * rate / 100)
            rng = random.Random(SEED)
            self.poison_indices = set(
                rng.sample(range(len(dataset)), count)
            )

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        image, label = self.dataset[index]

        if self.training and index in self.poison_indices:
            image = image.clone()
            image[:, -4:, -4:] = 1.0
            label = TARGET_LABEL

        return image, label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rate", type=int, required=True, choices=RATES
    )
    args = parser.parse_args()

    rate = args.rate
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Poisoning rate: {rate}%")
    print(f"Device: {device}")

    transform = transforms.ToTensor()

    train_base = datasets.CIFAR10(
        root=str(ROOT / "data"),
        train=True,
        download=True,
        transform=transform
    )

    test_base = datasets.CIFAR10(
        root=str(ROOT / "data"),
        train=False,
        download=True,
        transform=transform
    )

    train_data = PoisonedCIFAR(train_base, rate, True)
    test_data = PoisonedCIFAR(test_base, 0, False)

    train_loader = DataLoader(
        train_data, batch_size=BATCH_SIZE,
        shuffle=True, num_workers=0
    )

    test_loader = DataLoader(
        test_data, batch_size=BATCH_SIZE,
        shuffle=False, num_workers=0
    )

    model = create_model().to(device)
    optimizer = torch.optim.Adam(
        model.parameters(), lr=0.001
    )
    criterion = nn.CrossEntropyLoss()

    start = time.perf_counter()

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            correct += (
                outputs.argmax(dim=1) == labels
            ).sum().item()
            total += labels.size(0)

        print(
            f"Rate {rate}% | Epoch {epoch + 1}/{EPOCHS} "
            f"| Loss {total_loss / len(train_loader):.4f} "
            f"| Accuracy {correct / total:.4f}"
        )

    training_time = time.perf_counter() - start

    model.eval()
    clean_correct = 0
    clean_total = 0
    attack_successes = 0
    attack_total = 0
    inference_time = 0.0

    with torch.inference_mode():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            start = time.perf_counter()
            outputs = model(images)

            if device.type == "mps":
                torch.mps.synchronize()

            inference_time += time.perf_counter() - start

            predictions = outputs.argmax(dim=1)
            clean_correct += (
                predictions == labels
            ).sum().item()
            clean_total += labels.size(0)

            eligible = labels != TARGET_LABEL

            if eligible.any():
                triggered = images[eligible].clone()
                triggered[:, :, -4:, -4:] = 1.0

                attack_predictions = model(
                    triggered
                ).argmax(dim=1)

                attack_successes += (
                    attack_predictions == TARGET_LABEL
                ).sum().item()

                attack_total += eligible.sum().item()

    MODELS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    model_path = MODELS / f"resnet18_poison_{rate}pct.pth"
    torch.save(model.state_dict(), model_path)

    result = {
        "poisoning_rate_percent": rate,
        "target_label": TARGET_LABEL,
        "trigger": "4x4 white square bottom-right",
        "epochs": EPOCHS,
        "training_samples": len(train_data),
        "poisoned_samples": len(train_data.poison_indices),
        "test_samples": clean_total,
        "clean_accuracy": clean_correct / clean_total,
        "attack_success_rate": (
            attack_successes / attack_total
            if attack_total else 0.0
        ),
        "attack_successes": attack_successes,
        "attack_eligible_samples": attack_total,
        "training_time_seconds": training_time,
        "inference_latency_seconds_per_image": (
            inference_time / clean_total
        ),
        "device": str(device),
        "checkpoint": str(model_path.relative_to(ROOT))
    }

    result_path = RESULTS / f"poison_{rate}pct.json"
    result_path.write_text(json.dumps(result, indent=2))

    print("\nEXPERIMENT COMPLETED")
    print(json.dumps(result, indent=2))
    print(f"Results saved: {result_path}")


if __name__ == "__main__":
    main()
