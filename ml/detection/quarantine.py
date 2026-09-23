import json
from pathlib import Path


RESULT_FILE = (
    "experiments/week3/results/"
    "sanitization_results.json"
)

OUTPUT_FILE = (
    "data/quarantine/"
    "quarantine_manifest.json"
)


def main():

    with open(RESULT_FILE, "r") as f:
        results = json.load(f)

    quarantined = [
        result
        for result in results
        if result["status"] == "QUARANTINED"
    ]

    Path("data/quarantine").mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            quarantined,
            f,
            indent=2
        )

    print("Quarantined samples:", len(quarantined))
    print("Manifest:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
