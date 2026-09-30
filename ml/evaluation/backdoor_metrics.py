import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torchvision.models import resnet18
from torch.utils.data import DataLoader


TARGET_LABEL = 0


def add_trigger(image, size=4):

    image = image.clone()

    image[:, -size:, -size:] = 1.0

    return image


def create_model():

    model = resnet18(weights=None)

    model.fc = nn.Linear(
        model.fc.in_features,
        10
    )

    model.load_state_dict(
        torch.load(
            "models/week4/backdoored_resnet18.pth",
            map_location="cpu"
        )
    )

    model.eval()

    return model


def main():

    transform = transforms.ToTensor()

    dataset = datasets.CIFAR10(
        root="data",
        train=False,
        download=True,
        transform=transform
    )

    loader = DataLoader(
        dataset,
        batch_size=128,
        shuffle=False
    )

    model = create_model()

    clean_correct = 0
    total = 0

    attack_success = 0

    for images, labels in loader:

        outputs = model(images)

        predictions = outputs.argmax(
            dim=1
        )

        clean_correct += (
            predictions == labels
        ).sum().item()

        triggered_images = torch.stack(
            [
                add_trigger(image)
                for image in images
            ]
        )

        triggered_outputs = model(
            triggered_images
        )

        triggered_predictions = (
            triggered_outputs.argmax(dim=1)
        )

        attack_success += (
            triggered_predictions == TARGET_LABEL
        ).sum().item()

        total += labels.size(0)

    clean_accuracy = clean_correct / total

    attack_success_rate = (
        attack_success / total
    )

    print(
        f"Clean Accuracy: "
        f"{clean_accuracy * 100:.2f}%"
    )

    print(
        f"Attack Success Rate: "
        f"{attack_success_rate * 100:.2f}%"
    )


if __name__ == "__main__":
    main()
