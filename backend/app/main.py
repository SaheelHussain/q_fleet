"""
Q-Fleet (AuraQuanta) FastAPI Main Application Entrypoint
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="Q-Fleet (AuraQuanta) Quantum Maritime API",
    description="Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization Platform",
    version="1.0.0"
)

# Configure CORS for Frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "system": "Q-Fleet (AuraQuanta)",
        "description": "Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
