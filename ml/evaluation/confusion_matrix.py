import torch
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

from ml.data.dataset import get_dataloaders
from ml.models.resnet18 import create_model


MODEL_PATH = "models/resnet18_baseline.pth"
OUTPUT_PATH = "experiments/confusion_matrix_baseline.png"


CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]


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

    print()
    print("Generating predictions...")

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)

            outputs = model(images)

            predictions = outputs.argmax(dim=1)

            y_true.extend(
                labels.numpy()
            )

            y_pred.extend(
                predictions.cpu().numpy()
            )

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    print()
    print("Confusion Matrix:")
    print(cm)

    plt.figure(figsize=(10, 8))

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.title(
        "PoisonGuard - ResNet18 CIFAR-10 Baseline"
    )

    plt.colorbar()

    tick_marks = range(len(CLASSES))

    plt.xticks(
        tick_marks,
        CLASSES,
        rotation=45,
        ha="right"
    )

    plt.yticks(
        tick_marks,
        CLASSES
    )

    threshold = cm.max() / 2.0

    for i in range(cm.shape[0]):

        for j in range(cm.shape[1]):

            plt.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center"
            )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print()
    print("Confusion matrix image saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
