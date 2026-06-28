import math
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


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
        .main {
            background-color: #f7f9fc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .app-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #102033;
            margin-bottom: 0.2rem;
        }

        .app-subtitle {
            font-size: 1rem;
            color: #5f6f82;
            margin-bottom: 1.8rem;
        }

        .result-card {
            background: white;
            border: 1px solid #dfe7f1;
            border-radius: 8px;
            padding: 1.2rem;
            height: 100%;
            box-shadow: 0 1px 4px rgba(16, 32, 51, 0.06);
        }

        .result-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #6b7a90;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .result-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #102033;
        }

        .result-note {
            font-size: 0.88rem;
            color: #65758a;
            margin-top: 0.35rem;
        }

        .section-card {
            background: white;
            border: 1px solid #dfe7f1;
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 1px 4px rgba(16, 32, 51, 0.05);
            margin-bottom: 1rem;
        }

        .status-stable {
            color: #137333;
            font-weight: 800;
        }

        .status-marginal {
            color: #b06000;
            font-weight: 800;
        }

        .status-risk {
            color: #b3261e;
            font-weight: 800;
        }

        .recommendation-box {
            background: #eef6ff;
            border: 1px solid #c9def5;
            border-radius: 8px;
            padding: 1rem;
        }

        .small-muted {
            color: #6b7a90;
            font-size: 0.9rem;
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

    Uses a practical engineering approximation around water behavior.
    The value is clamped to avoid nonphysical results across the wide
    demonstration range from -180 C to +180 C.
    """
    gamma_20c = 0.0728
    slope = -0.000155
    gamma = gamma_20c + slope * (temp_c - 20.0)
    return float(np.clip(gamma, 0.025, 0.105))


def capillary_pressure(radius_m: float, contact_angle_deg: float, gamma: float) -> float:
    """
    Young-Laplace capillary pressure.

    Delta P = 2 * gamma * cos(theta) / r
    """
    theta_rad = math.radians(contact_angle_deg)
    return (2.0 * gamma * math.cos(theta_rad)) / radius_m


def calculate_stability_score(capillary_pressure_pa: float, flow_demand_pa: float) -> float:
    """
    Converts pressure margin into a 0-100 stability score.
    """
    if flow_demand_pa <= 0:
        return 100.0

    pressure_ratio = capillary_pressure_pa / flow_demand_pa

    if pressure_ratio <= 0:
        return 0.0

    score = 100.0 * (1.0 - math.exp(-0.85 * pressure_ratio))
    return float(np.clip(score, 0.0, 100.0))


def calculate_confidence_score(stability_score: float, pressure_ratio: float) -> float:
    """
    Estimates model confidence from prediction strength.
    Very low or very high stability states are easier to classify.
    """
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
        return "Excellent", "*****"
    if stability_score >= 75:
        return "Good", "****"
    if stability_score >= 55:
        return "Marginal", "***"
    return "High Risk", "**"


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
        temp_comment = "Low temperature increases estimated surface tension, which improves capillary pressure in this model."
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
The capillary pressure is calculated using the Young-Laplace equation:

Delta P = 2 * gamma * cos(theta) / r

where gamma is surface tension, theta is contact angle, and r is pore radius.

For this case:

- Surface tension: {gamma:.4f} N/m
- Pore radius: {radius_um:.2f} micrometers
- Contact angle: {contact_angle:.1f} degrees
- Temperature: {temp_c:.1f} C
- Capillary pressure: {cap_pressure:,.0f} Pa
- Flow demand: {flow_demand:,.0f} Pa
- Pressure ratio: {pressure_ratio:.2f}

The stability score is derived from the pressure ratio. A ratio above 1.0 means the
available capillary pressure exceeds the required hydraulic demand. Larger ratios
produce stronger stability predictions.

The most influential variables are pore radius and flow demand because they directly
control the pressure margin. Contact angle affects the cosine term in the Young-Laplace
equation. Temperature affects the prediction indirectly by changing the estimated
surface tension.
"""


def feature_importance(radius_um: float, flow_demand: float, contact_angle: float, temp_c: float) -> pd.DataFrame:
    radius_weight = min(55, 25 + radius_um * 0.35)
    flow_weight = min(45, 18 + flow_demand / 900)
    angle_weight = min(35, 8 + contact_angle * 0.22)
    temp_weight = min(25, 5 + abs(temp_c) * 0.05)

    total = radius_weight + flow_weight + angle_weight + temp_weight

    data = {
        "Feature": ["Radius", "Flow Demand", "Contact Angle", "Temperature"],
        "Importance": [
            radius_weight / total * 100,
            flow_weight / total * 100,
            angle_weight / total * 100,
            temp_weight / total * 100,
        ],
    }

    return pd.DataFrame(data).sort_values("Importance", ascending=False)


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
        recommendations.append("Maintain current operating window")
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

    parameters = {
        "Radius": radius_um,
        "Contact Angle": contact_angle,
        "Flow Demand": flow_demand,
        "Temperature": temp_c,
    }

    for name, value in parameters.items():
        low_value = value * 0.8
        high_value = value * 1.2

        if name == "Temperature":
            low_value = temp_c - 20
            high_value = temp_c + 20

        low_radius = radius_um
        low_angle = contact_angle
        low_demand = flow_demand
        low_temp = temp_c

        high_radius = radius_um
        high_angle = contact_angle
        high_demand = flow_demand
        high_temp = temp_c

        if name == "Radius":
            low_radius = max(low_value, 1)
            high_radius = max(high_value, 1)
        elif name == "Contact Angle":
            low_angle = float(np.clip(low_value, 0, 89))
            high_angle = float(np.clip(high_value, 0, 89))
        elif name == "Flow Demand":
            low_demand = max(low_value, 1)
            high_demand = max(high_value, 1)
        elif name == "Temperature":
            low_temp = float(np.clip(low_value, -180, 180))
            high_temp = float(np.clip(high_value, -180, 180))

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


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("LunarCap AI")
st.sidebar.caption("Capillary transport stability predictor")

st.sidebar.markdown("---")

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

st.sidebar.markdown("---")
st.sidebar.caption("Model: Young-Laplace + engineering stability scoring")


# ============================================================
# Inputs and Calculations
# ============================================================

radius_m = radius_um * 1e-6
gamma = surface_tension_water(temperature_c)
cap_pressure = capillary_pressure(radius_m, contact_angle, gamma)
pressure_ratio = cap_pressure / flow_demand if flow_demand > 0 else 999
stability_score = calculate_stability_score(cap_pressure, flow_demand)
confidence_score = calculate_confidence_score(stability_score, pressure_ratio)
system_status = classify_system(stability_score)
rating_label, rating_stars = health_rating(stability_score)

status_class = "status-stable"
if system_status == "Marginal":
    status_class = "status-marginal"
elif system_status == "High Risk":
    status_class = "status-risk"


# ============================================================
# Header
# ============================================================

st.markdown('<div class="app-title">LunarCap AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">AI-assisted capillary transport stability analysis for lunar water recycling systems.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Result Cards
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Capillary Pressure</div>
            <div class="result-value">{cap_pressure:,.0f} Pa</div>
            <div class="result-note">Young-Laplace prediction</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Stability Score</div>
            <div class="result-value">{stability_score:.0f}/100</div>
            <div class="result-note">Pressure margin based</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Confidence Score</div>
            <div class="result-value">{confidence_score:.0f}%</div>
            <div class="result-note">Classification confidence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">System Status</div>
            <div class="result-value {status_class}">{system_status}</div>
            <div class="result-note">{rating_stars} {rating_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Main Layout
# ============================================================

left_col, right_col = st.columns([1.45, 1.0])


# ============================================================
# Visualization
# ============================================================

with left_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Pressure vs Radius")

    radius_range_um = np.linspace(1, 150, 250)
    pressure_values = [
        capillary_pressure(r * 1e-6, contact_angle, gamma)
        for r in radius_range_um
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(radius_range_um, pressure_values, linewidth=2.5, color="#1f77b4")
    ax.axhline(flow_demand, linestyle="--", linewidth=2, color="#d62728", label="Flow Demand")
    ax.scatter([radius_um], [cap_pressure], color="#102033", s=70, zorder=5, label="Current Design")

    ax.set_title("Capillary Pressure Response to Pore Radius", fontsize=13, weight="bold")
    ax.set_xlabel("Pore Radius (micrometers)")
    ax.set_ylabel("Capillary Pressure (Pa)")
    ax.grid(True, alpha=0.25)
    ax.legend()

    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Feature Importance")

    importance_df = feature_importance(radius_um, flow_demand, contact_angle, temperature_c)

    for _, row in importance_df.iterrows():
        value = row["Importance"]
        st.write(f"**{row['Feature']}**")
        st.progress(value / 100)
        st.caption(f"{value:.0f}% contribution")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Engineering Summary and Recommendations
# ============================================================

with right_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("AI Engineering Summary")

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

    st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Engineering Recommendation")

    recommendations, predicted_improvement = recommendation_engine(
        stability_score,
        radius_um,
        contact_angle,
        flow_demand,
    )

    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)

    for item in recommendations:
        st.write(f"- {item}")

    st.write(f"**Predicted improvement:** +{predicted_improvement:.0f}% stability")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Operating Conditions")

    operating_df = pd.DataFrame(
        {
            "Variable": [
                "Pore Radius",
                "Contact Angle",
                "Flow Demand",
                "Temperature",
                "Surface Tension",
                "Pressure Ratio",
            ],
            "Value": [
                f"{radius_um:.1f} micrometers",
                f"{contact_angle:.1f} degrees",
                f"{flow_demand:,.0f} Pa",
                f"{temperature_c:.1f} C",
                f"{gamma:.4f} N/m",
                f"{pressure_ratio:.2f}",
            ],
        }
    )

    st.dataframe(operating_df, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# AI Explanation
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("Expandable AI Reasoning"):
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
st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Sensitivity Analysis
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Sensitivity Analysis")

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
        use_container_width=True,
        hide_index=True,
    )

    top_parameter = sensitivity_df.iloc[0]["Parameter"]
    top_change = sensitivity_df.iloc[0]["Max Score Change"]

    st.info(
        f"The strongest sensitivity is currently {top_parameter}, "
        f"which can shift the stability score by up to {top_change:.1f} points."
    )
else:
    st.caption("Click the button to perturb each input and rank its effect on stability.")

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Footer
# ============================================================

st.caption(
    "LunarCap AI uses simplified engineering equations for demonstration and early-stage design screening. "
    "Results should be validated with experimental or mission-specific data before operational use."
)
