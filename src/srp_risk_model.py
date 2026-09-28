# --------------------------------------------------
# BAGHEWALA SRP RISK MODEL
# --------------------------------------------------

def calculate_rod_floating_risk(
    viscosity_cp,
    spm,
    stroke_length_m
):
    """
    Prototype estimate of rod-floating risk.

    Higher viscosity and aggressive pumping conditions
    can increase the likelihood of undesirable rod/pump
    behavior.

    This is NOT a calibrated field failure model yet.
    """

    # Higher viscosity increases resistance
    viscosity_factor = viscosity_cp / 5000.0

    # Higher SPM increases dynamic loading
    speed_factor = spm / 6.0

    # Longer stroke increases mechanical movement
    stroke_factor = stroke_length_m / 2.5

    risk_score = (
        0.50 * viscosity_factor
        + 0.30 * speed_factor
        + 0.20 * stroke_factor
    )

    # Convert to 0–100 scale
    risk_score = risk_score * 50

    # Keep score within 0–100
    risk_score = max(
        0.0,
        min(risk_score, 100.0)
    )

    return risk_score


def classify_risk(risk_score):
    """
    Convert numerical risk into a simple category.
    """

    if risk_score < 30:
        return "LOW"

    elif risk_score < 60:
        return "MEDIUM"

    else:
        return "HIGH"


if __name__ == "__main__":

    viscosity = 7000.0
    spm = 6.0
    stroke = 2.5

    risk = calculate_rod_floating_risk(
        viscosity,
        spm,
        stroke
    )

    category = classify_risk(risk)

    print("Baghewala SRP Risk Model")
    print("------------------------")

    print(f"Oil viscosity : {viscosity:.0f} cP")
    print(f"SPM           : {spm:.1f}")
    print(f"Stroke        : {stroke:.2f} m")
    print(f"Risk score    : {risk:.2f}/100")
    print(f"Risk level    : {category}")