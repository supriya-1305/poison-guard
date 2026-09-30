import numpy as np
import torch

from ml.detection.strip_detector import (
    load_model,
    strip_score
)


def add_trigger(image):

    image = image.clone()

    image[:, -4:, -4:] = 1.0

    return image


def main():

    images = np.load(
        "data/backdoor/images.npy"
    )

    model = load_model()

    reference_images = torch.tensor(
        images[100:120],
        dtype=torch.float32
    )

    clean_image = torch.tensor(
        images[0],
        dtype=torch.float32
    )

    triggered_image = add_trigger(
        clean_image
    )

    clean_score = strip_score(
        model,
        clean_image,
        reference_images
    )

    triggered_score = strip_score(
        model,
        triggered_image,
        reference_images
    )

    print(
        f"Clean entropy: {clean_score:.6f}"
    )

    print(
        f"Triggered entropy: {triggered_score:.6f}"
    )


if __name__ == "__main__":
    main()
