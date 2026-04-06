# api.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
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
def get_plants():
    return monitor.get_all_plants()


@app.get("/api/plants/{plant_id}/status")
def get_plant_status(plant_id: str, audience_level: str = Query("beginner")):
    return monitor.get_plant_status(plant_id, audience_level=audience_level)


@app.get("/api/plants/{plant_id}/history")
def get_plant_history(plant_id: str, days: int = Query(7)):
    return monitor.get_sensor_history(plant_id, days=days)