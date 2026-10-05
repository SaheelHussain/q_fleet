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
  const [db, setDb] = useState({ vessels: null, routes: null, ports: null, fuels: null });

  useEffect(() => {
    async function initSystem() {
      try {
        const health = await api.getHealth();
        if (health.status === 'online') {
          setSystemStatus('online');

          // Pre-fetch catalogs
          const [vessels, routes, ports, fuels] = await Promise.all([
            api.getVessels(),
            api.getRoutes(),
            api.getPorts(),
            api.getFuelProfiles()
          ]);
          setDb({ vessels, routes, ports, fuels });
        }
      } catch (err) {
        console.error('Failed to connect to backend', err);
        setSystemStatus('offline');
      }
    }
    initSystem();
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} systemStatus={systemStatus} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {!db.vessels ? (
          <div className="flex flex-col items-center justify-center h-64 space-y-4">
            <div className="w-10 h-10 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
            <p className="text-cyan-400 font-mono tracking-widest text-sm animate-pulse">
              INITIALIZING QUANTUM STATE...
            </p>
          </div>
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
