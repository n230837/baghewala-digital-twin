import numpy as np
import plotly.graph_objects as go


# ============================================================
# BAGHEWALA DYNAMIC 3D DIGITAL TWIN
# CSS + SRP + THERMAL FIELD + FLOW ANIMATION
# ============================================================


# ============================================================
# COLORS
# ============================================================

TEMP_COLORS = [
    [0.00, "#123BFF"],
    [0.20, "#00AEEF"],
    [0.45, "#00D5C8"],
    [0.60, "#FFE600"],
    [0.80, "#FF8A00"],
    [1.00, "#FF2020"]
]

METAL = "#B9C0C8"
METAL_DARK = "#59616A"

ROD_COLOR = "#FFD447"
PUMP_COLOR = "#FF7417"
PLUNGER_COLOR = "#FFE36A"

STEAM_COLOR = "#8FEAFF"
OIL_COLOR = "#D18A20"

WHITE = "#F2F4F7"

GRID_COLOR = "rgba(220,230,240,0.16)"
BOX_COLOR = "rgba(220,230,240,0.50)"


# ============================================================
# THERMAL FIELD
# ============================================================

def generate_temperature_field(
    reservoir_temperature=47.0,
    heated_temperature=100.0,
    grid_size=22
):

    x = np.linspace(-7, 7, grid_size)
    y = np.linspace(-7, 7, grid_size)
    z = np.linspace(0, 8, grid_size)

    X, Y, Z = np.meshgrid(
        x,
        y,
        z,
        indexing="ij"
    )

    radius = np.sqrt(
        X ** 2 + Y ** 2
    )

    radial_decay = np.exp(
        -(radius / 4.2) ** 2
    )

    vertical_factor = (
        0.72
        +
        0.28
        * np.exp(
            -((Z - 4.0) / 4.5) ** 2
        )
    )

    thermal_fraction = (
        radial_decay
        * vertical_factor
    )

    temperature = (
        reservoir_temperature
        +
        (
            heated_temperature
            - reservoir_temperature
        )
        * thermal_fraction
    )

    return X, Y, Z, temperature


# ============================================================
# CYLINDER HELPER
# ============================================================

def cylinder_trace(
    x,
    y,
    z_start,
    z_end,
    radius,
    color,
    name,
    n=20
):

    theta = np.linspace(
        0,
        2 * np.pi,
        n
    )

    xs = []
    ys = []
    zs = []

    for z in [z_start, z_end]:

        xs.extend(
            x + radius * np.cos(theta)
        )

        ys.extend(
            y + radius * np.sin(theta)
        )

        zs.extend(
            [z] * n
        )

    i = []
    j = []
    k = []

    for p in range(n):

        q = (p + 1) % n

        i.extend([
            p,
            p + n
        ])

        j.extend([
            q,
            q + n
        ])

        k.extend([
            p + n,
            q
        ])

    return go.Mesh3d(
        x=xs,
        y=ys,
        z=zs,
        i=i,
        j=j,
        k=k,
        color=color,
        opacity=0.90,
        name=name,
        hovertemplate=(
            f"<b>{name}</b>"
            "<extra></extra>"
        )
    )


# ============================================================
# RESERVOIR BOX
# ============================================================

def add_reservoir_box(fig):

    x0, x1 = -7, 7
    y0, y1 = -7, 7
    z0, z1 = 0, 8

    corners = [
        (x0, y0, z0),
        (x1, y0, z0),
        (x1, y1, z0),
        (x0, y1, z0),

        (x0, y0, z1),
        (x1, y0, z1),
        (x1, y1, z1),
        (x0, y1, z1)
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),

        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),

        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    ]

    for a, b in edges:

        fig.add_trace(
            go.Scatter3d(

                x=[
                    corners[a][0],
                    corners[b][0]
                ],

                y=[
                    corners[a][1],
                    corners[b][1]
                ],

                z=[
                    corners[a][2],
                    corners[b][2]
                ],

                mode="lines",

                line=dict(
                    color=BOX_COLOR,
                    width=2
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )


# ============================================================
# RESERVOIR GRID
# ============================================================

def add_grid(fig):

    values = np.arange(
        -7,
        7.1,
        1
    )

    for x in values:

        fig.add_trace(
            go.Scatter3d(

                x=[x, x],
                y=[-7, 7],
                z=[0, 0],

                mode="lines",

                line=dict(
                    color=GRID_COLOR,
                    width=1
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )

    for y in values:

        fig.add_trace(
            go.Scatter3d(

                x=[-7, 7],
                y=[y, y],
                z=[0, 0],

                mode="lines",

                line=dict(
                    color=GRID_COLOR,
                    width=1
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )


# ============================================================
# WELL CASING
# ============================================================

def add_well(fig):

    fig.add_trace(
        cylinder_trace(
            0,
            0,
            0,
            12,
            0.18,
            METAL_DARK,
            "Well Casing"
        )
    )

    fig.add_trace(
        cylinder_trace(
            0,
            0,
            0,
            12,
            0.09,
            METAL,
            "Production Tubing"
        )
    )


# ============================================================
# SURFACE SRP
# ============================================================

def add_srp_unit(fig):

    # Base

    fig.add_trace(
        go.Scatter3d(

            x=[
                -2.3,
                2.3,
                2.3,
                -2.3,
                -2.3
            ],

            y=[
                -1.4,
                -1.4,
                1.4,
                1.4,
                -1.4
            ],

            z=[
                0,
                0,
                0,
                0,
                0
            ],

            mode="lines",

            line=dict(
                color=METAL_DARK,
                width=10
            ),

            hoverinfo="skip",
            showlegend=False
        )
    )

    # Supports

    for x in [-1.3, 1.3]:

        fig.add_trace(
            go.Scatter3d(

                x=[x, x],
                y=[0, 0],
                z=[0, 2.8],

                mode="lines",

                line=dict(
                    color=METAL,
                    width=13
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )

    # Walking beam

    fig.add_trace(
        go.Scatter3d(

            x=[-2.1, 2.1],
            y=[0, 0],
            z=[2.9, 2.9],

            mode="lines",

            line=dict(
                color=METAL,
                width=18
            ),

            name="Walking Beam",

            hovertemplate=(
                "<b>SRP Walking Beam</b>"
                "<extra></extra>"
            )
        )
    )

    # Pivot

    fig.add_trace(
        go.Scatter3d(

            x=[0],
            y=[0],
            z=[2.9],

            mode="markers",

            marker=dict(
                size=14,
                color=METAL
            ),

            hoverinfo="skip",
            showlegend=False
        )
    )


# ============================================================
# STEAM GENERATOR
# ============================================================

def add_steam_generator(fig):

    # Generator body

    fig.add_trace(
        go.Mesh3d(

            x=[
                -6.8,
                -5.0,
                -5.0,
                -6.8,
                -6.8,
                -5.0,
                -5.0,
                -6.8
            ],

            y=[
                -1.1,
                -1.1,
                1.1,
                1.1,
                -1.1,
                -1.1,
                1.1,
                1.1
            ],

            z=[
                2.4,
                2.4,
                2.4,
                2.4,
                4.5,
                4.5,
                4.5,
                4.5
            ],

            i=[
                0,
                0,
                0,
                4,
                4,
                4
            ],

            j=[
                1,
                2,
                4,
                5,
                6,
                0
            ],

            k=[
                2,
                3,
                5,
                6,
                7,
                4
            ],

            color=METAL_DARK,
            opacity=0.95,

            name="Steam Generator",

            hovertemplate=(
                "<b>CSS Steam Generator</b><br>"
                "Generates high-temperature steam"
                "<extra></extra>"
            )
        )
    )

    # Generator outlet

    fig.add_trace(
        go.Scatter3d(

            x=[
                -5.0,
                -4.0,
                -3.0,
                -2.0,
                -1.0,
                0
            ],

            y=[
                0,
                0,
                0,
                0,
                0,
                0
            ],

            z=[
                3.45,
                3.45,
                3.45,
                3.45,
                3.45,
                3.45
            ],

            mode="lines",

            line=dict(
                color=STEAM_COLOR,
                width=8
            ),

            name="Steam Injection Line",

            hovertemplate=(
                "<b>Steam Injection Line</b>"
                "<extra></extra>"
            )
        )
    )


# ============================================================
# WELLHEAD
# ============================================================

def add_wellhead(fig):

    fig.add_trace(
        go.Scatter3d(

            x=[
                -0.55,
                0.55
            ],

            y=[
                0,
                0
            ],

            z=[
                3.8,
                3.8
            ],

            mode="lines",

            line=dict(
                color=METAL,
                width=13
            ),

            name="Wellhead",

            hovertemplate=(
                "<b>Wellhead</b>"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter3d(

            x=[0],
            y=[0],
            z=[3.8],

            mode="markers",

            marker=dict(
                size=10,
                color=PUMP_COLOR
            ),

            hovertemplate=(
                "<b>Wellhead / Injection Point</b>"
                "<extra></extra>"
            ),

            showlegend=False
        )
    )


# ============================================================
# DOWNHOLE PUMP
# ============================================================

def add_downhole_pump(fig):

    pump_depth = 10.5

    fig.add_trace(
        cylinder_trace(
            0,
            0,
            pump_depth - 1.0,
            pump_depth + 1.0,
            0.28,
            PUMP_COLOR,
            "Downhole Pump"
        )
    )

    # Pump plunger

    fig.add_trace(
        cylinder_trace(
            0,
            0,
            pump_depth - 0.4,
            pump_depth + 0.4,
            0.12,
            PLUNGER_COLOR,
            "Pump Plunger"
        )
    )

    # Pump intake

    fig.add_trace(
        go.Scatter3d(

            x=[
                -1.1,
                0,
                1.1
            ],

            y=[
                0,
                0,
                0
            ],

            z=[
                pump_depth + 1,
                pump_depth + 1,
                pump_depth + 1
            ],

            mode="lines",

            line=dict(
                color=PUMP_COLOR,
                width=9
            ),

            name="Pump Intake",

            hovertemplate=(
                "<b>Pump Intake</b><br>"
                "Heavy oil enters pump"
                "<extra></extra>"
            )
        )
    )


# ============================================================
# SUCKER ROD
# ============================================================

def add_rod(fig):

    fig.add_trace(
        go.Scatter3d(

            x=[
                0,
                0
            ],

            y=[
                0,
                0
            ],

            z=[
                3.5,
                10.8
            ],

            mode="lines",

            line=dict(
                color=ROD_COLOR,
                width=8
            ),

            name="Sucker Rod",

            hovertemplate=(
                "<b>Sucker Rod</b><br>"
                "Reciprocating artificial lift"
                "<extra></extra>"
            )
        )
    )


# ============================================================
# PARTICLES
# ============================================================

def initial_particles():

    # Steam particles

    steam_x = np.array([
        -5.0,
        -4.2,
        -3.4,
        -2.6,
        -1.8,
        -1.0
    ])

    steam_y = np.zeros(6)

    steam_z = np.array([
        3.45,
        3.45,
        3.45,
        3.45,
        3.45,
        3.45
    ])

    # Oil particles

    oil_x = np.array([
        -5.0,
        -3.8,
        -2.6,
        -1.5,
        -0.7,
        0
    ])

    oil_y = np.array([
        1.8,
        1.4,
        1.0,
        0.6,
        0.3,
        0
    ])

    oil_z = np.ones(6) * 11.2

    return (
        steam_x,
        steam_y,
        steam_z,
        oil_x,
        oil_y,
        oil_z
    )

    # ============================================================
# ANIMATION FRAMES
# ============================================================

def create_particle_frames():

    frames = []

    (
        steam_x,
        steam_y,
        steam_z,
        oil_x,
        oil_y,
        oil_z
    ) = initial_particles()

    for frame_number in range(40):

        phase = (
            2
            * np.pi
            * frame_number
            / 40
        )

        # ====================================================
        # SRP WALKING BEAM
        # ====================================================

        beam_angle = (
            0.10
            * np.sin(phase)
        )

        left_x = (
            -2.1
            * np.cos(beam_angle)
        )

        right_x = (
            2.1
            * np.cos(beam_angle)
        )

        left_z = (
            2.9
            +
            2.1
            * np.sin(beam_angle)
        )

        right_z = (
            2.9
            -
            2.1
            * np.sin(beam_angle)
        )

        # ====================================================
        # ROD
        # ====================================================

        displacement = (
            0.45
            * np.sin(phase)
        )

        rod_bottom = (
            3.5
            + displacement
        )

        rod_top = (
            10.8
            + displacement
        )

        # ====================================================
        # PLUNGER
        # ====================================================

        plunger_bottom = (
            10.1
            + displacement
        )

        plunger_top = (
            10.9
            + displacement
        )

        # ====================================================
        # STEAM PARTICLES
        # ====================================================

        sx = (
            steam_x
            +
            0.12
            * np.sin(
                phase
                +
                np.arange(6)
            )
        )

        sy = (
            steam_y
            +
            0.25
            * np.sin(
                phase
                +
                np.arange(6)
            )
        )

        sz = (
            steam_z
            +
            0.18
            * np.sin(
                phase
                +
                np.arange(6)
            )
        )

        # ====================================================
        # OIL PARTICLES
        # ====================================================

        ox = (
            oil_x
            +
            0.20
            * np.sin(
                phase
                +
                np.arange(6)
            )
        )

        oy = (
            oil_y
            +
            0.15
            * np.cos(
                phase
                +
                np.arange(6)
            )
        )

        oz = (
            oil_z
            +
            0.12
            * np.sin(
                phase
                +
                np.arange(6)
            )
        )

        # ====================================================
        # IMPORTANT
        #
        # The trace numbers below are calculated from the
        # exact order in create_digital_twin_3d().
        #
        # 0       = Thermal field
        # 1-12    = Reservoir box
        # 13-42   = Grid
        # 43-44   = Well casing/tubing
        # 45-46   = Wellhead
        # 47      = SRP base
        # 48-49   = SRP supports
        # 50      = Walking beam
        # 51      = Pivot
        # 52      = Sucker rod
        # 53      = Pump barrel
        # 54      = Pump plunger
        # 55      = Pump intake
        # 56      = Steam generator
        # 57      = Steam line
        # 58      = Steam particles
        # 59      = Oil particles
        #
        # Thermal field is NEVER animated/replaced.
        # ====================================================

        frames.append(

            go.Frame(

                name=str(frame_number),

                traces=[
                    50,
                    52,
                    54,
                    58,
                    59
                ],

                data=[

                    # Walking beam

                    go.Scatter3d(

                        x=[
                            left_x,
                            right_x
                        ],

                        y=[
                            0,
                            0
                        ],

                        z=[
                            left_z,
                            right_z
                        ]
                    ),

                    # Sucker rod

                    go.Scatter3d(

                        x=[
                            0,
                            0
                        ],

                        y=[
                            0,
                            0
                        ],

                        z=[
                            rod_bottom,
                            rod_top
                        ]
                    ),

                    # Pump plunger

                    go.Scatter3d(

                        x=[
                            0,
                            0
                        ],

                        y=[
                            0,
                            0
                        ],

                        z=[
                            plunger_bottom,
                            plunger_top
                        ]
                    ),

                    # Steam particles

                    go.Scatter3d(

                        x=sx,
                        y=sy,
                        z=sz
                    ),

                    # Oil particles

                    go.Scatter3d(

                        x=ox,
                        y=oy,
                        z=oz
                    )
                ]
            )
        )

    return frames


# ============================================================
# MAIN DIGITAL TWIN
# ============================================================

def create_digital_twin_3d(
    reservoir_temperature=47.0,
    heated_temperature=100.0,
    production_temperature=70.0,
    steam_temperature=285.0
):

    fig = go.Figure()

    # ========================================================
    # TRACE 0 — THERMAL FIELD
    # ========================================================

    X, Y, Z, temperature = (
        generate_temperature_field(
            reservoir_temperature,
            heated_temperature
        )
    )

    fig.add_trace(
        go.Volume(

            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),

            value=temperature.flatten(),

            isomin=reservoir_temperature,
            isomax=heated_temperature,

            opacity=0.17,

            surface_count=8,

            colorscale=TEMP_COLORS,

            caps=dict(
                x_show=False,
                y_show=False,
                z_show=False
            ),

            colorbar=dict(

                title=dict(
                    text="Temperature<br>°C",

                    font=dict(
                        color="white"
                    )
                ),

                tickfont=dict(
                    color="white"
                ),

                thickness=16
            ),

            name="Thermal Field",

            hovertemplate=(
                "<b>Temperature</b><br>"
                "%{value:.1f} °C"
                "<extra></extra>"
            )
        )
    )

    # ========================================================
    # RESERVOIR
    # ========================================================

    add_reservoir_box(fig)

    add_grid(fig)

    # ========================================================
    # WELL
    # ========================================================

    add_well(fig)

    add_wellhead(fig)

    # ========================================================
    # SRP
    # ========================================================

    add_srp_unit(fig)

    add_rod(fig)

    # ========================================================
    # DOWNHOLE PUMP
    # ========================================================

    add_downhole_pump(fig)

    # ========================================================
    # STEAM GENERATOR
    # ========================================================

    add_steam_generator(fig)

    # ========================================================
    # INITIAL PARTICLES
    # ========================================================

    (
        steam_x,
        steam_y,
        steam_z,
        oil_x,
        oil_y,
        oil_z
    ) = initial_particles()

    # Steam particles

    fig.add_trace(
        go.Scatter3d(

            x=steam_x,
            y=steam_y,
            z=steam_z,

            mode="markers",

            marker=dict(
                size=9,
                color=STEAM_COLOR,
                opacity=0.95
            ),

            name="Steam Flow",

            hovertemplate=(
                "<b>Steam</b><br>"
                f"{steam_temperature:.0f} °C"
                "<extra></extra>"
            )
        )
    )

    # Oil particles

    fig.add_trace(
        go.Scatter3d(

            x=oil_x,
            y=oil_y,
            z=oil_z,

            mode="markers",

            marker=dict(
                size=9,
                color=OIL_COLOR,
                opacity=0.95
            ),

            name="Heavy Oil Flow",

            hovertemplate=(
                "<b>Heavy Oil</b><br>"
                "Toward pump"
                "<extra></extra>"
            )
        )
    )

    # ========================================================
    # ANIMATION
    # ========================================================

    fig.frames = create_particle_frames()

    # ========================================================
    # LABELS
    # ========================================================

    labels = [
        (-5.8, 0, 5.0, "♨ STEAM GENERATOR"),
        (3.2, 0, 3.5, "⚙ SRP UNIT"),
        (2.2, 0, 10.5, "🟠 DOWNHOLE PUMP"),
        (5.0, 1.7, 11.8, "🛢 OIL FLOW"),
        (-5.5, -3.0, 6.8, f"RESERVOIR<br>{reservoir_temperature:.0f} °C"),
        (4.5, -2.0, 5.8, f"HEATED ZONE<br>{heated_temperature:.0f} °C"),
        (3.8, 0, 13.5, f"PRODUCTION<br>{production_temperature:.1f} °C")
    ]

    for x, y, z, text in labels:

        fig.add_trace(
            go.Scatter3d(

                x=[x],
                y=[y],
                z=[z],

                mode="text",

                text=[text],

                textfont=dict(
                    color=WHITE,
                    size=10
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )

    # ========================================================
    # ANIMATION CONTROLS
    # ========================================================

    fig.update_layout(

        updatemenus=[

            dict(

                type="buttons",

                showactive=True,

                x=0.02,
                y=0.98,

                xanchor="left",
                yanchor="top",

                buttons=[

                    dict(

                        label="▶ START SRP + FLOW",

                        method="animate",

                        args=[

                            None,

                            dict(

                                frame=dict(
                                    duration=80,
                                    redraw=True
                                ),

                                transition=dict(
                                    duration=0
                                ),

                                fromcurrent=True,

                                mode="immediate"
                            )
                        ]
                    ),

                    dict(

                        label="⏸ PAUSE",

                        method="animate",

                        args=[

                            [None],

                            dict(

                                frame=dict(
                                    duration=0,
                                    redraw=False
                                ),

                                transition=dict(
                                    duration=0
                                ),

                                mode="immediate"
                            )
                        ]
                    )
                ]
            )
        ],

        # ====================================================
        # FRAME SLIDER
        # ====================================================

        sliders=[

            dict(

                active=0,

                x=0.20,
                y=0.02,

                len=0.60,

                currentvalue=dict(
                    prefix="Simulation cycle: "
                ),

                steps=[

                    dict(

                        label=str(i),

                        method="animate",

                        args=[

                            [str(i)],

                            dict(

                                mode="immediate",

                                frame=dict(
                                    duration=0,
                                    redraw=True
                                )
                            )
                        ]
                    )

                    for i in range(40)
                ]
            )
        ],

        # ====================================================
        # 3D SCENE
        # ====================================================

        scene=dict(

            bgcolor="#050607",

            xaxis=dict(

                title="X — Reservoir",

                color="#DDE3EA",

                gridcolor="#242A30",

                zerolinecolor="#505861",

                backgroundcolor="#050607",

                showbackground=True
            ),

            yaxis=dict(

                title="Y — Reservoir",

                color="#DDE3EA",

                gridcolor="#242A30",

                zerolinecolor="#505861",

                backgroundcolor="#050607",

                showbackground=True
            ),

            zaxis=dict(

                title="Depth / Height",

                color="#DDE3EA",

                gridcolor="#242A30",

                zerolinecolor="#505861",

                backgroundcolor="#050607",

                showbackground=True
            ),

            aspectmode="manual",

            aspectratio=dict(

                x=1.35,
                y=1.35,
                z=1.55
            ),

            camera=dict(

                eye=dict(
                    x=1.7,
                    y=1.7,
                    z=1.25
                )
            )
        ),

        # ====================================================
        # GENERAL LAYOUT
        # ====================================================

        title=dict(

            text=(
                "BAGHEWALA "
                "WELL-TO-SURFACE DIGITAL TWIN"
            ),

            font=dict(
                color="white",
                size=21
            ),

            x=0.03
        ),

        paper_bgcolor="#050607",

        plot_bgcolor="#050607",

        font=dict(
            color="white"
        ),

        legend=dict(

            orientation="v",

            x=0.82,
            y=0.82,

            xanchor="left",
            yanchor="top",

            bgcolor="rgba(5,6,7,0.82)",

            bordercolor="#41474F",

            borderwidth=1,

            font=dict(
                color="white",
                size=10
            )
        ),

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        )
    )

    return fig


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    fig = create_digital_twin_3d(

        reservoir_temperature=47.0,

        heated_temperature=100.0,

        production_temperature=70.0,

        steam_temperature=285.0
    )

    fig.show()