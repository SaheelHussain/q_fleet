"""
Maritime Telemetry Generator & Benchmark Dataset Suite
Generates high-fidelity, physics-calibrated voyage telemetry data for ML model training and validation.
"""

import random
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from app.data.vessels_database import VESSEL_CLASSES
from app.core.hydrodynamics import calculate_propulsion_and_fuel

def generate_voyage_telemetry(num_samples: int = 2500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates realistic voyage telemetry representing diverse operating conditions across all vessel classes.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    records: List[Dict[str, Any]] = []
    vessel_ids = list(VESSEL_CLASSES.keys())
    fuels = ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"]

    for i in range(num_samples):
        v_id = random.choice(vessel_ids)
        vessel = VESSEL_CLASSES[v_id]

        # Speed sampled around operational envelope
        speed_min = vessel["speed_min_knots"]
        speed_max = vessel["speed_max_knots"]
        speed_knots = float(np.random.uniform(speed_min, speed_max))

        # Draft between 70% ballast and 100% scantling
        draft_min = vessel["draft_design"] * 0.75
        draft_max = vessel["draft_scantling"]
        draft_m = float(np.random.uniform(draft_min, draft_max))

        # Trim between -1.5m (bow trim) and +2.5m (aft trim)
        trim_m = float(np.random.uniform(-0.8, 1.8))

        # Weather sea state (Weibull / Rayleigh distributed wave heights)
        hs_m = float(np.random.weibull(1.8) * 1.6)
        hs_m = max(0.2, min(hs_m, 8.5)) # Cap between calm and storm

        tp_s = float(4.5 + 1.8 * np.sqrt(hs_m) + np.random.normal(0, 0.5))
        tp_s = max(3.5, min(tp_s, 15.0))

        wind_speed_knots = float(hs_m * 6.5 + np.random.normal(0, 3.0))
        wind_speed_knots = max(0.0, min(wind_speed_knots, 55.0))

        wind_angle_deg = float(np.random.uniform(0, 360))
        wave_angle_deg = float((wind_angle_deg + np.random.normal(0, 15.0)) % 360)

        fuel_type = random.choice(vessel["supported_fuels"])

        # Compute physics ground truth
        calc = calculate_propulsion_and_fuel(
            vessel_id=v_id,
            speed_knots=speed_knots,
            draft_m=draft_m,
            trim_m=trim_m,
            hs_m=hs_m,
            tp_s=tp_s,
            wind_speed_knots=wind_speed_knots,
            wind_angle_deg=wind_angle_deg,
            wave_angle_deg=wave_angle_deg,
            fuel_type=fuel_type
        )

        # Add realistic sensor noise (0.8% - 1.8%)
        noise_factor = float(np.random.normal(1.0, 0.012))
        noisy_foc = calc["total_foc_mt_day"] * noise_factor

        records.append({
            "sample_id": i + 1,
            "vessel_id": v_id,
            "vessel_type": vessel["type"],
            "dwt": vessel["dwt"],
            "speed_knots": round(speed_knots, 2),
            "draft_m": round(draft_m, 2),
            "trim_m": round(trim_m, 2),
            "hs_m": round(hs_m, 2),
            "tp_s": round(tp_s, 2),
            "wind_speed_knots": round(wind_speed_knots, 2),
            "wind_angle_deg": round(wind_angle_deg, 1),
            "wave_angle_deg": round(wave_angle_deg, 1),
            "fuel_type": fuel_type,
            "power_kw": round(calc["power_kw"], 1),
            "engine_load_pct": round(calc["engine_load_pct"], 1),
            "resistance_total_kn": round(calc["resistance_total_kn"], 2),
            "sfoc_g_kwh": round(calc["sfoc_g_kwh"], 1),
            "foc_mt_day": round(noisy_foc, 3),
            "foc_ground_truth_mt_day": round(calc["total_foc_mt_day"], 3)
        })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_voyage_telemetry(100)
    print(f"Generated {len(df)} telemetry rows. Head:")
    print(df.head(3))
