import numpy as np

from ml.detection.duplicate_detector import (
    detect_duplicates
)


def test_duplicate_detection():

    image1 = np.zeros(
        (32, 32, 3),
        dtype=np.uint8
    )

    image2 = image1.copy()

    image3 = np.ones(
        (32, 32, 3),
        dtype=np.uint8
    )

    images = np.array([
        image1,
        image2,
        image3
    ])

    duplicates = detect_duplicates(
        images
    )

    assert 1 in duplicates
