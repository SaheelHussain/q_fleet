"""
Maritime Hydrodynamic Resistance & Engine Power Modeling
Implements Holtrop-Mennen calm water resistance, Kwon added wave resistance, Fujiwara wind drag,
dynamic trim adjustments, and engine SFOC multi-fuel consumption curves.
"""

import math
from typing import Dict, Any, Tuple
from app.data.vessels_database import get_vessel

# Physical Constants
RHO_SEAWATER = 1025.0    # kg/m3 (seawater density at 15 deg C)
NU_SEAWATER = 1.188e-6   # m2/s (kinematic viscosity)
RHO_AIR = 1.225          # kg/m3 (air density at 15 deg C)
GRAVITY = 9.80665        # m/s2 (gravitational acceleration)
KNOTS_TO_MS = 0.514444   # 1 knot in m/s

# Lower Heating Values (LHV) in MJ/kg for alternative marine fuels
FUEL_LHV_MJ_KG = {
    "VLSFO": 41.20,
    "MGO": 42.70,
    "LNG": 48.00,
    "e_Methanol": 19.90,
    "Green_Ammonia": 18.60,
    "Liquid_H2": 120.00
}

def holtrop_mennen_calm_water_resistance(
    vessel: Dict[str, Any],
    speed_ms: float,
    draft_m: float,
    trim_m: float = 0.0
) -> Tuple[float, Dict[str, float]]:
    """
    Calculates calm water resistance (N) using the Holtrop-Mennen empirical method.
    Returns Total Resistance (N) and component breakdown.
    """
    Lwl = vessel["length_wl"]
    Lpp = vessel["length_pp"]
    B = vessel["beam"]
    T = draft_m
    Cb = vessel["block_coefficient_cb"]
    Cp = vessel["prismatic_coefficient_cp"]
    Cm = vessel["midship_coeff_cm"]
    Cwp = vessel["waterplane_coeff_cwp"]
    S0 = vessel["wetted_surface_s0"]

    # Adjust displacement for draft variation
    draft_ratio = T / vessel["draft_design"]
    displacement_m3 = (vessel["displacement_design"] / 1.025) * (draft_ratio ** 0.88)

    # Adjusted wetted surface area with trim
    S = S0 * (draft_ratio ** 0.65) * (1.0 + 0.015 * abs(trim_m))

    if speed_ms < 0.1:
        return 0.0, {"Rf": 0.0, "Rw": 0.0, "Rb": 0.0, "Rtr": 0.0, "Ra": 0.0, "form_factor": 1.15}

    # Reynolds number & ITTC-1957 Friction Coefficient
    Re = (speed_ms * Lwl) / NU_SEAWATER
    Cf = 0.075 / ((math.log10(Re) - 2.0) ** 2)

    # Frictional Resistance (Rf)
    Rf = 0.5 * RHO_SEAWATER * (speed_ms ** 2) * S * Cf

    # Form Factor (1 + k1)
    lr = Lwl * (1.0 - Cp + (0.06 * Cp * 0.0) / (4.0 * Cp - 1.0)) if (4.0 * Cp - 1.0) != 0 else Lwl * 0.7
    c14 = 1.0 + 0.011 * 0.0 # c14 bulbous bow term

    term1 = 0.93
    term2 = 0.4871 * c14 * ((B / Lwl) ** 1.068) * ((T / Lwl) ** 0.4611) * ((Lwl / max(lr, 10.0)) ** 0.1216)
    term3 = ((Lwl ** 3) / max(displacement_m3, 100.0)) ** 0.365
    term4 = (1.0 - Cp) ** (-0.604)
    form_factor = term1 + term2 * term3 * term4
    form_factor = max(1.10, min(form_factor, 1.45)) # Physical bounds

    # Froude Number & Wave Resistance (Rw)
    Fn = speed_ms / math.sqrt(GRAVITY * Lwl)

    # Empirical wave resistance coefficients
    c1 = 2223105.0 * (max(0.01, c14) ** 3.7861) * ((T / B) ** 1.0796) * ((90.0 - 15.0) ** (-1.3757))
    c2 = 1.0 # Standard hull
    c5 = 1.0 - (0.8 * 0.0) / (B * T * Cm) # Transom effect

    m1 = 0.0140407 * (Lwl / T) - 1.75254 * ((displacement_m3 ** (1.0 / 3.0)) / Lwl) - 4.79323 * (B / Lwl) - 8.0798 * Cp
    m4 = 0.4 * math.exp(-0.034 * (Fn ** (-3.29)))
    d = -0.9
    lambda_param = 1.446 * Cp - 0.03 * (Lwl / B)

    exponent = m1 * (Fn ** d) + m4 * math.cos(lambda_param * (Fn ** (-2.0)))
    exponent = max(-30.0, min(exponent, 5.0)) # Numerical clamp

    Rw = c1 * c2 * c5 * displacement_m3 * RHO_SEAWATER * GRAVITY * math.exp(exponent) * 1e-4
    Rw = max(0.0, Rw)

    # Model-Ship Correlation Allowance (Ra)
    Ca = 0.006 * ((Lwl + 100.0) ** (-0.16)) - 0.00205 + 0.003 * math.sqrt(T / Lwl) * (Cb ** 4) * c2 * (0.04 - 0.0)
    Ca = max(0.0001, Ca)
    Ra = 0.5 * RHO_SEAWATER * (speed_ms ** 2) * S * Ca

    # Additional bulbous bow / transom terms approximation
    Rb = 0.03 * Rw
    Rtr = 0.02 * Rf

    # Total Calm Water Resistance
    R_calm = Rf * form_factor + Rw + Rb + Rtr + Ra

    return R_calm, {
        "Rf": Rf,
        "Rw": Rw,
        "Rb": Rb,
        "Rtr": Rtr,
        "Ra": Ra,
        "form_factor": form_factor
    }

def kwon_added_wave_resistance(
    vessel: Dict[str, Any],
    speed_ms: float,
    draft_m: float,
    hs_m: float,
    tp_s: float,
    relative_wave_angle_deg: float = 0.0
) -> float:
    """
    Calculates added wave resistance (N) in irregular waves using Kwon's empirical formulation.
    hs_m: Significant wave height (m)
    tp_s: Peak wave period (s)
    relative_wave_angle_deg: 0 = Head seas, 90 = Beam seas, 180 = Following seas.
    """
    if hs_m <= 0.05 or speed_ms < 0.1:
        return 0.0

    Lpp = vessel["length_pp"]
    B = vessel["beam"]
    Cb = vessel["block_coefficient_cb"]

    # Directional wave coefficient C_beta
    # Head seas (0 deg) experience max resistance, following seas (180 deg) minimal
    theta_rad = math.radians(abs(relative_wave_angle_deg) % 360)
    c_beta = 0.5 * (1.0 + math.cos(theta_rad)) # 1.0 at 0 deg, 0.5 at 90 deg, 0.0 at 180 deg
    c_beta = max(0.08, c_beta) # Small base resistance even in following swells

    # Non-dimensional wave height and ship parameters
    c_ship = (hs_m / max(Lpp, 50.0)) ** 1.8
    c_speed = 1.0 + 0.8 * (speed_ms / 10.0)
    c_form = (Cb / 0.70) ** 1.5 * (B / 40.0)

    # Added wave resistance in Newtons
    delta_R_wave = 0.5 * RHO_SEAWATER * GRAVITY * (hs_m ** 2) * (B ** 2) / Lpp * c_beta * c_form * c_speed * 1.8

    return delta_R_wave

def aerodynamic_wind_resistance(
    vessel: Dict[str, Any],
    ship_speed_ms: float,
    wind_speed_knots: float,
    relative_wind_angle_deg: float = 0.0
) -> float:
    """
    Calculates aerodynamic wind resistance (N) using Fujiwara / Isherwood coefficients.
    relative_wind_angle_deg: 0 = True headwind, 90 = Crosswind, 180 = Tailwind.
    """
    v_wind_ms = wind_speed_knots * KNOTS_TO_MS
    theta_rad = math.radians(abs(relative_wind_angle_deg) % 360)

    # Apparent relative wind speed (vector sum)
    v_rel_x = ship_speed_ms + v_wind_ms * math.cos(theta_rad)
    v_rel_y = v_wind_ms * math.sin(theta_rad)
    v_apparent_ms = math.sqrt(v_rel_x ** 2 + v_rel_y ** 2)

    apparent_angle_rad = math.atan2(v_rel_y, v_rel_x)

    # Aerodynamic drag coefficient Cx(theta)
    # Headwind Cx ~ 0.85, Tailwind Cx ~ -0.45
    c_x = 0.85 * math.cos(apparent_angle_rad)
    if math.cos(apparent_angle_rad) < 0:
        c_x *= 0.6 # Reduced drag/push in tailwind

    At = vessel["transverse_area_at"]
    R_wind = 0.5 * RHO_AIR * (v_apparent_ms ** 2) * At * c_x

    return R_wind

def calculate_propulsion_and_fuel(
    vessel_id: str,
    speed_knots: float,
    draft_m: float,
    trim_m: float = 0.0,
    hs_m: float = 1.5,
    tp_s: float = 7.0,
    wind_speed_knots: float = 15.0,
    wind_angle_deg: float = 0.0,
    wave_angle_deg: float = 0.0,
    fuel_type: str = "VLSFO"
) -> Dict[str, Any]:
    """
    Computes total hydrodynamic resistance, delivered shaft power, engine load %,
    Specific Fuel Oil Consumption (SFOC), and daily Fuel Oil Consumption (MT/day).
    """
    vessel = get_vessel(vessel_id)
    speed_ms = speed_knots * KNOTS_TO_MS

    # 1. Resistance Components
    R_calm, calm_breakdown = holtrop_mennen_calm_water_resistance(vessel, speed_ms, draft_m, trim_m)
    R_wave = kwon_added_wave_resistance(vessel, speed_ms, draft_m, hs_m, tp_s, wave_angle_deg)
    R_wind = aerodynamic_wind_resistance(vessel, speed_ms, wind_speed_knots, wind_angle_deg)

    R_total = R_calm + R_wave + R_wind
    R_total = max(100.0, R_total)

    # 2. Power and Propulsive Efficiency
    # Effective power PE = R_total * V
    PE_kw = (R_total * speed_ms) / 1000.0

    # Propulsive efficiency eta_D = eta_H * eta_O * eta_R (typically 0.68 - 0.73)
    eta_D = 0.705
    # Shaft transmission efficiency eta_S (typically 0.985)
    eta_S = 0.985

    # Delivered Brake/Shaft Power (kW)
    power_kw = PE_kw / (eta_D * eta_S)

    # Clamp to vessel MCR power with sea margin allowance
    mcr = vessel["mcr_power_kw"]
    engine_load_pct = (power_kw / mcr) * 100.0
    power_kw_clamped = min(power_kw, mcr * 1.05)

    # 3. Non-Linear SFOC Bathtub Load Curve (g/kWh)
    # Optimum SFOC is around 70-85% MCR load; increases at very low (<30%) and high (>95%) loads
    load_ratio = max(0.15, min(engine_load_pct / 100.0, 1.10))
    sfoc_base = vessel["sfoc_base_g_per_kwh"]

    # Quadratic SFOC multiplier curve
    sfoc_multiplier = 0.94 + 0.12 * ((load_ratio - 0.75) ** 2) + (0.05 / (load_ratio ** 1.5))
    sfoc_vlsfo_equivalent = sfoc_base * sfoc_multiplier

    # 4. Alternative Fuel Adjustment based on Lower Heating Value (LHV)
    # Mass of fuel required = Energy required / LHV
    lhv_vlsfo = FUEL_LHV_MJ_KG["VLSFO"]
    lhv_target = FUEL_LHV_MJ_KG.get(fuel_type, lhv_vlsfo)

    actual_sfoc = sfoc_vlsfo_equivalent * (lhv_vlsfo / lhv_target)

    # 5. Daily Fuel Consumption (Metric Tons / Day)
    # Main Engine FOC = (Power kW * SFOC g/kWh * 24 h) / 1,000,000 g/MT
    main_engine_foc_mt_day = (power_kw_clamped * actual_sfoc * 24.0) / 1e6

    # Auxiliary Engine FOC
    aux_power_kw = vessel["aux_power_kw"]
    aux_sfoc = vessel["aux_sfoc_g_per_kwh"] * (lhv_vlsfo / lhv_target)
    aux_engine_foc_mt_day = (aux_power_kw * aux_sfoc * 24.0) / 1e6

    total_foc_mt_day = main_engine_foc_mt_day + aux_engine_foc_mt_day

    # Fuel Consumption per Nautical Mile (MT / nm)
    foc_per_nm = total_foc_mt_day / (speed_knots * 24.0) if speed_knots > 0 else 0.0

    return {
        "vessel_id": vessel_id,
        "speed_knots": speed_knots,
        "draft_m": draft_m,
        "fuel_type": fuel_type,
        "resistance_total_kn": R_total / 1000.0,
        "resistance_calm_kn": R_calm / 1000.0,
        "resistance_wave_kn": R_wave / 1000.0,
        "resistance_wind_kn": R_wind / 1000.0,
        "power_kw": round(power_kw_clamped, 2),
        "engine_load_pct": round(engine_load_pct, 2),
        "sfoc_g_kwh": round(actual_sfoc, 2),
        "main_foc_mt_day": round(main_engine_foc_mt_day, 3),
        "aux_foc_mt_day": round(aux_engine_foc_mt_day, 3),
        "total_foc_mt_day": round(total_foc_mt_day, 3),
        "foc_per_nm": round(foc_per_nm, 5)
    }
