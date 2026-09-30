import math

import torch
import torch.nn as nn
from torchvision.models import resnet18


def load_model():

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


def entropy(probabilities):

    probabilities = probabilities[
        probabilities > 0
    ]

    return -torch.sum(
        probabilities *
        torch.log(probabilities)
    ).item()


def strip_score(
    model,
    image,
    reference_images,
    repetitions=10
):

    entropies = []

    for i in range(repetitions):

        reference = reference_images[
            i % len(reference_images)
        ]

        mixed = (
            0.5 * image +
            0.5 * reference
        )

        with torch.no_grad():

            output = model(
                mixed.unsqueeze(0)
            )

            probabilities = torch.softmax(
                output,
                dim=1
            )[0]

        entropies.append(
            entropy(probabilities)
        )

    return sum(entropies) / len(entropies)


def main():

    model = load_model()

    print(
        "STRIP-style detector initialized."
    )

    print(
        "Use prediction entropy to "
        "compare clean and triggered inputs."
    )


if __name__ == "__main__":
    main()
