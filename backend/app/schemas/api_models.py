"""
Pydantic Request & Response Data Models for Q-Fleet REST API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PredictFuelRequest(BaseModel):
    vessel_id: str = Field(default="container_15000_teu", description="ID of vessel class")
    speed_knots: float = Field(default=20.0, ge=5.0, le=30.0, description="Speed through water (knots)")
    draft_m: float = Field(default=14.5, ge=4.0, le=25.0, description="Vessel draft (m)")
    trim_m: float = Field(default=0.0, ge=-2.0, le=3.0, description="Vessel trim (m)")
    hs_m: float = Field(default=1.8, ge=0.0, le=15.0, description="Significant wave height (m)")
    tp_s: float = Field(default=7.5, ge=2.0, le=25.0, description="Peak wave period (s)")
    wind_speed_knots: float = Field(default=16.0, ge=0.0, le=80.0, description="True wind speed (knots)")
    wind_angle_deg: float = Field(default=30.0, ge=0.0, le=360.0, description="Relative wind angle (deg)")
    fuel_type: str = Field(default="VLSFO", description="Fuel type (VLSFO, MGO, LNG, e_Methanol, Green_Ammonia, Liquid_H2)")

class OptimizeRouteRequest(BaseModel):
    vessel_id: str = Field(default="container_15000_teu")
    route_id: str = Field(default="shanghai_rotterdam")
    fuel_type: str = Field(default="VLSFO")
    target_max_transit_days: Optional[float] = Field(default=None)
    weight_cost: float = Field(default=0.40, ge=0.0, le=1.0)
    weight_emissions: float = Field(default=0.40, ge=0.0, le=1.0)
    weight_time: float = Field(default=0.20, ge=0.0, le=1.0)

class OptimizeFleetRequest(BaseModel):
    available_vessel_ids: Optional[List[str]] = Field(default=None)
    carbon_tax_per_mt: float = Field(default=82.0, ge=0.0, le=300.0)
    weight_cost: float = Field(default=0.40, ge=0.0, le=1.0)
    weight_emissions: float = Field(default=0.45, ge=0.0, le=1.0)
    weight_reliability: float = Field(default=0.15, ge=0.0, le=1.0)

class BenchmarkRequest(BaseModel):
    vessel_id: str = Field(default="container_15000_teu")
    route_id: str = Field(default="shanghai_rotterdam")
    fuel_type: str = Field(default="VLSFO")
    iterations: int = Field(default=80, ge=20, le=200)

class CIIAuditRequest(BaseModel):
    vessel_id: str = Field(default="container_15000_teu")
    total_co2_emissions_mt: float = Field(default=4800.0, ge=0.0)
    total_distance_nm: float = Field(default=10520.0, ge=1.0)
    target_year: int = Field(default=2026, ge=2023, le=2030)

class ColdIroningRequest(BaseModel):
    aux_power_kw: float = Field(default=3500.0, ge=100.0)
    berth_hours: float = Field(default=36.0, ge=1.0)
    grid_emission_factor_kg_kwh: float = Field(default=0.28, ge=0.0, le=1.5)
    electricity_price_usd_per_kwh: float = Field(default=0.16, ge=0.01, le=1.0)

class ScenarioSimulationRequest(BaseModel):
    scenario_name: str = Field(default="Carbon_Tax_Spike_2030")
    fuel_price_multiplier: float = Field(default=1.25, ge=0.5, le=3.0)
    carbon_tax_usd: float = Field(default=150.0, ge=0.0, le=400.0)
    storm_severity_multiplier: float = Field(default=1.35, ge=0.5, le=2.5)
    target_year: int = Field(default=2030, ge=2024, le=2035)
