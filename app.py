import math
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="LunarCap AI",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg: #070b12;
            --panel: #101722;
            --panel-soft: #151f2d;
            --panel-light: #1b2736;
            --line: rgba(210, 225, 245, 0.14);
            --text: #f5f7fb;
            --muted: #9aa8ba;
            --soft: #cbd5e1;
            --cyan: #8be9ff;
            --blue: #8fb7ff;
            --mint: #a8f0cf;
            --lime: #d9f99d;
            --pink: #f7b7d8;
            --amber: #ffd28a;
            --red: #ff9f9f;
            --green: #86efac;
        }

        html, body, [class*="css"] {
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(139, 233, 255, 0.13), transparent 34rem),
                radial-gradient(circle at top right, rgba(247, 183, 216, 0.10), transparent 30rem),
                linear-gradient(180deg, #070b12 0%, #0a111c 48%, #070b12 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background: #060a11;
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text);
        }

        section[data-testid="stSidebar"] .stSlider label {
            font-weight: 720;
            color: var(--text) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: var(--muted);
        }

        h1, h2, h3, p, label, span, div {
            letter-spacing: 0;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.55rem;
            margin-bottom: 1rem;
            background:
                linear-gradient(135deg, rgba(16, 23, 34, 0.96), rgba(19, 32, 48, 0.96)),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.03) 0 1px, transparent 1px 64px),
                repeating-linear-gradient(0deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 64px);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -110px;
            top: -140px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(139, 233, 255, 0.26), transparent 65%);
            pointer-events: none;
        }

        .hero-grid {
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: 1.35fr 0.85fr;
            gap: 1.25rem;
            align-items: center;
        }

        .eyebrow {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-weight: 850;
            color: var(--cyan);
            margin-bottom: 0.5rem;
        }

        .hero-title {
            font-size: clamp(2rem, 4vw, 3.55rem);
            line-height: 0.98;
            margin: 0;
            font-weight: 900;
            color: var(--text);
        }

        .hero-copy {
            max-width: 720px;
            color: var(--soft);
            font-size: 1.02rem;
            line-height: 1.62;
            margin-top: 0.8rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            border-radius: 999px;
            padding: 0.42rem 0.78rem;
            margin-top: 1rem;
            font-size: 0.82rem;
            font-weight: 850;
            border: 1px solid transparent;
        }

        .status-stable {
            color: #052e16;
            background: linear-gradient(135deg, var(--green), var(--mint));
            border-color: rgba(168, 240, 207, 0.8);
        }

        .status-marginal {
            color: #3b2500;
            background: linear-gradient(135deg, var(--amber), #fff0b7);
            border-color: rgba(255, 210, 138, 0.85);
        }

        .status-risk {
            color: #450a0a;
            background: linear-gradient(135deg, var(--red), #ffc4c4);
            border-color: rgba(255, 159, 159, 0.85);
        }

        .orbit-card {
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1.1rem;
            background: rgba(255, 255, 255, 0.055);
            backdrop-filter: blur(10px);
        }

        .orbit {
            height: 210px;
            border-radius: 16px;
            position: relative;
            background:
                radial-gradient(circle at center, rgba(139, 233, 255, 0.13), transparent 58%),
                linear-gradient(135deg, rgba(139, 233, 255, 0.08), rgba(247, 183, 216, 0.08));
            border: 1px solid rgba(255,255,255,0.08);
        }

        .moon {
            position: absolute;
            width: 88px;
            height: 88px;
            left: calc(50% - 44px);
            top: calc(50% - 44px);
            border-radius: 50%;
            background:
                radial-gradient(circle at 32% 28%, #ffffff, #dce8f7 45%, #9db0c5);
            box-shadow: 0 0 38px rgba(139, 233, 255, 0.32);
        }

        .orbit-ring {
            position: absolute;
            inset: 36px;
            border: 1px dashed rgba(203, 213, 225, 0.38);
            border-radius: 50%;
        }

        .node {
            position: absolute;
            width: 12px;
            height: 12px;
            border-radius: 999px;
            background: var(--mint);
            box-shadow: 0 0 18px rgba(168, 240, 207, 0.8);
        }

        .node.one { left: 20%; top: 36%; }
        .node.two { right: 23%; top: 28%; background: var(--pink); }
        .node.three { right: 28%; bottom: 24%; background: var(--cyan); }

        .orbit-caption {
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
            color: var(--muted);
            font-size: 0.8rem;
            margin-top: 0.85rem;
        }

        .metric-card {
            min-height: 128px;
            border-radius: 16px;
            padding: 1rem;
            border: 1px solid var(--line);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.085), rgba(255,255,255,0.045));
            box-shadow: 0 16px 42px rgba(0,0,0,0.22);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 850;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.48rem;
        }

        .metric-value {
            color: var(--text);
            font-size: 1.8rem;
            line-height: 1.05;
            font-weight: 900;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.4;
            margin-top: 0.55rem;
        }

        .section-title {
            color: var(--text);
            font-size: 1.18rem;
            font-weight: 880;
            margin-bottom: 0.2rem;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.45;
            margin-bottom: 1rem;
        }

        .summary-text {
            color: var(--soft);
            font-size: 0.99rem;
            line-height: 1.72;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(180deg, rgba(255,255,255,0.078), rgba(255,255,255,0.04));
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: 0 18px 48px rgba(0,0,0,0.22);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        .health-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.68rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }

        .health-row:last-child {
            border-bottom: none;
        }

        .health-label {
            color: var(--muted);
        }

        .health-value {
            color: var(--text);
            font-weight: 820;
            text-align: right;
        }

        .rec-box {
            border: 1px solid rgba(139, 233, 255, 0.25);
            border-radius: 14px;
            padding: 1rem;
            background:
                linear-gradient(135deg, rgba(139, 233, 255, 0.12), rgba(168, 240, 207, 0.08));
        }

        .rec-item {
            color: var(--soft);
            margin-bottom: 0.52rem;
            line-height: 1.45;
        }

        .improvement {
            margin-top: 0.85rem;
            color: var(--mint);
            font-weight: 880;
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--cyan), var(--mint));
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid rgba(139, 233, 255, 0.28);
            background: linear-gradient(135deg, rgba(139, 233, 255, 0.22), rgba(168, 240, 207, 0.18));
            color: var(--text);
            font-weight: 850;
        }

        .stButton > button:hover {
            border-color: rgba(139, 233, 255, 0.65);
            color: white;
        }

        .stAlert {
            border-radius: 14px;
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .orbit {
                height: 170px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def surface_tension_water(temp_c: float) -> float:
    gamma_20c = 0.0728
    slope = -0.000155
    gamma = gamma_20c + slope * (temp_c - 20.0)
    return float(np.clip(gamma, 0.025, 0.105))


def capillary_pressure(radius_m: float, contact_angle_deg: float, gamma: float) -> float:
    theta_rad = math.radians(contact_angle_deg)
    return (2.0 * gamma * math.cos(theta_rad)) / radius_m


def calculate_stability_score(capillary_pressure_pa: float, flow_demand_pa: float) -> float:
    if flow_demand_pa <= 0:
        return 100.0

    pressure_ratio = capillary_pressure_pa / flow_demand_pa

    if pressure_ratio <= 0:
        return 0.0

    score = 100.0 * (1.0 - math.exp(-0.85 * pressure_ratio))
    return float(np.clip(score, 0.0, 100.0))


def calculate_confidence_score(stability_score: float, pressure_ratio: float) -> float:
    distance_from_boundary = abs(stability_score - 50.0)
    ratio_strength = min(pressure_ratio / 3.0, 1.0)
    confidence = 55.0 + (distance_from_boundary * 0.6) + (ratio_strength * 18.0)
    return float(np.clip(confidence, 50.0, 99.0))


def classify_system(stability_score: float) -> str:
    if stability_score >= 80:
        return "Stable"
    if stability_score >= 55:
        return "Marginal"
    return "High Risk"


def health_rating(stability_score: float) -> tuple[str, str]:
    if stability_score >= 90:
        return "Excellent", "5/5"
    if stability_score >= 75:
        return "Good", "4/5"
    if stability_score >= 55:
        return "Marginal", "3/5"
    return "High Risk", "2/5"


def status_css_class(status: str) -> str:
    if status == "Stable":
        return "status-stable"
    if status == "Marginal":
        return "status-marginal"
    return "status-risk"


def build_engineering_summary(
    status: str,
    confidence: float,
    cap_pressure: float,
    flow_demand: float,
    pressure_ratio: float,
    radius_um: float,
    contact_angle: float,
    temp_c: float,
) -> str:
    dominant_factor = "small pore radius"

    if contact_angle > 65:
        dominant_factor = "reduced wettability from the high contact angle"

    if radius_um > 80:
        dominant_factor = "large pore radius reducing capillary pressure"

    if temp_c > 100:
        temp_comment = "Elevated temperature reduces surface tension and weakens the capillary driving force."
    elif temp_c < -50:
        temp_comment = "Low temperature increases estimated surface tension, improving the pressure margin in this model."
    else:
        temp_comment = "Temperature has a secondary influence through its effect on surface tension."

    return (
        f"The system is classified as {status} with a confidence score of {confidence:.0f}%. "
        f"The calculated capillary pressure is {cap_pressure:,.0f} Pa against a required "
        f"hydraulic demand of {flow_demand:,.0f} Pa, producing a pressure margin of "
        f"{pressure_ratio:.2f}x. The dominant contributor is {dominant_factor}. "
        f"{temp_comment}"
    )


def build_ai_reasoning(
    cap_pressure: float,
    flow_demand: float,
    pressure_ratio: float,
    stability_score: float,
    gamma: float,
    radius_um: float,
    contact_angle: float,
    temp_c: float,
) -> str:
    return f"""
The model uses the Young-Laplace equation:

Delta P = 2 * gamma * cos(theta) / r

Current design state:

- Surface tension: {gamma:.4f} N/m
- Pore radius: {radius_um:.2f} micrometers
- Contact angle: {contact_angle:.1f} degrees
- Temperature: {temp_c:.1f} C
- Capillary pressure: {cap_pressure:,.0f} Pa
- Flow demand: {flow_demand:,.0f} Pa
- Pressure ratio: {pressure_ratio:.2f}
- Stability score: {stability_score:.1f}/100

A pressure ratio above 1.0 means capillary pressure exceeds hydraulic demand.
Pore radius and flow demand usually dominate the prediction because they directly
control pressure margin. Contact angle affects wettability through the cosine term,
while temperature modifies surface tension.
"""


def feature_importance(
    radius_um: float,
    flow_demand: float,
    contact_angle: float,
    temp_c: float,
) -> pd.DataFrame:
    radius_weight = min(55, 25 + radius_um * 0.35)
    flow_weight = min(45, 18 + flow_demand / 900)
    angle_weight = min(35, 8 + contact_angle * 0.22)
    temp_weight = min(25, 5 + abs(temp_c) * 0.05)

    total = radius_weight + flow_weight + angle_weight + temp_weight

    return pd.DataFrame(
        {
            "Feature": ["Radius", "Flow Demand", "Contact Angle", "Temperature"],
            "Importance": [
                radius_weight / total * 100,
                flow_weight / total * 100,
                angle_weight / total * 100,
                temp_weight / total * 100,
            ],
        }
    ).sort_values("Importance", ascending=False)


def recommendation_engine(
    stability_score: float,
    radius_um: float,
    contact_angle: float,
    flow_demand: float,
) -> tuple[list[str], float]:
    recommendations = []
    improvement = 0.0

    if radius_um > 20:
        recommendations.append("Reduce pore radius by 15% to increase capillary pressure.")
        improvement += 12.0

    if flow_demand > 1500:
        recommendations.append("Lower hydraulic flow demand to improve pressure margin.")
        improvement += 9.0

    if contact_angle > 45:
        recommendations.append("Increase wettability by reducing contact angle.")
        improvement += 7.0

    if stability_score < 60:
        recommendations.append("Increase design margin before operation.")
        improvement += 10.0

    if not recommendations:
        recommendations.append("Maintain the current operating window.")
        improvement = 3.0

    return recommendations, improvement


def run_sensitivity_analysis(
    radius_um: float,
    contact_angle: float,
    flow_demand: float,
    temp_c: float,
) -> pd.DataFrame:
    baseline_gamma = surface_tension_water(temp_c)
    baseline_pressure = capillary_pressure(radius_um * 1e-6, contact_angle, baseline_gamma)
    baseline_score = calculate_stability_score(baseline_pressure, flow_demand)

    rows = []

    for name in ["Radius", "Contact Angle", "Flow Demand", "Temperature"]:
        low_radius = radius_um
        high_radius = radius_um
        low_angle = contact_angle
        high_angle = contact_angle
        low_demand = flow_demand
        high_demand = flow_demand
        low_temp = temp_c
        high_temp = temp_c

        if name == "Radius":
            low_radius = max(radius_um * 0.8, 1)
            high_radius = max(radius_um * 1.2, 1)

        elif name == "Contact Angle":
            low_angle = float(np.clip(contact_angle * 0.8, 0, 89))
            high_angle = float(np.clip(contact_angle * 1.2, 0, 89))

        elif name == "Flow Demand":
            low_demand = max(flow_demand * 0.8, 1)
            high_demand = max(flow_demand * 1.2, 1)

        elif name == "Temperature":
            low_temp = float(np.clip(temp_c - 20, -180, 180))
            high_temp = float(np.clip(temp_c + 20, -180, 180))

        low_gamma = surface_tension_water(low_temp)
        high_gamma = surface_tension_water(high_temp)

        low_pressure = capillary_pressure(low_radius * 1e-6, low_angle, low_gamma)
        high_pressure = capillary_pressure(high_radius * 1e-6, high_angle, high_gamma)

        low_score = calculate_stability_score(low_pressure, low_demand)
        high_score = calculate_stability_score(high_pressure, high_demand)

        rows.append(
            {
                "Parameter": name,
                "Baseline Score": baseline_score,
                "Low Case Score": low_score,
                "High Case Score": high_score,
                "Max Score Change": max(
                    abs(low_score - baseline_score),
                    abs(high_score - baseline_score),
                ),
            }
        )

    return pd.DataFrame(rows).sort_values("Max Score Change", ascending=False)


def render_metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.sidebar.title("🌙 LunarCap AI")
st.sidebar.caption("Capillary transport stability predictor")
st.sidebar.divider()

radius_um = st.sidebar.slider(
    "Pore Radius (micrometers)",
    min_value=1.0,
    max_value=150.0,
    value=25.0,
    step=1.0,
)

contact_angle = st.sidebar.slider(
    "Contact Angle (degrees)",
    min_value=0.0,
    max_value=89.0,
    value=35.0,
    step=1.0,
)

flow_demand = st.sidebar.slider(
    "Flow Demand (Pa)",
    min_value=100.0,
    max_value=10000.0,
    value=1800.0,
    step=100.0,
)

temperature_c = st.sidebar.slider(
    "Temperature (C)",
    min_value=-180.0,
    max_value=180.0,
    value=20.0,
    step=5.0,
)

st.sidebar.divider()
st.sidebar.caption("Model: Young-Laplace equation with simplified stability scoring.")

radius_m = radius_um * 1e-6
gamma = surface_tension_water(temperature_c)
cap_pressure = capillary_pressure(radius_m, contact_angle, gamma)
pressure_ratio = cap_pressure / flow_demand if flow_demand > 0 else 999.0
stability_score = calculate_stability_score(cap_pressure, flow_demand)
confidence_score = calculate_confidence_score(stability_score, pressure_ratio)
system_status = classify_system(stability_score)
rating_label, rating_score = health_rating(stability_score)

summary = build_engineering_summary(
    system_status,
    confidence_score,
    cap_pressure,
    flow_demand,
    pressure_ratio,
    radius_um,
    contact_angle,
    temperature_c,
)

recommendations, predicted_improvement = recommendation_engine(
    stability_score,
    radius_um,
    contact_angle,
    flow_demand,
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div>
                <div class="eyebrow">Lunar Water Recycling Concept</div>
                <h1 class="hero-title">LunarCap AI</h1>
                <div class="hero-copy">
                    A physics-guided engineering dashboard for evaluating capillary
                    transport stability in porous media under lunar operating conditions.
                </div>
                <div class="status-pill {status_css_class(system_status)}">
                    Current system status: {system_status}
                </div>
            </div>
            <div class="orbit-card">
                <div class="orbit">
                    <div class="orbit-ring"></div>
                    <div class="moon"></div>
                    <div class="node one"></div>
                    <div class="node two"></div>
                    <div class="node three"></div>
                </div>
                <div class="orbit-caption">
                    <span>Porous medium</span>
                    <span>Capillary transport map</span>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)

with metric_cols[0]:
    render_metric_card(
        "Stability Score",
        f"{stability_score:.0f}/100",
        f"Health rating: {rating_label}",
    )

with metric_cols[1]:
    render_metric_card(
        "Capillary Pressure",
        f"{cap_pressure:,.0f} Pa",
        "Young-Laplace prediction",
    )

with metric_cols[2]:
    render_metric_card(
        "Pressure Ratio",
        f"{pressure_ratio:.2f}x",
        "Available pressure divided by demand",
    )

with metric_cols[3]:
    render_metric_card(
        "Confidence",
        f"{confidence_score:.0f}%",
        "Classification confidence estimate",
    )

st.write("")

left_col, right_col = st.columns([1.45, 1.0], gap="large")

with left_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">Pressure vs Radius</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Native Streamlit chart showing how capillary pressure changes as pore radius increases.</div>',
            unsafe_allow_html=True,
        )

        radius_range_um = np.linspace(1, 150, 180)
        pressure_values = [
            capillary_pressure(r * 1e-6, contact_angle, gamma)
            for r in radius_range_um
        ]

        chart_df = pd.DataFrame(
            {
                "Radius (micrometers)": radius_range_um,
                "Capillary Pressure": pressure_values,
                "Flow Demand": [flow_demand] * len(radius_range_um),
            }
        )

        st.line_chart(
            chart_df,
            x="Radius (micrometers)",
            y=["Capillary Pressure", "Flow Demand"],
            height=360,
            use_container_width=True,
        )

        st.caption(
            f"Current design point: {radius_um:.1f} micrometers with "
            f"{cap_pressure:,.0f} Pa capillary pressure."
        )

with right_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">Engineering Summary</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">A concise interpretation of the current transport state.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">System Snapshot</div>', unsafe_allow_html=True)

        snapshot_rows = [
            ("System Status", system_status),
            ("Health Rating", f"{rating_label} ({rating_score})"),
            ("Surface Tension", f"{gamma:.4f} N/m"),
            ("Flow Demand", f"{flow_demand:,.0f} Pa"),
            ("Temperature", f"{temperature_c:.1f} C"),
        ]

        for label, value in snapshot_rows:
            st.markdown(
                f"""
                <div class="health-row">
                    <div class="health-label">{label}</div>
                    <div class="health-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.write("")

support_left, support_right = st.columns([1.0, 1.0], gap="large")

with support_left:
    with st.container(border=True):
        st.markdown('<div class="section-title">Engineering Recommendation</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Suggested actions based on pressure margin and design sensitivity.</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="rec-box">', unsafe_allow_html=True)
        for item in recommendations:
            st.markdown(f'<div class="rec-item">• {item}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="improvement">Predicted improvement: +{predicted_improvement:.0f}% stability</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

with support_right:
    with st.container(border=True):
        st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Estimated contribution of each input to the current prediction.</div>',
            unsafe_allow_html=True,
        )

        importance_df = feature_importance(
            radius_um,
            flow_demand,
            contact_angle,
            temperature_c,
        )

        for _, row in importance_df.iterrows():
            importance = row["Importance"]
            st.write(f"**{row['Feature']}**")
            st.progress(importance / 100)
            st.caption(f"{importance:.0f}% contribution")

st.write("")

with st.container(border=True):
    st.markdown('<div class="section-title">Operating Conditions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-kicker">Current input values and derived model terms.</div>',
        unsafe_allow_html=True,
    )

    operating_df = pd.DataFrame(
        {
            "Variable": [
                "Pore Radius",
                "Contact Angle",
                "Flow Demand",
                "Temperature",
                "Surface Tension",
                "Capillary Pressure",
                "Pressure Ratio",
                "Stability Score",
                "Confidence Score",
            ],
            "Value": [
                f"{radius_um:.1f} micrometers",
                f"{contact_angle:.1f} degrees",
                f"{flow_demand:,.0f} Pa",
                f"{temperature_c:.1f} C",
                f"{gamma:.4f} N/m",
                f"{cap_pressure:,.0f} Pa",
                f"{pressure_ratio:.2f}x",
                f"{stability_score:.1f}/100",
                f"{confidence_score:.1f}%",
            ],
        }
    )

    st.dataframe(operating_df, hide_index=True, use_container_width=True)

st.write("")

with st.container(border=True):
    st.markdown('<div class="section-title">Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-kicker">Perturbs each input and ranks which variable has the strongest effect on stability.</div>',
        unsafe_allow_html=True,
    )

    run_analysis = st.button("Run Sensitivity Analysis")

    if run_analysis:
        sensitivity_df = run_sensitivity_analysis(
            radius_um,
            contact_angle,
            flow_demand,
            temperature_c,
        )

        st.dataframe(
            sensitivity_df.style.format(
                {
                    "Baseline Score": "{:.1f}",
                    "Low Case Score": "{:.1f}",
                    "High Case Score": "{:.1f}",
                    "Max Score Change": "{:.1f}",
                }
            ),
            hide_index=True,
            use_container_width=True,
        )

        top_parameter = sensitivity_df.iloc[0]["Parameter"]
        top_change = sensitivity_df.iloc[0]["Max Score Change"]

        st.info(
            f"The strongest sensitivity is currently {top_parameter}, "
            f"which can shift the stability score by up to {top_change:.1f} points."
        )
    else:
        st.caption("Click the button to test how much each input affects the stability score.")

st.write("")

with st.container(border=True):
    with st.expander("Technical Reasoning"):
        st.write(
            build_ai_reasoning(
                cap_pressure,
                flow_demand,
                pressure_ratio,
                stability_score,
                gamma,
                radius_um,
                contact_angle,
                temperature_c,
            )
        )

st.caption(
    "LunarCap AI uses simplified engineering equations for educational demonstration "
    "and early-stage design screening. Results should be validated with experimental "
    "or mission-specific data before operational use."
)
