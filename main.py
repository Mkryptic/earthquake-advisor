from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import asyncio
import os
import uuid

from agent.earthquake_advisor import earthquake_advisor_agent
from agent.multi_agent_coordinator import multi_agent_coordinator
from simulation.scenario_engine import scenario_engine

app = FastAPI(
    title="Disaster Ready: Earthquake Response Simulator",
    description="AI-powered earthquake preparedness simulator for Southeast Asia",
    version="1.0.0"
)

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    location: str = "general"

class Choice(BaseModel):
    choice_id: str

class ScenarioRequest(BaseModel):
    scenario_id: str = None
    location: str = None
    random: bool = False

class IncidentRequest(BaseModel):
    incident_type: str
    location: str
    severity: str = "medium"

@app.get("/")
def read_root():
    return {
        "message": "Disaster Ready: Earthquake Response Simulator",
        "description": "AI-powered earthquake preparedness for Southeast Asia",
        "endpoints": {
            "ask_agent": "/ask - Ask the earthquake safety advisor",
            "scenarios": "/scenarios - Get available scenarios",
            "start_scenario": "/scenario/start - Start a scenario",
            "submit_choice": "/scenario/choice - Submit a choice",
            "multi_agent": "/multi-agent/* - Multi-agent coordination features",
            "health": "/health - Health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "earthquake_simulator"}

# Agent Endpoints
@app.post("/ask")
async def ask_agent(query: Query):
    """
    Ask the earthquake advisor agent a question with optional location context.
    """
    try:
        async def event_generator():
            # Enhance question with location context if provided
            enhanced_question = query.question
            if query.location and query.location != "general":
                enhanced_question = f"[Location: {query.location}] {query.question}"
            
            agent_stream = earthquake_advisor_agent.stream_async(enhanced_question)
            async for event in agent_stream:
                if "data" in event:
                    yield {"data": event["data"]}

        return EventSourceResponse(event_generator())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.post("/ask/direct")
async def ask_agent_direct(query: Query):
    """
    Ask the agent and get a direct response (non-streaming).
    """
    try:
        enhanced_question = query.question
        if query.location and query.location != "general":
            enhanced_question = f"[Location: {query.location}] {query.question}"
        
        response = await earthquake_advisor_agent.ainvoke(enhanced_question)
        return {"response": response, "location": query.location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# Multi-Agent Coordination Endpoints
@app.post("/multi-agent/incident")
async def create_incident(request: IncidentRequest):
    """
    Create a new emergency incident for multi-agent coordination.
    """
    try:
        incident_id = str(uuid.uuid4())[:8]  # Short ID for demo
        
        incident = await multi_agent_coordinator.create_incident(
            incident_id=incident_id,
            incident_type=request.incident_type,
            location=request.location,
            severity=request.severity
        )
        
        return {"incident_id": incident_id, "incident": incident}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating incident: {str(e)}")

@app.get("/multi-agent/incident/{incident_id}")
async def get_incident_status(incident_id: str):
    """
    Get the status of a specific incident.
    """
    try:
        status = multi_agent_coordinator.get_incident_status(incident_id)
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting incident status: {str(e)}")

@app.post("/multi-agent/incident/{incident_id}/response")
async def get_coordinated_response(incident_id: str):
    """
    Get coordinated response from all emergency agents for an incident.
    """
    try:
        response = await multi_agent_coordinator.get_full_response(incident_id)
        if "error" in response:
            raise HTTPException(status_code=404, detail=response["error"])
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting coordinated response: {str(e)}")

@app.get("/multi-agent/incidents")
async def list_active_incidents():
    """
    List all active emergency incidents.
    """
    try:
        incidents = multi_agent_coordinator.list_active_incidents()
        return {"active_incidents": incidents, "count": len(incidents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing incidents: {str(e)}")

@app.post("/multi-agent/incident/{incident_id}/medical")
async def get_medical_response(incident_id: str):
    """
    Get medical team response for a specific incident.
    """
    try:
        response = await multi_agent_coordinator.get_medical_response(incident_id)
        return {"medical_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting medical response: {str(e)}")

@app.post("/multi-agent/incident/{incident_id}/evacuation")
async def get_evacuation_response(incident_id: str):
    """
    Get evacuation team response for a specific incident.
    """
    try:
        response = await multi_agent_coordinator.get_evacuation_response(incident_id)
        return {"evacuation_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting evacuation response: {str(e)}")

# Simulation Endpoints
@app.get("/scenarios")
def get_scenarios():
    """
    Get list of available earthquake scenarios.
    """
    try:
        scenarios = scenario_engine.get_available_scenarios()
        return {"scenarios": scenarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading scenarios: {str(e)}")

@app.post("/scenario/start")
def start_scenario(request: ScenarioRequest):
    """
    Start an earthquake scenario simulation.
    """
    try:
        if request.random:
            result = scenario_engine.get_random_scenario()
        elif request.location:
            result = scenario_engine.get_scenario_by_location(request.location)
        elif request.scenario_id:
            result = scenario_engine.start_scenario(request.scenario_id)
        else:
            raise HTTPException(status_code=400, detail="Must specify scenario_id, location, or random=True")
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting scenario: {str(e)}")

@app.post("/scenario/choice")
def submit_choice(choice: Choice):
    """
    Submit a choice for the current scenario.
    """
    try:
        result = scenario_engine.submit_choice(choice.choice_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting choice: {str(e)}")

@app.get("/scenario/status")
def get_scenario_status():
    """
    Get current scenario status.
    """
    try:
        has_active = scenario_engine.current_scenario is not None
        return {
            "has_active_scenario": has_active,
            "current_score": scenario_engine.score,
            "max_score": scenario_engine.max_score,
            "choices_made": len(scenario_engine.user_choices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

# Educational Endpoints
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

@app.get("/learn/southeast-asia")
def get_regional_info():
    """
    Get Southeast Asia specific earthquake information.
    """
    return {
        "high_risk_areas": [
            "Northern Myanmar",
            "Western Thailand", 
            "Myanmar-Thailand Border Region"
        ],
        "recent_activity": {
            "2024_myanmar_thailand": {
                "magnitude": 6.8,
                "location": "Myanmar-Thailand Border",
                "affected_cities": ["Bangkok", "Yangon", "Chiang Mai"],
                "lessons": [
                    "Cross-border preparedness is crucial",
                    "Urban areas need specific response plans",
                    "International coordination saves lives"
                ]
            }
        },
        "cultural_considerations": [
            "Multi-language emergency communications",
            "Community-based response systems",
            "Integration with traditional building styles",
            "Religious and cultural gathering places as shelters"
        ]
    }

@app.get("/demo/multi-agent")
async def demo_multi_agent():
    """
    Demo endpoint showing multi-agent coordination capabilities.
    """
    try:
        # Create a demo earthquake incident
        incident_id = "demo-" + str(uuid.uuid4())[:6]
        
        demo_incident = await multi_agent_coordinator.create_incident(
            incident_id=incident_id,
            incident_type="earthquake",
            location="Bangkok",
            severity="high"
        )
        
        # Get coordinated response
        coordinated_response = await multi_agent_coordinator.get_full_response(incident_id)
        
        return {
            "demo_description": "Multi-agent earthquake response coordination",
            "incident": demo_incident,
            "coordinated_response": coordinated_response,
            "explanation": "This demonstrates how multiple AI agents coordinate emergency response - medical, evacuation, and coordination agents working together."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 