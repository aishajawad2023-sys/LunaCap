# 🌙 LunarCap AI

AI-assisted capillary transport stability analysis for lunar water recycling systems.

LunarCap AI is an interactive engineering dashboard that predicts whether capillary-driven transport through porous media is likely to be stable, marginal, or high risk under different operating conditions.

The app uses simplified physics-based calculations, dynamic surface tension estimates, AI-style engineering reasoning, feature importance, and sensitivity analysis to support early-stage design exploration.

## Overview

Future lunar water recycling systems may rely on porous materials and capillary-driven flow to transport fluids in low-gravity environments.

LunarCap AI provides a simple, visual way to explore how key design variables affect capillary transport performance:

- Pore radius
- Contact angle
- Flow demand
- Temperature

The goal is to make capillary transport behavior easier to understand, compare, and explain.

## Features

- Young-Laplace capillary pressure calculation
- Temperature-dependent surface tension estimate
- Interactive engineering inputs
- Stability score prediction
- Confidence score estimate
- System status classification
- Engineering health rating
- AI-style engineering summary
- Expandable technical reasoning
- Feature importance visualization
- Native Streamlit pressure vs radius chart
- Engineering recommendations
- Sensitivity analysis

## Inputs

Users can adjust the following variables from the sidebar:

| Input | Description |
|---|---|
| Pore Radius | Radius of the porous transport pathway |
| Contact Angle | Wettability of the material surface |
| Flow Demand | Required hydraulic pressure demand |
| Temperature | Operating temperature environment |

The temperature range supports:

```text
-180 C to +180 C
