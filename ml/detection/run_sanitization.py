import json
from pathlib import Path

import numpy as np

from ml.detection.scanner import (
    run_scanner
)


DATA_DIR = Path(
    "data/poisoned"
)

OUTPUT_DIR = Path(
    "experiments/week3/results"
)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 60)
    print("PoisonGuard Data Sanitization Engine v1")
    print("=" * 60)

    print("\nLoading dataset...")

    images = np.load(
        DATA_DIR / "images.npy"
    )

    labels = np.load(
        DATA_DIR / "labels.npy"
    )

    features = np.load(
        DATA_DIR / "features.npy"
    )

    with open(
        DATA_DIR / "metadata.json"
    ) as f:

        metadata = json.load(f)

    print(
        "Images:",
        images.shape
    )

    print(
        "Labels:",
        labels.shape
    )

    print(
        "Features:",
        features.shape
    )

    print(
        "Metadata:",
        len(metadata)
    )

    results = run_scanner(
        images,
        labels,
        features,
        metadata
    )

    output_file = (
        OUTPUT_DIR /
        "sanitization_results.json"
    )

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )

    print("\nScanner completed.")

    print(
        "Results saved to:",
        output_file
    )


if __name__ == "__main__":
    main()
