# api.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

from backend_logic import PlantMonitor
import openrouter_llm
import db_api

app = FastAPI()

# Allow your Vite dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM + DB once
llm = openrouter_llm.OpenRouterExplainer()
db = db_api.PlantDatabase() 
monitor = PlantMonitor(llm=llm, database=db)


@app.get("/api/plants")
def get_plants(user_id: str = Query(...)):
    return monitor.get_all_plants(user_id)


@app.get("/api/plants/{plant_id}/status")
def get_plant_status(plant_id: str, user_id: str = Query(...), audience_level: str = Query("beginner")):
    return monitor.get_plant_status(plant_id, user_id = user_id, audience_level=audience_level)


@app.get("/api/plants/{plant_id}/history")
def get_plant_history(plant_id: str, days: int = Query(7)):
    return monitor.get_sensor_history(plant_id, days=days)

@app.get("/api/llm-test")
def test_llm(user_id: str):
    """NEW: Test LLM endpoint"""
    print(f"LLM test from user_id: {user_id}")
    return {
        "explanation": "Your Monstera needs more light. Move it closer to a window but avoid direct sun.",
        "user_id": user_id,
        "status": "success"
    }