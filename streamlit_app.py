import streamlit as st
import requests
import json
import asyncio
import aiohttp
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Disaster Ready: Earthquake Response Simulator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL - adjust for your deployment
API_BASE = "http://localhost:8000"

def init_session_state():
    """Initialize session state variables"""
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None
    if 'scenario_step' not in st.session_state:
        st.session_state.scenario_step = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_location' not in st.session_state:
        st.session_state.user_location = "general"

def render_header():
    """Render the main header"""
    st.title("🌍 Disaster Ready: Earthquake Response Simulator")
    st.markdown("""
    **AI-powered earthquake preparedness for Southeast Asia**  
    Learn life-saving skills through interactive scenarios and get expert advice from our AI safety advisor.
    """)
    
    # Location selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        location = st.selectbox(
            "📍 Your Location",
            options=["general", "bangkok", "yangon", "thailand", "myanmar"],
            index=["general", "bangkok", "yangon", "thailand", "myanmar"].index(st.session_state.user_location),
            help="Select your location for personalized advice and resources"
        )
        if location != st.session_state.user_location:
            st.session_state.user_location = location
            st.rerun()

def render_sidebar():
    """Render the sidebar with navigation"""
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Home", "🎯 Interactive Scenarios", "💬 Ask the Expert", "📚 Learn Basics", "📞 Emergency Contacts"],
        help="Navigate through different sections of the simulator"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🆘 Quick Emergency Info")
    st.sidebar.markdown(f"**Location:** {st.session_state.user_location.title()}")
    
    if st.session_state.user_location in ["bangkok", "thailand"]:
        st.sidebar.error("🚨 Emergency: 191")
        st.sidebar.info("🏥 Medical: 1669")
    elif st.session_state.user_location in ["yangon", "myanmar"]:
        st.sidebar.error("🚨 Emergency: 999")
        st.sidebar.info("🏥 Medical: 192")
    else:
        st.sidebar.info("Select your location for local emergency numbers")
    
    return page

def render_home():
    """Render the home page"""
    st.header("🏠 Welcome to Disaster Ready")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Interactive Scenarios")
        st.markdown("""
        Practice your earthquake response skills through realistic scenarios:
        - **Nighttime at Home** - Learn what to do when sleeping
        - **At the Office** - Workplace safety procedures  
        - **Public Spaces** - Shopping malls, schools, and more
        - **Driving** - Vehicle safety during earthquakes
        """)
        if st.button("Start Practice Scenarios", type="primary"):
            st.session_state.page = "scenarios"
            st.rerun()
    
    with col2:
        st.subheader("💬 AI Safety Advisor")
        st.markdown("""
        Get instant answers to your earthquake safety questions:
        - Emergency response procedures
        - Building safety assessments
        - Local hospital and evacuation information
        - Post-earthquake recovery guidance
        """)
        if st.button("Ask Questions", type="primary"):
            st.session_state.page = "expert"
            st.rerun()
    
    # Recent earthquake information
    st.markdown("---")
    st.subheader("📈 Recent Earthquake Activity")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Myanmar-Thailand Border", "6.8 Magnitude", "January 2024")
    with col2:
        st.metric("Affected Cities", "3 Major", "Bangkok, Yangon, Chiang Mai")
    with col3:
        st.metric("Risk Level", "High", "Border regions")
    
    st.info("🔔 Stay informed about earthquake risks in your area and practice preparedness regularly.")

def render_scenarios():
    """Render the interactive scenarios page"""
    st.header("🎯 Interactive Earthquake Scenarios")
    
    try:
        # Get available scenarios
        response = requests.get(f"{API_BASE}/scenarios")
        if response.status_code == 200:
            scenarios_data = response.json()
            scenarios = scenarios_data.get("scenarios", [])
            
            if not st.session_state.current_scenario:
                # Scenario selection
                st.subheader("Choose Your Scenario")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🎲 Random Scenario", type="primary"):
                        try:
                            start_response = requests.post(f"{API_BASE}/scenario/start", 
                                                         json={"random": True})
                            if start_response.status_code == 200:
                                st.session_state.current_scenario = start_response.json()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error starting random scenario: {e}")
                
                with col2:
                    location_scenario = st.selectbox(
                        "Choose by location:",
                        ["", "apartment", "office", "mall", "school"],
                        format_func=lambda x: x.title() if x else "Select location..."
                    )
                    if location_scenario and st.button("Start Location Scenario"):
                        try:
                            start_response = requests.post(f"{API_BASE}/scenario/start",
                                                         json={"location": location_scenario})
                            if start_response.status_code == 200:
                                st.session_state.current_scenario = start_response.json()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error starting scenario: {e}")
                
                # Display available scenarios
                st.subheader("Available Scenarios")
                for scenario in scenarios:
                    with st.expander(f"{scenario['title']} ({scenario['difficulty'].title()})"):
                        st.markdown(f"**Location:** {scenario['location'].title()}")
                        st.markdown(f"**Description:** {scenario['description']}")
                        if st.button(f"Start {scenario['title']}", key=scenario['id']):
                            try:
                                start_response = requests.post(f"{API_BASE}/scenario/start",
                                                             json={"scenario_id": scenario['id']})
                                if start_response.status_code == 200:
                                    st.session_state.current_scenario = start_response.json()
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error starting scenario: {e}")
            
            else:
                # Active scenario
                render_active_scenario()
                
        else:
            st.error("Unable to load scenarios. Please check if the API server is running.")
            
    except Exception as e:
        st.error(f"Connection error: {e}")
        st.info("Make sure the API server is running on http://localhost:8000")

def render_active_scenario():
    """Render an active scenario"""
    scenario = st.session_state.current_scenario
    
    if "scenario" in scenario:
        scenario_info = scenario["scenario"]
        
        # Scenario header
        st.subheader(f"🚨 {scenario_info['title']}")
        
        # Scenario details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Location", scenario_info.get('location', 'Unknown').title())
        with col2:
            st.metric("Magnitude", f"{scenario_info.get('magnitude', 'N/A')}")
        with col3:
            st.metric("Time", scenario_info.get('time', 'Unknown').title())
        
        # Scenario description
        st.markdown("### Situation")
        st.warning(scenario_info['description'])
        
        # Choices
        st.markdown("### What do you do?")
        choices = scenario.get("choices", [])
        
        for choice in choices:
            if st.button(choice["text"], key=choice["id"], type="secondary"):
                try:
                    choice_response = requests.post(f"{API_BASE}/scenario/choice",
                                                  json={"choice_id": choice["id"]})
                    if choice_response.status_code == 200:
                        result = choice_response.json()
                        handle_scenario_result(result)
                except Exception as e:
                    st.error(f"Error submitting choice: {e}")
        
        # Reset scenario button
        if st.button("🔄 Reset Scenario"):
            st.session_state.current_scenario = None
            st.rerun()

def handle_scenario_result(result):
    """Handle the result of a scenario choice"""
    if "choice_result" in result:
        # Show immediate feedback
        choice_result = result["choice_result"]
        
        if choice_result["correct"]:
            st.success(f"✅ Correct! {choice_result['explanation']}")
        else:
            st.error(f"❌ {choice_result['explanation']}")
        
        st.info(f"Score: {choice_result['score']} points")
        
        # Check for follow-up
        if "follow_up" in result:
            st.markdown("### Follow-up Question")
            st.info(result["follow_up"]["question"])
            
            for choice in result["follow_up"]["choices"]:
                if st.button(choice["text"], key=f"followup_{choice['id']}", type="secondary"):
                    try:
                        followup_response = requests.post(f"{API_BASE}/scenario/choice",
                                                        json={"choice_id": choice["id"]})
                        if followup_response.status_code == 200:
                            final_result = followup_response.json()
                            handle_scenario_completion(final_result)
                    except Exception as e:
                        st.error(f"Error submitting follow-up: {e}")
    
    elif "scenario_complete" in result:
        handle_scenario_completion(result)

def handle_scenario_completion(result):
    """Handle scenario completion"""
    if "results" in result:
        results = result["results"]
        
        st.markdown("### Scenario Complete! 🎉")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Your Score", f"{results['score']}/{results['max_score']}")
        with col2:
            st.metric("Percentage", f"{results['percentage']:.1f}%")
        with col3:
            performance = results['performance'].replace('_', ' ').title()
            st.metric("Performance", performance)
        
        # Performance message
        if results['performance'] == "excellent":
            st.success("🌟 Excellent! You demonstrated strong earthquake safety knowledge.")
        elif results['performance'] == "good":
            st.info("👍 Good job! Review the feedback to improve further.")
        elif results['performance'] == "needs_improvement":
            st.warning("📚 Keep learning! Practice these scenarios more.")
        else:
            st.error("⚠️ Study earthquake safety procedures - your choices could be dangerous.")
        
        # Lessons learned
        if results.get('lessons_learned'):
            st.markdown("### Key Lessons")
            for lesson in results['lessons_learned']:
                st.markdown(f"- {lesson}")
        
        # Reset for next scenario
        st.session_state.current_scenario = None
        
        if st.button("Try Another Scenario", type="primary"):
            st.rerun()

def render_expert_chat():
    """Render the expert chat interface"""
    st.header("💬 Ask the Earthquake Safety Expert")
    st.markdown("Get instant, AI-powered advice on earthquake safety and preparedness.")
    
    # Chat input
    user_question = st.text_input(
        "Ask your question:",
        placeholder="e.g., What should I do if an earthquake hits while I'm driving?",
        help="Ask anything about earthquake safety, emergency procedures, or local resources"
    )
    
    if st.button("Ask Expert", type="primary") or user_question:
        if user_question:
            # Add to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question,
                "timestamp": datetime.now()
            })
            
            # Get response from API
            try:
                with st.spinner("Getting expert advice..."):
                    response = requests.post(f"{API_BASE}/ask/direct",
                                           json={
                                               "question": user_question,
                                               "location": st.session_state.user_location
                                           })
                    
                    if response.status_code == 200:
                        result = response.json()
                        expert_response = result["response"]
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": expert_response,
                            "timestamp": datetime.now()
                        })
                    else:
                        st.error("Sorry, I couldn't get a response. Please try again.")
                        
            except Exception as e:
                st.error(f"Connection error: {e}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Conversation")
        for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
            timestamp = message["timestamp"].strftime("%H:%M")
            
            if message["role"] == "user":
                st.markdown(f"**You** ({timestamp}): {message['content']}")
            else:
                st.markdown(f"**🤖 Expert** ({timestamp}):")
                st.info(message['content'])
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

def render_learn_basics():
    """Render the learn basics page"""
    st.header("📚 Earthquake Safety Basics")
    
    try:
        response = requests.get(f"{API_BASE}/learn/basics")
        if response.status_code == 200:
            basics = response.json()
            
            # DROP, COVER, HOLD ON
            st.subheader("🚨 DROP, COVER, and HOLD ON")
            st.success(basics["drop_cover_hold"]["description"])
            
            for i, step in enumerate(basics["drop_cover_hold"]["steps"], 1):
                st.markdown(f"**{i}.** {step}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("❌ Common Mistakes")
                for mistake in basics["common_mistakes"]:
                    st.markdown(f"• {mistake}")
            
            with col2:
                st.subheader("✅ Preparation Tips")
                for tip in basics["preparation_tips"]:
                    st.markdown(f"• {tip}")
        
        # Regional information
        response = requests.get(f"{API_BASE}/learn/southeast-asia")
        if response.status_code == 200:
            regional = response.json()
            
            st.markdown("---")
            st.subheader("🌏 Southeast Asia Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**High Risk Areas:**")
                for area in regional["high_risk_areas"]:
                    st.markdown(f"• {area}")
            
            with col2:
                st.markdown("**Cultural Considerations:**")
                for consideration in regional["cultural_considerations"]:
                    st.markdown(f"• {consideration}")
            
            # Recent activity
            if "recent_activity" in regional:
                st.subheader("📈 Recent Activity")
                activity = regional["recent_activity"]["2024_myanmar_thailand"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Magnitude", activity["magnitude"])
                with col2:
                    st.metric("Location", activity["location"])
                with col3:
                    st.metric("Cities Affected", len(activity["affected_cities"]))
                
                st.markdown("**Key Lessons:**")
                for lesson in activity["lessons"]:
                    st.markdown(f"• {lesson}")
    
    except Exception as e:
        st.error(f"Error loading educational content: {e}")

def render_emergency_contacts():
    """Render emergency contacts based on location"""
    st.header("📞 Emergency Contacts")
    
    try:
        response = requests.post(f"{API_BASE}/ask/direct",
                               json={
                                   "question": f"emergency contacts for {st.session_state.user_location}",
                                   "location": st.session_state.user_location
                               })
        
        if response.status_code == 200:
            result = response.json()
            st.markdown(result["response"])
            
        # Additional resources
        st.markdown("---")
        st.subheader("🏥 Find Nearby Resources")
        
        if st.button("Find Hospitals"):
            hospital_response = requests.post(f"{API_BASE}/ask/direct",
                                            json={
                                                "question": f"nearest hospitals in {st.session_state.user_location}",
                                                "location": st.session_state.user_location
                                            })
            if hospital_response.status_code == 200:
                result = hospital_response.json()
                st.markdown(result["response"])
        
        if st.button("Find Evacuation Centers"):
            evacuation_response = requests.post(f"{API_BASE}/ask/direct",
                                               json={
                                                   "question": f"evacuation centers in {st.session_state.user_location}",
                                                   "location": st.session_state.user_location
                                               })
            if evacuation_response.status_code == 200:
                result = evacuation_response.json()
                st.markdown(result["response"])
    
    except Exception as e:
        st.error(f"Error loading emergency contacts: {e}")

def main():
    """Main application function"""
    init_session_state()
    render_header()
    
    page = render_sidebar()
    
    # Route to different pages
    if page == "🏠 Home":
        render_home()
    elif page == "🎯 Interactive Scenarios":
        render_scenarios()
    elif page == "💬 Ask the Expert":
        render_expert_chat()
    elif page == "📚 Learn Basics":
        render_learn_basics()
    elif page == "📞 Emergency Contacts":
        render_emergency_contacts()
    
    # Footer
    st.markdown("---")
    st.markdown("🌍 **Disaster Ready** - Preparing Southeast Asia for earthquake safety")
    st.markdown("*Always follow local emergency authorities and official disaster response guidelines.*")

if __name__ == "__main__":
    main() 