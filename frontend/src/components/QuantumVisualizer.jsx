import React, { useState, useEffect } from 'react';
import { Atom, Zap, ShieldAlert, Sparkles } from 'lucide-react';

export default function QuantumVisualizer({ tunnelingEvents = 42, alpha = 0.65 }) {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPhase((prev) => (prev + 0.05) % (Math.PI * 2));
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // Compute Bloch Vector Coordinates
  const theta = Math.PI / 3 + Math.sin(phase) * 0.2;
  const phi = phase;
  const r = 50;
  const bx = r * Math.sin(theta) * Math.cos(phi);
  const by = r * Math.cos(theta); // Vertical (Z-axis)
  const bz = r * Math.sin(theta) * Math.sin(phi);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-950/80 p-5 rounded-2xl border border-cyan-500/30 shadow-xl shadow-cyan-950/30 backdrop-blur-md">
      {/* 1. Bloch Sphere Visualizer */}
      <div className="flex flex-col items-center justify-center p-4 bg-slate-900/60 rounded-xl border border-slate-800 relative overflow-hidden">
        <div className="absolute top-2 left-3 flex items-center space-x-1.5">
          <Atom className="w-4 h-4 text-cyan-400 animate-spin" style={{ animationDuration: '8s' }} />
          <span className="text-xs font-mono font-semibold text-cyan-300">Qubit State Space (Bloch Sphere)</span>
        </div>

        <svg viewBox="-80 -80 160 160" className="w-48 h-48 my-2">
          {/* Sphere Outline */}
          <circle cx="0" cy="0" r={r} fill="none" stroke="#1e293b" strokeWidth="1.5" />
          <ellipse cx="0" cy="0" rx={r} ry={r * 0.35} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="2,2" />

          {/* Coordinate Axes */}
          <line x1="0" y1={-r - 12} x2="0" y2={r + 12} stroke="#475569" strokeWidth="1" />
          <line x1={-r - 12} y1="0" x2={r + 12} y2="0" stroke="#475569" strokeWidth="1" />

          {/* State Labels */}
          <text x="5" y={-r - 4} fill="#38bdf8" fontSize="10" fontFamily="monospace">|0⟩ (Optimal Speed)</text>
          <text x="5" y={r + 14} fill="#94a3b8" fontSize="10" fontFamily="monospace">|1⟩ (Excess FOC)</text>

          {/* Bloch Vector State */}
          <line
            x1="0"
            y1="0"
            x2={bx}
            y2={-by}
            stroke="#06b6d4"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          <circle cx={bx} cy={-by} r="4.5" fill="#22d3ee" className="animate-ping" style={{ transformOrigin: `${bx}px ${-by}px` }} />
          <circle cx={bx} cy={-by} r="3.5" fill="#a5f3fc" />
        </svg>

        <div className="w-full flex justify-between items-center text-[11px] font-mono text-slate-400 px-2 mt-1">
          <span>|Ψ⟩ = α|0⟩ + β|1⟩</span>
          <span className="text-cyan-400">Prob(|0⟩) = {(Math.cos(theta / 2) ** 2 * 100).toFixed(1)}%</span>
        </div>
      </div>

      {/* 2. Quantum Delta Potential Well & Tunneling */}
      <div className="flex flex-col justify-between p-4 bg-slate-900/60 rounded-xl border border-slate-800">
        <div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1.5">
              <Zap className="w-4 h-4 text-teal-400" />
              <span className="text-xs font-mono font-semibold text-teal-300">Delta-Potential Well Mechanics</span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60 font-mono">
              α-Annealing: {alpha.toFixed(2)}
            </span>
          </div>

          <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
            Unlike classical gradient trapping, particles sample wavefunctions <code className="text-cyan-300">ψ(x) ~ exp(-|x-p|/L)</code>, allowing instant quantum tunneling across high hydrodynamic resistance barriers.
          </p>
        </div>

        {/* Energy Landscape SVG */}
        <div className="my-2 bg-slate-950 p-2 rounded-lg border border-slate-800 relative">
          <svg viewBox="0 0 240 70" className="w-full h-16">
            {/* Multi-modal Potential Landscape */}
            <path
              d="M 10 35 Q 40 5, 70 45 Q 100 65, 130 20 Q 160 -10, 190 50 Q 215 65, 230 35"
              fill="none"
              stroke="#475569"
              strokeWidth="2"
            />
            {/* Global Optimum Potential Well */}
            <path
              d="M 120 20 L 130 65 L 140 20"
              fill="none"
              stroke="#06b6d4"
              strokeWidth="1.5"
              strokeDasharray="2,2"
            />
            {/* Quantum Tunneling Particle */}
            <circle
              cx={130 + Math.sin(phase * 2) * 15}
              cy={50 + Math.cos(phase * 2) * 8}
              r="4"
              fill="#2dd4bf"
              className="animate-pulse"
            />
          </svg>
          <div className="absolute top-1 right-2 text-[9px] text-slate-500 font-mono">
            V(x) = -γ δ(x - mbest)
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 gap-2 pt-1">
          <div className="bg-slate-950/70 p-2 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-500 font-mono block">Tunneling Escapes</span>
            <span className="text-sm font-bold text-teal-300 font-mono flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-teal-400" /> {tunnelingEvents} events
            </span>
          </div>
          <div className="bg-slate-950/70 p-2 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-500 font-mono block">Exploration Radius</span>
            <span className="text-sm font-bold text-cyan-300 font-mono">
              L = {(alpha * 12.4).toFixed(1)} kn
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
