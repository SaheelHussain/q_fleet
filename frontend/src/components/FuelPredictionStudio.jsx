import React, { useState } from 'react';
import { Flame, Wind, Waves, Thermometer, Play } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../services/api';

export default function FuelPredictionStudio({ db }) {
  const [form, setForm] = useState({
    vessel_id: 'container_15000_teu',
    speed_knots: 20.0,
    draft_m: 14.5,
    trim_m: 0.0,
    hs_m: 1.8,
    tp_s: 7.5,
    wind_speed_knots: 16.0,
    wind_angle_deg: 30.0,
    fuel_type: 'VLSFO',
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (key, val) => setForm((f) => ({ ...f, [key]: val }));

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await api.predictFuel({ ...form });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fuelComparisonData = result
    ? [
        { fuel: 'VLSFO', wtw: result.physical_components.calm_water_foc_mt_day * 3.17, color: '#64748b' },
        { fuel: 'LNG', wtw: result.physical_components.calm_water_foc_mt_day * 2.75, color: '#38bdf8' },
        { fuel: 'e-Methanol', wtw: result.physical_components.calm_water_foc_mt_day * 0.18, color: '#34d399' },
        { fuel: 'Gr. Ammonia', wtw: result.physical_components.calm_water_foc_mt_day * 0.02, color: '#6ee7b7' },
      ]
    : [];

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-400 flex items-center gap-2">
              <Flame className="w-5 h-5 text-amber-400" /> Q-PINN Dynamic Fuel Prediction Studio
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Physics-Informed Quantum ML predictor combining Holtrop-Mennen resistance with Pauli-Z quantum feature encoding.
            </p>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="flex items-center space-x-2 px-5 py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-bold rounded-xl shadow-md shadow-amber-500/20 transition-all active:scale-95 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                <span>Predicting...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Predict FOC</span>
              </>
            )}
          </button>
        </div>

        {/* Input Controls */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
          {[
            { label: 'Speed', key: 'speed_knots', unit: 'kn', min: 5, max: 30, step: 0.5 },
            { label: 'Draft', key: 'draft_m', unit: 'm', min: 4, max: 25, step: 0.5 },
            { label: 'Trim', key: 'trim_m', unit: 'm', min: -2, max: 3, step: 0.1 },
            { label: 'Wave Hs', key: 'hs_m', unit: 'm', min: 0, max: 12, step: 0.1 },
            { label: 'Wind Speed', key: 'wind_speed_knots', unit: 'kn', min: 0, max: 80, step: 1 },
          ].map(({ label, key, unit, min, max, step }) => (
            <div key={key} className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <label className="text-[11px] text-slate-500 font-mono block mb-2">
                {label} ({unit})
              </label>
              <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={form[key]}
                onChange={(e) => handleChange(key, parseFloat(e.target.value))}
                className="w-full accent-amber-400 h-1 bg-slate-800 rounded-full appearance-none cursor-pointer mb-2"
              />
              <span className="text-sm font-bold font-mono text-amber-300">
                {form[key]} {unit}
              </span>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Vessel Class</label>
            <select
              value={form.vessel_id}
              onChange={(e) => handleChange('vessel_id', e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-amber-300 focus:outline-none focus:border-amber-500"
            >
              {db.vessels &&
                Object.entries(db.vessels).map(([id, v]) => (
                  <option key={id} value={id}>
                    {v.name}
                  </option>
                ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Fuel Type</label>
            <select
              value={form.fuel_type}
              onChange={(e) => handleChange('fuel_type', e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-amber-300 focus:outline-none focus:border-amber-500"
            >
              {db.fuels && Object.keys(db.fuels).map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Prediction Results */}
        {result && (
          <div className="mt-6 space-y-5 animate-in fade-in duration-300">
            {/* Headline KPIs */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-amber-950/40 to-orange-950/40 border border-amber-800/40 p-4 rounded-xl">
                <div className="text-[11px] text-amber-400 font-mono">Predicted FOC</div>
                <div className="text-2xl font-bold text-white font-mono mt-1">
                  {result.predicted_foc_mt_day} <span className="text-xs text-amber-300">MT/day</span>
                </div>
              </div>

              <div className="bg-slate-950/40 border border-slate-800 p-4 rounded-xl">
                <div className="text-[11px] text-slate-400 font-mono">Engine Power</div>
                <div className="text-2xl font-bold text-orange-300 font-mono mt-1">
                  {result.engine_power_kw.toLocaleString()} <span className="text-xs text-slate-400">kW</span>
                </div>
              </div>

              <div className="bg-slate-950/40 border border-slate-800 p-4 rounded-xl">
                <div className="text-[11px] text-slate-400 font-mono">Q-PINN Confidence</div>
                <div className="text-2xl font-bold text-teal-300 font-mono mt-1">
                  {result.model_confidence_pct}%
                </div>
              </div>

              <div className="bg-slate-950/40 border border-slate-800 p-4 rounded-xl">
                <div className="text-[11px] text-slate-400 font-mono">WtW Emissions Rate</div>
                <div className="text-2xl font-bold text-red-300 font-mono mt-1">
                  {result.wtw_emissions_kg_per_nm} <span className="text-xs text-slate-400">kgCO2e/nm</span>
                </div>
              </div>
            </div>

            {/* Fuel Emissions Comparison Chart */}
            <div className="bg-slate-950 p-5 rounded-xl border border-slate-800">
              <h3 className="text-sm font-bold text-slate-200 font-mono mb-4">
                Cross-Fuel WtW Emission Intensity Comparison (Voyage Conditions)
              </h3>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={fuelComparisonData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                    <XAxis type="number" stroke="#64748b" fontSize={11} />
                    <YAxis type="category" dataKey="fuel" stroke="#64748b" fontSize={11} width={90} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    />
                    <Bar dataKey="wtw" fill="#f59e0b" radius={[0, 4, 4, 0]} name="WtW CO2e/day (MT)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
