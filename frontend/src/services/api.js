/**
 * API Client Service for Q-Fleet (AuraQuanta)
 * Interacts with FastAPI backend endpoints
 */

// In production, require an explicit backend URL instead of accidentally
// requesting API paths from the static frontend host.
const API_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : '')
).replace(/\/$/, '');

async function request(path, options) {
  if (!API_URL) {
    throw new Error('Backend URL is not configured. Set VITE_API_BASE_URL in the deployment environment.');
  }

  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) {
    throw new Error(`Backend request failed (${res.status} ${res.statusText}).`);
  }

  if (!res.headers.get('content-type')?.includes('application/json')) {
    throw new Error('Backend returned a non-JSON response. Check that VITE_API_BASE_URL points to the FastAPI /api URL.');
  }

  return res.json();
}

export const api = {
  // Health & Catalog
  async getHealth() {
    return request('/health');
  },

  async getVessels() {
    return request('/fleet/vessels');
  },

  async getRoutes() {
    return request('/fleet/routes');
  },

  async getPorts() {
    return request('/fleet/ports');
  },

  async getFuelProfiles() {
    return request('/fuels/profiles');
  },

  // Predictive & Optimization Endpoints
  async predictFuel(payload) {
    return request('/predict/fuel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async optimizeRoute(payload) {
    return request('/optimize/route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async optimizeFleet(payload) {
    return request('/optimize/fleet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async runBenchmark(payload) {
    return request('/benchmark/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async runMLBenchmark() {
    return request('/benchmark/ml', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
  },

  async auditCII(payload) {
    return request('/cii/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async auditColdIroning(payload) {
    return request('/cold-ironing/benefit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },

  async simulateScenario(payload) {
    return request('/simulate/scenario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  },
};
