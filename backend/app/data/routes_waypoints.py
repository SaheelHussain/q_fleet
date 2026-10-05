"""
Global Maritime Shipping Corridors & Oceanic Route Waypoints
Includes segmented navigational legs, distances, historical sea-state matrices, and port infrastructure.
"""

from typing import Dict, List, Any

PORTS_CATALOG: Dict[str, Dict[str, Any]] = {
    "CNSHA": {
        "id": "CNSHA",
        "name": "Port of Shanghai",
        "country": "China",
        "lat": 31.2304,
        "lon": 121.4737,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.55,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol"]
    },
    "NLRTM": {
        "id": "NLRTM",
        "name": "Port of Rotterdam",
        "country": "Netherlands",
        "lat": 51.9244,
        "lon": 4.4777,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.22,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"]
    },
    "SGSIN": {
        "id": "SGSIN",
        "name": "Port of Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lon": 103.8198,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.38,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia"]
    },
    "AEJEA": {
        "id": "AEJEA",
        "name": "Jebel Ali / Dubai",
        "country": "UAE",
        "lat": 25.0083,
        "lon": 55.0600,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.44,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol"]
    },
    "INBOM": {
        "id": "INBOM",
        "name": "Jawaharlal Nehru Port (JNPT) / Mumbai",
        "country": "India",
        "lat": 18.9500,
        "lon": 72.9500,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.68,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG"]
    },
    "BEANR": {
        "id": "BEANR",
        "name": "Port of Antwerp-Bruges",
        "country": "Belgium",
        "lat": 51.2194,
        "lon": 4.4025,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.18,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Green_Ammonia", "Liquid_H2"]
    },
    "USNYC": {
        "id": "USNYC",
        "name": "Port of New York & New Jersey",
        "country": "USA",
        "lat": 40.6700,
        "lon": -74.1300,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.28,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol"]
    },
    "JPYOK": {
        "id": "JPYOK",
        "name": "Port of Yokohama",
        "country": "Japan",
        "lat": 35.4437,
        "lon": 139.6380,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.42,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol", "Liquid_H2"]
    },
    "USLAX": {
        "id": "USLAX",
        "name": "Port of Los Angeles / Long Beach",
        "country": "USA",
        "lat": 33.7430,
        "lon": -118.2673,
        "cold_ironing_available": True,
        "grid_emission_factor_kg_kwh": 0.20,
        "bunkering_fuels": ["VLSFO", "MGO", "LNG", "e_Methanol"]
    }
}

MARITIME_ROUTES: Dict[str, Dict[str, Any]] = {
    "shanghai_rotterdam": {
        "id": "shanghai_rotterdam",
        "name": "Shanghai to Rotterdam (Asia-Europe via Suez)",
        "origin_port": "CNSHA",
        "dest_port": "NLRTM",
        "total_distance_nm": 10520.0,
        "typical_transit_days_at_18kn": 24.3,
        "segments": [
            {
                "seg_id": 1,
                "name": "East China Sea to Taiwan Strait",
                "start_coord": [31.23, 121.47],
                "end_coord": [22.00, 119.50],
                "distance_nm": 620.0,
                "mean_hs_m": 2.1,
                "mean_tp_s": 7.5,
                "mean_wind_knots": 16.5,
                "wind_direction_deg": 45.0,
                "current_drift_knots": 0.8
            },
            {
                "seg_id": 2,
                "name": "South China Sea Transit",
                "start_coord": [22.00, 119.50],
                "end_coord": [1.35, 103.82],
                "distance_nm": 1420.0,
                "mean_hs_m": 1.8,
                "mean_tp_s": 6.8,
                "mean_wind_knots": 14.0,
                "wind_direction_deg": 60.0,
                "current_drift_knots": -0.4
            },
            {
                "seg_id": 3,
                "name": "Malacca Strait & Andaman Sea",
                "start_coord": [1.35, 103.82],
                "end_coord": [6.00, 80.00],
                "distance_nm": 1380.0,
                "mean_hs_m": 1.4,
                "mean_tp_s": 6.0,
                "mean_wind_knots": 11.0,
                "wind_direction_deg": 90.0,
                "current_drift_knots": 0.2
            },
            {
                "seg_id": 4,
                "name": "Arabian Sea to Gulf of Aden",
                "start_coord": [6.00, 80.00],
                "end_coord": [12.50, 45.00],
                "distance_nm": 2150.0,
                "mean_hs_m": 2.8,
                "mean_tp_s": 8.4,
                "mean_wind_knots": 20.0,
                "wind_direction_deg": 225.0, # Monsoon waves
                "current_drift_knots": -0.6
            },
            {
                "seg_id": 5,
                "name": "Red Sea to Suez Canal",
                "start_coord": [12.50, 45.00],
                "end_coord": [29.95, 32.55],
                "distance_nm": 1310.0,
                "mean_hs_m": 1.5,
                "mean_tp_s": 5.5,
                "mean_wind_knots": 15.0,
                "wind_direction_deg": 340.0,
                "current_drift_knots": -0.3
            },
            {
                "seg_id": 6,
                "name": "Mediterranean Sea Transit",
                "start_coord": [31.25, 32.30],
                "end_coord": [36.00, -5.30],
                "distance_nm": 1920.0,
                "mean_hs_m": 2.2,
                "mean_tp_s": 7.0,
                "mean_wind_knots": 18.0,
                "wind_direction_deg": 270.0,
                "current_drift_knots": -0.2
            },
            {
                "seg_id": 7,
                "name": "Bay of Biscay to English Channel",
                "start_coord": [36.00, -5.30],
                "end_coord": [49.50, -4.00],
                "distance_nm": 1080.0,
                "mean_hs_m": 3.6, # Heavy North Atlantic swells
                "mean_tp_s": 9.5,
                "mean_wind_knots": 24.0,
                "wind_direction_deg": 260.0,
                "current_drift_knots": -0.5
            },
            {
                "seg_id": 8,
                "name": "North Sea Approach to Rotterdam",
                "start_coord": [49.50, -4.00],
                "end_coord": [51.92, 4.48],
                "distance_nm": 640.0,
                "mean_hs_m": 2.4,
                "mean_tp_s": 7.2,
                "mean_wind_knots": 19.0,
                "wind_direction_deg": 240.0,
                "current_drift_knots": 0.4
            }
        ]
    },
    "singapore_dubai": {
        "id": "singapore_dubai",
        "name": "Singapore to Dubai (Middle East Corridor)",
        "origin_port": "SGSIN",
        "dest_port": "AEJEA",
        "total_distance_nm": 3480.0,
        "typical_transit_days_at_16kn": 9.1,
        "segments": [
            {
                "seg_id": 1,
                "name": "Malacca Strait Outbound",
                "start_coord": [1.35, 103.82],
                "end_coord": [5.70, 95.30],
                "distance_nm": 520.0,
                "mean_hs_m": 1.2,
                "mean_tp_s": 5.2,
                "mean_wind_knots": 10.0,
                "wind_direction_deg": 80.0,
                "current_drift_knots": 0.3
            },
            {
                "seg_id": 2,
                "name": "Bay of Bengal Crossing",
                "start_coord": [5.70, 95.30],
                "end_coord": [6.00, 80.20],
                "distance_nm": 950.0,
                "mean_hs_m": 2.0,
                "mean_tp_s": 7.2,
                "mean_wind_knots": 15.0,
                "wind_direction_deg": 210.0,
                "current_drift_knots": -0.2
            },
            {
                "seg_id": 3,
                "name": "Arabian Sea Transit",
                "start_coord": [6.00, 80.20],
                "end_coord": [16.00, 60.00],
                "distance_nm": 1320.0,
                "mean_hs_m": 2.5,
                "mean_tp_s": 8.0,
                "mean_wind_knots": 18.0,
                "wind_direction_deg": 230.0,
                "current_drift_knots": -0.4
            },
            {
                "seg_id": 4,
                "name": "Gulf of Oman & Strait of Hormuz to Dubai",
                "start_coord": [16.00, 60.00],
                "end_coord": [25.01, 55.06],
                "distance_nm": 690.0,
                "mean_hs_m": 1.4,
                "mean_tp_s": 5.8,
                "mean_wind_knots": 12.0,
                "wind_direction_deg": 320.0,
                "current_drift_knots": 0.1
            }
        ]
    },
    "mumbai_antwerp": {
        "id": "mumbai_antwerp",
        "name": "Mumbai (JNPT) to Antwerp-Bruges",
        "origin_port": "INBOM",
        "dest_port": "BEANR",
        "total_distance_nm": 6620.0,
        "typical_transit_days_at_15kn": 18.4,
        "segments": [
            {
                "seg_id": 1,
                "name": "Arabian Sea to Gulf of Aden",
                "start_coord": [18.95, 72.95],
                "end_coord": [12.50, 45.00],
                "distance_nm": 1640.0,
                "mean_hs_m": 2.6,
                "mean_tp_s": 8.1,
                "mean_wind_knots": 19.0,
                "wind_direction_deg": 220.0,
                "current_drift_knots": -0.5
            },
            {
                "seg_id": 2,
                "name": "Red Sea to Suez",
                "start_coord": [12.50, 45.00],
                "end_coord": [29.95, 32.55],
                "distance_nm": 1310.0,
                "mean_hs_m": 1.5,
                "mean_tp_s": 5.5,
                "mean_wind_knots": 15.0,
                "wind_direction_deg": 340.0,
                "current_drift_knots": -0.3
            },
            {
                "seg_id": 3,
                "name": "Eastern & Western Mediterranean",
                "start_coord": [31.25, 32.30],
                "end_coord": [36.00, -5.30],
                "distance_nm": 1920.0,
                "mean_hs_m": 2.2,
                "mean_tp_s": 7.0,
                "mean_wind_knots": 17.5,
                "wind_direction_deg": 270.0,
                "current_drift_knots": -0.2
            },
            {
                "seg_id": 4,
                "name": "Atlantic Coast & English Channel to Antwerp",
                "start_coord": [36.00, -5.30],
                "end_coord": [51.22, 4.40],
                "distance_nm": 1750.0,
                "mean_hs_m": 3.4,
                "mean_tp_s": 9.2,
                "mean_wind_knots": 22.0,
                "wind_direction_deg": 250.0,
                "current_drift_knots": -0.4
            }
        ]
    },
    "rotterdam_new_york": {
        "id": "rotterdam_new_york",
        "name": "Rotterdam to New York (Transatlantic)",
        "origin_port": "NLRTM",
        "dest_port": "USNYC",
        "total_distance_nm": 3380.0,
        "typical_transit_days_at_18kn": 7.8,
        "segments": [
            {
                "seg_id": 1,
                "name": "English Channel Outbound",
                "start_coord": [51.92, 4.48],
                "end_coord": [49.50, -5.50],
                "distance_nm": 420.0,
                "mean_hs_m": 2.2,
                "mean_tp_s": 6.8,
                "mean_wind_knots": 18.0,
                "wind_direction_deg": 240.0,
                "current_drift_knots": 0.2
            },
            {
                "seg_id": 2,
                "name": "Mid North Atlantic Great Circle Leg 1",
                "start_coord": [49.50, -5.50],
                "end_coord": [48.00, -30.00],
                "distance_nm": 1150.0,
                "mean_hs_m": 3.8, # Severe North Atlantic weather
                "mean_tp_s": 10.0,
                "mean_wind_knots": 25.0,
                "wind_direction_deg": 270.0,
                "current_drift_knots": -0.6
            },
            {
                "seg_id": 3,
                "name": "Mid North Atlantic Great Circle Leg 2",
                "start_coord": [48.00, -30.00],
                "end_coord": [44.00, -55.00],
                "distance_nm": 1120.0,
                "mean_hs_m": 3.5,
                "mean_tp_s": 9.5,
                "mean_wind_knots": 23.0,
                "wind_direction_deg": 280.0,
                "current_drift_knots": -0.5
            },
            {
                "seg_id": 4,
                "name": "US East Coast Approach to New York",
                "start_coord": [44.00, -55.00],
                "end_coord": [40.67, -74.13],
                "distance_nm": 690.0,
                "mean_hs_m": 2.0,
                "mean_tp_s": 6.5,
                "mean_wind_knots": 15.0,
                "wind_direction_deg": 290.0,
                "current_drift_knots": 0.3
            }
        ]
    },
    "yokohama_los_angeles": {
        "id": "yokohama_los_angeles",
        "name": "Yokohama to Los Angeles (Transpacific)",
        "origin_port": "JPYOK",
        "dest_port": "USLAX",
        "total_distance_nm": 4840.0,
        "typical_transit_days_at_19kn": 10.6,
        "segments": [
            {
                "seg_id": 1,
                "name": "Japan Coast to North Pacific Kuroshio",
                "start_coord": [35.44, 139.64],
                "end_coord": [38.00, 160.00],
                "distance_nm": 1050.0,
                "mean_hs_m": 2.8,
                "mean_tp_s": 8.5,
                "mean_wind_knots": 20.0,
                "wind_direction_deg": 260.0,
                "current_drift_knots": 1.2 # Favorable Kuroshio Current
            },
            {
                "seg_id": 2,
                "name": "Central North Pacific Great Circle",
                "start_coord": [38.00, 160.00],
                "end_coord": [40.00, -170.00],
                "distance_nm": 1450.0,
                "mean_hs_m": 3.7,
                "mean_tp_s": 9.8,
                "mean_wind_knots": 24.0,
                "wind_direction_deg": 270.0,
                "current_drift_knots": 0.5
            },
            {
                "seg_id": 3,
                "name": "East North Pacific Transition",
                "start_coord": [40.00, -170.00],
                "end_coord": [37.00, -140.00],
                "distance_nm": 1380.0,
                "mean_hs_m": 3.2,
                "mean_tp_s": 9.0,
                "mean_wind_knots": 21.0,
                "wind_direction_deg": 290.0,
                "current_drift_knots": 0.3
            },
            {
                "seg_id": 4,
                "name": "California Coast Approach to Los Angeles",
                "start_coord": [37.00, -140.00],
                "end_coord": [33.74, -118.27],
                "distance_nm": 960.0,
                "mean_hs_m": 2.1,
                "mean_tp_s": 7.2,
                "mean_wind_knots": 16.0,
                "wind_direction_deg": 310.0,
                "current_drift_knots": -0.2
            }
        ]
    }
}

def get_route(route_id: str) -> Dict[str, Any]:
    if route_id not in MARITIME_ROUTES:
        raise ValueError(f"Unknown route: {route_id}. Available: {list(MARITIME_ROUTES.keys())}")
    return MARITIME_ROUTES[route_id]

def get_all_routes() -> Dict[str, Dict[str, Any]]:
    return MARITIME_ROUTES

def get_all_ports() -> Dict[str, Dict[str, Any]]:
    return PORTS_CATALOG
