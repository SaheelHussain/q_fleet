"""
IMO Carbon Intensity Indicator (CII) & EU ETS Carbon Auditing Engine
Implements IMO MEPC.337(76) / MEPC.354(78) A-E rating boundaries, reduction factors Z,
and EU Emissions Trading System (ETS) allowance tax liabilities.
"""

from typing import Dict, Any
from app.data.vessels_database import get_vessel

# IMO CII Boundary multipliers (d1, d2, d3, d4) by vessel type
CII_BOUNDARY_FACTORS = {
    "container": {"d1": 0.82, "d2": 0.93, "d3": 1.08, "d4": 1.19},
    "bulk_carrier": {"d1": 0.86, "d2": 0.94, "d3": 1.06, "d4": 1.18},
    "tanker": {"d1": 0.82, "d2": 0.93, "d3": 1.08, "d4": 1.20},
    "gas_carrier": {"d1": 0.85, "d2": 0.95, "d3": 1.06, "d4": 1.21},
    "ro_ro_cargo": {"d1": 0.76, "d2": 0.89, "d3": 1.12, "d4": 1.30}
}

# IMO Annual Reduction Factor Z (%)
IMO_REDUCTION_FACTORS = {
    2023: 5.0,
    2024: 7.0,
    2025: 9.0,
    2026: 11.0,
    2027: 13.0,
    2028: 15.0,
    2029: 17.5,
    2030: 21.0
}

# EU ETS Carbon Allowance Price (USD per MT CO2)
DEFAULT_EU_ETS_CARBON_PRICE_USD = 82.0 # ~75 EUR/tCO2

def calculate_imo_cii_rating(
    vessel_id: str,
    total_co2_emissions_mt: float,
    total_distance_nm: float,
    target_year: int = 2026
) -> Dict[str, Any]:
    """
    Computes Attained CII, Required CII, and official IMO A/B/C/D/E rating.
    """
    vessel = get_vessel(vessel_id)
    dwt = vessel["dwt"]
    cat = vessel["imo_cii_category"]
    a = vessel["cii_ref_a"]
    c = vessel["cii_ref_c"]

    if total_distance_nm <= 0.0 or dwt <= 0.0:
        return {
            "error": "Distance and DWT must be greater than zero."
        }

    # 1. Attained Annual Efficiency Ratio (AER / CII) in gCO2 / (DWT * nm)
    # Total CO2 in grams = MT * 1e6
    attained_cii = (total_co2_emissions_mt * 1e6) / (dwt * total_distance_nm)

    # 2. Reference CII Baseline
    cii_ref = a * (dwt ** (-c))

    # 3. Required CII for Year
    z_factor = IMO_REDUCTION_FACTORS.get(target_year, 11.0)
    required_cii = cii_ref * (1.0 - z_factor / 100.0)

    # 4. Boundary thresholds
    boundaries = CII_BOUNDARY_FACTORS.get(cat, CII_BOUNDARY_FACTORS["container"])
    th_a = boundaries["d1"] * required_cii
    th_b = boundaries["d2"] * required_cii
    th_c = boundaries["d3"] * required_cii
    th_d = boundaries["d4"] * required_cii

    # 5. Determine Rating
    if attained_cii <= th_a:
        rating = "A"
        rating_description = "Superior (Major Outperformance)"
        color_badge = "#10b981" # Green
        compliance_status = "Compliant"
    elif attained_cii <= th_b:
        rating = "B"
        rating_description = "Minor Superior"
        color_badge = "#34d399" # Emerald
        compliance_status = "Compliant"
    elif attained_cii <= th_c:
        rating = "C"
        rating_description = "Moderate / Baseline"
        color_badge = "#f59e0b" # Amber
        compliance_status = "Compliant"
    elif attained_cii <= th_d:
        rating = "D"
        rating_description = "Minor Inferior (Corrective Action Required if 3 consecutive years)"
        color_badge = "#f97316" # Orange
        compliance_status = "Warning"
    else:
        rating = "E"
        rating_description = "Inferior (Mandatory Plan of Corrective Actions - SEEMP III)"
        color_badge = "#ef4444" # Red
        compliance_status = "Non-Compliant"

    # Ratio attained / required
    ratio_to_required = attained_cii / required_cii

    return {
        "vessel_id": vessel_id,
        "vessel_name": vessel["name"],
        "target_year": target_year,
        "z_reduction_pct": z_factor,
        "dwt": dwt,
        "total_distance_nm": round(total_distance_nm, 1),
        "total_co2_mt": round(total_co2_emissions_mt, 2),
        "attained_cii": round(attained_cii, 4),
        "required_cii": round(required_cii, 4),
        "ratio_to_required": round(ratio_to_required, 3),
        "cii_rating": rating,
        "rating_description": rating_description,
        "compliance_status": compliance_status,
        "color_badge": color_badge,
        "thresholds": {
            "A_max": round(th_a, 4),
            "B_max": round(th_b, 4),
            "C_max": round(th_c, 4),
            "D_max": round(th_d, 4)
        }
    }

def calculate_eu_ets_tax(
    total_ttw_co2e_mt: float,
    voyage_scope: str = "extra_eu", # "intra_eu" = 100%, "extra_eu" = 50%
    carbon_price_usd_per_mt: float = DEFAULT_EU_ETS_CARBON_PRICE_USD,
    phase_in_pct: float = 100.0 # 2026 is 100% full phase-in
) -> Dict[str, Any]:
    """
    Computes EU ETS carbon tax liability for voyages touching European Economic Area (EEA) ports.
    """
    scope_multiplier = 1.0 if voyage_scope == "intra_eu" else 0.50
    taxable_emissions_mt = total_ttw_co2e_mt * scope_multiplier * (phase_in_pct / 100.0)
    total_tax_usd = taxable_emissions_mt * carbon_price_usd_per_mt

    return {
        "total_emissions_mt": round(total_ttw_co2e_mt, 2),
        "voyage_scope": voyage_scope,
        "scope_coverage_pct": int(scope_multiplier * 100),
        "phase_in_pct": phase_in_pct,
        "taxable_emissions_mt": round(taxable_emissions_mt, 2),
        "carbon_price_usd_per_mt": carbon_price_usd_per_mt,
        "total_ets_tax_usd": round(total_tax_usd, 2)
    }
