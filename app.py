import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Disaster Ready: Earthquake Response Simulator",
    page_icon="🌍",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

def init_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_location' not in st.session_state:
        st.session_state.user_location = "general"

def main():
    init_session_state()
    
    st.title("🌍 Disaster Ready: Earthquake Response Simulator")
    st.markdown("**AI-powered earthquake preparedness for Southeast Asia**")
    
    # Location selector
    location = st.selectbox(
        "📍 Your Location",
        options=["general", "bangkok", "yangon", "thailand", "myanmar"]
    )
    st.session_state.user_location = location
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Ask Expert", "🎯 Scenarios", "📚 Learn"])
    
    with tab1:
        st.header("Ask the Earthquake Safety Expert")
        
        user_question = st.text_input("Ask your question:")
        
        if st.button("Ask") and user_question:
            try:
                response = requests.post(f"{API_BASE}/ask/direct",
                                       json={
                                           "question": user_question,
                                           "location": location
                                       })
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Expert Response:")
                    st.write(result["response"])
                else:
                    st.error("Error getting response")
                    
            except Exception as e:
                st.error(f"Connection error: {e}")
    
    with tab2:
        st.header("Interactive Scenarios")
        
        if st.button("Start Random Scenario"):
            try:
                response = requests.post(f"{API_BASE}/scenario/start",
                                       json={"random": True})
                if response.status_code == 200:
                    scenario = response.json()
                    st.write("**Scenario:**", scenario["scenario"]["title"])
                    st.write(scenario["scenario"]["description"])
                    
                    for choice in scenario["choices"]:
                        if st.button(choice["text"], key=choice["id"]):
                            choice_response = requests.post(f"{API_BASE}/scenario/choice",
                                                          json={"choice_id": choice["id"]})
                            if choice_response.status_code == 200:
                                result = choice_response.json()
                                st.write(result)
                                
            except Exception as e:
                st.error(f"Error: {e}")
    
    with tab3:
        st.header("Learn Earthquake Safety")
        
        try:
            response = requests.get(f"{API_BASE}/learn/basics")
            if response.status_code == 200:
                basics = response.json()
                
                st.subheader("DROP, COVER, and HOLD ON")
                for step in basics["drop_cover_hold"]["steps"]:
                    st.write(f"• {step}")
                    
        except Exception as e:
            st.error(f"Error loading content: {e}")

if __name__ == "__main__":
    main() 