"""
Quantum Genetic Algorithm (QGA / QEA) Engine
Implements Qubit Chromosomes, Quantum Rotation Gates, and Quantum NOT-gate Mutation
for discrete combinatorial fleet-to-route assignment, alternative fuel retrofits, and shore power schedules.
"""

import math
import random
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from app.data.vessels_database import VESSEL_CLASSES
from app.data.routes_waypoints import MARITIME_ROUTES, PORTS_CATALOG
from app.core.hydrodynamics import calculate_propulsion_and_fuel
from app.core.green_fuels_lca import calculate_voyage_emissions_and_cost, calculate_cold_ironing_benefit
from app.core.cii_calculator import calculate_imo_cii_rating

class QGAOptimizer:
    def __init__(
        self,
        population_size: int = 30,
        max_generations: int = 80,
        rotation_step_theta: float = 0.05 * math.pi,
        mutation_rate: float = 0.03
    ):
        self.population_size = population_size
        self.max_generations = max_generations
        self.theta_0 = rotation_step_theta
        self.mutation_rate = mutation_rate

    def optimize_fleet_deployment(
        self,
        cargo_demands: Optional[Dict[str, float]] = None,
        available_vessel_ids: Optional[List[str]] = None,
        carbon_tax_per_mt: float = 82.0,
        weight_cost: float = 0.40,
        weight_emissions: float = 0.45,
        weight_reliability: float = 0.15
    ) -> Dict[str, Any]:
        """
        Solves the combinatorial fleet assignment & green retrofit scheduling problem using QGA.
        """
        if available_vessel_ids is None:
            available_vessel_ids = list(VESSEL_CLASSES.keys())

        routes = list(MARITIME_ROUTES.values())
        vessels = [VESSEL_CLASSES[vid] for vid in available_vessel_ids]

        num_routes = len(routes)
        num_vessels = len(vessels)
        fuel_options = ["VLSFO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"]

        # Chromosome Encoding:
        # For each route:
        #   - Vessel choice (bits to encode vessel index)
        #   - Fuel choice (bits to encode fuel option)
        #   - Speed strategy (0: Slow Steaming 14kn, 1: Normal 18kn, 2: Express 21kn)
        #   - Cold-ironing toggle (1 bit)
        # Total Qubits per route = 3 (vessel) + 3 (fuel) + 2 (speed) + 1 (cold-ironing) = 9 qubits
        qubits_per_route = 9
        total_qubits = num_routes * qubits_per_route

        # Initialize Qubit population with equal superposition (1/sqrt(2), 1/sqrt(2))
        # pop_alpha: (pop_size, total_qubits), pop_beta: (pop_size, total_qubits)
        pop_alpha = np.full((self.population_size, total_qubits), 1.0 / math.sqrt(2.0))
        pop_beta = np.full((self.population_size, total_qubits), 1.0 / math.sqrt(2.0))

        def decode_individual(bits: np.ndarray) -> List[Dict[str, Any]]:
            assignments = []
            for r_idx, route in enumerate(routes):
                offset = r_idx * qubits_per_route

                # Vessel index
                v_bits = bits[offset : offset + 3]
                v_val = int(v_bits[0] * 4 + v_bits[1] * 2 + v_bits[2]) % num_vessels
                assigned_vessel = vessels[v_val]

                # Fuel index
                f_bits = bits[offset + 3 : offset + 6]
                f_val = int(f_bits[0] * 4 + f_bits[1] * 2 + f_bits[2]) % len(fuel_options)
                chosen_fuel = fuel_options[f_val]

                # Speed mode
                s_bits = bits[offset + 6 : offset + 8]
                s_mode = int(s_bits[0] * 2 + s_bits[1]) % 3
                if s_mode == 0:
                    speed = max(assigned_vessel["speed_min_knots"], assigned_vessel["speed_design_knots"] * 0.85) # Slow steam
                    speed_label = "Eco Slow Steaming"
                elif s_mode == 1:
                    speed = assigned_vessel["speed_design_knots"] # Normal
                    speed_label = "Design Speed"
                else:
                    speed = min(assigned_vessel["speed_max_knots"], assigned_vessel["speed_design_knots"] * 1.08) # Express
                    speed_label = "Express Transit"

                # Cold-ironing
                cold_iron = bool(bits[offset + 8] == 1)

                assignments.append({
                    "route_id": route["id"],
                    "route_name": route["name"],
                    "distance_nm": route["total_distance_nm"],
                    "origin_port": route["origin_port"],
                    "dest_port": route["dest_port"],
                    "vessel_id": assigned_vessel["id"],
                    "vessel_name": assigned_vessel["name"],
                    "vessel_dwt": assigned_vessel["dwt"],
                    "fuel_type": chosen_fuel,
                    "speed_knots": round(float(speed), 2),
                    "speed_mode": speed_label,
                    "cold_ironing_enabled": cold_iron
                })
            return assignments

        def evaluate_fleet_fitness(assignments: List[Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
            total_fleet_fuel_mt = 0.0
            total_fleet_cost_usd = 0.0
            total_fleet_wtw_ghg_mt = 0.0
            total_fleet_direct_co2_mt = 0.0
            route_reports = []

            for plan in assignments:
                v_id = plan["vessel_id"]
                speed = plan["speed_knots"]
                dist = plan["distance_nm"]
                fuel = plan["fuel_type"]
                vessel = VESSEL_CLASSES[v_id]

                transit_hours = dist / speed
                hydro = calculate_propulsion_and_fuel(
                    vessel_id=v_id,
                    speed_knots=speed,
                    draft_m=vessel["draft_design"],
                    trim_m=0.0,
                    fuel_type=fuel
                )
                voyage_fuel_mt = (hydro["total_foc_mt_day"] / 24.0) * transit_hours
                total_fleet_fuel_mt += voyage_fuel_mt

                lca = calculate_voyage_emissions_and_cost(fuel, voyage_fuel_mt)
                voyage_cost = lca["fuel_cost_usd"]
                voyage_wtw_ghg = lca["wtw_emissions_mt_co2e"]
                voyage_direct_co2 = lca["direct_co2_mt"]

                # Cold-Ironing benefit during 36-hour port turnaround
                cold_iron_benefit = {"net_co2e_saved_mt": 0.0, "net_cost_saving_usd": 0.0}
                if plan["cold_ironing_enabled"] and vessel["shore_power_equipped"]:
                    cold_iron_benefit = calculate_cold_ironing_benefit(
                        aux_power_kw=vessel["aux_power_kw"],
                        berth_hours=36.0,
                        grid_emission_factor_kg_kwh=0.28
                    )
                    voyage_wtw_ghg -= cold_iron_benefit["net_co2e_saved_mt"]
                    voyage_cost -= cold_iron_benefit["net_cost_saving_usd"]

                # Carbon Tax liability
                carbon_tax = voyage_direct_co2 * carbon_tax_per_mt
                voyage_total_cost = voyage_cost + carbon_tax

                total_fleet_cost_usd += voyage_total_cost
                total_fleet_wtw_ghg_mt += voyage_wtw_ghg
                total_fleet_direct_co2_mt += voyage_direct_co2

                # IMO CII Audit
                cii_res = calculate_imo_cii_rating(
                    vessel_id=v_id,
                    total_co2_emissions_mt=voyage_direct_co2,
                    total_distance_nm=dist
                )

                route_reports.append({
                    **plan,
                    "transit_days": round(transit_hours / 24.0, 2),
                    "fuel_consumed_mt": round(voyage_fuel_mt, 2),
                    "fuel_cost_usd": round(voyage_cost, 2),
                    "carbon_tax_usd": round(carbon_tax, 2),
                    "total_cost_usd": round(voyage_total_cost, 2),
                    "wtw_ghg_mt": round(voyage_wtw_ghg, 2),
                    "cold_ironing_co2_saved_mt": round(cold_iron_benefit["net_co2e_saved_mt"], 2),
                    "cii_rating": cii_res["cii_rating"],
                    "cii_color": cii_res["color_badge"]
                })

            # Fitness formulation (normalized minimization)
            # Reference baseline: 5 routes * standard VLSFO ~ $4.5M cost, ~18k MT GHG
            ref_cost = 4500000.0
            ref_ghg = 18000.0

            fitness = (
                weight_cost * (total_fleet_cost_usd / ref_cost) +
                weight_emissions * (total_fleet_wtw_ghg_mt / ref_ghg)
            )

            summary = {
                "total_fuel_mt": total_fleet_fuel_mt,
                "total_cost_usd": total_fleet_cost_usd,
                "total_wtw_ghg_mt": total_fleet_wtw_ghg_mt,
                "total_direct_co2_mt": total_fleet_direct_co2_mt,
                "route_reports": route_reports
            }
            return fitness, summary

        best_global_bits = np.zeros(total_qubits, dtype=int)
        best_global_fitness = float("inf")
        best_global_summary: Dict[str, Any] = {}
        convergence_history: List[Dict[str, Any]] = []

        # Quantum Rotation Gate Lookup Sign Table
        # delta_theta = s(alpha, beta) * theta_0
        for gen in range(self.max_generations):
            # 1. Quantum State Collapse / Measurement: sample classical binary strings
            measured_population = np.zeros((self.population_size, total_qubits), dtype=int)
            pop_fitness = np.zeros(self.population_size)
            pop_summaries = []

            for p in range(self.population_size):
                for q in range(total_qubits):
                    prob_1 = pop_beta[p, q] ** 2
                    measured_population[p, q] = 1 if random.random() < prob_1 else 0

                decoded = decode_individual(measured_population[p])
                fit, summ = evaluate_fleet_fitness(decoded)
                pop_fitness[p] = fit
                pop_summaries.append(summ)

                if fit < best_global_fitness:
                    best_global_fitness = fit
                    best_global_bits = measured_population[p].copy()
                    best_global_summary = summ

            # 2. Quantum Rotation Gate Update
            for p in range(self.population_size):
                for q in range(total_qubits):
                    x_pq = measured_population[p, q]
                    b_q = best_global_bits[q]

                    # Guidance lookup
                    alpha = pop_alpha[p, q]
                    beta = pop_beta[p, q]

                    if x_pq == 0 and b_q == 1:
                        # Rotate toward |1> state
                        if alpha * beta > 0:
                            delta_theta = self.theta_0
                        elif alpha * beta < 0:
                            delta_theta = -self.theta_0
                        elif alpha == 0:
                            delta_theta = 0.0
                        else:
                            delta_theta = self.theta_0
                    elif x_pq == 1 and b_q == 0:
                        # Rotate toward |0> state
                        if alpha * beta > 0:
                            delta_theta = -self.theta_0
                        elif alpha * beta < 0:
                            delta_theta = self.theta_0
                        elif alpha == 0:
                            delta_theta = -self.theta_0
                        else:
                            delta_theta = 0.0
                    else:
                        delta_theta = 0.0

                    # Apply Quantum Rotation Matrix
                    new_alpha = alpha * math.cos(delta_theta) - beta * math.sin(delta_theta)
                    new_beta = alpha * math.sin(delta_theta) + beta * math.cos(delta_theta)

                    # 3. Quantum NOT-Gate Mutation (Quantum Tunneling)
                    if random.random() < self.mutation_rate:
                        # Invert amplitudes: alpha <-> beta
                        new_alpha, new_beta = new_beta, new_alpha

                    # Normalization safeguard
                    norm = math.sqrt(new_alpha ** 2 + new_beta ** 2) + 1e-9
                    pop_alpha[p, q] = new_alpha / norm
                    pop_beta[p, q] = new_beta / norm

            convergence_history.append({
                "generation": gen + 1,
                "best_fitness": round(float(best_global_fitness), 5),
                "fleet_cost_usd": round(float(best_global_summary["total_cost_usd"]), 2),
                "fleet_ghg_mt": round(float(best_global_summary["total_wtw_ghg_mt"]), 2),
                "fleet_fuel_mt": round(float(best_global_summary["total_fuel_mt"]), 2)
            })

        # Baseline Traditional Fleet (All VLSFO at Design Speed without Cold-Ironing)
        trad_fuel_mt = 0.0
        trad_cost_usd = 0.0
        trad_ghg_mt = 0.0
        for plan in best_global_summary["route_reports"]:
            vessel = VESSEL_CLASSES[plan["vessel_id"]]
            dist = plan["distance_nm"]
            speed = vessel["speed_design_knots"]
            transit_h = dist / speed
            h = calculate_propulsion_and_fuel(
                vessel_id=plan["vessel_id"],
                speed_knots=speed,
                draft_m=vessel["draft_design"],
                trim_m=0.0,
                fuel_type="VLSFO"
            )
            v_f_mt = (h["total_foc_mt_day"] / 24.0) * transit_h
            trad_fuel_mt += v_f_mt
            lca = calculate_voyage_emissions_and_cost("VLSFO", v_f_mt)
            c_tax = lca["direct_co2_mt"] * carbon_tax_per_mt
            trad_cost_usd += (lca["fuel_cost_usd"] + c_tax)
            trad_ghg_mt += lca["wtw_emissions_mt_co2e"]

        net_ghg_cut_pct = max(0.0, (trad_ghg_mt - best_global_summary["total_wtw_ghg_mt"]) / trad_ghg_mt) * 100.0 if trad_ghg_mt > 0 else 0.0
        net_cost_cut_usd = max(0.0, trad_cost_usd - best_global_summary["total_cost_usd"])

        return {
            "total_routes_managed": num_routes,
            "optimized_fleet_cost_usd": round(best_global_summary["total_cost_usd"], 2),
            "baseline_fleet_cost_usd": round(trad_cost_usd, 2),
            "cost_savings_usd": round(net_cost_cut_usd, 2),
            "optimized_fleet_ghg_mt": round(best_global_summary["total_wtw_ghg_mt"], 2),
            "baseline_fleet_ghg_mt": round(trad_ghg_mt, 2),
            "ghg_reduction_pct": round(net_ghg_cut_pct, 1),
            "optimized_fleet_fuel_mt": round(best_global_summary["total_fuel_mt"], 2),
            "baseline_fleet_fuel_mt": round(trad_fuel_mt, 2),
            "route_deployments": best_global_summary["route_reports"],
            "convergence_history": convergence_history,
            "qubit_state_distribution": {
                "mean_alpha_sq": round(float(np.mean(pop_alpha ** 2)), 4),
                "mean_beta_sq": round(float(np.mean(pop_beta ** 2)), 4)
            }
        }

# Global Singleton Instance
qga_optimizer = QGAOptimizer()
