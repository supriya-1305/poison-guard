import json

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)


RESULT_FILE = (
    "experiments/week3/results/"
    "sanitization_results.json"
)


def main():

    with open(RESULT_FILE, "r") as f:
        results = json.load(f)

    y_true = []
    y_pred = []

    for result in results:

        # Ground truth:
        # anything other than "clean" is actually poisoned
        actual = (
            result["ground_truth_poison"] != "clean"
        )

        # Prediction:
        # QUARANTINED means detected as suspicious
        predicted = (
            result["status"] == "QUARANTINED"
        )

        y_true.append(int(actual))
        y_pred.append(int(predicted))

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    print()
    print("====================================")
    print("POISONGUARD SANITIZATION METRICS")
    print("====================================")

    print()
    print("Confusion Matrix:")
    print(cm)

    tn, fp, fn, tp = cm.ravel()

    print()
    print("True Negatives :", tn)
    print("False Positives:", fp)
    print("False Negatives:", fn)
    print("True Positives :", tp)

    print()
    print("Classification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=[
                "Clean",
                "Poisoned"
            ],
            zero_division=0
        )
    )


if __name__ == "__main__":
    main()
