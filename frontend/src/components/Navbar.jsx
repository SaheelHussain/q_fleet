import React from 'react';
import {
  Anchor,
  Cpu,
  Flame,
  BarChart3,
  MapPin,
  ShieldCheck,
  Sparkles,
  Layers
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemStatus }) {
  const navItems = [
    { id: 'optimization', label: 'Quantum Optimizer', icon: Cpu },
    { id: 'prediction', label: 'Q-PINN Predictor', icon: Flame },
    { id: 'routes', label: 'Oceanic Digital Twin', icon: MapPin },
    { id: 'greenfleet', label: 'Green Fuels & LCA', icon: Layers },
    { id: 'benchmark', label: 'Benchmark Arena', icon: BarChart3 },
    { id: 'cii', label: 'IMO CII & Compliance', icon: ShieldCheck },
  ];

  return (
    <header className="bg-slate-900 border-b border-cyan-500/20 sticky top-0 z-50 backdrop-blur-md bg-opacity-95 shadow-lg shadow-cyan-950/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg shadow-md shadow-cyan-500/30">
              <Anchor className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-400">
                  Q-FLEET
                </span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-700/50 flex items-center gap-1 font-mono">
                  <Sparkles className="w-3 h-3 text-cyan-300" /> AURAQUANTA
                </span>
              </div>
              <p className="text-[10px] text-slate-400 tracking-tight">Quantum-Inspired Maritime Decarbonization</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-cyan-950/80 text-cyan-300 border border-cyan-500/40 shadow-sm shadow-cyan-500/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* System Status Indicators */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 bg-slate-950/60 border border-slate-800 px-3 py-1.5 rounded-full text-xs">
              <span className={`w-2 h-2 rounded-full ${systemStatus === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
              <span className="text-slate-300 font-mono text-[11px]">
                {systemStatus === 'online'
                  ? 'Quantum Engine Active'
                  : systemStatus === 'connecting'
                    ? 'Connecting...'
                    : 'Backend Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
