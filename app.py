import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="LunarCap AI",
    page_icon="🌙",
    layout="wide"
)

# -----------------------------
# Constants
# -----------------------------
SURFACE_TENSION = 0.072  # N/m (water at room temperature)

# -----------------------------
# Physics Functions
# -----------------------------
def calculate_capillary_pressure(radius_m, contact_angle_deg):
    theta = np.radians(contact_angle_deg)
    pressure = (2 * SURFACE_TENSION * np.cos(theta)) / radius_m
    return pressure

def calculate_stability_score(capillary_pressure, flow_demand):
    return capillary_pressure / flow_demand

def determine_status(score):
    if score > 3000:
        return "🟢 Stable"

    elif score > 1500:
        return "🟡 Marginal"

    else:
        return "🔴 Dry-Out Risk"

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🌙 LunarCap AI")

st.sidebar.write(
    """
    **Capillary Transport Stability Predictor**

    Simulates capillary-driven transport
    inside porous materials for future
    lunar water recycling systems.
    """
)

# -----------------------------
# Main Title
# -----------------------------
st.title("🌙 LunarCap AI")

st.subheader(
    "Physics-Based Capillary Transport Predictor"
)

st.write(
    """
Adjust the engineering parameters below and predict
the stability of capillary transport using the
Young-Laplace equation.
"""
)

# -----------------------------
# User Inputs
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    radius = st.slider(
        "Pore Radius (μm)",
        1,
        100,
        20
    )

    contact_angle = st.slider(
        "Contact Angle (°)",
        0,
        90,
        30
    )

with col2:

    temperature = st.slider(
        "Temperature (°C)",
        20,
        100,
        50
    )

    flow_demand = st.slider(
        "Flow Demand",
        1,
        100,
        50
    )

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Stability"):

    radius_m = radius * 1e-6

    capillary_pressure = calculate_capillary_pressure(
        radius_m,
        contact_angle
    )

    score = calculate_stability_score(
        capillary_pressure,
        flow_demand
    )

    status = determine_status(score)

    st.divider()

    st.header("Results")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Capillary Pressure",
            f"{capillary_pressure:,.1f} Pa"
        )

    with c2:

        st.metric(
            "Stability Score",
            f"{score:,.1f}"
        )

    st.success(f"Prediction: {status}")

    # -----------------------------
    # Graph
    # -----------------------------
    st.subheader("Pressure vs Pore Radius")

    radii = np.linspace(
        1e-6,
        100e-6,
        200
    )

    pressures = (
        2 * SURFACE_TENSION *
        np.cos(np.radians(contact_angle))
    ) / radii

    graph = pd.DataFrame(
        {
            "Radius (μm)": radii * 1e6,
            "Pressure (Pa)": pressures
        }
    )

    st.line_chart(
        graph,
        x="Radius (μm)",
        y="Pressure (Pa)"
    )

    st.subheader("Engineering Interpretation")

    if score > 3000:

        st.info(
            """
The pore radius is sufficiently small to generate
strong capillary pressure.

The liquid transport is expected to remain stable
under the selected operating conditions.
"""
        )

    elif score > 1500:

        st.warning(
            """
The system is operating near its stability limit.

Reducing pore radius or lowering flow demand
would improve transport reliability.
"""
        )

    else:

        st.error(
            """
Capillary pressure is insufficient for the
required flow demand.

The membrane may experience dry-out,
resulting in unstable transport.
"""
        )
