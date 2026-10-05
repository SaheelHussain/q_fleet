"""
FastAPI REST API Routes Definition
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.data.vessels_database import get_all_vessels, get_vessel
from app.data.routes_waypoints import get_all_routes, get_all_ports, get_route
from app.core.q_pinn_predictor import q_pinn_model
from app.core.qpso_optimizer import qpso_optimizer
from app.core.qga_optimizer import qga_optimizer
from app.core.benchmark_engine import (
    run_head_to_head_optimization_benchmark,
    run_ml_prediction_benchmark
)
from app.core.cii_calculator import calculate_imo_cii_rating, calculate_eu_ets_tax
from app.core.green_fuels_lca import calculate_cold_ironing_benefit, FUEL_LCA_PROFILES
from app.schemas.api_models import (
    PredictFuelRequest,
    OptimizeRouteRequest,
    OptimizeFleetRequest,
    BenchmarkRequest,
    CIIAuditRequest,
    ColdIroningRequest,
    ScenarioSimulationRequest
)

router = APIRouter()

@router.get("/health")
def health_check() -> Dict[str, Any]:
    return {
        "status": "online",
        "service": "Q-Fleet (AuraQuanta) Quantum Maritime Engine",
        "version": "1.0.0",
        "quantum_modules": {
            "q_pinn_predictor": "ready",
            "qpso_optimizer": "ready",
            "qga_fleet_scheduler": "ready",
            "classical_benchmarks": "ready",
            "imo_cii_auditor": "ready"
        }
    }

@router.get("/fleet/vessels")
def list_vessels() -> Dict[str, Any]:
    return get_all_vessels()

@router.get("/fleet/routes")
def list_routes() -> Dict[str, Any]:
    return get_all_routes()

@router.get("/fleet/ports")
def list_ports() -> Dict[str, Any]:
    return get_all_ports()

@router.get("/fuels/profiles")
def list_fuel_profiles() -> Dict[str, Any]:
    return FUEL_LCA_PROFILES

@router.post("/predict/fuel")
def predict_fuel_consumption(req: PredictFuelRequest) -> Dict[str, Any]:
    try:
        res = q_pinn_model.predict(
            vessel_id=req.vessel_id,
            speed_knots=req.speed_knots,
            draft_m=req.draft_m,
            trim_m=req.trim_m,
            hs_m=req.hs_m,
            tp_s=req.tp_s,
            wind_speed_knots=req.wind_speed_knots,
            wind_angle_deg=req.wind_angle_deg,
            fuel_type=req.fuel_type
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize/route")
def optimize_voyage_trajectory(req: OptimizeRouteRequest) -> Dict[str, Any]:
    try:
        res = qpso_optimizer.optimize_route_trajectory(
            vessel_id=req.vessel_id,
            route_id=req.route_id,
            fuel_type=req.fuel_type,
            target_max_transit_days=req.target_max_transit_days,
            weight_cost=req.weight_cost,
            weight_emissions=req.weight_emissions,
            weight_time=req.weight_time
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize/fleet")
def optimize_fleet_deployment(req: OptimizeFleetRequest) -> Dict[str, Any]:
    try:
        res = qga_optimizer.optimize_fleet_deployment(
            available_vessel_ids=req.available_vessel_ids,
            carbon_tax_per_mt=req.carbon_tax_per_mt,
            weight_cost=req.weight_cost,
            weight_emissions=req.weight_emissions,
            weight_reliability=req.weight_reliability
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/benchmark/run")
def benchmark_optimization(req: BenchmarkRequest) -> Dict[str, Any]:
    try:
        res = run_head_to_head_optimization_benchmark(
            vessel_id=req.vessel_id,
            route_id=req.route_id,
            fuel_type=req.fuel_type,
            iterations=req.iterations
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/benchmark/ml")
def benchmark_machine_learning() -> Dict[str, Any]:
    try:
        return run_ml_prediction_benchmark()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cii/audit")
def audit_imo_cii(req: CIIAuditRequest) -> Dict[str, Any]:
    try:
        cii_res = calculate_imo_cii_rating(
            vessel_id=req.vessel_id,
            total_co2_emissions_mt=req.total_co2_emissions_mt,
            total_distance_nm=req.total_distance_nm,
            target_year=req.target_year
        )
        ets_res = calculate_eu_ets_tax(
            total_ttw_co2e_mt=req.total_co2_emissions_mt,
            voyage_scope="extra_eu"
        )
        return {
            "cii_rating_audit": cii_res,
            "eu_ets_liability": ets_res
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cold-ironing/benefit")
def audit_cold_ironing(req: ColdIroningRequest) -> Dict[str, Any]:
    try:
        return calculate_cold_ironing_benefit(
            aux_power_kw=req.aux_power_kw,
            berth_hours=req.berth_hours,
            grid_emission_factor_kg_kwh=req.grid_emission_factor_kg_kwh,
            electricity_price_usd_per_kwh=req.electricity_price_usd_per_kwh
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulate/scenario")
def simulate_future_scenario(req: ScenarioSimulationRequest) -> Dict[str, Any]:
    """
    Stress-tests fleet under external disruptions (carbon price spikes, weather surges, 2030 regulations).
    """
    try:
        base_opt = qga_optimizer.optimize_fleet_deployment(
            carbon_tax_per_mt=req.carbon_tax_usd
        )
        return {
            "scenario_name": req.scenario_name,
            "target_year": req.target_year,
            "simulated_carbon_tax_usd": req.carbon_tax_usd,
            "fuel_price_multiplier": req.fuel_price_multiplier,
            "storm_severity_multiplier": req.storm_severity_multiplier,
            "fleet_results": base_opt
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
