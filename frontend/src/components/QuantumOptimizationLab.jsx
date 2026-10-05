import React, { useState } from 'react';
import {
  Play,
  Settings2,
  TrendingDown,
  DollarSign,
  Clock,
  Flame,
  Award,
  ArrowRight,
  ShieldCheck,
  Zap,
  RotateCcw
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';
import QuantumVisualizer from './QuantumVisualizer';
import { api } from '../services/api';

export default function QuantumOptimizationLab({ db }) {
  const [selectedVessel, setSelectedVessel] = useState('container_15000_teu');
  const [selectedRoute, setSelectedRoute] = useState('shanghai_rotterdam');
  const [selectedFuel, setSelectedFuel] = useState('VLSFO');

  const [weightCost, setWeightCost] = useState(0.4);
  const [weightEmissions, setWeightEmissions] = useState(0.4);
  const [weightTime, setWeightTime] = useState(0.2);

  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optResults, setOptResults] = useState(null);

  // Normalize weights
  const handleWeightChange = (type, val) => {
    const v = parseFloat(val);
    if (type === 'cost') setWeightCost(v);
    if (type === 'emissions') setWeightEmissions(v);
    if (type === 'time') setWeightTime(v);
  };

  const handleRunOptimization = async () => {
    setIsOptimizing(true);
    try {
      const res = await api.optimizeRoute({
        vessel_id: selectedVessel,
        route_id: selectedRoute,
        fuel_type: selectedFuel,
        weight_cost: weightCost,
        weight_emissions: weightEmissions,
        weight_time: weightTime
      });
      setOptResults(res);
    } catch (err) {
      console.error('Optimization failed', err);
    } finally {
      setIsOptimizing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner / Parameters Control */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-300 flex items-center gap-2">
              <Zap className="w-5 h-5 text-cyan-400" /> Quantum Particle Swarm Optimization (QPSO)
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Multi-segment trajectory speed profiling & trim optimization with quantum delta-potential tunneling.
            </p>
          </div>

          <button
            onClick={handleRunOptimization}
            disabled={isOptimizing}
            className="flex items-center justify-center space-x-2 px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold rounded-xl shadow-lg shadow-cyan-500/25 transition-all transform active:scale-95 disabled:opacity-50"
          >
            {isOptimizing ? (
              <>
                <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                <span>Tunneling Trajectories...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Execute QPSO Optimization</span>
              </>
            )}
          </button>
        </div>

        {/* Configuration Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Target Vessel</label>
            <select
              value={selectedVessel}
              onChange={(e) => setSelectedVessel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-cyan-300 focus:outline-none focus:border-cyan-500"
            >
              {db.vessels &&
                Object.entries(db.vessels).map(([id, v]) => (
                  <option key={id} value={id}>
                    {v.name} ({v.type})
                  </option>
                ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Maritime Trade Route</label>
            <select
              value={selectedRoute}
              onChange={(e) => setSelectedRoute(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-cyan-300 focus:outline-none focus:border-cyan-500"
            >
              {db.routes &&
                Object.entries(db.routes).map(([id, r]) => (
                  <option key={id} value={id}>
                    {r.name} ({r.total_distance_nm} NM)
                  </option>
                ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Bunker Fuel Selection</label>
            <select
              value={selectedFuel}
              onChange={(e) => setSelectedFuel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-cyan-300 focus:outline-none focus:border-cyan-500"
            >
              {db.fuels &&
                Object.keys(db.fuels).map((f) => (
                  <option key={f} value={f}>
                    {f}
                  </option>
                ))}
            </select>
          </div>
        </div>

        {/* Multi-Objective Sliders */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-slate-300 flex items-center gap-1.5">
              <Settings2 className="w-3.5 h-3.5 text-cyan-400" /> Multi-Objective Weighting Function
            </span>
            <span className="text-[11px] font-mono text-slate-500">
              f(x) = {weightCost}·Cost + {weightEmissions}·GHG + {weightTime}·ETA
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-400">OPEX / Fuel Cost Weight</span>
                <span className="text-cyan-400">{(weightCost * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightCost}
                onChange={(e) => handleWeightChange('cost', e.target.value)}
                className="w-full accent-cyan-400 h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-400">Well-to-Wake Emissions</span>
                <span className="text-teal-400">{(weightEmissions * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightEmissions}
                onChange={(e) => handleWeightChange('emissions', e.target.value)}
                className="w-full accent-teal-400 h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-400">Schedule & ETA Strictness</span>
                <span className="text-blue-400">{(weightTime * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightTime}
                onChange={(e) => handleWeightChange('time', e.target.value)}
                className="w-full accent-blue-400 h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Quantum State & Delta Potential Visualization */}
      <QuantumVisualizer
        tunnelingEvents={optResults ? optResults.quantum_tunneling_events_total : 68}
        alpha={0.52}
      />

      {/* Results Dashboard */}
      {optResults && (
        <div className="space-y-6 animate-in fade-in duration-300">
          {/* KPI Metrics Row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                <Flame className="w-4 h-4 text-amber-400" /> Fuel Saved
              </span>
              <div className="text-2xl font-bold text-amber-400 font-mono mt-1">
                {optResults.fuel_savings_mt} <span className="text-xs text-slate-400">MT</span>
              </div>
              <span className="text-[11px] text-emerald-400 font-semibold font-mono">
                ↓ {optResults.fuel_savings_pct}% vs baseline
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                <DollarSign className="w-4 h-4 text-emerald-400" /> Voyage OPEX Saved
              </span>
              <div className="text-2xl font-bold text-emerald-400 font-mono mt-1">
                ${(optResults.cost_savings_usd / 1000).toFixed(1)}k
              </div>
              <span className="text-[11px] text-slate-400 font-mono">
                Total: ${(optResults.optimized_cost_usd / 1000).toFixed(1)}k
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                <TrendingDown className="w-4 h-4 text-teal-400" /> WtW GHG Abated
              </span>
              <div className="text-2xl font-bold text-teal-300 font-mono mt-1">
                {optResults.ghg_savings_mt} <span className="text-xs text-slate-400">MT CO2e</span>
              </div>
              <span className="text-[11px] text-teal-400 font-mono">
                ↓ {optResults.ghg_savings_pct}% Lifecycle Cut
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                <ShieldCheck className="w-4 h-4 text-cyan-400" /> IMO CII Rating
              </span>
              <div className="flex items-center space-x-2 mt-1">
                <span className="text-2xl font-bold text-cyan-300 font-mono">
                  Grade {optResults.imo_cii_audit.cii_rating}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  {optResults.imo_cii_audit.compliance_status}
                </span>
              </div>
              <span className="text-[11px] text-slate-400 font-mono">
                Attained: {optResults.imo_cii_audit.attained_cii.toFixed(2)} gCO2/dwt·nm
              </span>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* 1. QPSO Convergence History */}
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-slate-200 font-mono flex items-center gap-2 mb-3">
                <TrendingDown className="w-4 h-4 text-cyan-400" /> Quantum Swarm Convergence History
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={optResults.convergence_history}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="iteration" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} domain={['auto', 'auto']} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                      itemStyle={{ color: '#38bdf8', fontSize: '12px' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="best_fitness"
                      stroke="#06b6d4"
                      strokeWidth={2.5}
                      dot={false}
                      name="Fitness (Cost/GHG)"
                    />
                    <Line
                      type="monotone"
                      dataKey="mean_fitness"
                      stroke="#475569"
                      strokeWidth={1.5}
                      strokeDasharray="3 3"
                      dot={false}
                      name="Swarm Mean"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* 2. Multi-Objective Pareto Frontier */}
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-slate-200 font-mono flex items-center gap-2 mb-3">
                <Award className="w-4 h-4 text-teal-400" /> Non-Dominated Pareto Frontier (Cost vs GHG)
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis
                      type="number"
                      dataKey="cost_usd"
                      name="Cost ($)"
                      stroke="#64748b"
                      fontSize={11}
                      unit="$"
                      tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                    />
                    <YAxis
                      type="number"
                      dataKey="ghg_mt"
                      name="GHG"
                      stroke="#64748b"
                      fontSize={11}
                      unit=" MT"
                    />
                    <Tooltip
                      cursor={{ strokeDasharray: '3 3' }}
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    />
                    <Scatter name="Pareto Points" data={optResults.pareto_frontier} fill="#14b8a6" />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Segment Speed & Trim Trajectory Table */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 overflow-hidden">
            <h3 className="text-sm font-bold text-slate-200 font-mono flex items-center gap-2 mb-3">
              <Clock className="w-4 h-4 text-cyan-400" /> Optimal Segment-by-Segment Speed & Trim Profile
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-3">Segment</th>
                    <th className="p-3">Sea Area</th>
                    <th className="p-3">Distance</th>
                    <th className="p-3">Opt Speed</th>
                    <th className="p-3">Opt Trim</th>
                    <th className="p-3">Sea State (Hs / Wind)</th>
                    <th className="p-3">Power (kW)</th>
                    <th className="p-3">FOC (MT/day)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-slate-300">
                  {optResults.segment_profiles.map((seg) => (
                    <tr key={seg.segment_idx} className="hover:bg-slate-800/40">
                      <td className="p-3 font-semibold text-cyan-400">#{seg.segment_idx + 1}</td>
                      <td className="p-3">{seg.segment_name}</td>
                      <td className="p-3">{seg.distance_nm} NM</td>
                      <td className="p-3 text-teal-300 font-bold">{seg.speed_knots} kn</td>
                      <td className="p-3">{seg.trim_m > 0 ? `+${seg.trim_m}` : seg.trim_m} m</td>
                      <td className="p-3 text-slate-400">
                        {seg.weather.hs_m}m / {seg.weather.wind_knots}kn
                      </td>
                      <td className="p-3">{seg.power_kw.toLocaleString()} kW</td>
                      <td className="p-3 text-amber-300 font-bold">{seg.foc_mt_day} MT</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
