import math
import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="LunarCap AI",
    page_icon="LC",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --bg: #f4f7fb;
            --panel: #ffffff;
            --ink: #172033;
            --muted: #667085;
            --line: #d9e2ef;
            --blue: #2563eb;
            --cyan: #0891b2;
            --green: #16833a;
            --amber: #b76e00;
            --red: #b42318;
        }

        html, body, [class*="css"] {
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background: var(--bg);
            color: var(--ink);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1240px;
        }

        section[data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] * {
            color: #f9fafb;
        }

        section[data-testid="stSidebar"] .stSlider label {
            color: #f9fafb !important;
            font-weight: 650;
        }

        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #cbd5e1;
        }

        .hero {
            background: linear-gradient(135deg, #ffffff 0%, #eef6ff 58%, #e7fbff 100%);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.5rem 1.6rem;
            margin-bottom: 1.1rem;
        }

        .eyebrow {
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--cyan);
            margin-bottom: 0.35rem;
        }

        .hero-title {
            font-size: 2.25rem;
            line-height: 1.05;
            font-weight: 850;
            color: var(--ink);
            margin: 0;
        }

        .hero-copy {
            max-width: 760px;
            margin-top: 0.65rem;
            font-size: 1rem;
            line-height: 1.55;
            color: var(--muted);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.36rem 0.72rem;
            font-size: 0.82rem;
            font-weight: 800;
            margin-top: 0.85rem;
            border: 1px solid transparent;
        }

        .status-stable {
            background: #e9f8ef;
            color: var(--green);
            border-color: #b9e6c8;
        }

        .status-marginal {
            background: #fff5df;
            color: var(--amber);
            border-color: #f4d18a;
        }

        .status-risk {
            background: #fff0ed;
            color: var(--red);
            border-color: #f2b8b0;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem 1rem 0.95rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
            min-height: 122px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 850;
            letter-spacing: 0.075em;
            text-transform: uppercase;
            margin-bottom: 0.42rem;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.75rem;
            font-weight: 850;
            line-height: 1.1;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.86rem;
            margin-top: 0.55rem;
            line-height: 1.35;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 820;
            color: var(--ink);
            margin-bottom: 0.2rem;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .summary-text {
            font-size: 0.98rem;
            line-height: 1.68;
            color: #243044;
        }

        .recommendation {
            background: #f0f7ff;
            border: 1px solid #c8def7;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 0.5rem;
        }

        .recommendation ul {
            margin-bottom: 0.4rem;
        }

        .small-muted {
            color: var(--muted);
            font-size: 0.88rem;
        }

        .health-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            border-bottom: 1px solid #edf1f7;
            padding: 0.58rem 0;
        }

        .health-row:last-child {
            border-bottom: none;
        }

        .health-label {
            color: var(--muted);
        }

        .health-value {
            color: var(--ink);
            font-weight: 760;
            text-align: right;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line);
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        }

        .stProgress > div > div > div > div {
            background-color: var(--blue);
        }

        button[kind="primary"] {
            border-radius: 8px;
            font-weight: 750;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Physics Functions
# ============================================================

def surface_tension_water(temp_c: float) -> float:
    """
    Estimate water surface tension in N/m as a function of temperature.
    This is a simplified engineering approximation for demo use.
    """
    gamma_20c = 0.0728
    slope = -0.000155
    gamma = gamma_20c + slope * (temp_c - 20.0)
    return float(np.clip(gamma, 0.025, 0.105))


def capillary_pressure(radius_m: float, contact_angle_deg: float, gamma: float) -> float:
    """
    Young-Laplace capillary pressure:
    Delta P = 2 * gamma * cos(theta) / r
    """
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


# ============================================================
# AI Helper Functions
# ============================================================

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
        temp_comment = "Elevated temperature reduces surface tension and weakens capillary driving force."
    elif temp_c < -50:
        temp_comment = "Low temperature increases estimated surface tension, improving capillary pressure in this model."
    else:
        temp_comment = "Temperature has a secondary influence through its effect on surface tension."

    return (
        f"The predicted transport regime is classified as {status} with a confidence score "
        f"of {confidence:.0f}%. The calculated capillary pressure is {cap_pressure:,.0f} Pa, "
        f"compared with a required hydraulic demand of {flow_demand:,.0f} Pa. This gives a "
        f"pressure margin factor of {pressure_ratio:.2f}. The dominant contributor to this "
        f"prediction is {dominant_factor}. {temp_comment}"
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

Where gamma is surface tension, theta is contact angle, and r is pore radius.

For the current design:

- Surface tension: {gamma:.4f} N/m
- Pore radius: {radius_um:.2f} micrometers
- Contact angle: {contact_angle:.1f} degrees
- Temperature: {temp_c:.1f} C
- Capillary pressure: {cap_pressure:,.0f} Pa
- Flow demand: {flow_demand:,.0f} Pa
- Pressure ratio: {pressure_ratio:.2f}
- Stability score: {stability_score:.1f}/100

A pressure ratio above 1.0 means capillary pressure exceeds hydraulic demand.
Higher ratios indicate more design margin and therefore stronger transport stability.

The variables with the strongest influence are usually pore radius and flow demand.
Contact angle controls wettability through the cosine term. Temperature affects the
result indirectly by changing estimated surface tension.
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

    rows = [
        ("Radius", radius_weight / total * 100),
        ("Flow Demand", flow_weight / total * 100),
        ("Contact Angle", angle_weight / total * 100),
        ("Temperature", temp_weight / total * 100),
    ]

    return pd.DataFrame(rows, columns=["Feature", "Importance"]).sort_values(
        "Importance",
        ascending=False,
    )


def recommendation_engine(
    stability_score: float,
    radius_um: float,
    contact_angle: float,
    flow_demand: float,
) -> tuple[list[str], float]:
    recommendations = []
    improvement = 0.0

    if radius_um > 20:
        recommendations.append("Reduce pore radius by 15%")
        improvement += 12.0

    if flow_demand > 1500:
        recommendations.append("Lower flow demand")
        improvement += 9.0

    if contact_angle > 45:
        recommendations.append("Increase wettability")
        improvement += 7.0

    if stability_score < 60:
        recommendations.append("Increase capillary margin before operation")
        improvement += 10.0

    if not recommendations:
        recommendations.append("Maintain the current operating window")
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
    parameters = ["Radius", "Contact Angle", "Flow Demand", "Temperature"]

    for name in parameters:
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

        sensitivity = max(abs(low_score - baseline_score), abs(high_score - baseline_score))

        rows.append(
            {
                "Parameter": name,
                "Baseline Score": baseline_score,
                "Low Case Score": low_score,
                "High Case Score": high_score,
                "Max Score Change": sensitivity,
            }
        )

    return pd.DataFrame(rows).sort_values("Max Score Change", ascending=False)


def status_css_class(status: str) -> str:
    if status == "Stable":
        return "status-stable"
    if status == "Marginal":
        return "status-marginal"
    return "status-risk"


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


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("LunarCap AI")
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


# ============================================================
# Calculations
# ============================================================

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


# ============================================================
# Header
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">Capillary Transport Analysis</div>
        <h1 class="hero-title">LunarCap AI</h1>
        <div class="hero-copy">
            A clean engineering dashboard for estimating capillary transport stability
            in porous media used for lunar water recycling concepts.
        </div>
        <div class="status-pill {status_css_class(system_status)}">
            Current System Status: {system_status}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Primary Metrics
# ============================================================

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
        "Capillary pressure divided by flow demand",
    )

with metric_cols[3]:
    render_metric_card(
        "Confidence",
        f"{confidence_score:.0f}%",
        "Classification confidence estimate",
    )

st.write("")


# ============================================================
# Main Analysis
# ============================================================

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
            f"Current design point: {radius_um:.1f} micrometers, "
            f"{cap_pressure:,.0f} Pa capillary pressure."
        )

with right_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">AI Engineering Summary</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Plain-language interpretation of the current operating condition.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Engineering Snapshot</div>', unsafe_allow_html=True)

        rows = [
            ("System Status", system_status),
            ("Health Rating", f"{rating_label} ({rating_score})"),
            ("Surface Tension", f"{gamma:.4f} N/m"),
            ("Flow Demand", f"{flow_demand:,.0f} Pa"),
            ("Temperature", f"{temperature_c:.1f} C"),
        ]

        for label, value in rows:
            st.markdown(
                f"""
                <div class="health-row">
                    <div class="health-label">{label}</div>
                    <div class="health-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# Decision Support
# ============================================================

st.write("")
support_left, support_right = st.columns([1.0, 1.0], gap="large")

with support_left:
    with st.container(border=True):
        st.markdown('<div class="section-title">Engineering Recommendation</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Suggested design actions based on the current prediction.</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="recommendation">', unsafe_allow_html=True)
        for item in recommendations:
            st.write(f"- {item}")

        st.markdown(
            f"**Predicted improvement:** +{predicted_improvement:.0f}% stability"
        )
        st.markdown("</div>", unsafe_allow_html=True)

with support_right:
    with st.container(border=True):
        st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-kicker">Estimated contribution of each input to the prediction.</div>',
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


# ============================================================
# Operating Conditions
# ============================================================

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

    st.dataframe(
        operating_df,
        hide_index=True,
        use_container_width=True,
    )


# ============================================================
# Sensitivity Analysis
# ============================================================

st.write("")
with st.container(border=True):
    st.markdown('<div class="section-title">Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-kicker">Perturbs each input and ranks which variable has the strongest effect on stability.</div>',
        unsafe_allow_html=True,
    )

    run_analysis = st.button("Run Sensitivity Analysis", type="primary")

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


# ============================================================
# Technical Reasoning
# ============================================================

st.write("")
with st.container(border=True):
    with st.expander("Technical AI Reasoning"):
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


# ============================================================
# Footer
# ============================================================

st.caption(
    "LunarCap AI uses simplified engineering equations for educational demonstration "
    "and early-stage design screening. Results should be validated with experimental "
    "or mission-specific data before operational use."
)
