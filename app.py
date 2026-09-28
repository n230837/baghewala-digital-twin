import os
import sys

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from thermal_model import simulate_css_cycle
from viscosity_model_v2 import calculate_viscosity
from production_model_v2 import calculate_production_rate
from srp_candidate_predictor import predict_candidate
from srp_reliability_model import calculate_reliability_score
from srp_failure_detection import evaluate_srp_condition
from vfd_model import evaluate_vfd_setting

from digital_twin_3d import create_digital_twin_3d

from three_objective_optimizer import (
    find_three_objective_pareto_front
)

from integrated_reliability_optimizer import (
    run_reliability_optimization
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Baghewala Digital Twin",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 0.1rem;
}

.hero-subtitle {
    font-size: 1rem;
    opacity: 0.7;
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.5rem;
    margin-bottom: 0.7rem;
}

.pipeline-box {
    text-align: center;
    padding: 0.7rem 0.3rem;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.20);
    background: rgba(128,128,128,0.05);
    min-height: 95px;
}

.pipeline-icon {
    font-size: 1.4rem;
}

.pipeline-name {
    font-size: 0.75rem;
    font-weight: 650;
    margin-top: 0.2rem;
}

.pipeline-value {
    font-size: 0.78rem;
    opacity: 0.65;
    margin-top: 0.3rem;
}

.footer {
    text-align: center;
    opacity: 0.5;
    font-size: 0.75rem;
    margin-top: 2rem;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">🛢️ BAGHEWALA DIGITAL TWIN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'AI-Enabled Well-to-Surface Optimization • CSS + SRP • Heavy-Oil Operations'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ CONTROL PANEL")
st.sidebar.caption("Configure the operating scenario")

st.sidebar.markdown("### WELL")

well_id = st.sidebar.selectbox(
    "Reference Well",
    [
        "NK-68",
        "NK-7",
        "NK-77",
        "NK-82",
        "NK-86",
        "NK-91",
        "NK-93"
    ]
)


# ============================================================
# CSS CONTROLS
# ============================================================

st.sidebar.markdown("### 🔥 CSS")

steam_temperature = st.sidebar.slider(
    "Steam Temperature",
    250,
    320,
    285,
    5
)

steam_volume = st.sidebar.slider(
    "Steam Volume (m³)",
    300,
    700,
    500,
    100
)

injection_days = st.sidebar.slider(
    "Injection Duration (days)",
    14,
    21,
    21,
    1
)

soak_days = st.sidebar.slider(
    "Soak Duration (days)",
    5,
    7,
    5,
    1
)


# ============================================================
# SRP / VFD CONTROL
# ============================================================

st.sidebar.markdown("### ⚙️ SRP / VFD")

vfd_frequency = st.sidebar.slider(
    "VFD Frequency (Hz)",
    35.0,
    60.0,
    45.0,
    1.0
)

vfd_state = evaluate_vfd_setting(
    vfd_frequency_hz=vfd_frequency
)

spm = vfd_state["spm"]


# ============================================================
# DIGITAL TWIN CALCULATIONS
# ============================================================

thermal = simulate_css_cycle(
    initial_temperature_c=47.0,
    steam_temperature_c=steam_temperature,
    steam_volume_m3=steam_volume,
    injection_days=injection_days,
    soak_days=soak_days
)

production_temperature = (
    thermal["production_start_temperature_c"]
)

viscosity = calculate_viscosity(
    production_temperature
)

srp = predict_candidate(
    well_id=well_id,
    viscosity_cp=viscosity,
    spm=spm
)

production = calculate_production_rate(
    viscosity_cp=viscosity,
    pump_fillage_percent=srp["predicted_pump_fillage"],
    pump_efficiency=1.0
)

risk = calculate_reliability_score(
    viscosity_cp=viscosity,
    spm=spm,
    rod_load_range=srp["state_load_range"],
    pump_fillage=srp["predicted_pump_fillage"]
)


# ============================================================
# RISK CLASSIFICATION
# ============================================================

if risk < 30:
    risk_class = "LOW"

elif risk < 60:
    risk_class = "MEDIUM"

else:
    risk_class = "HIGH"


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🧠 DIGITAL TWIN",
        "🧊 3D DIGITAL TWIN",
        "🚀 OPTIMIZATION",
        "⚠️ FAILURE DETECTION"
    ]
)


# ============================================================
# TAB 1 — DIGITAL TWIN
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        'LIVE WELL STATE'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🌡️ PRODUCTION TEMPERATURE",
            f"{production_temperature:.1f} °C"
        )

        st.caption("After CSS soak")


    with c2:

        st.metric(
            "💧 OIL VISCOSITY",
            f"{viscosity:,.0f} cP"
        )

        st.caption("Temperature-dependent")


    with c3:

        st.metric(
            "🛢️ PREDICTED PRODUCTION",
            f"{production:.2f} BPD"
        )

        st.caption("Prototype prediction")


    with c4:

        st.metric(
            "🛡️ SRP RISK",
            f"{risk:.1f}/100"
        )

        st.caption(
            f"{risk_class} • Prototype indicator"
        )


    # ========================================================
    # PIPELINE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        'WELL-TO-SURFACE DIGITAL TWIN'
        '</div>',
        unsafe_allow_html=True
    )

    pipeline = [

        ("🔥", "CSS STEAM", f"{steam_temperature} °C"),

        (
            "🌡️",
            "HEATED RESERVOIR",
            f"{thermal['heated_temperature_c']:.1f} °C"
        ),

        (
            "🌡️",
            "PRODUCTION TEMP.",
            f"{production_temperature:.1f} °C"
        ),

        (
            "💧",
            "VISCOSITY",
            f"{viscosity:,.0f} cP"
        ),

        (
            "⚡",
            "VFD / SPM",
            f"{vfd_frequency:.0f} Hz / {spm:.1f} SPM"
        ),

        (
            "⚙️",
            "SRP FILLAGE",
            f"{srp['predicted_pump_fillage']:.1f}%"
        ),

        (
            "🛢️",
            "PRODUCTION",
            f"{production:.1f} BPD"
        )
    ]

    cols = st.columns(7)

    for col, item in zip(cols, pipeline):

        with col:

            st.markdown(
                (
                    '<div class="pipeline-box">'
                    f'<div class="pipeline-icon">{item[0]}</div>'
                    f'<div class="pipeline-name">{item[1]}</div>'
                    f'<div class="pipeline-value">{item[2]}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


    # ========================================================
    # SRP STATE + RELIABILITY
    # ========================================================

    st.divider()

    left, right = st.columns(2)


    with left:

        st.markdown(
            '<div class="section-title">'
            '⚙️ SRP OPERATING STATE'
            '</div>',
            unsafe_allow_html=True
        )

        srp_table = pd.DataFrame(
            {
                "Parameter": [
                    "Reference Well",
                    "VFD Frequency",
                    "Pump Speed",
                    "Pump Fillage",
                    "Rod Load Range",
                    "SPM Bin",
                    "Calibration"
                ],

                "Value": [
                    well_id,
                    f"{vfd_frequency:.1f} Hz",
                    f"{spm:.1f} SPM",
                    f"{srp['predicted_pump_fillage']:.2f}%",
                    f"{srp['state_load_range']:.1f} kg",
                    srp["spm_bin"],
                    srp["calibration_status"]
                ]
            }
        )

        st.dataframe(
            srp_table,
            use_container_width=True,
            hide_index=True
        )


    with right:

        st.markdown(
            '<div class="section-title">'
            '🛡️ RELIABILITY INDICATOR'
            '</div>',
            unsafe_allow_html=True
        )

        st.metric(
            "Prototype Risk Score",
            f"{risk:.2f}/100"
        )

        st.progress(
            min(max(risk / 100.0, 0.0), 1.0)
        )

        if risk_class == "LOW":

            st.success(
                "LOW prototype risk region"
            )

        elif risk_class == "MEDIUM":

            st.warning(
                "MEDIUM prototype risk region"
            )

        else:

            st.error(
                "HIGH prototype risk region"
            )


    # ========================================================
    # MODEL VALIDATION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🤖 SRP MODEL VALIDATION'
        '</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "MAE",
            f"{srp['model_mae_percent']:.2f} pp"
        )

        st.caption(
            "Pump-fillage prediction error"
        )


    with m2:

        st.metric(
            "R²",
            f"{srp['model_r2']:.3f}"
        )

        st.caption(
            "Chronological held-out test"
        )


    with m3:

        st.metric(
            "Validation",
            "Chronological"
        )

        st.caption(
            "Train → future test period"
        )


    # ========================================================
    # DATA NOTE
    # ========================================================

    st.divider()

    st.info(
        "Prototype note: the SRP model uses an external SRP "
        "dataset for behavioral modeling. It is not Baghewala "
        "well-level data. The architecture is designed for "
        "future calibration using Oil India's historical "
        "Baghewala historian."
    )


# ============================================================
# TAB 2 — 3D DIGITAL TWIN
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        '🧊 LIVE 3D WELL-TO-SURFACE DIGITAL TWIN'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Interactive visualization driven by the same CSS, "
        "viscosity, SRP and production calculations."
    )


    # ========================================================
    # CREATE 3D MODEL
    # ========================================================

    fig_3d = create_digital_twin_3d(

        reservoir_temperature=
            thermal["initial_temperature_c"],

        heated_temperature=
            thermal["heated_temperature_c"],

        production_temperature=
            production_temperature,

        steam_temperature=
            steam_temperature
    )


    # ========================================================
    # DISPLAY 3D MODEL
    # ========================================================

    st.plotly_chart(
        fig_3d,
        use_container_width=True,
        config={
            "displaylogo": False,
            "scrollZoom": True
        }
    )


    # ========================================================
    # LIVE STATE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🎛️ LIVE SIMULATION STATE'
        '</div>',
        unsafe_allow_html=True
    )

    d1, d2, d3 = st.columns(3)
    d4, d5, d6 = st.columns(3)


    with d1:

        st.metric(
            "🔥 Steam Temperature",
            f"{steam_temperature} °C"
        )


    with d2:

        st.metric(
            "♨ Heated Reservoir",
            f"{thermal['heated_temperature_c']:.1f} °C"
        )


    with d3:

        st.metric(
            "🌡 Production Temperature",
            f"{production_temperature:.1f} °C"
        )


    with d4:

        st.metric(
            "💧 Viscosity",
            f"{viscosity:,.0f} cP"
        )


    with d5:

        st.metric(
            "⚡ VFD / SRP",
            f"{vfd_frequency:.0f} Hz / {spm:.1f} SPM"
        )


    with d6:

        st.metric(
            "🛢️ Production",
            f"{production:.2f} BPD"
        )


    st.info(
        "The 3D scene is a visualization layer over the "
        "digital-twin calculations. The thermal field is a "
        "physics-informed visualization, not measured 3D "
        "reservoir temperature data."
    )

 # ============================================================
# TAB 3 — OPTIMIZATION
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">'
        '🚀 INTEGRATED OPTIMIZATION ENGINE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
### THREE-OBJECTIVE OPTIMIZATION

🛢️ **Production ↑** &nbsp;&nbsp;&nbsp;
⚡ **Steam Energy ↓** &nbsp;&nbsp;&nbsp;
🛡️ **Reliability Risk ↓**
"""
    )

    st.divider()

    st.info(
        "The optimizer evaluates the prototype operating space "
        "and returns non-dominated scenarios. These scenarios "
        "are not field-validated operating recommendations."
    )


    # ========================================================
    # RUN OPTIMIZATION
    # ========================================================

    if st.button(
        "🚀 RUN 1,350-SCENARIO OPTIMIZATION",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Running CSS → viscosity → SRP → production → "
            "energy → reliability optimization..."
        ):

            candidate_spm_values = [
                3.5,
                4.0,
                4.5,
                5.0,
                5.5,
                6.0,
                6.5,
                7.0,
                7.5
            ]

            # ------------------------------------------------
            # EXISTING OPTIMIZATION LOGIC
            # ------------------------------------------------

            results = run_reliability_optimization(
                well_id=well_id,
                candidate_spm_values=candidate_spm_values
            )

            pareto_results = (
                find_three_objective_pareto_front(
                    results
                )
            )


        # ----------------------------------------------------
        # SAVE RESULTS
        # ----------------------------------------------------

        st.session_state["results"] = results

        st.session_state["pareto"] = (
            pareto_results
        )

        st.session_state["optimization_well"] = (
            well_id
        )

        st.success(
            f"Optimization complete • "
            f"{len(results):,} scenarios evaluated • "
            f"{len(pareto_results):,} Pareto scenarios identified"
        )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if "results" in st.session_state:

        results = st.session_state["results"]

        pareto_results = (
            st.session_state["pareto"]
        )

        optimization_well = (
            st.session_state.get(
                "optimization_well",
                well_id
            )
        )


        # ====================================================
        # OPTIMIZATION REFERENCE
        # ====================================================

        st.caption(
            f"Optimization reference well: "
            f"**{optimization_well}**"
        )


        # ====================================================
        # SUMMARY METRICS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '📊 OPTIMIZATION SUMMARY'
            '</div>',
            unsafe_allow_html=True
        )


        max_production = max(
            x["predicted_production_bpd"]
            for x in results
        )


        min_energy = min(
            x["steam_energy_kwh"]
            for x in results
        )


        min_risk = min(
            x["reliability_risk"]
            for x in results
        )


        a, b, c, d = st.columns(4)


        with a:

            st.metric(
                "Scenarios",
                f"{len(results):,}"
            )


        with b:

            st.metric(
                "Pareto Set",
                f"{len(pareto_results):,}"
            )


        with c:

            st.metric(
                "Max Production",
                f"{max_production:.2f} BPD"
            )


        with d:

            st.metric(
                "Minimum Risk",
                f"{min_risk:.2f}/100"
            )


        # ====================================================
        # PARETO TABLE
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🎯 PARETO OPERATING SET'
            '</div>',
            unsafe_allow_html=True
        )


        pareto_table = pd.DataFrame(
            [

                {
                    "Steam °C":
                        x["steam_temperature_c"],

                    "Steam m³":
                        x["steam_volume_m3"],

                    "Injection":
                        x["injection_days"],

                    "Soak":
                        x["soak_days"],

                    "SPM":
                        x["spm"],

                    "Fillage %":
                        x["pump_fillage_percent"],

                    "Production BPD":
                        x["predicted_production_bpd"],

                    "Energy kWh":
                        x["steam_energy_kwh"],

                    "BPD/kWh":
                        x["production_per_energy"],

                    "Risk":
                        x["reliability_risk"]
                }

                for x in pareto_results

            ]
        )


        pareto_table = (
            pareto_table
            .sort_values("Production BPD")
            .reset_index(drop=True)
        )


        st.dataframe(
            pareto_table,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # PARETO SCATTER
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '📈 INTERACTIVE PARETO FRONT'
            '</div>',
            unsafe_allow_html=True
        )


        st.caption(
            "Hover over a point to inspect the complete "
            "operating scenario."
        )


        fig = px.scatter(

            pareto_table,

            x="Energy kWh",

            y="Production BPD",

            color="Risk",

            size="Production BPD",

            hover_data=[

                "Steam °C",
                "Steam m³",
                "Injection",
                "Soak",
                "SPM",
                "Fillage %",
                "BPD/kWh",
                "Risk"

            ],

            labels={

                "Energy kWh":
                    "Steam Energy (kWh)",

                "Production BPD":
                    "Predicted Production (BPD)",

                "Risk":
                    "Reliability Risk"

            },

            title=(
                "Production vs Steam Energy vs "
                "Reliability Risk"
            )
        )


        fig.update_layout(
            height=600,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ====================================================
        # SCENARIO EXPLORER
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🎯 SCENARIO EXPLORER'
            '</div>',
            unsafe_allow_html=True
        )


        st.caption(
            "Select a Pareto scenario to inspect its "
            "complete CSS + SRP operating configuration."
        )


        # ----------------------------------------------------
        # SCENARIO SELECTOR
        # ----------------------------------------------------

        scenario_options = list(
            range(len(pareto_table))
        )


        selected_scenario = st.selectbox(

            "Select Pareto Scenario",

            scenario_options,

            format_func=lambda x: (

                f"Scenario {x + 1} • "

                f"{pareto_table.iloc[x]['Production BPD']:.2f} BPD • "

                f"Risk {pareto_table.iloc[x]['Risk']:.1f}"

            )
        )


        selected = pareto_table.iloc[
            selected_scenario
        ]


        # ====================================================
        # SELECTED SCENARIO KPI CARDS
        # ====================================================

        s1, s2, s3, s4 = st.columns(4)


        with s1:

            st.metric(
                "🔥 Steam",
                f"{selected['Steam °C']:.0f} °C"
            )

            st.caption(
                f"{selected['Steam m³']:.0f} m³"
            )


        with s2:

            st.metric(
                "⚙️ SRP Speed",
                f"{selected['SPM']:.1f} SPM"
            )

            st.caption(
                f"Fillage: "
                f"{selected['Fillage %']:.1f}%"
            )


        with s3:

            st.metric(
                "🛢️ Production",
                f"{selected['Production BPD']:.2f} BPD"
            )

            st.caption(
                f"Efficiency: "
                f"{selected['BPD/kWh']:.6f}"
            )


        with s4:

            st.metric(
                "🛡️ Reliability Risk",
                f"{selected['Risk']:.2f}/100"
            )


            if selected["Risk"] < 30:

                st.success("LOW")

            elif selected["Risk"] < 60:

                st.warning("MEDIUM")

            else:

                st.error("HIGH")


        # ====================================================
        # SCENARIO PLAN
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '📋 SELECTED SCENARIO CONFIGURATION'
            '</div>',
            unsafe_allow_html=True
        )


        scenario_plan = pd.DataFrame(

            {

                "Parameter": [

                    "Reference Well",
                    "Steam Temperature",
                    "Steam Volume",
                    "Injection Duration",
                    "Soak Duration",
                    "SRP Speed",
                    "Pump Fillage",
                    "Predicted Production",
                    "Steam Energy",
                    "Production / Energy",
                    "Reliability Risk"

                ],

                "Selected Scenario": [

                    optimization_well,

                    f"{selected['Steam °C']:.0f} °C",

                    f"{selected['Steam m³']:.0f} m³",

                    f"{selected['Injection']:.0f} days",

                    f"{selected['Soak']:.0f} days",

                    f"{selected['SPM']:.1f} SPM",

                    f"{selected['Fillage %']:.2f}%",

                    f"{selected['Production BPD']:.2f} BPD",

                    f"{selected['Energy kWh']:,.0f} kWh",

                    f"{selected['BPD/kWh']:.6f}",

                    f"{selected['Risk']:.2f}/100"

                ]

            }

        )


        st.dataframe(

            scenario_plan,

            use_container_width=True,

            hide_index=True
        )

# ====================================================
        # SCENARIO ANALYSIS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🔎 SCENARIO ANALYSIS'
            '</div>',
            unsafe_allow_html=True
        )


        i1, i2, i3 = st.columns(3)


        # ====================================================
        # CSS ANALYSIS
        # ====================================================

        with i1:

            st.markdown("### 🔥 CSS")

            st.write(
                f"Steam temperature: "
                f"**{selected['Steam °C']:.0f} °C**"
            )

            st.write(
                f"Steam volume: "
                f"**{selected['Steam m³']:.0f} m³**"
            )

            st.write(
                f"Injection duration: "
                f"**{selected['Injection']:.0f} days**"
            )

            st.write(
                f"Soak duration: "
                f"**{selected['Soak']:.0f} days**"
            )


        # ====================================================
        # SRP ANALYSIS
        # ====================================================

        with i2:

            st.markdown("### ⚙️ SRP")

            st.write(
                f"Pump speed: "
                f"**{selected['SPM']:.1f} SPM**"
            )

            st.write(
                f"Predicted fillage: "
                f"**{selected['Fillage %']:.2f}%**"
            )

            st.write(
                "The SRP state is evaluated through "
                "the prototype fillage and reliability models."
            )


        # ====================================================
        # PERFORMANCE ANALYSIS
        # ====================================================

        with i3:

            st.markdown("### 📊 PERFORMANCE")

            st.write(
                f"Production: "
                f"**{selected['Production BPD']:.2f} BPD**"
            )

            st.write(
                f"Steam energy: "
                f"**{selected['Energy kWh']:,.0f} kWh**"
            )

            st.write(
                f"Risk indicator: "
                f"**{selected['Risk']:.2f}/100**"
            )


        # ====================================================
        # SELECTED SCENARIO 3D PREVIEW
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🧊 SELECTED SCENARIO — 3D PREVIEW'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Run the selected Pareto scenario through the "
            "same digital-twin visualization layer."
        )


        # ====================================================
        # 3D PREVIEW BUTTON
        # ====================================================

        if st.button(
            "🧊 VISUALIZE SELECTED SCENARIO",
            use_container_width=True
        ):

            # ------------------------------------------------
            # THERMAL MODEL
            # ------------------------------------------------

            selected_thermal = simulate_css_cycle(

                initial_temperature_c=47.0,

                steam_temperature_c=
                    selected["Steam °C"],

                steam_volume_m3=
                    selected["Steam m³"],

                injection_days=
                    selected["Injection"],

                soak_days=
                    selected["Soak"]
            )


            # ------------------------------------------------
            # PRODUCTION TEMPERATURE
            # ------------------------------------------------

            selected_production_temperature = (
                selected_thermal[
                    "production_start_temperature_c"
                ]
            )


            # ------------------------------------------------
            # VISCOSITY
            # ------------------------------------------------

            selected_viscosity = calculate_viscosity(
                selected_production_temperature
            )


            # ------------------------------------------------
            # SRP PREDICTION
            # ------------------------------------------------

            selected_srp = predict_candidate(

                well_id=optimization_well,

                viscosity_cp=selected_viscosity,

                spm=selected["SPM"]
            )


            # ------------------------------------------------
            # PRODUCTION
            # ------------------------------------------------

            selected_production = calculate_production_rate(

                viscosity_cp=selected_viscosity,

                pump_fillage_percent=
                    selected_srp[
                        "predicted_pump_fillage"
                    ],

                pump_efficiency=1.0
            )


            # ------------------------------------------------
            # RELIABILITY
            # ------------------------------------------------

            selected_risk = calculate_reliability_score(

                viscosity_cp=selected_viscosity,

                spm=selected["SPM"],

                rod_load_range=
                    selected_srp[
                        "state_load_range"
                    ],

                pump_fillage=
                    selected_srp[
                        "predicted_pump_fillage"
                    ]
            )


            # ------------------------------------------------
            # CREATE 3D DIGITAL TWIN
            # ------------------------------------------------

            selected_fig = create_digital_twin_3d(

                reservoir_temperature=
                    selected_thermal[
                        "initial_temperature_c"
                    ],

                heated_temperature=
                    selected_thermal[
                        "heated_temperature_c"
                    ],

                production_temperature=
                    selected_production_temperature,

                steam_temperature=
                    selected["Steam °C"]
            )


            # ------------------------------------------------
            # DISPLAY 3D MODEL
            # ------------------------------------------------

            st.plotly_chart(

                selected_fig,

                use_container_width=True,

                config={
                    "displaylogo": False,
                    "scrollZoom": True
                }
            )


            # =================================================
            # 3D SCENARIO KPIs
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'LIVE SCENARIO STATE'
                '</div>',
                unsafe_allow_html=True
            )


            v1, v2, v3, v4 = st.columns(4)


            with v1:

                st.metric(
                    "Production Temp.",
                    f"{selected_production_temperature:.1f} °C"
                )


            with v2:

                st.metric(
                    "Viscosity",
                    f"{selected_viscosity:,.0f} cP"
                )


            with v3:

                st.metric(
                    "Pump Fillage",
                    f"{selected_srp['predicted_pump_fillage']:.1f}%"
                )


            with v4:

                st.metric(
                    "Risk",
                    f"{selected_risk:.1f}/100"
                )


        # ====================================================
        # DIGITAL TWIN DECISION LAYER
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🧠 DIGITAL TWIN DECISION LAYER'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            """
The integrated digital twin evaluates the interaction between:

**CSS → Reservoir Heating → Viscosity Reduction → SRP State
→ Pump Fillage → Production → Steam Energy → Reliability**

This allows CSS and SRP operating conditions to be evaluated
together rather than as independent optimization problems.
"""
        )


        # ====================================================
        # ENGINEERING NOTE
        # ====================================================

        st.info(
            "Engineering note: the displayed scenarios are "
            "prototype, physics-informed simulations. They "
            "should be calibrated against Oil India's actual "
            "Baghewala historian before being used for field "
            "operational decisions."
        )


        # ====================================================
        # MODEL LIMITATIONS
        # ====================================================

        with st.expander(
            "⚠️ Prototype assumptions & limitations"
        ):

            st.markdown(
                """
**Data**

- Well-level Baghewala historian data is not publicly available.
- The initial prototype therefore uses physics-constrained
  synthetic data and an external SRP behavioral dataset.
- The external SRP dataset is **not Baghewala data**.

**Physics**

- Reservoir temperature is represented through a simplified
  thermal-response model.
- Viscosity is estimated using a temperature-dependent
  Arrhenius-type relationship.
- Production is represented using a prototype mobility/fillage
  model.
- Steam energy uses a simplified enthalpy assumption.

**Reliability**

- Reliability is represented by a composite operating-risk
  indicator.
- It is **not a statistically validated failure probability**.

**3D Visualization**

- The reservoir thermal field is a visualization mapping.
- It is **not measured 3D reservoir temperature data**.
- Equipment geometry is representative rather than a field CAD
  model.

**Deployment**

- Final operating parameters require calibration and validation
  using Oil India's historical Baghewala well-level data.
"""
            )


        # ====================================================
        # DATA PROVENANCE
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '📚 DATA & MODEL PROVENANCE'
            '</div>',
            unsafe_allow_html=True
        )


        provenance = pd.DataFrame(
            {
                "Component": [
                    "CSS Thermal Model",
                    "Viscosity Model",
                    "SRP Behavioral Model",
                    "Production Model",
                    "Steam Energy Model",
                    "Reliability Model",
                    "3D Digital Twin"
                ],

                "Current Prototype Basis": [

                    "Physics-informed assumptions",

                    "Temperature-dependent "
                    "viscosity relationship",

                    "External SRP sensor dataset",

                    "Mobility + pump fillage model",

                    "Simplified steam-energy model",

                    "Composite operating-risk indicator",

                    "Visualization driven by "
                    "digital-twin state variables"
                ]
            }
        )


        st.dataframe(
            provenance,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # FINAL STATUS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '✅ DIGITAL TWIN STATUS'
            '</div>',
            unsafe_allow_html=True
        )


        status1, status2, status3, status4 = st.columns(4)


        with status1:

            st.success(
                "CSS Model Active"
            )


        with status2:

            st.success(
                "Viscosity Model Active"
            )


        with status3:

            st.success(
                "SRP Model Active"
            )


        with status4:

            st.success(
                "Optimization Active"
            )


# ============================================================
# TAB 4 — FAILURE DETECTION
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">'
        '⚠️ SRP FAILURE & CONDITION DETECTION'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Prototype detection layer for rod-floating and impact-loading conditions."
    )

    st.divider()

    failure_state = evaluate_srp_condition(
        viscosity_cp=viscosity,
        spm=spm,
        pump_fillage=srp["predicted_pump_fillage"],
        rod_load_range=srp["state_load_range"]
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        st.metric(
            "🪢 ROD FLOATING",
            f"{failure_state['rod_floating_score']:.1f}/100"
        )
        if failure_state["rod_floating_status"] == "NORMAL":
            st.success(failure_state["rod_floating_status"])
        elif failure_state["rod_floating_status"] == "WARNING":
            st.warning(failure_state["rod_floating_status"])
        else:
            st.error(failure_state["rod_floating_status"])

    with f2:
        st.metric(
            "⚡ IMPACT LOADING",
            f"{failure_state['impact_loading_score']:.1f}/100"
        )
        if failure_state["impact_loading_status"] == "NORMAL":
            st.success(failure_state["impact_loading_status"])
        elif failure_state["impact_loading_status"] == "WARNING":
            st.warning(failure_state["impact_loading_status"])
        else:
            st.error(failure_state["impact_loading_status"])

    with f3:
        st.metric(
            "🛡️ OVERALL SRP CONDITION",
            f"{failure_state['overall_srp_condition_score']:.1f}/100"
        )
        if failure_state["overall_srp_condition"] == "NORMAL":
            st.success(failure_state["overall_srp_condition"])
        elif failure_state["overall_srp_condition"] == "WARNING":
            st.warning(failure_state["overall_srp_condition"])
        else:
            st.error(failure_state["overall_srp_condition"])

    st.divider()

    st.markdown("### CURRENT SRP CONDITIONS")

    failure_inputs = pd.DataFrame({
        "Parameter": [
            "Reference Well",
            "VFD Frequency",
            "Pump Speed",
            "Pump Fillage",
            "Rod Load Range",
            "Oil Viscosity"
        ],
        "Current Value": [
            well_id,
            f"{vfd_frequency:.1f} Hz",
            f"{spm:.1f} SPM",
            f"{srp['predicted_pump_fillage']:.1f}%",
            f"{srp['state_load_range']:.1f} kg",
            f"{viscosity:,.0f} cP"
        ]
    })

    st.dataframe(
        failure_inputs,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "The failure detector is a physics-informed prototype indicator. "
        "It is not a statistically validated failure probability and should "
        "be calibrated with Baghewala field failure/intervention history."
    )

    st.divider()

    st.markdown("### DETECTION LOGIC")

    st.write(
        "**Rod floating:** combines viscosity, pumping speed, pump fillage "
        "and rod-load behavior to identify potentially unfavorable operating conditions."
    )

    st.write(
        "**Impact loading:** combines rod-load variation, pumping speed "
        "and high pump fillage to identify potentially severe loading conditions."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
<div class="footer">

<b>BAGHEWALA DIGITAL TWIN</b><br>

AI + Physics-Informed Optimization for Heavy-Oil Operations<br>

CSS • Thermal Response • Viscosity • SRP • Production • Energy • Reliability

</div>
""",
    unsafe_allow_html=True
)           