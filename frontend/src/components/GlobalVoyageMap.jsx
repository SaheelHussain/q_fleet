import React, { useState } from 'react';
import { Compass, Waves, Wind, MapPin, Navigation } from 'lucide-react';

export default function GlobalVoyageMap({ db }) {
  const [selectedRouteId, setSelectedRouteId] = useState('shanghai_rotterdam');
  const route = db.routes ? db.routes[selectedRouteId] : null;

  // Project lat/lon to SVG coordinates
  const project = (lat, lon) => {
    const x = ((lon + 180) / 360) * 800;
    const y = ((90 - lat) / 180) * 400;
    return [x, y];
  };

  const polylinePoints = route
    ? route.waypoints
        .map((wp) => {
          const [x, y] = project(wp.lat, wp.lon);
          return `${x},${y}`;
        })
        .join(' ')
    : '';

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-300 flex items-center gap-2">
              <Compass className="w-5 h-5 text-cyan-400" /> Oceanic Digital Twin & MetOcean Route Monitor
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Real-time maritime corridors with significant wave height ($H_s$), peak periods ($T_p$), and directional wind fields.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <select
              value={selectedRouteId}
              onChange={(e) => setSelectedRouteId(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-cyan-300 focus:outline-none focus:border-cyan-500"
            >
              {db.routes &&
                Object.entries(db.routes).map(([id, r]) => (
                  <option key={id} value={id}>
                    {r.name}
                  </option>
                ))}
            </select>
          </div>
        </div>

        {/* Global Interactive SVG Oceanic Map */}
        <div className="bg-slate-950 rounded-xl border border-slate-800 p-4 relative overflow-hidden">
          <svg viewBox="0 0 800 400" className="w-full h-auto bg-[#070d19] rounded-lg">
            {/* World Grid Lines */}
            {[-60, -30, 0, 30, 60].map((lat) => {
              const [, y] = project(lat, 0);
              return <line key={lat} x1="0" y1={y} x2="800" y2={y} stroke="#1e293b" strokeWidth="0.5" />;
            })}
            {[-120, -60, 0, 60, 120].map((lon) => {
              const [x] = project(0, lon);
              return <line key={lon} x1={x} y1="0" x2={x} y2="400" stroke="#1e293b" strokeWidth="0.5" />;
            })}

            {/* Global Trade Lane Paths */}
            {db.routes &&
              Object.entries(db.routes).map(([id, r]) => {
                const pts = r.waypoints
                  .map((wp) => {
                    const [x, y] = project(wp.lat, wp.lon);
                    return `${x},${y}`;
                  })
                  .join(' ');
                const isSelected = id === selectedRouteId;
                return (
                  <polyline
                    key={id}
                    points={pts}
                    fill="none"
                    stroke={isSelected ? '#06b6d4' : '#334155'}
                    strokeWidth={isSelected ? '3' : '1'}
                    strokeDasharray={isSelected ? 'none' : '2,2'}
                    className="transition-all duration-300 cursor-pointer"
                    onClick={() => setSelectedRouteId(id)}
                  />
                );
              })}

            {/* Ports on Selected Route */}
            {route &&
              route.waypoints.map((wp, idx) => {
                const [x, y] = project(wp.lat, wp.lon);
                const isPort = idx === 0 || idx === route.waypoints.length - 1;
                return (
                  <g key={idx} transform={`translate(${x}, ${y})`}>
                    <circle
                      r={isPort ? '5' : '3'}
                      fill={isPort ? '#22d3ee' : '#14b8a6'}
                      stroke="#0f172a"
                      strokeWidth="1.5"
                    />
                    {isPort && (
                      <text
                        x="8"
                        y="4"
                        fill="#e2e8f0"
                        fontSize="9"
                        fontFamily="monospace"
                        fontWeight="bold"
                      >
                        {wp.name}
                      </text>
                    )}
                  </g>
                );
              })}
          </svg>

          {/* Route Summary Floating Overlay */}
          {route && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Origin → Destination</span>
                <span className="text-xs font-bold text-slate-200">{route.origin} → {route.destination}</span>
              </div>
              <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Corridor Length</span>
                <span className="text-xs font-bold text-cyan-300 font-mono">{route.total_distance_nm.toLocaleString()} NM</span>
              </div>
              <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">Voyage Segments</span>
                <span className="text-xs font-bold text-teal-300 font-mono">{route.segments.length} Navigational Zones</span>
              </div>
              <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-lg">
                <span className="text-[10px] text-slate-500 font-mono block">ECA / Coastal Zone</span>
                <span className="text-xs font-bold text-amber-300 font-mono">
                  {route.segments.some((s) => s.is_eca) ? 'Strict 0.1% Sulfur (ECA)' : 'Standard High Seas'}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Metocean Segments Breakdown */}
        {route && (
          <div className="mt-6">
            <h3 className="text-sm font-bold text-slate-300 font-mono mb-3 flex items-center gap-2">
              <Waves className="w-4 h-4 text-cyan-400" /> Historical Sea State & Weather by Segment
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {route.segments.map((seg, i) => (
                <div key={i} className="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-cyan-400">#{i + 1} {seg.name}</span>
                    <span className="text-[10px] font-mono text-slate-500">{seg.distance_nm} NM</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-2 text-[11px] font-mono">
                    <div className="flex items-center space-x-1 text-slate-400">
                      <Waves className="w-3.5 h-3.5 text-blue-400" />
                      <span>Hs: <b className="text-slate-200">{seg.mean_hs_m}m</b></span>
                    </div>
                    <div className="flex items-center space-x-1 text-slate-400">
                      <Wind className="w-3.5 h-3.5 text-teal-400" />
                      <span>Wind: <b className="text-slate-200">{seg.mean_wind_knots}kn</b></span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
