import time

import torch

from ml.data.dataset import get_dataloaders
from ml.models.resnet18 import create_model
from ml.evaluation.metrics import calculate_metrics


MODEL_PATH = "models/resnet18_baseline.pth"


def get_device():

    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def main():

    device = get_device()

    print("Device:", device)

    print("Loading CIFAR-10 dataset...")

    _, _, test_loader = get_dataloaders()

    print("Test batches:", len(test_loader))

    print()
    print("Loading ResNet18 model...")

    model = create_model().to(device)

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device,
        weights_only=True
    )

    model.load_state_dict(checkpoint)

    model.eval()

    print("Model loaded successfully.")

    y_true = []
    y_pred = []

    total_inference_time = 0.0
    total_samples = 0

    print()
    print("Running inference...")

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)

            start = time.perf_counter()

            outputs = model(images)

            if device.type == "mps":
                torch.mps.synchronize()

            end = time.perf_counter()

            total_inference_time += end - start

            total_samples += images.size(0)

            predictions = outputs.argmax(dim=1)

            y_true.extend(
                labels.cpu().numpy()
            )

            y_pred.extend(
                predictions.cpu().numpy()
            )

    metrics = calculate_metrics(
        y_true,
        y_pred
    )

    latency = (
        total_inference_time /
        total_samples
    )

    print()
    print("Baseline Metrics")
    print("====================")

    print(
        "Accuracy:",
        metrics["accuracy"]
    )

    print(
        "Precision:",
        metrics["precision"]
    )

    print(
        "Recall:",
        metrics["recall"]
    )

    print(
        "F1:",
        metrics["f1"]
    )

    print(
        "Inference latency per image:",
        latency,
        "seconds"
    )

    print()
    print("Confusion Matrix:")

    print(
        metrics["confusion_matrix"]
    )


if __name__ == "__main__":
    main()
