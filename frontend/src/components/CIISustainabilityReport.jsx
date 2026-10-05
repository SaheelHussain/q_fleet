import React, { useState } from 'react';
import { ShieldCheck, Download, AlertTriangle, CheckCircle2, TrendingUp, HelpCircle } from 'lucide-react';
import { api } from '../services/api';

export default function CIISustainabilityReport({ db }) {
  const [vessel, setVessel] = useState('container_15000_teu');
  const [co2, setCo2] = useState(4800);
  const [dist, setDist] = useState(10520);
  const [year, setYear] = useState(2026);
  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAudit = async () => {
    setLoading(true);
    try {
      const res = await api.auditCII({
        vessel_id: vessel,
        total_co2_emissions_mt: co2,
        total_distance_nm: dist,
        target_year: year,
      });
      setAudit(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const ciiGrades = ['A', 'B', 'C', 'D', 'E'];
  const gradeColors = {
    A: 'bg-emerald-500 text-slate-950',
    B: 'bg-teal-500 text-slate-950',
    C: 'bg-amber-400 text-slate-950',
    D: 'bg-orange-500 text-slate-950',
    E: 'bg-red-600 text-white',
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-cyan-300 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-teal-400" /> IMO CII Rating Auditor & EU ETS Liability Tracker
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Official MEPC.337(76) Operational Carbon Intensity Indicator rating & European Maritime ETS tax exposure.
            </p>
          </div>

          <button
            onClick={handleAudit}
            disabled={loading}
            className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-cyan-500 text-slate-950 font-bold rounded-xl shadow-lg shadow-teal-500/20 text-xs transition-all active:scale-95 disabled:opacity-50"
          >
            {loading ? 'Auditing CII...' : 'Run Compliance Audit'}
          </button>
        </div>

        {/* Inputs */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Vessel Class</label>
            <select
              value={vessel}
              onChange={(e) => setVessel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-teal-300 focus:outline-none focus:border-teal-500"
            >
              {db.vessels && Object.entries(db.vessels).map(([id, v]) => (
                <option key={id} value={id}>{v.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Voyage CO2 (MT)</label>
            <input
              type="number"
              value={co2}
              onChange={(e) => setCo2(parseFloat(e.target.value))}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            />
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Distance (NM)</label>
            <input
              type="number"
              value={dist}
              onChange={(e) => setDist(parseFloat(e.target.value))}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            />
          </div>
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Target Compliance Year</label>
            <select
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-teal-300 focus:outline-none focus:border-teal-500"
            >
              {[2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030].map((y) => (
                <option key={y} value={y}>{y} (Z={((y - 2019) * 2).toFixed(0)}%)</option>
              ))}
            </select>
          </div>
        </div>

        {/* Audit Results */}
        {audit && (
          <div className="space-y-6 animate-in fade-in duration-300">
            {/* CII Rating Badge Bar */}
            <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="flex items-center space-x-6">
                <div className="flex flex-col items-center">
                  <span className="text-[10px] text-slate-500 font-mono mb-1">IMO CII RATING</span>
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center font-black text-3xl shadow-lg ${gradeColors[audit.cii_rating_audit.cii_rating]}`}>
                    {audit.cii_rating_audit.cii_rating}
                  </div>
                </div>

                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-lg font-bold text-slate-200">
                      Grade {audit.cii_rating_audit.cii_rating} — {audit.cii_rating_audit.rating_label}
                    </span>
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono">
                      {audit.cii_rating_audit.compliance_status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Attained: <b className="text-teal-300 font-mono">{audit.cii_rating_audit.attained_cii.toFixed(3)}</b> gCO2/dwt·nm | Required: <b className="text-slate-200 font-mono">{audit.cii_rating_audit.required_cii.toFixed(3)}</b>
                  </p>
                </div>
              </div>

              {/* CII Grade Spectrum */}
              <div className="flex space-x-1.5 bg-slate-900 p-2 rounded-xl border border-slate-800">
                {ciiGrades.map((g) => (
                  <div
                    key={g}
                    className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs ${
                      g === audit.cii_rating_audit.cii_rating
                        ? gradeColors[g] + ' scale-110 shadow-md ring-2 ring-white/50'
                        : 'bg-slate-800 text-slate-500'
                    }`}
                  >
                    {g}
                  </div>
                ))}
              </div>
            </div>

            {/* EU ETS Carbon Tax Card */}
            <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800">
              <h3 className="text-sm font-bold text-slate-200 font-mono mb-4">
                European Union Emissions Trading System (EU ETS) Tax Exposure
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-slate-900 p-3 rounded-lg">
                  <span className="text-[10px] text-slate-500 font-mono block">EUA Carbon Price</span>
                  <span className="text-lg font-bold text-cyan-300 font-mono">
                    ${audit.eu_ets_liability.eua_price_eur_per_mt}/MT
                  </span>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg">
                  <span className="text-[10px] text-slate-500 font-mono block">Surrender Coverage</span>
                  <span className="text-lg font-bold text-slate-200 font-mono">
                    {(audit.eu_ets_liability.scope_factor * 100).toFixed(0)}% (Phase-In: {(audit.eu_ets_liability.phase_in_rate * 100).toFixed(0)}%)
                  </span>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg">
                  <span className="text-[10px] text-slate-500 font-mono block">Surrender Liability</span>
                  <span className="text-lg font-bold text-amber-300 font-mono">
                    {audit.eu_ets_liability.taxable_co2e_mt.toFixed(1)} MT
                  </span>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg">
                  <span className="text-[10px] text-slate-500 font-mono block">Total ETS Tax</span>
                  <span className="text-lg font-bold text-red-400 font-mono">
                    ${audit.eu_ets_liability.total_ets_tax_usd.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
