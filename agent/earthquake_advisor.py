from strands import Agent, tool
import json
import os

# Load community data
def load_community_data():
    try:
        with open("data/community_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

COMMUNITY_DATA = load_community_data()

@tool
def get_emergency_contacts(location: str = "general") -> str:
    """
    Get emergency contact numbers for a specific location.
    
    Args:
        location (str): Location (thailand, myanmar, or general)
    
    Returns:
        str: Emergency contact information
    """
    contacts = COMMUNITY_DATA.get("emergency_contacts", {})
    
    if location.lower() in ["thailand", "bangkok"]:
        thai_contacts = contacts.get("thailand", {})
        return f"""Thailand Emergency Contacts:
🚨 Emergency Hotline: {thai_contacts.get('emergency_hotline', 'N/A')}
🏥 Medical Emergency: {thai_contacts.get('medical_emergency', 'N/A')}
🚒 Fire Brigade: {thai_contacts.get('fire_brigade', 'N/A')}
👮 Tourist Police: {thai_contacts.get('tourist_police', 'N/A')}
🌊 Disaster Management: {thai_contacts.get('disaster_management', 'N/A')}"""
    
    elif location.lower() in ["myanmar", "yangon"]:
        myanmar_contacts = contacts.get("myanmar", {})
        return f"""Myanmar Emergency Contacts:
🚨 Emergency Hotline: {myanmar_contacts.get('emergency_hotline', 'N/A')}
🏥 Medical Emergency: {myanmar_contacts.get('medical_emergency', 'N/A')}
🚒 Fire Brigade: {myanmar_contacts.get('fire_brigade', 'N/A')}
👮 Police: {myanmar_contacts.get('police', 'N/A')}
🌊 Disaster Management: {myanmar_contacts.get('disaster_management', 'N/A')}"""
    
    else:
        intl_contacts = contacts.get("international", {})
        return f"""International Emergency Contacts:
🔴 Red Cross: {intl_contacts.get('red_cross', 'N/A')}
🏥 WHO Emergency: {intl_contacts.get('who_emergency', 'N/A')}

For local contacts, specify 'thailand' or 'myanmar'."""

@tool
def get_earthquake_safety_advice(situation: str) -> str:
    """
    Provides specific earthquake safety advice based on the situation.
    
    Args:
        situation (str): Description of the current situation
    
    Returns:
        str: Specific safety advice
    """
    situation_lower = situation.lower()
    
    if any(word in situation_lower for word in ["sleeping", "bed", "night", "asleep"]):
        return """🛏️ DURING EARTHQUAKE WHILE SLEEPING:
✅ STAY in bed
✅ COVER your head and neck with a pillow
✅ HOLD ON until shaking stops
❌ DON'T run outside during shaking
❌ DON'T stand up during shaking

After shaking stops: Check for injuries and hazards before moving."""
    
    elif any(word in situation_lower for word in ["office", "work", "desk", "building"]):
        return """🏢 DURING EARTHQUAKE AT OFFICE:
✅ DROP under your desk
✅ COVER your head and neck
✅ HOLD ON to your desk
❌ DON'T use elevators
❌ DON'T run to exits during shaking

After shaking: Use stairs for evacuation, never elevators."""
    
    elif any(word in situation_lower for word in ["outside", "street", "outdoor"]):
        return """🌳 DURING EARTHQUAKE OUTDOORS:
✅ Move AWAY from buildings, power lines, trees
✅ DROP to the ground if you can't move away
✅ COVER your head and neck
❌ DON'T enter damaged buildings
❌ DON'T stand near tall structures

Stay alert for aftershocks and falling debris."""
    
    elif any(word in situation_lower for word in ["car", "driving", "vehicle"]):
        return """🚗 DURING EARTHQUAKE WHILE DRIVING:
✅ STOP as quickly and safely as possible
✅ Stay IN the vehicle
✅ AVOID bridges, overpasses, power lines
❌ DON'T stop under bridges or overpasses
❌ DON'T get out during shaking

After shaking: Check for road damage before continuing."""
    
    elif any(word in situation_lower for word in ["school", "classroom", "students"]):
        return """🏫 DURING EARTHQUAKE AT SCHOOL:
✅ DROP, COVER, and HOLD ON
✅ Get under desks or tables
✅ Stay calm and follow teacher's instructions
❌ DON'T run to doorways
❌ DON'T run outside during shaking

Teachers: Lead by example, give clear directions."""
    
    else:
        return """⚡ GENERAL EARTHQUAKE SAFETY - DROP, COVER, HOLD ON:
✅ DROP to hands and knees immediately
✅ COVER head and neck with arms/find shelter under table
✅ HOLD ON to shelter and protect yourself

❌ DON'T run outside during shaking
❌ DON'T stand in doorways
❌ DON'T use elevators

Remember: Most injuries occur when people try to move during earthquakes."""

@tool
def find_nearest_hospital(location: str) -> str:
    """
    Find nearest hospitals with emergency services.
    
    Args:
        location (str): Your current location (bangkok, yangon, etc.)
    
    Returns:
        str: List of nearby hospitals
    """
    hospitals = COMMUNITY_DATA.get("hospitals", {})
    location_lower = location.lower()
    
    if "bangkok" in location_lower or "thailand" in location_lower:
        bangkok_hospitals = hospitals.get("bangkok", [])
        result = "🏥 BANGKOK EMERGENCY HOSPITALS:\n\n"
        for hospital in bangkok_hospitals:
            result += f"📍 {hospital.get('name', 'Unknown')}\n"
            result += f"   📞 {hospital.get('phone', 'N/A')}\n"
            result += f"   📍 {hospital.get('address', 'N/A')}\n"
            if hospital.get('emergency_24h'):
                result += "   ⏰ 24/7 Emergency\n"
            if hospital.get('trauma_center'):
                result += "   🚑 Trauma Center\n"
            result += "\n"
        return result
    
    elif "yangon" in location_lower or "myanmar" in location_lower:
        yangon_hospitals = hospitals.get("yangon", [])
        result = "🏥 YANGON EMERGENCY HOSPITALS:\n\n"
        for hospital in yangon_hospitals:
            result += f"📍 {hospital.get('name', 'Unknown')}\n"
            result += f"   📞 {hospital.get('phone', 'N/A')}\n"
            result += f"   📍 {hospital.get('address', 'N/A')}\n"
            if hospital.get('emergency_24h'):
                result += "   ⏰ 24/7 Emergency\n"
            if hospital.get('trauma_center'):
                result += "   🚑 Trauma Center\n"
            result += "\n"
        return result
    
    else:
        return "Please specify your location (Bangkok or Yangon) to find nearby hospitals."

@tool
def get_evacuation_centers(location: str) -> str:
    """
    Get information about evacuation centers and safe areas.
    
    Args:
        location (str): Your current location
    
    Returns:
        str: List of evacuation centers
    """
    centers = COMMUNITY_DATA.get("evacuation_centers", {})
    location_lower = location.lower()
    
    if "bangkok" in location_lower:
        bangkok_centers = centers.get("bangkok", [])
        result = "🏕️ BANGKOK EVACUATION CENTERS:\n\n"
        for center in bangkok_centers:
            result += f"📍 {center.get('name', 'Unknown')}\n"
            result += f"   📍 {center.get('address', 'N/A')}\n"
            result += f"   👥 Capacity: {center.get('capacity', 'Unknown')} people\n"
            facilities = center.get('facilities', [])
            if facilities:
                result += f"   🏗️ Facilities: {', '.join(facilities)}\n"
            result += "\n"
        return result
    
    elif "yangon" in location_lower:
        yangon_centers = centers.get("yangon", [])
        result = "🏕️ YANGON EVACUATION CENTERS:\n\n"
        for center in yangon_centers:
            result += f"📍 {center.get('name', 'Unknown')}\n"
            result += f"   📍 {center.get('address', 'N/A')}\n"
            result += f"   👥 Capacity: {center.get('capacity', 'Unknown')} people\n"
            facilities = center.get('facilities', [])
            if facilities:
                result += f"   🏗️ Facilities: {', '.join(facilities)}\n"
            result += "\n"
        return result
    
    else:
        return "Please specify your location (Bangkok or Yangon) to find evacuation centers."

@tool
def check_building_safety(building_description: str) -> str:
    """
    Provide guidance on assessing building safety after an earthquake.
    
    Args:
        building_description (str): Description of the building or damage observed
    
    Returns:
        str: Safety assessment guidance
    """
    return """🏗️ POST-EARTHQUAKE BUILDING SAFETY CHECK:

🔍 LOOK FOR THESE DANGER SIGNS:
❌ Cracks in walls, especially at corners
❌ Doors/windows that won't open or close
❌ Broken gas lines (smell of gas)
❌ Electrical damage (sparks, exposed wires)
❌ Water line breaks
❌ Tilting or leaning structure
❌ Broken glass or debris

✅ IF BUILDING SEEMS SAFE:
• Still be cautious of aftershocks
• Keep emergency supplies ready
• Have evacuation plan ready

⚠️ IF YOU SEE DAMAGE:
• EVACUATE immediately
• Don't use elevators
• Turn off utilities if trained to do so
• Call local authorities

🚨 WHEN IN DOUBT, GET OUT!
Don't risk your life for belongings."""

# Create an enhanced agent with multiple tools
earthquake_advisor_agent = Agent(
    tools=[
        get_earthquake_safety_advice,
        get_emergency_contacts,
        find_nearest_hospital,
        get_evacuation_centers,
        check_building_safety
    ]
) 