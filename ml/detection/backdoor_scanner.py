from ml.detection.backdoor_risk import (
    calculate_backdoor_risk,
    classify_risk
)


def scan_model(
    activation_score,
    strip_score
):

    risk = calculate_backdoor_risk(
        activation_score,
        strip_score
    )

    status = classify_risk(risk)

    return {
        "activation_score": activation_score,
        "strip_score": strip_score,
        "backdoor_risk": risk,
        "status": status
    }


if __name__ == "__main__":

    result = scan_model(
        activation_score=80,
        strip_score=75
    )

    print(result)
