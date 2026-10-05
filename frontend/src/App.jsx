import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import QuantumOptimizationLab from './components/QuantumOptimizationLab';
import GlobalVoyageMap from './components/GlobalVoyageMap';
import FuelPredictionStudio from './components/FuelPredictionStudio';
import GreenFleetStudio from './components/GreenFleetStudio';
import BenchmarkArena from './components/BenchmarkArena';
import CIISustainabilityReport from './components/CIISustainabilityReport';
import { api } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('optimization');
  const [systemStatus, setSystemStatus] = useState('connecting');
  const [connectionError, setConnectionError] = useState('');
  const [retryCount, setRetryCount] = useState(0);
  const [db, setDb] = useState({ vessels: null, routes: null, ports: null, fuels: null });

  useEffect(() => {
    async function initSystem() {
      setSystemStatus('connecting');
      setConnectionError('');
      try {
        const health = await api.getHealth();
        if (health.status !== 'online') {
          throw new Error('The backend health check did not report an online status.');
        }

        // Pre-fetch catalogs
        const [vessels, routes, ports, fuels] = await Promise.all([
          api.getVessels(),
          api.getRoutes(),
          api.getPorts(),
          api.getFuelProfiles()
        ]);
        setDb({ vessels, routes, ports, fuels });
        setSystemStatus('online');
      } catch (err) {
        console.error('Failed to connect to backend', err);
        setConnectionError(err instanceof Error ? err.message : 'An unexpected error occurred.');
        setSystemStatus('offline');
      }
    }
    initSystem();
  }, [retryCount]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} systemStatus={systemStatus} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {systemStatus === 'connecting' ? (
          <div className="flex flex-col items-center justify-center h-64 space-y-4">
            <div className="w-10 h-10 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
            <p className="text-cyan-400 font-mono tracking-widest text-sm animate-pulse">
              INITIALIZING QUANTUM STATE...
            </p>
          </div>
        ) : systemStatus === 'offline' ? (
          <section
            className="mx-auto mt-12 max-w-2xl rounded-2xl border border-amber-500/30 bg-slate-950/70 p-8 text-center shadow-xl"
            role="alert"
          >
            <h1 className="text-xl font-semibold text-amber-300">Backend unavailable</h1>
            <p className="mt-3 text-sm leading-6 text-slate-300">
              The dashboard needs its FastAPI backend to load vessel, route, and fuel data.
              Configure <code className="text-cyan-300">VITE_API_BASE_URL</code> to your deployed backend URL ending in <code className="text-cyan-300">/api</code>, then redeploy this site.
            </p>
            <p className="mt-3 break-words font-mono text-xs text-slate-400">{connectionError}</p>
            <button
              type="button"
              onClick={() => setRetryCount((count) => count + 1)}
              className="mt-6 rounded-lg bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              Retry connection
            </button>
          </section>
        ) : (
          <div className="animate-in fade-in duration-500">
            {activeTab === 'optimization' && <QuantumOptimizationLab db={db} />}
            {activeTab === 'routes' && <GlobalVoyageMap db={db} />}
            {activeTab === 'prediction' && <FuelPredictionStudio db={db} />}
            {activeTab === 'greenfleet' && <GreenFleetStudio db={db} />}
            {activeTab === 'benchmark' && <BenchmarkArena db={db} />}
            {activeTab === 'cii' && <CIISustainabilityReport db={db} />}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
