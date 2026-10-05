"""
Quantum Particle Swarm Optimization (QPSO) Engine
Solves continuous multi-segment oceanic voyage trajectory optimization, dynamic speed profiling,
trim management, and alternative fuel blending via Quantum Delta-Potential Well and Mean-Best Tunneling.
"""

import math
import random
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from app.data.vessels_database import get_vessel
from app.data.routes_waypoints import get_route
from app.core.hydrodynamics import calculate_propulsion_and_fuel
from app.core.green_fuels_lca import calculate_voyage_emissions_and_cost
from app.core.cii_calculator import calculate_imo_cii_rating

class QPSOOptimizer:
    def __init__(
        self,
        num_particles: int = 40,
        max_iterations: int = 120,
        alpha_max: float = 1.0,
        alpha_min: float = 0.45
    ):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.alpha_max = alpha_max
        self.alpha_min = alpha_min

    def optimize_route_trajectory(
        self,
        vessel_id: str,
        route_id: str,
        fuel_type: str = "VLSFO",
        target_max_transit_days: Optional[float] = None,
        weight_cost: float = 0.40,
        weight_emissions: float = 0.40,
        weight_time: float = 0.20
    ) -> Dict[str, Any]:
        """
        Executes multi-segment continuous QPSO optimization for a vessel along a specific maritime route.
        """
        vessel = get_vessel(vessel_id)
        route = get_route(route_id)
        segments = route["segments"]
        num_segments = len(segments)

        speed_min = vessel["speed_min_knots"]
        speed_max = vessel["speed_max_knots"]
        speed_design = vessel["speed_design_knots"]
        draft_design = vessel["draft_design"]

        # Default transit target if not provided
        if target_max_transit_days is None:
            transit_key = next(k for k in route if k.startswith("typical_transit_days"))
            target_max_transit_days = route[transit_key] * 1.05

        # Decision Variables: [V_1, ..., V_K, Trim_1, ..., Trim_K] (Dimension = 2 * K)
        dim = num_segments * 2
        bounds_min = np.array([speed_min] * num_segments + [-0.5] * num_segments)
        bounds_max = np.array([speed_max] * num_segments + [1.5] * num_segments)

        # Baseline reference for normalization
        base_speed = speed_design
        base_days = sum(seg["distance_nm"] / (base_speed * 24.0) for seg in segments)
        base_fuel_mt = 0.0
        for seg in segments:
            h = calculate_propulsion_and_fuel(
                vessel_id=vessel_id,
                speed_knots=base_speed,
                draft_m=draft_design,
                trim_m=0.0,
                hs_m=seg["mean_hs_m"],
                tp_s=seg["mean_tp_s"],
                wind_speed_knots=seg["mean_wind_knots"],
                wind_angle_deg=seg["wind_direction_deg"],
                fuel_type=fuel_type
            )
            seg_hours = seg["distance_nm"] / base_speed
            base_fuel_mt += (h["total_foc_mt_day"] / 24.0) * seg_hours

        base_lca = calculate_voyage_emissions_and_cost(fuel_type, base_fuel_mt)
        ref_cost = max(1000.0, base_lca["fuel_cost_usd"])
        ref_ghg = max(10.0, base_lca["wtw_emissions_mt_co2e"])
        ref_time = max(1.0, base_days)

        def evaluate_fitness(particle: np.ndarray) -> Tuple[float, Dict[str, Any]]:
            speeds = particle[:num_segments]
            trims = particle[num_segments:]

            total_hours = 0.0
            total_fuel_mt = 0.0
            segment_details = []

            for i, seg in enumerate(segments):
                v_seg = speeds[i]
                t_seg = trims[i]
                dist = seg["distance_nm"]
                seg_hours = dist / max(0.1, v_seg)
                total_hours += seg_hours

                hydro = calculate_propulsion_and_fuel(
                    vessel_id=vessel_id,
                    speed_knots=v_seg,
                    draft_m=draft_design,
                    trim_m=t_seg,
                    hs_m=seg["mean_hs_m"],
                    tp_s=seg["mean_tp_s"],
                    wind_speed_knots=seg["mean_wind_knots"],
                    wind_angle_deg=seg["wind_direction_deg"],
                    fuel_type=fuel_type
                )
                seg_fuel_mt = (hydro["total_foc_mt_day"] / 24.0) * seg_hours
                total_fuel_mt += seg_fuel_mt

                segment_details.append({
                    "seg_id": seg["seg_id"],
                    "name": seg["name"],
                    "distance_nm": dist,
                    "optimized_speed_knots": round(float(v_seg), 2),
                    "optimized_trim_m": round(float(t_seg), 2),
                    "transit_hours": round(float(seg_hours), 1),
                    "fuel_consumed_mt": round(float(seg_fuel_mt), 2),
                    "engine_load_pct": hydro["engine_load_pct"],
                    "wave_height_m": seg["mean_hs_m"]
                })

            total_days = total_hours / 24.0
            lca = calculate_voyage_emissions_and_cost(fuel_type, total_fuel_mt)
            cost_usd = lca["fuel_cost_usd"]
            ghg_wtw_mt = lca["wtw_emissions_mt_co2e"]

            # Multi-objective normalized cost
            f_cost = cost_usd / ref_cost
            f_ghg = ghg_wtw_mt / ref_ghg
            f_time = total_days / ref_time

            # Schedule delay penalty
            eta_delay_days = max(0.0, total_days - target_max_transit_days)
            eta_penalty = (eta_delay_days ** 2) * 5.0

            total_fitness = (
                weight_cost * f_cost +
                weight_emissions * f_ghg +
                weight_time * f_time +
                eta_penalty
            )

            metrics = {
                "total_fuel_mt": total_fuel_mt,
                "total_days": total_days,
                "cost_usd": cost_usd,
                "ghg_wtw_mt": ghg_wtw_mt,
                "direct_co2_mt": lca["direct_co2_mt"],
                "segment_details": segment_details,
                "eta_delay_days": eta_delay_days
            }
            return total_fitness, metrics

        # Initialize Swarm
        particles = np.zeros((self.num_particles, dim))
        for p in range(self.num_particles):
            particles[p] = np.random.uniform(bounds_min, bounds_max)

        pbest = particles.copy()
        pbest_fitness = np.zeros(self.num_particles)
        pbest_metrics = []

        for p in range(self.num_particles):
            fit, met = evaluate_fitness(particles[p])
            pbest_fitness[p] = fit
            pbest_metrics.append(met)

        gbest_idx = int(np.argmin(pbest_fitness))
        gbest = pbest[gbest_idx].copy()
        gbest_fitness = pbest_fitness[gbest_idx]
        gbest_metrics = pbest_metrics[gbest_idx]

        convergence_curve: List[Dict[str, Any]] = []
        tunneling_events_count = 0
        pareto_archive: List[Dict[str, Any]] = []

        # Optimization Loop
        for it in range(self.max_iterations):
            # Dynamic Contraction-Expansion coefficient alpha
            alpha = self.alpha_max - (it / self.max_iterations) * (self.alpha_max - self.alpha_min)

            # Calculate Mean-Best position mbest across swarm
            mbest = np.mean(pbest, axis=0)

            for p in range(self.num_particles):
                phi = np.random.uniform(0.0, 1.0, size=dim)
                # Local stochastic attractor point
                p_attractor = phi * pbest[p] + (1.0 - phi) * gbest

                u = np.random.uniform(0.0, 1.0, size=dim)
                # Random sign (+ or -) with probability 0.5
                sign = np.where(np.random.uniform(0.0, 1.0, size=dim) > 0.5, 1.0, -1.0)

                # Quantum Tunneling delta-potential position update
                # X(t+1) = p +/- alpha * |mbest - X(t)| * ln(1/u)
                particles[p] = p_attractor + sign * alpha * np.abs(mbest - particles[p]) * np.log(1.0 / (u + 1e-9))

                # Boundary clamping
                particles[p] = np.clip(particles[p], bounds_min, bounds_max)

                # Evaluate fitness
                fit, met = evaluate_fitness(particles[p])

                if fit < pbest_fitness[p]:
                    # Check if tunneling occurred (escaped local barrier)
                    if np.linalg.norm(particles[p] - pbest[p]) > (np.linalg.norm(bounds_max - bounds_min) * 0.15):
                        tunneling_events_count += 1
                    pbest[p] = particles[p].copy()
                    pbest_fitness[p] = fit
                    pbest_metrics[p] = met

                    if fit < gbest_fitness:
                        gbest = particles[p].copy()
                        gbest_fitness = fit
                        gbest_metrics = met

                # Add to Pareto archive if non-dominated candidate
                if it % 5 == 0 and len(pareto_archive) < 60:
                    pareto_archive.append({
                        "cost_usd": round(met["cost_usd"], 2),
                        "ghg_wtw_mt": round(met["ghg_wtw_mt"], 2),
                        "transit_days": round(met["total_days"], 2),
                        "avg_speed_knots": round(float(np.mean(particles[p][:num_segments])), 2),
                        "fuel_type": fuel_type
                    })

            convergence_curve.append({
                "iteration": it + 1,
                "best_fitness": round(float(gbest_fitness), 5),
                "best_fuel_mt": round(float(gbest_metrics["total_fuel_mt"]), 2),
                "best_ghg_mt": round(float(gbest_metrics["ghg_wtw_mt"]), 2),
                "best_cost_usd": round(float(gbest_metrics["cost_usd"]), 2),
                "alpha_parameter": round(float(alpha), 3),
                "tunneling_events": tunneling_events_count
            })

        # Calculate final IMO CII rating
        cii_audit = calculate_imo_cii_rating(
            vessel_id=vessel_id,
            total_co2_emissions_mt=gbest_metrics["direct_co2_mt"],
            total_distance_nm=route["total_distance_nm"],
            target_year=2026
        )

        # Calculate Baseline vs Optimized Savings
        baseline_fuel_mt = base_fuel_mt
        optimized_fuel_mt = gbest_metrics["total_fuel_mt"]
        fuel_savings_mt = max(0.0, baseline_fuel_mt - optimized_fuel_mt)
        fuel_savings_pct = (fuel_savings_mt / baseline_fuel_mt) * 100.0 if baseline_fuel_mt > 0 else 0.0

        baseline_ghg_mt = base_lca["wtw_emissions_mt_co2e"]
        optimized_ghg_mt = gbest_metrics["ghg_wtw_mt"]
        ghg_savings_mt = max(0.0, baseline_ghg_mt - optimized_ghg_mt)
        ghg_savings_pct = (ghg_savings_mt / baseline_ghg_mt) * 100.0 if baseline_ghg_mt > 0 else 0.0

        baseline_cost_usd = base_lca["fuel_cost_usd"]
        optimized_cost_usd = gbest_metrics["cost_usd"]
        cost_savings_usd = max(0.0, baseline_cost_usd - optimized_cost_usd)

        # Filter Pareto Frontier to only non-dominated points
        pareto_archive.sort(key=lambda x: x["cost_usd"])
        filtered_pareto: List[Dict[str, Any]] = []
        min_ghg = float("inf")
        for sol in pareto_archive:
            if sol["ghg_wtw_mt"] < min_ghg:
                filtered_pareto.append(sol)
                min_ghg = sol["ghg_wtw_mt"]

        return {
            "vessel_id": vessel_id,
            "vessel_name": vessel["name"],
            "route_id": route_id,
            "route_name": route["name"],
            "fuel_type": fuel_type,
            "total_distance_nm": route["total_distance_nm"],
            "target_transit_days": round(target_max_transit_days, 1),
            "optimized_transit_days": round(gbest_metrics["total_days"], 2),
            "baseline_transit_days": round(base_days, 2),
            "optimized_fuel_mt": round(optimized_fuel_mt, 2),
            "baseline_fuel_mt": round(baseline_fuel_mt, 2),
            "fuel_savings_pct": round(fuel_savings_pct, 1),
            "fuel_savings_mt": round(fuel_savings_mt, 2),
            "optimized_ghg_wtw_mt": round(optimized_ghg_mt, 2),
            "baseline_ghg_wtw_mt": round(baseline_ghg_mt, 2),
            "ghg_savings_pct": round(ghg_savings_pct, 1),
            "optimized_cost_usd": round(optimized_cost_usd, 2),
            "baseline_cost_usd": round(baseline_cost_usd, 2),
            "cost_savings_usd": round(cost_savings_usd, 2),
            "average_speed_knots": round(float(np.mean(gbest[:num_segments])), 2),
            "segments_breakdown": gbest_metrics["segment_details"],
            "convergence_history": convergence_curve,
            "quantum_tunneling_events_total": tunneling_events_count,
            "pareto_frontier": filtered_pareto,
            "imo_cii_audit": cii_audit
        }

# Global Singleton Instance
qpso_optimizer = QPSOOptimizer()
