
import json
from collections import Counter
from pathlib import Path

RESULTS_FILE = Path(
    "experiments/week3/results/sanitization_results.json"
)
METADATA_FILE = Path("data/poisoned/metadata.json")
OUTPUT_FILE = Path(
    "experiments/week7/results/sanitization_manifest.json"
)
REPORT_FILE = Path(
    "experiments/week7/results/sanitization_evaluation.txt"
)

RISK_THRESHOLD = 40.0


def main():
    if not RESULTS_FILE.is_file():
        raise FileNotFoundError(RESULTS_FILE)

    if not METADATA_FILE.is_file():
        raise FileNotFoundError(METADATA_FILE)

    results = json.loads(RESULTS_FILE.read_text())
    metadata = json.loads(METADATA_FILE.read_text())

    if len(results) != len(metadata):
        raise ValueError(
            "Scanner results and metadata lengths do not match."
        )

    retained = []
    quarantined = []

    for result, meta in zip(results, metadata):
        index = int(result["dataset_index"])

        if index != int(meta["dataset_index"]):
            raise ValueError(
                f"Dataset index mismatch at position {index}."
            )

        risk = float(result["risk_score"])

        record = {
            "dataset_index": index,
            "sample_id": meta["sample_id"],
            "risk_score": risk,
            "decision": (
                "QUARANTINED"
                if risk >= RISK_THRESHOLD
                else "RETAINED"
            ),
        }

        if risk >= RISK_THRESHOLD:
            quarantined.append(record)
        else:
            retained.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "experiment": "PoisonGuard Week 7 sanitization",
        "risk_threshold": RISK_THRESHOLD,
        "source_results": str(RESULTS_FILE),
        "source_metadata": str(METADATA_FILE),
        "original_sample_count": len(results),
        "retained_count": len(retained),
        "quarantined_count": len(quarantined),
        "retained_indices": [
            item["dataset_index"] for item in retained
        ],
        "quarantined_indices": [
            item["dataset_index"] for item in quarantined
        ],
        "quarantined_samples": quarantined,
        "note": (
            "Experimental manifest only. Original data are unchanged. "
            "Retention does not guarantee samples are clean."
        ),
    }

    OUTPUT_FILE.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    # Ground-truth labels are used only for retrospective evaluation,
    # never to make the retention/quarantine decision.
    actual_poisoned = [
        meta["poison_type"] != "clean" for meta in metadata
    ]
    predicted_quarantined = [
        float(result["risk_score"]) >= RISK_THRESHOLD
        for result in results
    ]

    tp = sum(a and p for a, p in zip(
        actual_poisoned, predicted_quarantined
    ))
    fp = sum((not a) and p for a, p in zip(
        actual_poisoned, predicted_quarantined
    ))
    fn = sum(a and (not p) for a, p in zip(
        actual_poisoned, predicted_quarantined
    ))
    tn = sum((not a) and (not p) for a, p in zip(
        actual_poisoned, predicted_quarantined
    ))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    report = [
        "PoisonGuard Week 7 — Sanitization Evaluation",
        f"Risk threshold: {RISK_THRESHOLD}",
        f"Total samples: {len(results)}",
        f"Retained: {len(retained)}",
        f"Quarantined: {len(quarantined)}",
        f"TP: {tp}",
        f"FP: {fp}",
        f"FN: {fn}",
        f"TN: {tn}",
        f"Precision: {precision:.4f}",
        f"Recall: {recall:.4f}",
        "",
        "Ground truth is used only for retrospective evaluation.",
        "This result does not prove backdoor removal.",
    ]

    REPORT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n".join(report))
    print("Manifest saved to:", OUTPUT_FILE)
    print("Report saved to:", REPORT_FILE)


if __name__ == "__main__":
    main()

