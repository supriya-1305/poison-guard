def get_status(risk_score):

    if risk_score >= 70:

        return "QUARANTINED"

    return "CLEAN"


def get_risk_level(risk_score):

    if risk_score >= 70:

        return "HIGH"

    if risk_score >= 40:

        return "MEDIUM"

    return "LOW"
