/**
 * API Client Service for Q-Fleet (AuraQuanta)
 * Interacts with FastAPI backend endpoints
 */

// Prefer a deployment-specific backend URL. In Vercel, set VITE_API_BASE_URL
// to your production FastAPI URL; for local dev, this falls back to the Docker
// or local backend running on port 8000.
const API_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost'
    ? `${window.location.origin}/api`
    : 'http://localhost:8000/api')
).replace(/\/$/, '');

export const api = {
  // Health & Catalog
  async getHealth() {
    const res = await fetch(`${API_URL}/health`);
    return res.json();
  },

  async getVessels() {
    const res = await fetch(`${API_URL}/fleet/vessels`);
    return res.json();
  },

  async getRoutes() {
    const res = await fetch(`${API_URL}/fleet/routes`);
    return res.json();
  },

  async getPorts() {
    const res = await fetch(`${API_URL}/fleet/ports`);
    return res.json();
  },

  async getFuelProfiles() {
    const res = await fetch(`${API_URL}/fuels/profiles`);
    return res.json();
  },

  // Predictive & Optimization Endpoints
  async predictFuel(payload) {
    const res = await fetch(`${API_URL}/predict/fuel`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async optimizeRoute(payload) {
    const res = await fetch(`${API_URL}/optimize/route`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async optimizeFleet(payload) {
    const res = await fetch(`${API_URL}/optimize/fleet`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async runBenchmark(payload) {
    const res = await fetch(`${API_URL}/benchmark/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async runMLBenchmark() {
    const res = await fetch(`${API_URL}/benchmark/ml`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return res.json();
  },

  async auditCII(payload) {
    const res = await fetch(`${API_URL}/cii/audit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async auditColdIroning(payload) {
    const res = await fetch(`${API_URL}/cold-ironing/benefit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async simulateScenario(payload) {
    const res = await fetch(`${API_URL}/simulate/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },
};
