# ============================================================
# SRP RELIABILITY MODEL
# ============================================================
#
# Prototype risk/operating-state model.
#
# IMPORTANT:
# This is NOT a measured Baghewala failure-probability model.
# It is a physics/feature-based prototype that will later be
# calibrated with actual field failure/intervention data.
# ============================================================


# ============================================================
# LIMITS / REFERENCE VALUES
# ============================================================

REFERENCE_VISCOSITY_CP = 5000.0
REFERENCE_SPM = 5.0
REFERENCE_LOAD_RANGE_KG = 2500.0

LOW_FILLAGE_THRESHOLD = 40.0
HIGH_FILLAGE_THRESHOLD = 90.0

HIGH_LOAD_THRESHOLD_KG = 2647.39


# ============================================================
# INDIVIDUAL RISK INDICATORS
# ============================================================

def calculate_viscosity_stress(viscosity_cp):

    if viscosity_cp <= 0:
        raise ValueError("Viscosity must be positive.")

    stress = viscosity_cp / REFERENCE_VISCOSITY_CP

    # Convert to 0–100 scale
    score = min(stress * 50.0, 100.0)

    return score


def calculate_speed_stress(spm):

    if spm < 0:
        raise ValueError("SPM cannot be negative.")

    # Higher speed increases mechanical cycling.
    score = (spm / REFERENCE_SPM) * 50.0

    return min(score, 100.0)


def calculate_load_stress(rod_load_range):

    if rod_load_range < 0:
        raise ValueError(
            "Rod-load range cannot be negative."
        )

    score = (
        rod_load_range
        / REFERENCE_LOAD_RANGE_KG
    ) * 50.0

    return min(score, 100.0)


def calculate_fillage_risk(pump_fillage):

    if not 0 <= pump_fillage <= 100:
        raise ValueError(
            "Pump fillage must be between 0 and 100%."
        )

    # Very low fillage indicates poor pump utilization.
    if pump_fillage < LOW_FILLAGE_THRESHOLD:

        risk = 100.0 - (
            pump_fillage
            / LOW_FILLAGE_THRESHOLD
            * 50.0
        )

    # Extremely high fillage can indicate an operating
    # condition approaching the upper envelope.
    elif pump_fillage > HIGH_FILLAGE_THRESHOLD:

        risk = (
            pump_fillage
            - HIGH_FILLAGE_THRESHOLD
        ) * 5.0

    else:

        risk = 0.0

    return min(max(risk, 0.0), 100.0)


# ============================================================
# ROD FLOATING INDICATOR
# ============================================================

def calculate_rod_floating_indicator(
    viscosity_cp,
    spm,
    pump_fillage
):

    viscosity_factor = (
        viscosity_cp
        / REFERENCE_VISCOSITY_CP
    )

    speed_factor = (
        spm
        / REFERENCE_SPM
    )

    # High viscosity + high speed + poor fillage
    # represents a potentially unfavorable operating state.
    indicator = (
        0.45 * viscosity_factor
        + 0.30 * speed_factor
        + 0.25 * (1.0 - pump_fillage / 100.0)
    )

    indicator *= 100.0

    return min(max(indicator, 0.0), 100.0)


# ============================================================
# OVERALL RELIABILITY SCORE
# ============================================================

def calculate_reliability_score(
    viscosity_cp,
    spm,
    rod_load_range,
    pump_fillage
):

    viscosity_stress = calculate_viscosity_stress(
        viscosity_cp
    )

    speed_stress = calculate_speed_stress(
        spm
    )

    load_stress = calculate_load_stress(
        rod_load_range
    )

    fillage_risk = calculate_fillage_risk(
        pump_fillage
    )

    rod_floating_indicator = (
        calculate_rod_floating_indicator(
            viscosity_cp,
            spm,
            pump_fillage
        )
    )

    # Weighted prototype score
    reliability_risk = (
        0.25 * viscosity_stress
        + 0.15 * speed_stress
        + 0.30 * load_stress
        + 0.10 * fillage_risk
        + 0.20 * rod_floating_indicator
    )

    return min(
        max(reliability_risk, 0.0),
        100.0
    )


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_reliability(risk_score):

    if risk_score < 25:

        return "LOW RISK"

    elif risk_score < 50:

        return "MODERATE RISK"

    elif risk_score < 75:

        return "HIGH RISK"

    else:

        return "VERY HIGH RISK"


# ============================================================
# COMPLETE SRP RELIABILITY ANALYSIS
# ============================================================

def analyze_srp_reliability(
    viscosity_cp,
    spm,
    rod_load_range,
    pump_fillage
):

    viscosity_stress = calculate_viscosity_stress(
        viscosity_cp
    )

    speed_stress = calculate_speed_stress(
        spm
    )

    load_stress = calculate_load_stress(
        rod_load_range
    )

    fillage_risk = calculate_fillage_risk(
        pump_fillage
    )

    rod_floating_indicator = (
        calculate_rod_floating_indicator(
            viscosity_cp,
            spm,
            pump_fillage
        )
    )

    reliability_risk = calculate_reliability_score(
        viscosity_cp=viscosity_cp,
        spm=spm,
        rod_load_range=rod_load_range,
        pump_fillage=pump_fillage
    )

    classification = classify_reliability(
        reliability_risk
    )

    return {

        "viscosity_stress": viscosity_stress,

        "speed_stress": speed_stress,

        "load_stress": load_stress,

        "fillage_risk": fillage_risk,

        "rod_floating_indicator":
            rod_floating_indicator,

        "overall_risk_score":
            reliability_risk,

        "risk_class":
            classification
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("          SRP RELIABILITY MODEL")
    print("================================================")

    # Example operating condition
    viscosity = 4049.40
    spm = 3.5
    rod_load_range = 1250.0
    pump_fillage = 91.68

    result = analyze_srp_reliability(
        viscosity_cp=viscosity,
        spm=spm,
        rod_load_range=rod_load_range,
        pump_fillage=pump_fillage
    )

    print("\nINPUT")
    print("----------------")

    print(
        f"Viscosity       : "
        f"{viscosity:.2f} cP"
    )

    print(
        f"SPM             : "
        f"{spm:.2f}"
    )

    print(
        f"Rod load range  : "
        f"{rod_load_range:.2f} kg"
    )

    print(
        f"Pump fillage    : "
        f"{pump_fillage:.2f}%"
    )

    print("\nRELIABILITY ANALYSIS")
    print("----------------")

    print(
        f"Viscosity stress       : "
        f"{result['viscosity_stress']:.2f}"
    )

    print(
        f"Speed stress           : "
        f"{result['speed_stress']:.2f}"
    )

    print(
        f"Load stress            : "
        f"{result['load_stress']:.2f}"
    )

    print(
        f"Fillage risk           : "
        f"{result['fillage_risk']:.2f}"
    )

    print(
        f"Rod floating indicator : "
        f"{result['rod_floating_indicator']:.2f}"
    )

    print(
        f"Overall risk score     : "
        f"{result['overall_risk_score']:.2f}"
    )

    print(
        f"Risk class             : "
        f"{result['risk_class']}"
    )

    print("\n================================================")
    print("       SRP RELIABILITY MODEL COMPLETE")
    print("================================================")