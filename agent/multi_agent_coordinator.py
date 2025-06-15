from strands import Agent, tool
import json
import asyncio
from typing import Dict, List
from datetime import datetime

# Load community data
def load_community_data():
    try:
        with open("data/community_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

COMMUNITY_DATA = load_community_data()

@tool
def coordinate_emergency_response(incident_type: str, location: str, severity: str) -> str:
    """
    Coordinate emergency response between multiple agents.
    
    Args:
        incident_type (str): Type of emergency (earthquake, medical, fire)
        location (str): Location of the incident
        severity (str): Severity level (low, medium, high, critical)
    
    Returns:
        str: Coordination response with resource allocation
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    response = f"🚨 EMERGENCY COORDINATION CENTER - {timestamp}\n"
    response += f"📍 Location: {location}\n"
    response += f"⚡ Incident: {incident_type.title()}\n"
    response += f"🔥 Severity: {severity.title()}\n\n"
    
    if severity.lower() in ["high", "critical"]:
        response += "🔴 CRITICAL RESPONSE ACTIVATED\n"
        response += "✅ Fire & Rescue dispatched\n"
        response += "✅ Medical teams en route\n"
        response += "✅ Police for crowd control\n"
        if incident_type.lower() == "earthquake":
            response += "✅ Building safety inspectors notified\n"
            response += "✅ Evacuation centers opening\n"
    else:
        response += "🟡 STANDARD RESPONSE ACTIVATED\n"
        response += "✅ Local emergency teams dispatched\n"
        response += "✅ Medical standby activated\n"
    
    return response

@tool
def get_resource_availability(location: str, resource_type: str) -> str:
    """
    Check availability of emergency resources in a location.
    
    Args:
        location (str): Location to check
        resource_type (str): Type of resource (medical, fire, police, evacuation)
    
    Returns:
        str: Resource availability status
    """
    location_lower = location.lower()
    
    if "bangkok" in location_lower or "thailand" in location_lower:
        if resource_type.lower() == "medical":
            hospitals = COMMUNITY_DATA.get("hospitals", {}).get("bangkok", [])
            return f"🏥 Bangkok Medical Resources:\n• {len(hospitals)} hospitals available\n• All trauma centers operational\n• Ambulance fleet ready"
        elif resource_type.lower() == "evacuation":
            centers = COMMUNITY_DATA.get("evacuation_centers", {}).get("bangkok", [])
            total_capacity = sum(center.get("capacity", 0) for center in centers)
            return f"🏕️ Bangkok Evacuation Centers:\n• {len(centers)} centers available\n• Total capacity: {total_capacity:,} persons\n• All facilities operational"
    
    elif "yangon" in location_lower or "myanmar" in location_lower:
        if resource_type.lower() == "medical":
            hospitals = COMMUNITY_DATA.get("hospitals", {}).get("yangon", [])
            return f"🏥 Yangon Medical Resources:\n• {len(hospitals)} hospitals available\n• Emergency wards operational\n• Medical supplies adequate"
        elif resource_type.lower() == "evacuation":
            centers = COMMUNITY_DATA.get("evacuation_centers", {}).get("yangon", [])
            total_capacity = sum(center.get("capacity", 0) for center in centers)
            return f"🏕️ Yangon Evacuation Centers:\n• {len(centers)} centers available\n• Total capacity: {total_capacity:,} persons\n• Basic facilities ready"
    
    return f"Resource information for {location} not available in current database."

# Create specialized agents for different emergency roles
medical_agent = Agent(
    tools=[get_resource_availability]
)

evacuation_agent = Agent(
    tools=[get_resource_availability]
)

coordination_agent = Agent(
    tools=[coordinate_emergency_response, get_resource_availability]
)

class MultiAgentCoordinator:
    """Coordinates multiple specialized emergency response agents"""
    
    def __init__(self):
        self.agents = {
            "medical": medical_agent,
            "evacuation": evacuation_agent,
            "coordination": coordination_agent
        }
        self.active_incidents = {}
    
    async def create_incident(self, incident_id: str, incident_type: str, location: str, severity: str) -> Dict:
        """Create a new emergency incident"""
        incident = {
            "id": incident_id,
            "type": incident_type,
            "location": location,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "responses": []
        }
        
        self.active_incidents[incident_id] = incident
        
        # Get initial coordination response
        coordination_response = await self.agents["coordination"].ainvoke(
            f"New {incident_type} incident at {location}, severity {severity}. Please coordinate initial response."
        )
        
        incident["responses"].append({
            "agent": "coordination",
            "response": coordination_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return incident
    
    async def get_medical_response(self, incident_id: str) -> str:
        """Get medical team response for an incident"""
        if incident_id not in self.active_incidents:
            return "Incident not found"
        
        incident = self.active_incidents[incident_id]
        location = incident["location"]
        
        response = await self.agents["medical"].ainvoke(
            f"Medical emergency response needed for {incident['type']} at {location}. "
            f"Severity: {incident['severity']}. Provide medical resource allocation."
        )
        
        incident["responses"].append({
            "agent": "medical",
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    async def get_evacuation_response(self, incident_id: str) -> str:
        """Get evacuation team response for an incident"""
        if incident_id not in self.active_incidents:
            return "Incident not found"
        
        incident = self.active_incidents[incident_id]
        location = incident["location"]
        
        response = await self.agents["evacuation"].ainvoke(
            f"Evacuation coordination needed for {incident['type']} at {location}. "
            f"Severity: {incident['severity']}. Provide evacuation plan and resource status."
        )
        
        incident["responses"].append({
            "agent": "evacuation",
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    async def get_full_response(self, incident_id: str) -> Dict:
        """Get coordinated response from all agents"""
        if incident_id not in self.active_incidents:
            return {"error": "Incident not found"}
        
        # Get responses from all specialized agents
        medical_response = await self.get_medical_response(incident_id)
        evacuation_response = await self.get_evacuation_response(incident_id)
        
        incident = self.active_incidents[incident_id]
        
        return {
            "incident": incident,
            "coordinated_response": {
                "medical": medical_response,
                "evacuation": evacuation_response,
                "coordination": incident["responses"][0]["response"]  # Initial coordination response
            }
        }
    
    def get_incident_status(self, incident_id: str) -> Dict:
        """Get current status of an incident"""
        if incident_id not in self.active_incidents:
            return {"error": "Incident not found"}
        
        return self.active_incidents[incident_id]
    
    def list_active_incidents(self) -> List[Dict]:
        """List all active incidents"""
        return list(self.active_incidents.values())

# Global coordinator instance
multi_agent_coordinator = MultiAgentCoordinator() 