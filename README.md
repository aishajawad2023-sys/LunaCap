# 🌙 LunarCap AI
The app uses simplified physics-based calculations and rule-based engineering reasoning to estimate whether a capillary transport design is stable, marginal, or high risk under different operating conditions.

## Overview

Lunar water recycling systems may rely on porous media and capillary-driven transport to move fluids in low-gravity environments. This application provides an interactive way to explore how pore radius, contact angle, flow demand, and temperature influence capillary pressure and transport stability.

The model is designed as an educational and early-stage engineering demonstration, not as a certified mission simulation.

## Features

- Young-Laplace capillary pressure calculation
- Temperature-dependent surface tension estimate
- Interactive engineering inputs
- Stability score prediction
- Confidence score estimate
- System status classification
- Engineering health rating
- AI-style engineering summary
- Expandable reasoning explanation
- Feature importance visualization
- Pressure vs radius plot
- Engineering recommendations
- Sensitivity analysis

## Inputs

The user can adjust:

- Pore radius
- Contact angle
- Flow demand
- Temperature

The temperature range supports values from:

```text
-180 C to +180 C
Outputs
The application displays:
Capillary Pressure
Stability Score
Confidence Score
System Status
Engineering Health Rating
AI Engineering Summary
Feature Importance
Engineering Recommendations
Sensitivity Analysis Results
Physics Model
The core calculation is based on the Young-Laplace equation:
Delta P = 2 * gamma * cos(theta) / r
Where:
Delta P is capillary pressure
gamma is surface tension
theta is contact angle
r is pore radius
Smaller pore radius generally increases capillary pressure. Lower contact angle improves wettability and increases the capillary driving force. Higher flow demand makes the system harder to stabilize.
AI-Style Reasoning
The app includes an AI-style engineering summary and expandable reasoning section. These explanations are generated locally using Python logic based on the calculated results.
This version does not require an OpenAI API key.
Sensitivity Analysis
The sensitivity analysis feature perturbs each major input and estimates which variable has the strongest influence on the stability score. This helps identify which design parameter should be improved first.
Tech Stack
Python
Streamlit
NumPy
Pandas
Matplotlib
