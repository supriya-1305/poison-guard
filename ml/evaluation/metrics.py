import time

import torch
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from ml.data.dataset import get_dataloaders
from ml.models.resnet18 import create_model


MODEL_PATH = "models/resnet18_baseline.pth"


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def calculate_metrics(y_true, y_pred):

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm
    }


def main():

    device = get_device()

    print("Device:", device)

    print("Loading CIFAR-10 dataset...")

    train_loader, val_loader, test_loader = get_dataloaders()

    print("Test batches:", len(test_loader))

    print()
    print("Loading ResNet18 model...")

    model = create_model()

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device,
        weights_only=True
    )

    model.load_state_dict(checkpoint)

    model = model.to(device)

    model.eval()

    print("Model loaded successfully.")

    y_true = []
    y_pred = []

    print()
    print("Running inference...")

    # Warm-up
    with torch.no_grad():

        warmup_images, _ = next(iter(test_loader))

        warmup_images = warmup_images.to(device)

        _ = model(warmup_images)

        if device.type == "mps":
            torch.mps.synchronize()

    # Measure inference time
    start_time = time.perf_counter()

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)

            outputs = model(images)

            predictions = outputs.argmax(dim=1)

            y_true.extend(labels.cpu().numpy())

            y_pred.extend(predictions.cpu().numpy())

    if device.type == "mps":
        torch.mps.synchronize()

    inference_time = time.perf_counter() - start_time

    metrics = calculate_metrics(
        y_true,
        y_pred
    )

    total_samples = len(y_true)

    inference_latency_ms = (
        inference_time / total_samples
    ) * 1000

    print()
    print("==============================")
    print("DAY 5 — MODEL EVALUATION")
    print("==============================")

    print()
    print("Accuracy:", metrics["accuracy"])

    print("Precision:", metrics["precision"])

    print("Recall:", metrics["recall"])

    print("F1 Score:", metrics["f1"])

    print()
    print("Inference Time:",
          inference_time,
          "seconds")

    print(
        "Inference Latency:",
        inference_latency_ms,
        "ms/image"
    )

    print()
    print("Confusion Matrix:")
    print(metrics["confusion_matrix"])

    print()
    print("Number of test samples:",
          total_samples)


if __name__ == "__main__":
    main()
