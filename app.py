"""
==================================================================================
 GEAR TRAIN RATIO & SPEED CALCULATOR  (Simple & Compound Gear Trains)
 Diploma in Mechanical Engineering — Semester 3 — Python Mini Project (Topic 23)

 Group      : Mr. Pythons
 Members    : Abdul Mukhtadir Faizaan  (25012250610060)
              Akshit Valand            (25012251210007)
              Daksh Talsaniya          (25012251210006)
              Shaikh Mohammed Jalis    (24012250670909)
 Guide      : Shaikh Mohammed Azim
==================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------------
st.set_page_config(
    page_title="Gear Train Ratio Calculator | Mr. Pythons",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------------
# THEME — WHITE / BLUE / BLACK
# ----------------------------------------------------------------------------------
BLUE = "#1565C0"
LIGHT_BLUE = "#5E92F3"
DARK_BLUE = "#0D3C78"
BLACK = "#0B0B0B"
WHITE = "#FFFFFF"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {WHITE};
        color: {BLACK};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {BLACK};
    }}
    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}
    h1, h2, h3 {{
        color: {DARK_BLUE} !important;
        font-family: 'Trebuchet MS', sans-serif;
    }}
    .header-box {{
        background: linear-gradient(90deg, {BLACK} 0%, {DARK_BLUE} 60%, {BLUE} 100%);
        padding: 18px 24px;
        border-radius: 10px;
        margin-bottom: 14px;
    }}
    .header-box h1 {{
        color: {WHITE} !important;
        margin: 0;
    }}
    .header-box p {{
        color: #D6E4FF !important;
        margin: 4px 0 0 0;
    }}
    div[data-testid="stMetric"] {{
        background-color: #EAF2FF;
        border: 1px solid {BLUE};
        border-radius: 10px;
        padding: 10px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {DARK_BLUE} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {BLACK} !important;
    }}
    .stButton>button {{
        background-color: {BLUE};
        color: {WHITE};
        border-radius: 8px;
        border: none;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #EAF2FF;
        border-radius: 8px 8px 0 0;
        color: {DARK_BLUE};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {BLUE} !important;
        color: {WHITE} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-box">
        <h1>⚙️ Simple &amp; Compound Gear Train — Ratio &amp; Speed Calculator</h1>
        <p>Diploma in Mechanical Engineering · Semester 3 · Python Mini Project · Topic 23</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_team, col_guide = st.columns([3, 2])
with col_team:
    st.markdown("#### 👥 Group: **Mr. Pythons**")
    TEAM = [
        ("Abdul Mukhtadir Faizaan", "25012250610060"),
        ("Akshit Valand", "25012251210007"),
        ("Daksh Talsaniya", "25012251210006"),
        ("Shaikh Mohammed Jalis", "24012250670909"),
    ]
    st.table({"Member Name": [m[0] for m in TEAM], "Enrollment No.": [m[1] for m in TEAM]})
with col_guide:
    st.markdown("#### 🎓 Guide")
    st.write("**Shaikh Mohammed Azim**")
    st.markdown("#### 📘 Topic")
    st.write("23 — Simple & Compound Gear Train Ratio & Speed Calculator")

st.divider()

# ----------------------------------------------------------------------------------
# SIDEBAR — INPUTS
# ----------------------------------------------------------------------------------
st.sidebar.header("🔧 Input Parameters")

mode = st.sidebar.radio("Gear Train Type", ["Simple Gear Train", "Compound Gear Train"])

input_rpm = st.sidebar.number_input(
    "Input (Driver) Speed, N₁ (RPM)", min_value=1.0, max_value=20000.0, value=1440.0, step=10.0
)
input_torque = st.sidebar.number_input(
    "Input Torque, T₁ (N·m)  [0 = skip torque/power calc]", min_value=0.0, max_value=100000.0, value=50.0, step=1.0
)
efficiency_pct = st.sidebar.slider("Mechanical Efficiency η per mesh (%)", 50, 100, 96)
efficiency_mesh = efficiency_pct / 100.0

teeth = []
stage_teeth = []

if mode == "Simple Gear Train":
    n_gears = st.sidebar.slider("Total number of gears in the train", 2, 6, 3)
    st.sidebar.caption("Gear 1 = driver, last gear = final driven gear, in-between = idlers.")
    for i in range(n_gears):
        if i == 0:
            label = f"Driver Gear — T₁ (teeth)"
            default = 20
        elif i == n_gears - 1:
            label = f"Last Driven Gear — T{n_gears} (teeth)"
            default = 50
        else:
            label = f"Idler Gear {i} — T{i+1} (teeth)"
            default = 30
        t = st.sidebar.number_input(label, min_value=8, max_value=300, value=default, step=1, key=f"simple_{i}")
        teeth.append(int(t))
else:
    n_stages = st.sidebar.slider("Number of gear pairs (stages)", 1, 4, 2)
    st.sidebar.caption("Each stage: a driver gear meshing with a driven gear; consecutive stages share a shaft.")
    for i in range(n_stages):
        c1, c2 = st.sidebar.columns(2)
        td = c1.number_input(f"Stage {i+1} Driver T", min_value=8, max_value=300, value=20 + i * 5, step=1, key=f"cd_{i}")
        tn = c2.number_input(f"Stage {i+1} Driven T", min_value=8, max_value=300, value=40 + i * 5, step=1, key=f"cn_{i}")
        stage_teeth.append((int(td), int(tn)))

# ----------------------------------------------------------------------------------
# VALIDATION
# ----------------------------------------------------------------------------------
errors = []
if input_rpm <= 0:
    errors.append("Input speed must be greater than zero.")
if mode == "Simple Gear Train":
    if any(t < 8 for t in teeth):
        errors.append("Every gear must have at least 8 teeth (avoids undercutting in involute gears).")
else:
    for i, (td, tn) in enumerate(stage_teeth):
        if td < 8 or tn < 8:
            errors.append(f"Stage {i+1}: teeth counts must be at least 8.")
if efficiency_mesh <= 0:
    errors.append("Efficiency must be greater than zero.")

if errors:
    for e in errors:
        st.error(f"⚠️ {e}")
    st.stop()

# ----------------------------------------------------------------------------------
# CORE CALCULATIONS
# ----------------------------------------------------------------------------------
if mode == "Simple Gear Train":
    n_meshes = len(teeth) - 1
    train_value = teeth[0] / teeth[-1]                 # N_out / N_in  (idlers cancel out)
    overall_efficiency = efficiency_mesh ** n_meshes
    stage_speeds = [input_rpm * (teeth[0] / t) for t in teeth]   # RPM of every gear in the chain
    stage_labels = [f"Gear {i+1}\n(T={t})" for i, t in enumerate(teeth)]
else:
    n_meshes = len(stage_teeth)
    train_value = 1.0
    for td, tn in stage_teeth:
        train_value *= td / tn
    overall_efficiency = efficiency_mesh ** n_meshes
    stage_speeds = [input_rpm]
    running = input_rpm
    for td, tn in stage_teeth:
        running = running * (td / tn)
        stage_speeds.append(running)
    stage_labels = ["Input Shaft"] + [f"Shaft {i+1}\n(after stage {i+1})" for i in range(n_meshes)]

output_rpm = input_rpm * train_value
direction_same = (n_meshes % 2 == 0)

output_torque = None
mech_advantage = None
input_power_kw = None
output_power_kw = None
if input_torque > 0:
    output_torque = input_torque * (input_rpm / output_rpm) * overall_efficiency
    mech_advantage = output_torque / input_torque
    input_power_kw = 2 * np.pi * input_rpm * input_torque / 60000.0
    output_power_kw = 2 * np.pi * output_rpm * output_torque / 60000.0

# ----------------------------------------------------------------------------------
# TABS
# ----------------------------------------------------------------------------------
tab_calc, tab_3d, tab_graphs = st.tabs(["📐 Results & Formulas", "🌀 3D Animated Model", "📈 Graphs"])

# ====================================================================================
# TAB 1 — RESULTS & FORMULAS
# ====================================================================================
with tab_calc:
    st.subheader("📊 Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Train Value  (e = N_out / N_in)", f"{train_value:.4f}")
    c2.metric("Output Speed  N_out", f"{output_rpm:,.2f} RPM")
    c3.metric("Rotation Direction", "Same as input ↻" if direction_same else "Opposite to input ↺")
    c4.metric("No. of Meshes", f"{n_meshes}")

    if output_torque is not None:
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Output Torque  T_out", f"{output_torque:,.2f} N·m")
        d2.metric("Mechanical Advantage", f"{mech_advantage:.3f}")
        d3.metric("Input Power", f"{input_power_kw:,.3f} kW")
        d4.metric("Output Power", f"{output_power_kw:,.3f} kW  (loss {input_power_kw-output_power_kw:.3f} kW)")

    st.divider()
    st.subheader("📖 Formulas Used")

    st.markdown("**1. Fundamental gear meshing relation** (speed is inversely proportional to teeth count):")
    st.latex(r"N_1 \, T_1 = N_2 \, T_2 \qquad \Rightarrow \qquad \frac{N_2}{N_1} = \frac{T_1}{T_2}")

    if mode == "Simple Gear Train":
        st.markdown("**2. Train Value — Simple Gear Train** (idler-gear teeth cancel out; they only affect direction):")
        st.latex(r"e \;=\; \frac{N_{out}}{N_{in}} \;=\; \frac{T_{\text{driver}}}{T_{\text{last driven}}} \;=\; \frac{T_1}{T_n}")
    else:
        st.markdown("**2. Train Value — Compound Gear Train** (product of each stage's driver/driven ratio):")
        st.latex(
            r"e \;=\; \frac{N_{out}}{N_{in}} \;=\; \prod_{i=1}^{k}\frac{T_{driver,i}}{T_{driven,i}}"
            r"\;=\; \frac{T_1 \times T_3 \times \cdots}{T_2 \times T_4 \times \cdots}"
        )

    st.markdown("**3. Output Speed:**")
    st.latex(r"N_{out} = N_{in} \times e")

    st.markdown("**4. Direction of rotation** — every external gear mesh reverses the sense of rotation:")
    st.latex(r"\text{If } (\text{no. of meshes}) \text{ is even} \Rightarrow \text{same direction}, \quad \text{if odd} \Rightarrow \text{opposite direction}")

    st.markdown("**5. Output Torque & Mechanical Advantage** (accounting for mesh efficiency η):")
    st.latex(r"T_{out} = T_{in} \times \frac{N_{in}}{N_{out}} \times \eta_{overall}, \qquad \eta_{overall} = \eta_{mesh}^{\,(\text{no. of meshes})}")
    st.latex(r"\text{Mechanical Advantage} = \frac{T_{out}}{T_{in}}")

    st.markdown("**6. Power transmitted (kW), with N in RPM and T in N·m:**")
    st.latex(r"P = \frac{2 \pi N T}{60000}\ \text{kW}")

    st.info(
        "Note: efficiency is applied **per mesh** and compounded across every mesh in the train "
        "(overall η = η_mesh^(number of meshes)), matching how losses accumulate along a real gear train."
    )

# ====================================================================================
# TAB 2 — 3D ANIMATED MODEL
# ====================================================================================
with tab_3d:
    st.subheader("🌀 3D Animated Gear Train")
    st.caption(
        "Gears are drawn to scale relative to their teeth count and rotate at the exact calculated "
        "speed ratio and direction (not mechanically exact meshing geometry — for visual understanding only)."
    )

    MODULE = 0.6          # arbitrary visual scale (mm-equivalent), not a real design module
    HEIGHT = 1.0           # gear thickness
    N_THETA = 70           # resolution around the gear rim
    TOOTH_DEPTH_FRAC = 0.12
    N_FRAMES = 30

    def gear_wall(radius, teeth_n, x_center, z_offset, phase, color):
        """Return a go.Surface representing a squared-tooth cylindrical gear wall."""
        theta = np.linspace(0, 2 * np.pi, N_THETA)
        depth = radius * TOOTH_DEPTH_FRAC
        r = radius + depth * 0.5 * np.sign(np.sin(teeth_n * (theta - phase)))
        z_levels = np.array([z_offset - HEIGHT / 2, z_offset + HEIGHT / 2])
        Theta, Z = np.meshgrid(theta, z_levels)
        R = np.tile(r, (2, 1))
        X = x_center + R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return go.Surface(
            x=X, y=Y, z=Z,
            surfacecolor=np.ones_like(Z),
            colorscale=[[0, color], [1, color]],
            showscale=False, cmin=0, cmax=1,
            lighting=dict(ambient=0.55, diffuse=0.6, specular=0.3),
        )

    # ---- build the list of gear "elements" to draw & animate ----
    elements = []  # dict: x, r, teeth, speed_ratio(rel. to input), direction(+1/-1), z_offset, color, label
    colors_cycle = [BLUE, BLACK, LIGHT_BLUE, DARK_BLUE]

    if mode == "Simple Gear Train":
        x = 0.0
        radii = [t * MODULE / 2 for t in teeth]
        for i, t in enumerate(teeth):
            speed_rel = teeth[0] / t
            direction = 1 if i % 2 == 0 else -1
            elements.append(dict(
                x=x, r=radii[i], teeth=t, speed=speed_rel, dirn=direction,
                z=0.0, color=colors_cycle[i % len(colors_cycle)], label=f"Gear {i+1} (T={t})",
            ))
            if i < len(teeth) - 1:
                x += radii[i] + radii[i + 1]
    else:
        x = 0.0
        cur_speed = 1.0
        cur_dir = 1
        for i, (td, tn) in enumerate(stage_teeth):
            r_drv = td * MODULE / 2
            r_drn = tn * MODULE / 2
            z_off = i * 0.05  # tiny stack offset so compound gears are visually distinguishable
            elements.append(dict(
                x=x, r=r_drv, teeth=td, speed=cur_speed, dirn=cur_dir,
                z=z_off, color=colors_cycle[(2 * i) % len(colors_cycle)], label=f"Stage {i+1} Driver (T={td})",
            ))
            x_driven = x + r_drv + r_drn
            new_speed = cur_speed * (td / tn)
            new_dir = -cur_dir
            elements.append(dict(
                x=x_driven, r=r_drn, teeth=tn, speed=new_speed, dirn=new_dir,
                z=z_off, color=colors_cycle[(2 * i + 1) % len(colors_cycle)], label=f"Stage {i+1} Driven (T={tn})",
            ))
            x = x_driven
            cur_speed = new_speed
            cur_dir = new_dir

    def build_traces(t_val):
        traces = []
        for el in elements:
            phase = el["dirn"] * el["speed"] * t_val
            traces.append(gear_wall(el["r"], el["teeth"], el["x"], el["z"], phase, el["color"]))
        return traces

    t_values = np.linspace(0, 2 * np.pi, N_FRAMES, endpoint=False)
    frames = [go.Frame(data=build_traces(t), name=str(k)) for k, t in enumerate(t_values)]

    fig3d = go.Figure(data=build_traces(0.0), frames=frames)

    # gear labels as 3D text
    for el in elements:
        fig3d.add_trace(go.Scatter3d(
            x=[el["x"]], y=[el["r"] + 0.4], z=[el["z"] + HEIGHT],
            mode="text", text=[el["label"]], textfont=dict(color=BLACK, size=12),
            showlegend=False,
        ))

    fig3d.update_layout(
        height=560,
        paper_bgcolor=WHITE,
        scene=dict(
            xaxis=dict(title="X", backgroundcolor=WHITE, gridcolor="#CFE0FF"),
            yaxis=dict(title="Y", backgroundcolor=WHITE, gridcolor="#CFE0FF"),
            zaxis=dict(title="Z", backgroundcolor=WHITE, gridcolor="#CFE0FF"),
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        updatemenus=[dict(
            type="buttons", showactive=False, y=1, x=0, xanchor="left", yanchor="top",
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
            ],
        )],
        sliders=[dict(
            steps=[dict(method="animate", args=[[str(k)], dict(mode="immediate",
                    frame=dict(duration=0, redraw=True), transition=dict(duration=0))], label=str(k))
                   for k in range(N_FRAMES)],
            active=0, x=0.1, len=0.85,
        )],
    )

    st.plotly_chart(fig3d, use_container_width=True)
    st.caption(
        "Blue/black gears rotate at their true relative speed (∝ inverse of teeth count) and reverse "
        "direction at every mesh, exactly as calculated in the Results tab."
    )

# ====================================================================================
# TAB 3 — GRAPHS
# ====================================================================================
with tab_graphs:
    st.subheader("📈 Speed Distribution Along the Train")
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    bars = ax1.bar(stage_labels, stage_speeds, color=BLUE, edgecolor=BLACK, linewidth=1.2, zorder=3)
    ax1.set_ylabel("Speed (RPM)")
    ax1.set_title("Rotational Speed at Each Gear / Shaft", color=BLACK)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax1.set_facecolor(WHITE)
    fig1.patch.set_facecolor(WHITE)
    for b in bars:
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{b.get_height():,.0f}",
                  ha="center", va="bottom", fontsize=8, color=BLACK)
    st.pyplot(fig1)

    st.subheader("📈 Sensitivity — Output Speed vs. Final-Stage Driven Teeth")
    if mode == "Simple Gear Train":
        base_first, base_last = teeth[0], teeth[-1]
        sweep = np.arange(max(8, base_last - 20), base_last + 21, 1)
        out_speeds = input_rpm * (base_first / sweep)
        current_val = base_last
    else:
        base_td, base_tn = stage_teeth[-1]
        other_ratio = train_value / (base_td / base_tn)
        sweep = np.arange(max(8, base_tn - 20), base_tn + 21, 1)
        out_speeds = input_rpm * other_ratio * (base_td / sweep)
        current_val = base_tn

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(sweep, out_speeds, color=BLUE, linewidth=2, zorder=3)
    ax2.axvline(current_val, color=BLACK, linestyle="--", linewidth=1, zorder=2)
    ax2.scatter([current_val], [output_rpm], color=BLACK, zorder=4, s=45, label="Current design")
    ax2.set_xlabel("Final driven gear teeth count")
    ax2.set_ylabel("Output Speed (RPM)")
    ax2.set_title("Effect of Final Driven Gear Size on Output Speed", color=BLACK)
    ax2.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax2.legend()
    ax2.set_facecolor(WHITE)
    fig2.patch.set_facecolor(WHITE)
    st.pyplot(fig2)

    if output_torque is not None:
        st.subheader("📈 Torque & Power Comparison")
        colp, colt = st.columns(2)
        with colt:
            fig3, ax3 = plt.subplots(figsize=(5, 4))
            ax3.bar(["Input Torque", "Output Torque"], [input_torque, output_torque],
                    color=[BLACK, BLUE], edgecolor=BLACK, zorder=3)
            ax3.set_ylabel("Torque (N·m)")
            ax3.set_title("Torque: Input vs Output", color=BLACK)
            ax3.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
            ax3.set_facecolor(WHITE)
            fig3.patch.set_facecolor(WHITE)
            st.pyplot(fig3)
        with colp:
            fig4, ax4 = plt.subplots(figsize=(5, 4))
            labels = ["Output Power", "Power Lost (friction)"]
            values = [output_power_kw, max(input_power_kw - output_power_kw, 0)]
            ax4.pie(values, labels=labels, colors=[BLUE, BLACK], autopct="%1.1f%%",
                    textprops=dict(color=WHITE, weight="bold"), wedgeprops=dict(edgecolor=WHITE))
            ax4.set_title(f"Power Balance (Input = {input_power_kw:.3f} kW)", color=BLACK)
            fig4.patch.set_facecolor(WHITE)
            st.pyplot(fig4)
    else:
        st.caption("Enter an Input Torque (> 0) in the sidebar to see torque and power comparison graphs.")

st.divider()
st.caption(
    "Mr. Pythons · Diploma Mechanical Engineering, Semester 3 · Python Mini Project (Streamlit) · "
    "Guide: Shaikh Mohammed Azim"
)
