from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json

app = FastAPI(
    title="Disaster Ready: Earthquake Response Simulator",
    description="AI-powered earthquake preparedness simulator for Southeast Asia",
    version="1.0.0"
)

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    location: str = "general"

@app.get("/")
def read_root():
    return {
        "message": "Disaster Ready: Earthquake Response Simulator",
        "description": "AI-powered earthquake preparedness for Southeast Asia",
        "status": "Basic API running - Strands Agent temporarily disabled",
        "endpoints": {
            "health": "/health - Health check",
            "basic_advice": "/basic-advice - Basic earthquake advice",
            "scenarios": "/scenarios - Get available scenarios",
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "earthquake_simulator"}

@app.post("/ask/direct")
async def ask_agent_direct(query: Query):
    """
    Provide basic earthquake advice without Strands Agent (for testing).
    """
    advice = {
        "sleeping": "If an earthquake hits while sleeping: Stay in bed, cover your head with a pillow, and hold on until shaking stops.",
        "office": "At the office: Drop under your desk, cover your head and neck, hold on to the desk until shaking stops.",
        "driving": "While driving: Pull over safely away from buildings and power lines, stay in your vehicle until shaking stops.",
        "general": "Remember: DROP, COVER, and HOLD ON. Don't run outside during shaking."
    }
    
    question_lower = query.question.lower()
    response = advice["general"]  # default
    
    if any(word in question_lower for word in ["sleep", "bed", "night"]):
        response = advice["sleeping"]
    elif any(word in question_lower for word in ["office", "work", "desk"]):
        response = advice["office"]
    elif any(word in question_lower for word in ["driv", "car", "vehicle"]):
        response = advice["driving"]
    
    return {"response": response, "location": query.location, "note": "This is basic advice. Full AI agent requires AWS credentials."}

@app.get("/scenarios")
def get_scenarios():
    """
    Get list of available earthquake scenarios.
    """
    try:
        with open("data/scenarios.json", "r") as f:
            data = json.load(f)
        scenarios = data.get("scenarios", [])
        return {"scenarios": [{"id": s["id"], "title": s["title"], "description": s["description"]} for s in scenarios]}
    except Exception as e:
        return {"scenarios": [], "error": str(e)}

@app.get("/learn/basics")
def get_earthquake_basics():
    """
    Get basic earthquake safety information.
    """
    return {
        "drop_cover_hold": {
            "title": "DROP, COVER, and HOLD ON",
            "description": "The universal earthquake response",
            "steps": [
                "DROP to your hands and knees immediately",
                "COVER your head and neck with your arms; if under a table, hold on",
                "HOLD ON to your shelter and protect yourself until shaking stops"
            ]
        },
        "common_mistakes": [
            "Running outside during shaking",
            "Standing in doorways",
            "Using elevators during/after earthquake",
            "Stopping under overpasses while driving"
        ],
        "preparation_tips": [
            "Create an emergency kit",
            "Identify safe spots in each room", 
            "Practice earthquake drills",
            "Secure heavy furniture and objects",
            "Know how to turn off utilities"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🌍 Starting Disaster Ready API on port {port}")
    print("📝 Note: This is the basic version. For full AI features, configure AWS credentials.")
    uvicorn.run(app, host="0.0.0.0", port=port) 