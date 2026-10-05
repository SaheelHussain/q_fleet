import React, { useState } from 'react';
import { BarChart3, Zap, Play, TrendingUp } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { api } from '../services/api';

export default function BenchmarkArena({ db }) {
  const [vessel, setVessel] = useState('container_15000_teu');
  const [route, setRoute] = useState('singapore_dubai');
  const [fuel, setFuel] = useState('VLSFO');
  const [iterations, setIterations] = useState(80);
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState(null);

  const handleRun = async () => {
    setRunning(true);
    try {
      const res = await api.runBenchmark({ vessel_id: vessel, route_id: route, fuel_type: fuel, iterations });
      setResults(res);
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  // Merge convergence curves for unified chart
  const convergenceChartData =
    results
      ? results.quantum_qpso.convergence_curve.map((qp, idx) => ({
          iteration: qp.iteration,
          QPSO: qp.fitness,
          ClassicalPSO: results.classical_pso.convergence_curve[idx]?.best_fitness ?? null,
          ClassicalGA: results.classical_ga.convergence_curve[idx]?.best_fitness ?? null,
        }))
      : [];

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-violet-400 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-purple-400" /> Quantum vs Classical Algorithm Benchmark Arena
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Head-to-head convergence race: QPSO vs Classical PSO vs Classical GA optimization algorithms.
            </p>
          </div>
          <button
            onClick={handleRun}
            disabled={running}
            className="flex items-center space-x-2 px-5 py-2.5 bg-gradient-to-r from-purple-500 to-violet-500 hover:from-purple-400 hover:to-violet-400 text-white font-bold rounded-xl shadow-lg shadow-purple-500/25 transition-all active:scale-95 disabled:opacity-50"
          >
            {running ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Racing Algorithms...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Start Benchmark Race</span>
              </>
            )}
          </button>
        </div>

        {/* Config Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Vessel</label>
            <select
              value={vessel}
              onChange={(e) => setVessel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-purple-300 focus:outline-none focus:border-purple-500"
            >
              {db.vessels && Object.entries(db.vessels).map(([id, v]) => (
                <option key={id} value={id}>{v.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Route</label>
            <select
              value={route}
              onChange={(e) => setRoute(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-purple-300 focus:outline-none focus:border-purple-500"
            >
              {db.routes && Object.entries(db.routes).map(([id, r]) => (
                <option key={id} value={id}>{r.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Fuel</label>
            <select
              value={fuel}
              onChange={(e) => setFuel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-purple-300 focus:outline-none focus:border-purple-500"
            >
              {db.fuels && Object.keys(db.fuels).map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Iterations</label>
            <input
              type="number"
              value={iterations}
              min="20"
              max="200"
              onChange={(e) => setIterations(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-purple-300 font-mono focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        {/* Results */}
        {results && (
          <div className="space-y-6 animate-in fade-in duration-300">
            {/* Algorithm Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {/* QPSO Card */}
              <div className="bg-gradient-to-br from-cyan-950/40 to-teal-950/40 border border-cyan-600/40 rounded-2xl p-5 shadow-lg shadow-cyan-900/20">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 bg-cyan-900/50 rounded-lg"><Zap className="w-5 h-5 text-cyan-400" /></div>
                  <span className="text-xs px-2 py-0.5 bg-emerald-950/60 text-emerald-300 border border-emerald-800/50 rounded-full font-mono">WINNER</span>
                </div>
                <h3 className="text-sm font-bold text-cyan-300 font-mono mb-4">{results.quantum_qpso.name}</h3>
                <table className="w-full text-xs font-mono">
                  <tbody className="divide-y divide-slate-800">
                    <tr>
                      <td className="py-1.5 text-slate-400">Fuel Saved</td>
                      <td className="py-1.5 text-right text-emerald-300 font-semibold">{results.quantum_qpso.fuel_savings_pct}%</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">GHG Reduced</td>
                      <td className="py-1.5 text-right text-teal-300 font-semibold">{results.quantum_qpso.ghg_reduction_pct}%</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Conv. Iterations</td>
                      <td className="py-1.5 text-right text-cyan-300 font-semibold">{results.quantum_qpso.iterations_to_optimum}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Tunneling Events</td>
                      <td className="py-1.5 text-right text-amber-300 font-semibold">{results.quantum_qpso.tunneling_events}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Runtime</td>
                      <td className="py-1.5 text-right text-slate-200">{results.quantum_qpso.runtime_ms} ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Classical PSO Card */}
              <div className="bg-slate-950 border border-slate-700/60 rounded-2xl p-5">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 bg-slate-800 rounded-lg"><BarChart3 className="w-5 h-5 text-slate-400" /></div>
                </div>
                <h3 className="text-sm font-bold text-slate-300 font-mono mb-4">{results.classical_pso.name}</h3>
                <table className="w-full text-xs font-mono">
                  <tbody className="divide-y divide-slate-800">
                    <tr>
                      <td className="py-1.5 text-slate-400">Best Fitness</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_pso.best_fitness?.toFixed(4)}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Conv. Iterations</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_pso.iterations_to_optimum}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Runtime</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_pso.runtime_ms} ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Classical GA Card */}
              <div className="bg-slate-950 border border-slate-700/60 rounded-2xl p-5">
                <div className="p-2 bg-slate-800 rounded-lg inline-block mb-3"><TrendingUp className="w-5 h-5 text-slate-400" /></div>
                <h3 className="text-sm font-bold text-slate-300 font-mono mb-4">{results.classical_ga.name}</h3>
                <table className="w-full text-xs font-mono">
                  <tbody className="divide-y divide-slate-800">
                    <tr>
                      <td className="py-1.5 text-slate-400">Best Fitness</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_ga.best_fitness?.toFixed(4)}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Conv. Iterations</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_ga.iterations_to_optimum}</td>
                    </tr>
                    <tr>
                      <td className="py-1.5 text-slate-400">Runtime</td>
                      <td className="py-1.5 text-right text-slate-200">{results.classical_ga.runtime_ms} ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Summary Banner */}
            <div className="bg-gradient-to-r from-cyan-950/30 to-teal-950/30 border border-cyan-700/30 rounded-2xl p-5 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <span className="text-[10px] text-slate-500 font-mono block">Convergence Speedup</span>
                <span className="text-2xl font-bold text-cyan-300 font-mono">{results.summary_metrics.convergence_speedup_vs_cpso}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 font-mono block">Fuel Saved by QPSO</span>
                <span className="text-2xl font-bold text-amber-300 font-mono">{results.summary_metrics.qpso_fuel_savings_mt} MT</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 font-mono block">Cost Savings</span>
                <span className="text-2xl font-bold text-emerald-300 font-mono">${(results.summary_metrics.qpso_cost_savings_usd / 1000).toFixed(1)}k</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 font-mono block">Pareto Solutions Found</span>
                <span className="text-2xl font-bold text-violet-300 font-mono">{results.summary_metrics.pareto_solutions_found}</span>
              </div>
            </div>

            {/* Convergence Race Chart */}
            <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800">
              <h3 className="text-sm font-bold text-slate-200 font-mono mb-4">
                Algorithm Convergence Race — Fitness vs Iteration
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={convergenceChartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="iteration" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} domain={["auto", "auto"]} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="QPSO" stroke="#06b6d4" strokeWidth={2.5} dot={false} name="QPSO (Quantum)" />
                    <Line type="monotone" dataKey="ClassicalPSO" stroke="#94a3b8" strokeWidth={1.5} dot={false} strokeDasharray="4 4" name="Classical PSO" />
                    <Line type="monotone" dataKey="ClassicalGA" stroke="#475569" strokeWidth={1.5} dot={false} strokeDasharray="4 4" name="Classical GA" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
