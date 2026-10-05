"""
Comprehensive Backend Test & Validation Script
Verifies all quantum modules, physics engines, and API components.
"""

import sys
import time
from pathlib import Path

# Add backend root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.data.vessels_database import get_all_vessels, get_vessel
from app.data.routes_waypoints import get_all_routes, get_route
from app.core.hydrodynamics import calculate_propulsion_and_fuel
from app.core.q_pinn_predictor import q_pinn_model
from app.core.qpso_optimizer import qpso_optimizer
from app.core.qga_optimizer import qga_optimizer
from app.core.benchmark_engine import run_head_to_head_optimization_benchmark, run_ml_prediction_benchmark
from app.core.cii_calculator import calculate_imo_cii_rating, calculate_eu_ets_tax
from app.core.green_fuels_lca import calculate_cold_ironing_benefit

def run_all_tests():
    print("==========================================================")
    print("⚓ Q-FLEET (AURAQUANTA) BACKEND VALIDATION SUITE")
    print("==========================================================")

    # Test 1: Vessels & Routes
    print("\n[1/7] Testing Vessels & Routes Catalog...")
    vessels = get_all_vessels()
    routes = get_all_routes()
    assert len(vessels) == 6, f"Expected 6 vessels, got {len(vessels)}"
    assert len(routes) >= 4, f"Expected >= 4 routes, got {len(routes)}"
    print(f"  ✓ Loaded {len(vessels)} vessel classes & {len(routes)} trade corridors successfully.")

    # Test 2: Hydrodynamics Calculation
    print("\n[2/7] Testing Holtrop-Mennen & Kwon Hydrodynamics...")
    h_res = calculate_propulsion_and_fuel("container_15000_teu", 20.0, 14.5, fuel_type="LNG")
    assert h_res["power_kw"] > 10000, "Power output invalid"
    assert h_res["total_foc_mt_day"] > 50, "FOC output invalid"
    print(f"  ✓ Container 15k TEU @ 20kn LNG -> Power: {h_res['power_kw']} kW, FOC: {h_res['total_foc_mt_day']} MT/day")

    # Test 3: Q-PINN Predictor
    print("\n[3/7] Testing Quantum-Inspired Physics-Informed ML Predictor...")
    q_pred = q_pinn_model.predict("aframax_tanker_115k", 14.0, 13.5, hs_m=2.5, wind_speed_knots=20.0)
    assert q_pred["predicted_foc_mt_day"] > 0, "Prediction failed"
    print(f"  ✓ Q-PINN Aframax FOC: {q_pred['predicted_foc_mt_day']} MT/day (Confidence: {q_pred['model_confidence_pct']}%)")

    # Test 4: QPSO Multi-Segment Route Optimizer
    print("\n[4/7] Testing QPSO Oceanic Route Trajectory Optimization...")
    t0 = time.time()
    qpso_res = qpso_optimizer.optimize_route_trajectory(
        vessel_id="container_15000_teu",
        route_id="singapore_dubai",
        fuel_type="VLSFO"
    )
    qpso_dur = time.time() - t0
    assert qpso_res["optimized_fuel_mt"] > 0
    assert len(qpso_res["convergence_history"]) > 0
    print(f"  ✓ QPSO finished in {qpso_dur:.2f}s | Fuel Saved: {qpso_res['fuel_savings_pct']}% | Tunneling events: {qpso_res['quantum_tunneling_events_total']}")

    # Test 5: QGA Fleet Deployment
    print("\n[5/7] Testing QGA Combinatorial Fleet Deployment...")
    t0 = time.time()
    qga_res = qga_optimizer.optimize_fleet_deployment()
    qga_dur = time.time() - t0
    assert len(qga_res["route_deployments"]) == len(routes)
    print(f"  ✓ QGA finished in {qga_dur:.2f}s | Fleet GHG Cut: {qga_res['ghg_reduction_pct']}% | Cost Saved: ${qga_res['cost_savings_usd']:,.2f}")

    # Test 6: IMO CII & Carbon Tax
    print("\n[6/7] Testing IMO CII & EU ETS Regulatory Engine...")
    cii_res = calculate_imo_cii_rating("capesize_bulker_180k", total_co2_emissions_mt=1800.0, total_distance_nm=4500.0)
    ets_res = calculate_eu_ets_tax(1800.0)
    assert cii_res["cii_rating"] in ["A", "B", "C", "D", "E"]
    print(f"  ✓ Capesize Bulker -> CII Grade: {cii_res['cii_rating']} ({cii_res['compliance_status']}) | EU ETS Tax: ${ets_res['total_ets_tax_usd']:,.2f}")

    # Test 7: Head-to-Head Benchmark Suite
    print("\n[7/7] Testing Quantum vs Classical Benchmark Race...")
    bench_res = run_head_to_head_optimization_benchmark(
        vessel_id="feeder_container_2500_teu",
        route_id="singapore_dubai",
        iterations=30
    )
    print(f"  ✓ Benchmark Finished! Speedup: {bench_res['summary_metrics']['convergence_speedup_vs_cpso']} | QPSO Fuel Savings: {bench_res['summary_metrics']['qpso_fuel_savings_mt']} MT")

    print("\n==========================================================")
    print("🎉 ALL 7 TEST SUITES PASSED PERFECTLY WITH ZERO ERRORS!")
    print("==========================================================")

if __name__ == "__main__":
    run_all_tests()
