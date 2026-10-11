
import json
import time
from pathlib import Path

import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from ml.models.resnet18 import create_model

MODEL_PATH = "models/week5/backdoored_resnet18.pth"
RESULTS_PATH = "experiments/week5/evaluation_results.json"
TARGET_LABEL = 0
BATCH_SIZE = 128


def add_trigger(images):
    """Apply the same 4x4 white-square trigger used during training."""
    images = images.clone()
    images[:, :, -4:, -4:] = 1.0
    return images


def main():
    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )
    print("Device:", device)

    model = create_model().to(device)
    state = torch.load(
        MODEL_PATH,
        map_location=device,
        weights_only=True
    )
    model.load_state_dict(state)
    model.eval()
    print("Week 5 model loaded successfully.")

    dataset = datasets.CIFAR10(
        root="data",
        train=False,
        download=True,
        transform=transforms.ToTensor()
    )
    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0
    )

    clean_correct = 0
    clean_total = 0
    attack_successes = 0
    attack_total = 0
    start = time.perf_counter()

    with torch.inference_mode():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            # Evaluate normal, unmodified test images.
            clean_predictions = model(images).argmax(dim=1)
            clean_correct += (clean_predictions == labels).sum().item()
            clean_total += labels.size(0)

            # Evaluate triggered images, excluding target-class images.
            eligible = labels != TARGET_LABEL
            if eligible.any():
                triggered = add_trigger(images[eligible])
                triggered_predictions = model(triggered).argmax(dim=1)
                attack_successes += (
                    triggered_predictions == TARGET_LABEL
                ).sum().item()
                attack_total += eligible.sum().item()

    elapsed = time.perf_counter() - start
    clean_accuracy = clean_correct / clean_total
    asr = attack_successes / attack_total if attack_total else 0.0

    results = {
        "model": MODEL_PATH,
        "test_dataset": "CIFAR-10 test split",
        "test_samples": clean_total,
        "target_label": TARGET_LABEL,
        "clean_correct": clean_correct,
        "clean_accuracy": clean_accuracy,
        "attack_successes": attack_successes,
        "attack_eligible_samples": attack_total,
        "attack_success_rate": asr,
        "evaluation_time_seconds": elapsed
    }

    Path(RESULTS_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w") as file:
        json.dump(results, file, indent=2)

    print("\n===== WEEK 5 BACKDOOR EVALUATION =====")
    print(f"Clean test accuracy: {clean_accuracy:.4%}")
    print(f"Attack success rate: {asr:.4%}")
    print(f"Successful target predictions: {attack_successes}/{attack_total}")
    print(f"Evaluation time: {elapsed:.2f} seconds")
    print("Results saved to:", RESULTS_PATH)


if __name__ == "__main__":
    main()

