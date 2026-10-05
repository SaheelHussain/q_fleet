import React, { useState } from 'react';
import { Layers, PlugZap, RefreshCcw, DollarSign, Leaf, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';

export default function GreenFleetStudio({ db }) {
  const [auxPower, setAuxPower] = useState(3500);
  const [berthHours, setBerthHours] = useState(36);
  const [gridFactor, setGridFactor] = useState(0.28);
  const [elecPrice, setElecPrice] = useState(0.16);

  const [coldIroningRes, setColdIroningRes] = useState(null);
  const [calculating, setCalculating] = useState(false);

  const handleCalculateColdIroning = async () => {
    setCalculating(true);
    try {
      const res = await api.auditColdIroning({
        aux_power_kw: auxPower,
        berth_hours: berthHours,
        grid_emission_factor_kg_kwh: gridFactor,
        electricity_price_usd_per_kwh: elecPrice,
      });
      setColdIroningRes(res);
    } catch (e) {
      console.error(e);
    } finally {
      setCalculating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 flex items-center gap-2">
              <Layers className="w-5 h-5 text-emerald-400" /> Green Fuel LCA & Port Cold-Ironing Studio
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Well-to-Wake lifecycle carbon accounting, alternative propulsion retrofit feasibility, and shore power optimization.
            </p>
          </div>
        </div>

        {/* 1. Marine Fuel Lifecycle Profiles */}
        <div className="mb-8">
          <h3 className="text-sm font-bold text-slate-200 font-mono mb-3 flex items-center gap-2">
            <Leaf className="w-4 h-4 text-emerald-400" /> Alternative Marine Fuel LCA Catalog (IMO Decarbonization Trajectory)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {db.fuels &&
              Object.entries(db.fuels).map(([key, f]) => (
                <div key={key} className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-emerald-300">{key}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                      ${f.price_usd_per_mt}/MT
                    </span>
                  </div>
                  <div className="mt-3 space-y-1 text-[11px] font-mono text-slate-400">
                    <div className="flex justify-between">
                      <span>Energy Density:</span>
                      <span className="text-slate-200">{f.lhv_mj_kg} MJ/kg</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Well-to-Tank:</span>
                      <span className="text-slate-200">{f.wt_t_co2e_factor} gCO2e/g</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Tank-to-Wake:</span>
                      <span className="text-slate-200">{f.tt_w_co2e_factor} gCO2e/g</span>
                    </div>
                    <div className="flex justify-between font-semibold text-emerald-400 pt-1 border-t border-slate-800">
                      <span>Total WtW Factor:</span>
                      <span>{(f.wt_t_co2e_factor + f.tt_w_co2e_factor).toFixed(2)} gCO2e/g</span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* 2. Port Cold-Ironing (Shore Power) Configurator */}
        <div className="bg-slate-950 p-5 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-slate-200 font-mono flex items-center gap-2">
              <PlugZap className="w-4 h-4 text-cyan-400" /> Port Berth Cold-Ironing (Shore Power) Calculator
            </h3>
            <button
              onClick={handleCalculateColdIroning}
              disabled={calculating}
              className="px-4 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold rounded-lg text-xs transition-all disabled:opacity-50"
            >
              {calculating ? 'Auditing...' : 'Evaluate Berth Benefits'}
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <label className="text-[10px] text-slate-500 font-mono block mb-1">Auxiliary Power (kW)</label>
              <input
                type="number"
                value={auxPower}
                onChange={(e) => setAuxPower(parseFloat(e.target.value))}
                className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-cyan-300 font-mono"
              />
            </div>
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <label className="text-[10px] text-slate-500 font-mono block mb-1">Berth Duration (Hours)</label>
              <input
                type="number"
                value={berthHours}
                onChange={(e) => setBerthHours(parseFloat(e.target.value))}
                className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-cyan-300 font-mono"
              />
            </div>
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <label className="text-[10px] text-slate-500 font-mono block mb-1">Grid EF (kgCO2/kWh)</label>
              <input
                type="number"
                step="0.05"
                value={gridFactor}
                onChange={(e) => setGridFactor(parseFloat(e.target.value))}
                className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-cyan-300 font-mono"
              />
            </div>
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <label className="text-[10px] text-slate-500 font-mono block mb-1">Grid Price ($/kWh)</label>
              <input
                type="number"
                step="0.01"
                value={elecPrice}
                onChange={(e) => setElecPrice(parseFloat(e.target.value))}
                className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-cyan-300 font-mono"
              />
            </div>
          </div>

          {coldIroningRes && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-slate-800">
              <div className="bg-slate-900 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Diesel Fuel Saved</span>
                <span className="text-base font-bold text-amber-300 font-mono">{coldIroningRes.fuel_saved_mgo_mt} MT</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Net Port GHG Cut</span>
                <span className="text-base font-bold text-emerald-300 font-mono">{coldIroningRes.net_co2e_reduction_mt} MT CO2e</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Net Cost Savings</span>
                <span className="text-base font-bold text-cyan-300 font-mono">${coldIroningRes.net_cost_savings_usd.toLocaleString()}</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">GHG Abatement %</span>
                <span className="text-base font-bold text-teal-300 font-mono">{coldIroningRes.emission_reduction_pct}%</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
