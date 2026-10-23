
import json
import time
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from ml.models.resnet18 import create_model


MODEL_PATH = Path(
    "models/week7/resnet18_sanitized_candidate.pth"
)
OUTPUT_PATH = Path(
    "experiments/week7/results/sanitized_candidate_evaluation.json"
)

TARGET_LABEL = 0
BATCH_SIZE = 128

CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD = (0.2470, 0.2435, 0.2616)


def add_trigger(images):
    """Apply a white 4x4 trigger in normalized image space."""
    images = images.clone()

    mean = images.new_tensor(CIFAR_MEAN).view(1, 3, 1, 1)
    std = images.new_tensor(CIFAR_STD).view(1, 3, 1, 1)

    # White pixels in [0, 1], converted to normalized values.
    white = (1.0 - mean) / std
    images[:, :, -4:, -4:] = white

    return images

def main():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(MODEL_PATH)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )
    print("Device:", device)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
    ])

    test_dataset = datasets.CIFAR10(
        root="data",
        train=False,
        download=True,
        transform=transform,
    )

    loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
    )

    model = create_model().to(device)
    state = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )
    model.load_state_dict(state)
    model.eval()

    clean_correct = 0
    total = 0
    attack_successes = 0
    attack_total = 0
    start = time.perf_counter()

    with torch.inference_mode():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            clean_predictions = model(images).argmax(dim=1)
            clean_correct += (
                clean_predictions == labels
            ).sum().item()
            total += labels.size(0)

            # Exclude samples already belonging to the target class.
            eligible = labels != TARGET_LABEL

            if eligible.any():
                triggered_images = add_trigger(images[eligible])
                triggered_predictions = model(
                    triggered_images
                ).argmax(dim=1)

                attack_successes += (
                    triggered_predictions == TARGET_LABEL
                ).sum().item()
                attack_total += eligible.sum().item()

    elapsed = time.perf_counter() - start

    results = {
        "model": str(MODEL_PATH),
        "dataset": "CIFAR-10 test split",
        "test_samples": total,
        "target_label": TARGET_LABEL,
        "clean_correct": clean_correct,
        "clean_accuracy": clean_correct / total,
        "attack_successes": attack_successes,
        "attack_eligible_samples": attack_total,
        "attack_success_rate": (
            attack_successes / attack_total
            if attack_total else 0.0
        ),
        "evaluation_time_seconds": elapsed,
        "status": "evaluated_not_yet_approved",
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(results, indent=2))

    print("\n===== WEEK 7 CANDIDATE EVALUATION =====")
    print(f"Clean accuracy: {results['clean_accuracy']:.2%}")
    print(
        "Attack success rate: "
        f"{results['attack_success_rate']:.2%}"
    )
    print(
        "Successful triggered predictions: "
        f"{attack_successes}/{attack_total}"
    )
    print("Evaluation time:", round(elapsed, 2), "seconds")
    print("Results saved to:", OUTPUT_PATH)
    print("Status: evaluated_not_yet_approved")


if __name__ == "__main__":
    main()

