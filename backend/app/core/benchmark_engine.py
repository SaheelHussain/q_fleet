"""
Head-to-Head Benchmarking Harness
Executes empirical comparisons between Quantum-Inspired Algorithms (QPSO, QGA, Q-PINN)
and Classical Baselines (CPSO, CGA, Random Forest, MLP) across accuracy, convergence, and optimality metrics.
"""

import time
import numpy as np
from typing import Dict, Any, List
from app.core.qpso_optimizer import qpso_optimizer
from app.core.classical_baselines import ClassicalPSO, ClassicalGA, classical_ml_benchmarks

def run_head_to_head_optimization_benchmark(
    vessel_id: str = "container_15000_teu",
    route_id: str = "shanghai_rotterdam",
    fuel_type: str = "VLSFO",
    iterations: int = 80
) -> Dict[str, Any]:
    """
    Executes a side-by-side comparative race between QPSO, Classical PSO, and Classical GA.
    """
    # 1. Run Quantum Particle Swarm Optimization (QPSO)
    t0 = time.time()
    qpso_opt = qpso_optimizer.optimize_route_trajectory(
        vessel_id=vessel_id,
        route_id=route_id,
        fuel_type=fuel_type
    )
    qpso_time_ms = (time.time() - t0) * 1000.0

    # 2. Run Classical PSO
    cpso = ClassicalPSO(num_particles=40, max_iterations=iterations)
    cpso_res = cpso.run(vessel_id, route_id, fuel_type)

    # 3. Run Classical GA
    cga = ClassicalGA(population_size=40, max_generations=iterations)
    cga_res = cga.run(vessel_id, route_id, fuel_type)

    # Compute comparative convergence speedup
    qpso_final_cost = qpso_opt["optimized_cost_usd"]
    baseline_cost = qpso_opt["baseline_cost_usd"]

    # Calculate convergence iterations to reach 95% of best fitness
    qpso_conv = qpso_opt["convergence_history"]
    qpso_min_fit = qpso_conv[-1]["best_fitness"]
    qpso_iter_95 = next((item["iteration"] for item in qpso_conv if item["best_fitness"] <= qpso_min_fit * 1.05), len(qpso_conv))

    cpso_conv = cpso_res["convergence_curve"]
    cpso_min_fit = cpso_conv[-1]["best_fitness"]
    cpso_iter_95 = next((item["iteration"] for item in cpso_conv if item["best_fitness"] <= cpso_min_fit * 1.05), len(cpso_conv))

    cga_conv = cga_res["convergence_curve"]
    cga_min_fit = cga_conv[-1]["best_fitness"]
    cga_iter_95 = next((item["iteration"] for item in cga_conv if item["best_fitness"] <= cga_min_fit * 1.05), len(cga_conv))

    speedup_ratio = round(float(cpso_iter_95 / max(1, qpso_iter_95)), 2)

    return {
        "vessel_id": vessel_id,
        "route_id": route_id,
        "fuel_type": fuel_type,
        "quantum_qpso": {
            "name": "Quantum Particle Swarm (QPSO)",
            "optimized_fuel_mt": qpso_opt["optimized_fuel_mt"],
            "optimized_cost_usd": qpso_final_cost,
            "optimized_ghg_mt": qpso_opt["optimized_ghg_wtw_mt"],
            "fuel_savings_pct": qpso_opt["fuel_savings_pct"],
            "ghg_reduction_pct": qpso_opt["ghg_savings_pct"],
            "iterations_to_optimum": qpso_iter_95,
            "runtime_ms": round(qpso_time_ms, 2),
            "tunneling_events": qpso_opt["quantum_tunneling_events_total"],
            "convergence_curve": [{"iteration": c["iteration"], "fitness": c["best_fitness"]} for c in qpso_conv[:50]]
        },
        "classical_pso": {
            "name": "Classical PSO",
            "runtime_ms": cpso_res["runtime_ms"],
            "iterations_to_optimum": cpso_iter_95,
            "best_fitness": cpso_res["best_fitness"],
            "convergence_curve": cpso_conv[:50]
        },
        "classical_ga": {
            "name": "Classical GA",
            "runtime_ms": cga_res["runtime_ms"],
            "iterations_to_optimum": cga_iter_95,
            "best_fitness": cga_res["best_fitness"],
            "convergence_curve": cga_conv[:50]
        },
        "summary_metrics": {
            "convergence_speedup_vs_cpso": f"{speedup_ratio}x faster",
            "qpso_fuel_savings_mt": qpso_opt["fuel_savings_mt"],
            "qpso_cost_savings_usd": qpso_opt["cost_savings_usd"],
            "local_minima_escaped_via_tunneling": qpso_opt["quantum_tunneling_events_total"],
            "pareto_solutions_found": len(qpso_opt["pareto_frontier"])
        }
    }

def run_ml_prediction_benchmark() -> Dict[str, Any]:
    """
    Evaluates ML regressors (Q-PINN, Random Forest, MLP) across statistical accuracy metrics.
    """
    return classical_ml_benchmarks.train_and_evaluate(train_samples=1500)
