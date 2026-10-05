"""
Standardized Maritime Vessel Classes Catalog
Detailed naval architectural parameters, dimensions, engine capacities, and hydrodynamic coefficients.
"""

from typing import Dict, Any

VESSEL_CLASSES: Dict[str, Dict[str, Any]] = {
    "container_15000_teu": {
        "id": "container_15000_teu",
        "name": "Ultra Large Container Vessel (15,000 TEU)",
        "type": "Container",
        "dwt": 150000.0,
        "teu_capacity": 15000,
        "length_pp": 366.0,          # m
        "length_wl": 375.0,          # m
        "beam": 51.2,                # m
        "draft_design": 14.5,        # m
        "draft_scantling": 16.0,     # m
        "displacement_design": 165000.0, # metric tons
        "block_coefficient_cb": 0.65,
        "prismatic_coefficient_cp": 0.67,
        "midship_coeff_cm": 0.97,
        "waterplane_coeff_cwp": 0.78,
        "transverse_area_at": 980.0, # m2 (frontal windage area)
        "wetted_surface_s0": 26500.0, # m2
        "mcr_power_kw": 68000.0,     # 2-stroke slow-speed diesel
        "rpm_design": 84.0,
        "speed_design_knots": 22.0,
        "speed_min_knots": 10.0,
        "speed_max_knots": 24.5,
        "sfoc_base_g_per_kwh": 165.0, # g/kWh for VLSFO
        "aux_power_kw": 3500.0,      # for reefer load & hoteling
        "aux_sfoc_g_per_kwh": 195.0,
        "imo_cii_category": "container",
        "cii_ref_a": 1984.0,
        "cii_ref_c": 0.489,
        "supported_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 24000000,
            "e_Methanol": 14000000,
            "Green_Ammonia": 19000000,
            "Liquid_H2": 32000000
        },
        "shore_power_equipped": True
    },
    "capesize_bulker_180k": {
        "id": "capesize_bulker_180k",
        "name": "Capesize Bulk Carrier (180,000 DWT)",
        "type": "Bulk Carrier",
        "dwt": 180000.0,
        "teu_capacity": 0,
        "length_pp": 285.0,
        "length_wl": 292.0,
        "beam": 45.0,
        "draft_design": 16.5,
        "draft_scantling": 18.2,
        "displacement_design": 205000.0,
        "block_coefficient_cb": 0.84,
        "prismatic_coefficient_cp": 0.85,
        "midship_coeff_cm": 0.99,
        "waterplane_coeff_cwp": 0.90,
        "transverse_area_at": 520.0,
        "wetted_surface_s0": 21500.0,
        "mcr_power_kw": 18500.0,
        "rpm_design": 72.0,
        "speed_design_knots": 14.5,
        "speed_min_knots": 8.5,
        "speed_max_knots": 16.0,
        "sfoc_base_g_per_kwh": 158.0,
        "aux_power_kw": 850.0,
        "aux_sfoc_g_per_kwh": 190.0,
        "imo_cii_category": "bulk_carrier",
        "cii_ref_a": 4745.0,
        "cii_ref_c": 0.401,
        "supported_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 15000000,
            "e_Methanol": 9500000,
            "Green_Ammonia": 12500000,
            "Liquid_H2": 21000000
        },
        "shore_power_equipped": False
    },
    "aframax_tanker_115k": {
        "id": "aframax_tanker_115k",
        "name": "Aframax Crude Oil Tanker (115,000 DWT)",
        "type": "Tanker",
        "dwt": 115000.0,
        "teu_capacity": 0,
        "length_pp": 245.0,
        "length_wl": 250.0,
        "beam": 42.0,
        "draft_design": 13.5,
        "draft_scantling": 15.0,
        "displacement_design": 132000.0,
        "block_coefficient_cb": 0.82,
        "prismatic_coefficient_cp": 0.83,
        "midship_coeff_cm": 0.985,
        "waterplane_coeff_cwp": 0.88,
        "transverse_area_at": 460.0,
        "wetted_surface_s0": 17200.0,
        "mcr_power_kw": 14000.0,
        "rpm_design": 78.0,
        "speed_design_knots": 14.2,
        "speed_min_knots": 8.0,
        "speed_max_knots": 15.5,
        "sfoc_base_g_per_kwh": 162.0,
        "aux_power_kw": 1100.0,
        "aux_sfoc_g_per_kwh": 192.0,
        "imo_cii_category": "tanker",
        "cii_ref_a": 5247.0,
        "cii_ref_c": 0.410,
        "supported_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 13500000,
            "e_Methanol": 8500000,
            "Green_Ammonia": 11000000,
            "Liquid_H2": 18500000
        },
        "shore_power_equipped": True
    },
    "lng_carrier_174k": {
        "id": "lng_carrier_174k",
        "name": "LNG Carrier (174,000 m³ Q-Flex)",
        "type": "Gas Carrier",
        "dwt": 95000.0,
        "teu_capacity": 0,
        "length_pp": 290.0,
        "length_wl": 299.0,
        "beam": 45.8,
        "draft_design": 11.5,
        "draft_scantling": 12.5,
        "displacement_design": 118000.0,
        "block_coefficient_cb": 0.74,
        "prismatic_coefficient_cp": 0.76,
        "midship_coeff_cm": 0.98,
        "waterplane_coeff_cwp": 0.82,
        "transverse_area_at": 810.0,
        "wetted_surface_s0": 19400.0,
        "mcr_power_kw": 25000.0,
        "rpm_design": 82.0,
        "speed_design_knots": 19.5,
        "speed_min_knots": 10.0,
        "speed_max_knots": 21.0,
        "sfoc_base_g_per_kwh": 150.0, # High efficiency dual-fuel gas
        "aux_power_kw": 2800.0,
        "aux_sfoc_g_per_kwh": 180.0,
        "imo_cii_category": "gas_carrier",
        "cii_ref_a": 8120.0,
        "cii_ref_c": 0.456,
        "supported_fuels": ["LNG", "MGO", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 0, # Native LNG
            "e_Methanol": 11000000,
            "Green_Ammonia": 14000000,
            "Liquid_H2": 26000000
        },
        "shore_power_equipped": True
    },
    "roro_car_carrier_25k": {
        "id": "roro_car_carrier_25k",
        "name": "Pure Car & Truck Carrier / Ro-Ro (7,000 CEU)",
        "type": "Ro-Ro Cargo",
        "dwt": 25000.0,
        "teu_capacity": 0,
        "length_pp": 210.0,
        "length_wl": 218.0,
        "beam": 32.2,
        "draft_design": 7.8,
        "draft_scantling": 8.8,
        "displacement_design": 38000.0,
        "block_coefficient_cb": 0.58,
        "prismatic_coefficient_cp": 0.61,
        "midship_coeff_cm": 0.95,
        "waterplane_coeff_cwp": 0.72,
        "transverse_area_at": 1100.0, # High aerodynamic box profile
        "wetted_surface_s0": 9800.0,
        "mcr_power_kw": 21000.0,
        "rpm_design": 96.0,
        "speed_design_knots": 20.0,
        "speed_min_knots": 10.0,
        "speed_max_knots": 22.0,
        "sfoc_base_g_per_kwh": 168.0,
        "aux_power_kw": 1800.0,
        "aux_sfoc_g_per_kwh": 198.0,
        "imo_cii_category": "ro_ro_cargo",
        "cii_ref_a": 5762.0,
        "cii_ref_c": 0.381,
        "supported_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 12000000,
            "e_Methanol": 7500000,
            "Green_Ammonia": 9800000,
            "Liquid_H2": 16500000
        },
        "shore_power_equipped": True
    },
    "feeder_container_2500_teu": {
        "id": "feeder_container_2500_teu",
        "name": "Regional Feeder Container (2,500 TEU)",
        "type": "Container",
        "dwt": 34000.0,
        "teu_capacity": 2500,
        "length_pp": 195.0,
        "length_wl": 202.0,
        "beam": 30.5,
        "draft_design": 9.5,
        "draft_scantling": 10.8,
        "displacement_design": 42000.0,
        "block_coefficient_cb": 0.68,
        "prismatic_coefficient_cp": 0.70,
        "midship_coeff_cm": 0.96,
        "waterplane_coeff_cwp": 0.79,
        "transverse_area_at": 540.0,
        "wetted_surface_s0": 8900.0,
        "mcr_power_kw": 16200.0,
        "rpm_design": 98.0,
        "speed_design_knots": 18.5,
        "speed_min_knots": 9.0,
        "speed_max_knots": 20.5,
        "sfoc_base_g_per_kwh": 172.0,
        "aux_power_kw": 1400.0,
        "aux_sfoc_g_per_kwh": 200.0,
        "imo_cii_category": "container",
        "cii_ref_a": 1984.0,
        "cii_ref_c": 0.489,
        "supported_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"],
        "retrofit_cost_usd": {
            "LNG": 8500000,
            "e_Methanol": 5200000,
            "Green_Ammonia": 6800000,
            "Liquid_H2": 11500000
        },
        "shore_power_equipped": True
    }
}

def get_vessel(vessel_id: str) -> Dict[str, Any]:
    if vessel_id not in VESSEL_CLASSES:
        raise ValueError(f"Unknown vessel class: {vessel_id}. Available: {list(VESSEL_CLASSES.keys())}")
    return VESSEL_CLASSES[vessel_id]

def get_all_vessels() -> Dict[str, Dict[str, Any]]:
    return VESSEL_CLASSES
