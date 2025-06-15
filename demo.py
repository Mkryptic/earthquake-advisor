#!/usr/bin/env python3
"""
Demo script for Disaster Ready: Earthquake Response Simulator
Tests the agent and scenario functionality
"""

import asyncio
import json
from agent.earthquake_advisor import earthquake_advisor_agent
from simulation.scenario_engine import scenario_engine

async def demo_agent():
    """Demonstrate the AI agent capabilities"""
    print("🤖 TESTING AI EARTHQUAKE ADVISOR")
    print("=" * 40)
    
    test_questions = [
        "What should I do if an earthquake hits while I'm sleeping?",
        "How do I check if a building is safe after an earthquake?",
        "What are the emergency numbers for Thailand?",
        "Find hospitals in Bangkok",
        "What should I do if I'm driving during an earthquake?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("💬 Answer:")
        try:
            response = await earthquake_advisor_agent.ainvoke(question)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)

def demo_scenarios():
    """Demonstrate the interactive scenarios"""
    print("\n🎯 TESTING INTERACTIVE SCENARIOS")
    print("=" * 40)
    
    # Get available scenarios
    scenarios = scenario_engine.get_available_scenarios()
    print(f"📋 Available scenarios: {len(scenarios)}")
    
    for scenario in scenarios:
        print(f"• {scenario['title']} ({scenario['difficulty']})")
    
    # Start a random scenario
    print("\n🎲 Starting random scenario...")
    scenario = scenario_engine.get_random_scenario()
    
    if "error" not in scenario:
        print(f"📖 Scenario: {scenario['scenario']['title']}")
        print(f"📍 Location: {scenario['scenario']['location']}")
        print(f"📏 Magnitude: {scenario['scenario']['magnitude']}")
        print(f"🕒 Time: {scenario['scenario']['time']}")
        print(f"📝 Description: {scenario['scenario']['description']}")
        
        print("\n🤔 Choices:")
        for i, choice in enumerate(scenario['choices'], 1):
            print(f"{i}. {choice['text']}")
        
        # Simulate choosing the first option
        first_choice = scenario['choices'][0]['id']
        print(f"\n✅ Selecting: {scenario['choices'][0]['text']}")
        
        result = scenario_engine.submit_choice(first_choice)
        print(f"📊 Result: {result}")
    else:
        print(f"❌ Error: {scenario['error']}")

def demo_data():
    """Demonstrate the community data"""
    print("\n🏥 TESTING COMMUNITY DATA")
    print("=" * 40)
    
    try:
        with open("data/community_data.json", "r") as f:
            data = json.load(f)
        
        print("📞 Emergency Contacts:")
        for country, contacts in data.get("emergency_contacts", {}).items():
            print(f"  {country.title()}:")
            for service, number in contacts.items():
                print(f"    {service}: {number}")
        
        print("\n🏥 Hospitals:")
        for city, hospitals in data.get("hospitals", {}).items():
            print(f"  {city.title()}: {len(hospitals)} hospitals")
        
        print("\n🏕️ Evacuation Centers:")
        for city, centers in data.get("evacuation_centers", {}).items():
            print(f"  {city.title()}: {len(centers)} centers")
            
    except FileNotFoundError:
        print("❌ Community data file not found")

async def main():
    """Run the complete demo"""
    print("🌍 DISASTER READY: EARTHQUAKE RESPONSE SIMULATOR")
    print("🔥 COMPREHENSIVE DEMO")
    print("=" * 60)
    
    # Test agent
    await demo_agent()
    
    # Test scenarios
    demo_scenarios()
    
    # Test data
    demo_data()
    
    print("\n✅ Demo completed!")
    print("🚀 To run the full application:")
    print("   python main.py  (for API)")
    print("   streamlit run app.py  (for web interface)")

if __name__ == "__main__":
    asyncio.run(main()) 