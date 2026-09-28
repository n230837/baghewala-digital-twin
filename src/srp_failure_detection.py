import numpy as np


# ============================================================
# SRP FAILURE / OPERATING CONDITION DETECTION
# ============================================================

def detect_rod_floating(
    viscosity_cp,
    spm,
    pump_fillage,
    rod_load_range
):
    """
    Prototype rod-floating indicator.

    Higher viscosity, higher pumping speed, low pump fillage,
    and abnormal load behavior increase the likelihood of
    rod-floating conditions.

    Returns:
        score       : 0–100 indicator
        status      : NORMAL / WARNING / HIGH RISK
    """

    if viscosity_cp <= 0:
        raise ValueError("Viscosity must be positive.")

    if spm < 0:
        raise ValueError("SPM cannot be negative.")

    if not 0 <= pump_fillage <= 100:
        raise ValueError(
            "Pump fillage must be between 0 and 100%."
        )

    if rod_load_range < 0:
        raise ValueError(
            "Rod load range cannot be negative."
        )

    # --------------------------------------------------------
    # Individual stress factors
    # --------------------------------------------------------

    viscosity_factor = min(
        viscosity_cp / 10000.0,
        2.0
    )

    speed_factor = min(
        spm / 6.0,
        2.0
    )

    low_fillage_factor = max(
        0.0,
        (50.0 - pump_fillage) / 50.0
    )

    load_factor = min(
        rod_load_range / 5000.0,
        2.0
    )

    # --------------------------------------------------------
    # Composite rod-floating indicator
    # --------------------------------------------------------

    score = (
        0.35 * viscosity_factor +
        0.20 * speed_factor +
        0.30 * low_fillage_factor +
        0.15 * load_factor
    ) * 50.0

    score = float(
        np.clip(score, 0.0, 100.0)
    )

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    if score < 30:
        status = "NORMAL"

    elif score < 60:
        status = "WARNING"

    else:
        status = "HIGH RISK"

    return {
        "rod_floating_score": score,
        "rod_floating_status": status
    }


# ============================================================
# IMPACT LOADING DETECTION
# ============================================================

def detect_impact_loading(
    rod_load_range,
    spm,
    pump_fillage
):
    """
    Prototype impact-loading indicator.

    Large rod-load variation combined with high pumping speed
    and high pump fillage can indicate potentially severe
    loading conditions.

    Returns:
        score       : 0–100 indicator
        status      : NORMAL / WARNING / HIGH RISK
    """

    if rod_load_range < 0:
        raise ValueError(
            "Rod load range cannot be negative."
        )

    if spm < 0:
        raise ValueError("SPM cannot be negative.")

    if not 0 <= pump_fillage <= 100:
        raise ValueError(
            "Pump fillage must be between 0 and 100%."
        )

    # --------------------------------------------------------
    # Load variation
    # --------------------------------------------------------

    load_factor = min(
        rod_load_range / 5000.0,
        2.0
    )

    # --------------------------------------------------------
    # Pump speed
    # --------------------------------------------------------

    speed_factor = min(
        spm / 6.0,
        2.0
    )

    # --------------------------------------------------------
    # High fillage contribution
    # --------------------------------------------------------

    high_fillage_factor = max(
        0.0,
        (pump_fillage - 80.0) / 20.0
    )

    # --------------------------------------------------------
    # Composite impact-loading indicator
    # --------------------------------------------------------

    score = (
        0.50 * load_factor +
        0.30 * speed_factor +
        0.20 * high_fillage_factor
    ) * 50.0

    score = float(
        np.clip(score, 0.0, 100.0)
    )

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    if score < 30:
        status = "NORMAL"

    elif score < 60:
        status = "WARNING"

    else:
        status = "HIGH RISK"

    return {
        "impact_loading_score": score,
        "impact_loading_status": status
    }


# ============================================================
# COMBINED SRP CONDITION
# ============================================================

def evaluate_srp_condition(
    viscosity_cp,
    spm,
    pump_fillage,
    rod_load_range
):
    """
    Evaluate rod-floating and impact-loading conditions
    together.
    """

    rod_floating = detect_rod_floating(
        viscosity_cp=viscosity_cp,
        spm=spm,
        pump_fillage=pump_fillage,
        rod_load_range=rod_load_range
    )

    impact_loading = detect_impact_loading(
        rod_load_range=rod_load_range,
        spm=spm,
        pump_fillage=pump_fillage
    )

    overall_score = (
        0.50 * rod_floating["rod_floating_score"] +
        0.50 * impact_loading["impact_loading_score"]
    )

    if overall_score < 30:
        overall_status = "NORMAL"

    elif overall_score < 60:
        overall_status = "WARNING"

    else:
        overall_status = "HIGH RISK"

    return {
        **rod_floating,
        **impact_loading,
        "overall_srp_condition_score": float(
            overall_score
        ),
        "overall_srp_condition": overall_status
    }