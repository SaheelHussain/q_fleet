/**
 * API Client Service for Q-Fleet (AuraQuanta)
 * Interacts with FastAPI backend endpoints
 */

const BASE_URL = 'http://localhost:8000/api';

export const api = {
  // Health & Catalog
  async getHealth() {
    const res = await fetch(`${BASE_URL}/health`);
    return res.json();
  },

  async getVessels() {
    const res = await fetch(`${BASE_URL}/fleet/vessels`);
    return res.json();
  },

  async getRoutes() {
    const res = await fetch(`${BASE_URL}/fleet/routes`);
    return res.json();
  },

  async getPorts() {
    const res = await fetch(`${BASE_URL}/fleet/ports`);
    return res.json();
  },

  async getFuelProfiles() {
    const res = await fetch(`${BASE_URL}/fuels/profiles`);
    return res.json();
  },

  // Predictive & Optimization Endpoints
  async predictFuel(payload) {
    const res = await fetch(`${BASE_URL}/predict/fuel`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async optimizeRoute(payload) {
    const res = await fetch(`${BASE_URL}/optimize/route`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async optimizeFleet(payload) {
    const res = await fetch(`${BASE_URL}/optimize/fleet`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async runBenchmark(payload) {
    const res = await fetch(`${BASE_URL}/benchmark/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async runMLBenchmark() {
    const res = await fetch(`${BASE_URL}/benchmark/ml`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return res.json();
  },

  async auditCII(payload) {
    const res = await fetch(`${BASE_URL}/cii/audit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async auditColdIroning(payload) {
    const res = await fetch(`${BASE_URL}/cold-ironing/benefit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async simulateScenario(payload) {
    const res = await fetch(`${BASE_URL}/simulate/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },
};
