def calculate_backdoor_risk(
    activation_score,
    strip_score
):

    activation_score = max(
        0,
        min(100, activation_score)
    )

    strip_score = max(
        0,
        min(100, strip_score)
    )

    risk = (
        0.6 * activation_score +
        0.4 * strip_score
    )

    return round(risk, 2)


def classify_risk(risk):

    if risk >= 70:
        return "HIGH RISK"

    if risk >= 40:
        return "SUSPICIOUS"

    return "SAFE"
