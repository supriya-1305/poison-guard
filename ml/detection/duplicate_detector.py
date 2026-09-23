import hashlib
import numpy as np


def image_hash(image):
    """
    Generate an exact content hash for an image.
    """

    return hashlib.sha256(
        image.tobytes()
    ).hexdigest()


def detect_duplicates(images):

    seen = {}
    duplicate_indices = []

    for index, image in enumerate(images):

        h = image_hash(image)

        if h in seen:

            duplicate_indices.append(
                index
            )

        else:

            seen[h] = index

    return duplicate_indices
