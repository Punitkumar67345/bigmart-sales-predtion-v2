import subprocess
import time
import sys
import os

def start_servers():
    print("========================================")
    print("🚀 INITIALIZING BIG MART INTELLIGENCE 🚀")
    print("========================================")
    
    # Get the absolute path of your main BIGMARTAPP folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Start FastAPI Backend
    print("🟢 Starting Backend Server (FastAPI on Port 8000)...")
    # Run uvicorn from the base directory so it finds backend.main
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"],
        cwd=base_dir 
    )
    
    # Wait 2 seconds for backend to wake up
    time.sleep(2) 
    
    # 2. Start Streamlit Frontend
    print("🌌 Starting Frontend UI (Streamlit on Port 8501)...")
    # Tell Streamlit to run specifically from inside the "frontend" folder
    frontend_dir = os.path.join(base_dir, "frontend")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        cwd=frontend_dir 
    )
    
    try:
        # Keep both running
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        # If you press Ctrl+C, kill both safely
        print("\n🛑 Shutting down all systems...")
        backend.terminate()
        frontend.terminate()
        print("✅ System offline. Have a great day!")

if __name__ == "__main__":
    start_servers()