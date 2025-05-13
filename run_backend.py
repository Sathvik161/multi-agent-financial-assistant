import subprocess
import os
import time
from threading import Thread

SERVICES = [
    {"name": "API Agent", "command": "uvicorn agents.api_agent:app --host 0.0.0.0 --port 8001"},
    {"name": "Scraping Agent", "command": "uvicorn agents.scraping_agent:app --host 0.0.0.0 --port 8002"},
    {"name": "Retriever Agent", "command": "uvicorn agents.retriever_agent:app --host 0.0.0.0 --port 8003"},
    {"name": "Analysis Agent", "command": "uvicorn agents.analysis_agent:app --host 0.0.0.0 --port 8004"},
    {"name": "Language Agent", "command": "uvicorn agents.language_agent:app --host 0.0.0.0 --port 8005"},
    {"name": "Voice Agent", "command": "uvicorn agents.voice_agent:app --host 0.0.0.0 --port 8006"},
    {"name": "Orchestrator", "command": "uvicorn orchestrator.orchestrator:app --host 0.0.0.0 --port 8007 --reload"}
]

def run_service(command, name):
    print(f"🚀 Starting {name}...")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed: {e}")

if __name__ == "__main__":
    os.makedirs("data/filings", exist_ok=True)
    
    # Start services sequentially with delays
    for service in SERVICES:
        Thread(target=run_service, args=(service["command"], service["name"])).start()
        time.sleep(2)  # Increased delay between services
    
    print("\n✅ All backend services should be running!")
    print("Orchestrator URL: http://localhost:8000")
    print("Press Ctrl+C to stop all services")
    
    try:
        while True:  # Keep main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")