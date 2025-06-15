#!/usr/bin/env python3
"""
Disaster Ready: Earthquake Response Simulator
Run script to start both API and Streamlit app
"""

import subprocess
import sys
import time
import threading

def run_api():
    """Run the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    subprocess.run([sys.executable, "main.py"])

def run_streamlit():
    """Run the Streamlit frontend"""
    print("🌐 Starting Streamlit frontend...")
    time.sleep(3)  # Wait for API to start
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def main():
    print("🌍 Disaster Ready: Earthquake Response Simulator")
    print("=" * 50)
    
    # Start API in background thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Start Streamlit in main thread
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\n👋 Shutting down simulator...")
        sys.exit(0)

if __name__ == "__main__":
    main() 