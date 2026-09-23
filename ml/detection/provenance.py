from pathlib import Path
import hashlib
import json


def sha256_file(path):

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:

        for block in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):

            sha256.update(block)

    return sha256.hexdigest()


def create_provenance():

    files = [
        "data/poisoned/images.npy",
        "data/poisoned/labels.npy",
        "data/poisoned/metadata.json"
    ]

    provenance = {}

    for file in files:

        path = Path(file)

        if path.exists():

            provenance[file] = {
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path)
            }

    provenance["dataset"] = "CIFAR-10"
    provenance["seed"] = 42
    provenance["label_poison_rate"] = 0.05
    provenance["feature_anomaly_rate"] = 0.02

    with open(
        "experiments/week3/data_provenance.json",
        "w"
    ) as f:

        json.dump(
            provenance,
            f,
            indent=2
        )

    print(
        json.dumps(
            provenance,
            indent=2
        )
    )


if __name__ == "__main__":
    create_provenance()
