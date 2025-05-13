# orchestrator/orchestrator.py

from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Microservice URLs
ANALYSIS_URL = "http://localhost:8004/analyze"
LLM_URL = "http://localhost:8005/generate_briefing"

@app.get("/briefing")
def get_briefing(
    tickers: str = Query("TSM,005930.KQ"),
    query: str = Query("What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?")
):
    # 1. Get structured input from analysis agent
    analysis = requests.get(ANALYSIS_URL, params={"tickers": tickers, "query": query}).json()
    prompt_input = analysis.get("prompt_input", "")

    # 2. Get narrative from LLM
    llm_response = requests.get(LLM_URL, params={"query_input": prompt_input}).json()
    return {
        "query": query,
        "prompt_input": prompt_input,
        "narrative": llm_response.get("narrative", "LLM failed to respond.")
    }
