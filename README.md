# Q-Fleet (AuraQuanta) — Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization

**Problem Statement ID:** 26138 (Egreen Quanta)  
**Theme:** Clean & Green Technology / Maritime Logistics & Decarbonization  

---

## 🌊 Overview & Core Capabilities

**Q-Fleet (AuraQuanta)** is an enterprise-grade maritime decarbonization platform that merges **Quantum-Inspired Metaheuristics (QPSO & QGA)** with **Physics-Informed Quantum Neural Networks (Q-PINN)** and **Naval Architecture Hydrodynamics (Holtrop-Mennen & Kwon)** to optimize oceanic vessel speed profiling, fuel selection, and fleet-wide deployment.

### Key Innovations:
1. **Q-PINN Dynamic Fuel Predictor**: Combines Holtrop-Mennen calm water resistance, Kwon irregular wave added resistance, and Fujiwara wind drag with Pauli-Z/ZZ quantum feature Hilbert space embedding.
2. **Quantum Particle Swarm Optimization (QPSO)**: Continuous multi-segment route optimization using delta-potential well wavefunctions and mean-best (mbest) quantum tunneling to escape local minima.
3. **Quantum Genetic Algorithm (QGA)**: Discrete combinatorial fleet deployment using Qubit chromosomes ($\alpha, \beta$ amplitudes) updated via Quantum Rotation Gates and NOT-gate mutations.
4. **Well-to-Wake (WtW) Alternative Fuel LCA**: Comprehensive carbon accounting for 6 marine fuels (VLSFO, MGO, LNG, e-Methanol, Green Ammonia, Liquid $H_2$) factoring in methane and $N_2O$ slip.
5. **IMO CII & EU ETS Compliance Engine**: Official MEPC.337(76) Carbon Intensity Indicator (A-E rating) and European Emissions Trading System (EU ETS) tax calculator.
6. **Port Cold-Ironing (Shore Power) Configurator**: Analyzes auxiliary generator diesel fuel offset by zero-emission port grid power.
7. **Classical vs Quantum Benchmarking Arena**: Real-time head-to-head empirical races comparing QPSO/QGA against Classical PSO, Classical GA, and Random Forest regressors.

---

## 🏗️ Architecture & Project Structure

```text
q-fleet/
├── backend/
│   ├── app/
│   │   ├── main.py                       # FastAPI entrypoint (Port 8000)
│   │   ├── core/
│   │   │   ├── hydrodynamics.py          # Holtrop-Mennen & Kwon resistance engine
│   │   │   ├── q_pinn_predictor.py       # Quantum Physics-Informed ML predictor
│   │   │   ├── qpso_optimizer.py         # Quantum Particle Swarm with Delta Potential
│   │   │   ├── qga_optimizer.py          # Quantum Genetic Algorithm with Qubit gates
│   │   │   ├── green_fuels_lca.py        # Well-to-Wake LCA profiles & Cold-Ironing
│   │   │   ├── cii_calculator.py         # IMO CII (A-E) & EU ETS tax calculator
│   │   │   ├── classical_baselines.py    # Classical PSO, GA, and ML baselines
│   │   │   └── benchmark_engine.py       # Head-to-head empirical benchmark suite
│   │   ├── data/
│   │   │   ├── vessels_database.py       # 6 realistic vessel classes & specifications
│   │   │   ├── routes_waypoints.py       # 5 global maritime trade corridors & waypoints
│   │   │   └── synthetic_telemetry.py    # Physics-calibrated voyage telemetry generator
│   │   ├── schemas/
│   │   │   └── api_models.py             # Pydantic request/response data models
│   │   └── api/
│   │       └── routes.py                 # REST API endpoints
│   ├── test_suite.py                     # Comprehensive 7-test backend validation suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                       # Master dashboard & tab navigator
│   │   ├── components/
│   │   │   ├── Navbar.jsx                # Navigation & live quantum engine status
│   │   │   ├── QuantumOptimizationLab.jsx# QPSO speed/trim profiling & Pareto frontier
│   │   │   ├── QuantumVisualizer.jsx     # Bloch Sphere & Delta Potential Well animations
│   │   │   ├── GlobalVoyageMap.jsx       # Interactive Oceanic Digital Twin with MetOcean data
│   │   │   ├── FuelPredictionStudio.jsx  # Q-PINN live resistance & FOC estimator
│   │   │   ├── GreenFleetStudio.jsx      # Alternative fuels & Shore Power cold-ironing
│   │   │   ├── BenchmarkArena.jsx        # Head-to-head Quantum vs Classical race
│   │   │   └── CIISustainabilityReport.jsx# IMO CII A-E rating & EU ETS tax exposure
│   │   └── services/
│   │       └── api.js                    # REST API client
│   └── package.json
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup & Startup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 2. Frontend Setup & Startup
```bash
cd frontend
npm install
npm run dev
```
- Interactive Dashboard: [http://localhost:5173](http://localhost:5173)

### 3. Deploy to Vercel
The frontend is configured for Vercel deployment from the repository root using [vercel.json](vercel.json). Import this GitHub repository into Vercel and keep the Vercel project root set to the repository root.

#### Deploy the FastAPI backend to Render
The root [render.yaml](render.yaml) defines the FastAPI web service. In Render, create a new Blueprint and select this GitHub repository. Render will build the backend from `backend/`, start Uvicorn on Render's assigned port, and use `/api/health` for its health check. The blueprint also allows the current Vercel deployment origin through CORS.

After Render finishes deploying, copy the service's public URL (for example, `https://q-fleet-api.onrender.com`) and set this Vercel environment variable:

```text
VITE_API_BASE_URL=https://your-render-service.onrender.com/api
```

Redeploy the Vercel project after adding the variable. If you use another Vercel domain, update `FRONTEND_ORIGINS` in Render to that exact site origin. For multiple frontend domains, separate origins with commas. The local backend defaults to `http://localhost:5173`.

The Render free service may take a short time to wake after inactivity; retry the connection from the dashboard if it reports the backend as unavailable.

### 4. Run Backend Validation Test Suite
```bash
cd backend
python test_suite.py
```

---

## 📊 Mathematical Modeling Reference

### Hydrodynamic Total Resistance
$$R_{\text{total}} = R_{\text{calm}} (v, \Delta, T, C_b) + \Delta R_{\text{wave}} (H_s, T_p, v, \theta_{\text{wave}}) + R_{\text{wind}} (V_{\text{wind}}, \theta_{\text{wind}}, A_{\text{trans}})$$

### QPSO Delta-Potential Well Position Update
$$X_i(t+1) = p_i(t) \pm \alpha(t) \cdot |mbest(t) - X_i(t)| \cdot \ln(1/u), \quad u \sim U(0, 1)$$

### QGA Qubit Rotation Gate
$$\begin{bmatrix} \alpha_j' \\ \beta_j' \end{bmatrix} = \begin{bmatrix} \cos(\Delta \theta_j) & -\sin(\Delta \theta_j) \\ \sin(\Delta \theta_j) & \cos(\Delta \theta_j) \end{bmatrix} \begin{bmatrix} \alpha_j \\ \beta_j \end{bmatrix}$$
