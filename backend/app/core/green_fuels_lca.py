"""
Green Alternative Fuels Life-Cycle Assessment (LCA) & Shore Power / Cold-Ironing Engine
Computes Well-to-Wake (WtW), Well-to-Tank (WtT), and Tank-to-Wake (TtW) lifecycle emissions,
including methane slip, N2O emissions, and port shore-power grid offsets.
"""

from typing import Dict, Any

# Lifecycle Greenhouse Gas Emission Factors (IMO MEPC & European Renewable Energy Directive RED II)
# All emission factors in gCO2e / MJ of fuel energy unless specified
FUEL_LCA_PROFILES: Dict[str, Dict[str, Any]] = {
    "VLSFO": {
        "name": "Very Low Sulphur Fuel Oil (0.5% S)",
        "lhv_mj_kg": 41.20,
        "density_kg_m3": 890.0,
        "price_usd_per_mt": 620.0,
        "wtt_gco2e_per_mj": 13.5,       # Extraction & refining
        "ttw_co2_factor_g_per_g": 3.151, # Direct combustion: 3.151 g CO2 / g fuel
        "ttw_gco2e_per_mj": 76.5,
        "methane_slip_pct": 0.0,
        "n2o_slip_g_per_kg": 0.08,
        "total_wtw_gco2e_per_mj": 90.0,
        "carbon_intensity_rating": "Fossil High"
    },
    "MGO": {
        "name": "Marine Gas Oil (0.1% S)",
        "lhv_mj_kg": 42.70,
        "density_kg_m3": 845.0,
        "price_usd_per_mt": 780.0,
        "wtt_gco2e_per_mj": 14.4,
        "ttw_co2_factor_g_per_g": 3.206,
        "ttw_gco2e_per_mj": 75.1,
        "methane_slip_pct": 0.0,
        "n2o_slip_g_per_kg": 0.08,
        "total_wtw_gco2e_per_mj": 89.5,
        "carbon_intensity_rating": "Fossil Distillate"
    },
    "LNG": {
        "name": "Liquefied Natural Gas (Dual-Fuel)",
        "lhv_mj_kg": 48.00,
        "density_kg_m3": 450.0,
        "price_usd_per_mt": 710.0,
        "wtt_gco2e_per_mj": 18.5,       # Liquefaction & transport
        "ttw_co2_factor_g_per_g": 2.750,
        "ttw_gco2e_per_mj": 57.3,
        "methane_slip_pct": 2.2,        # Unburned CH4 slip in Otto-cycle (GWP100 = 28)
        "n2o_slip_g_per_kg": 0.05,
        "total_wtw_gco2e_per_mj": 78.4, # Includes methane slip penalty
        "carbon_intensity_rating": "Transitional Low-Carbon"
    },
    "e_Methanol": {
        "name": "Green e-Methanol (Power-to-X / Biogenic CO2)",
        "lhv_mj_kg": 19.90,
        "density_kg_m3": 792.0,
        "price_usd_per_mt": 950.0,
        "wtt_gco2e_per_mj": -65.0,      # Net negative from direct air capture / biogenic CO2 credit
        "ttw_co2_factor_g_per_g": 1.375,
        "ttw_gco2e_per_mj": 69.1,
        "methane_slip_pct": 0.0,
        "n2o_slip_g_per_kg": 0.02,
        "total_wtw_gco2e_per_mj": 15.2, # Near zero net lifecycle
        "carbon_intensity_rating": "Ultra-Low Carbon"
    },
    "Green_Ammonia": {
        "name": "Green Ammonia (Zero-Carbon NH3)",
        "lhv_mj_kg": 18.60,
        "density_kg_m3": 682.0,
        "price_usd_per_mt": 880.0,
        "wtt_gco2e_per_mj": 8.0,        # Renewable electrolysis + Haber-Bosch
        "ttw_co2_factor_g_per_g": 0.000, # Zero direct CO2 combustion
        "ttw_gco2e_per_mj": 4.8,        # Small N2O slip factor (GWP100 = 265)
        "methane_slip_pct": 0.0,
        "n2o_slip_g_per_kg": 0.45,
        "total_wtw_gco2e_per_mj": 12.8,
        "carbon_intensity_rating": "Zero Direct Carbon"
    },
    "Liquid_H2": {
        "name": "Liquid Green Hydrogen (LH2 Fuel Cell / ICE)",
        "lhv_mj_kg": 120.00,
        "density_kg_m3": 71.0,
        "price_usd_per_mt": 3600.0,
        "wtt_gco2e_per_mj": 11.5,       # Electrolysis & cryogenic liquefaction
        "ttw_co2_factor_g_per_g": 0.000, # Zero emissions (water vapor only)
        "ttw_gco2e_per_mj": 0.0,
        "methane_slip_pct": 0.0,
        "n2o_slip_g_per_kg": 0.00,
        "total_wtw_gco2e_per_mj": 11.5,
        "carbon_intensity_rating": "True Zero Emission"
    }
}

def calculate_voyage_emissions_and_cost(
    fuel_type: str,
    fuel_mass_mt: float,
    pilot_fuel_mass_mt: float = 0.0,
    pilot_fuel_type: str = "MGO"
) -> Dict[str, Any]:
    """
    Computes total Tank-to-Wake (TtW), Well-to-Tank (WtT), Well-to-Wake (WtW) emissions in Metric Tons CO2e,
    along with total fuel bunkering cost (USD).
    """
    profile = FUEL_LCA_PROFILES.get(fuel_type, FUEL_LCA_PROFILES["VLSFO"])
    lhv = profile["lhv_mj_kg"]

    # Energy in MJ: Fuel mass MT * 1,000 kg/MT * LHV MJ/kg
    energy_mj = fuel_mass_mt * 1000.0 * lhv

    # Well-to-Tank emissions (MT CO2e)
    wtt_emissions_mt = (energy_mj * profile["wtt_gco2e_per_mj"]) / 1e6

    # Tank-to-Wake emissions (MT CO2e)
    # Direct CO2 + Methane Slip + N2O Slip
    direct_co2_mt = fuel_mass_mt * profile["ttw_co2_factor_g_per_g"]

    # Methane slip impact (GWP-100 = 28)
    methane_slip_mt = fuel_mass_mt * (profile["methane_slip_pct"] / 100.0)
    methane_co2e_mt = methane_slip_mt * 28.0

    # N2O slip impact (GWP-100 = 265)
    n2o_slip_kg = fuel_mass_mt * 1000.0 * (profile["n2o_slip_g_per_kg"] / 1000.0)
    n2o_co2e_mt = (n2o_slip_kg * 265.0) / 1000.0

    ttw_emissions_mt = direct_co2_mt + methane_co2e_mt + n2o_co2e_mt

    # Total Well-to-Wake emissions (MT CO2e)
    wtw_emissions_mt = wtt_emissions_mt + ttw_emissions_mt

    # Fuel Cost (USD)
    fuel_cost_usd = fuel_mass_mt * profile["price_usd_per_mt"]

    # Add Pilot Fuel if dual-fuel (e.g., 2-5% MGO pilot for LNG/Ammonia)
    if pilot_fuel_mass_mt > 0.0:
        pilot_profile = FUEL_LCA_PROFILES.get(pilot_fuel_type, FUEL_LCA_PROFILES["MGO"])
        pilot_energy_mj = pilot_fuel_mass_mt * 1000.0 * pilot_profile["lhv_mj_kg"]
        wtt_emissions_mt += (pilot_energy_mj * pilot_profile["wtt_gco2e_per_mj"]) / 1e6
        ttw_emissions_mt += pilot_fuel_mass_mt * pilot_profile["ttw_co2_factor_g_per_g"]
        wtw_emissions_mt = wtt_emissions_mt + ttw_emissions_mt
        fuel_cost_usd += pilot_fuel_mass_mt * pilot_profile["price_usd_per_mt"]

    return {
        "fuel_type": fuel_type,
        "fuel_mass_mt": round(fuel_mass_mt, 3),
        "total_energy_gj": round(energy_mj / 1000.0, 2),
        "direct_co2_mt": round(direct_co2_mt, 3),
        "methane_slip_mt_co2e": round(methane_co2e_mt, 3),
        "n2o_slip_mt_co2e": round(n2o_co2e_mt, 3),
        "ttw_emissions_mt_co2e": round(ttw_emissions_mt, 3),
        "wtt_emissions_mt_co2e": round(wtt_emissions_mt, 3),
        "wtw_emissions_mt_co2e": round(wtw_emissions_mt, 3),
        "fuel_cost_usd": round(fuel_cost_usd, 2),
        "carbon_intensity_rating": profile["carbon_intensity_rating"]
    }

def calculate_cold_ironing_benefit(
    aux_power_kw: float,
    berth_hours: float,
    grid_emission_factor_kg_kwh: float = 0.35,
    electricity_price_usd_per_kwh: float = 0.16
) -> Dict[str, Any]:
    """
    Calculates environmental and financial benefits of port Shore-Power (Cold-Ironing) during vessel berthing.
    """
    total_energy_kwh = aux_power_kw * berth_hours

    # Standard auxiliary diesel generator baseline (MGO @ 200 g/kWh)
    baseline_mgo_consumed_mt = (aux_power_kw * 200.0 * berth_hours) / 1e6
    baseline_ttw_co2_mt = baseline_mgo_consumed_mt * 3.206
    baseline_wtw_co2e_mt = baseline_mgo_consumed_mt * (42.70 * 89.5 / 1000.0) # ~3.82 MT CO2e / MT MGO
    baseline_mgo_cost_usd = baseline_mgo_consumed_mt * 780.0

    # Shore Power Grid
    shore_emissions_mt_co2e = (total_energy_kwh * grid_emission_factor_kg_kwh) / 1000.0
    shore_electricity_cost_usd = total_energy_kwh * electricity_price_usd_per_kwh

    # Savings
    net_co2e_saved_mt = max(0.0, baseline_wtw_co2e_mt - shore_emissions_mt_co2e)
    co2e_reduction_pct = (net_co2e_saved_mt / baseline_wtw_co2e_mt) * 100.0 if baseline_wtw_co2e_mt > 0 else 0.0
    cost_diff_usd = shore_electricity_cost_usd - baseline_mgo_cost_usd

    return {
        "berth_hours": berth_hours,
        "energy_consumed_mwh": round(total_energy_kwh / 1000.0, 2),
        "diesel_saved_mt": round(baseline_mgo_consumed_mt, 3),
        "baseline_co2e_mt": round(baseline_wtw_co2e_mt, 3),
        "shore_grid_co2e_mt": round(shore_emissions_mt_co2e, 3),
        "net_co2e_saved_mt": round(net_co2e_saved_mt, 3),
        "co2e_reduction_pct": round(co2e_reduction_pct, 1),
        "baseline_cost_usd": round(baseline_mgo_cost_usd, 2),
        "shore_cost_usd": round(shore_electricity_cost_usd, 2),
        "net_cost_saving_usd": round(-cost_diff_usd, 2)
    }
