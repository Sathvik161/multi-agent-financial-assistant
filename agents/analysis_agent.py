# agents/analysis_agent.py

from fastapi import FastAPI, Query
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Local FastAPI microservice endpoints
API_AGENT_URL = "http://localhost:8001"
SCRAPER_AGENT_URL = "http://localhost:8002"
RETRIEVER_AGENT_URL = "http://localhost:8003"

class AnalysisRequest(BaseModel):
    portfolio_data: dict
    market_data: dict
    earnings_data: dict
    context_data: list = []

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        # Your analysis logic here
        return {
            "prompt_input": f"Analysis of {len(request.market_data)} stocks with {len(request.earnings_data)} earnings reports"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
def analyze(
    tickers: str = Query(...), 
    query: str = Query("asia tech earnings"), 
    region: str = "Asia", 
    sector: str = "Technology"
):
    ticker_list = tickers.split(",")

    # 1. Fetch exposure from API Agent
    exposure_resp = requests.get(
        f"{API_AGENT_URL}/get_sector_exposure", 
        params={"region": region, "sector": sector}
    )
    exposure_data = exposure_resp.json()

    # 2. Fetch stock price delta from API Agent
    stock_resp = requests.get(
        f"{API_AGENT_URL}/get_stock_data", 
        params={"tickers": ticker_list}
    )
    stock_data = stock_resp.json()

    # 3. Fetch earnings surprise from Scraping Agent
    earnings_resp = requests.get(
        f"{SCRAPER_AGENT_URL}/get_earnings_surprise", 
        params={"tickers": tickers}
    )
    earnings_data = earnings_resp.json()

    # 4. Retrieve context from Retriever Agent
    retriever_resp = requests.get(
        f"{RETRIEVER_AGENT_URL}/retrieve", 
        params={"query": query, "k": 3}
    )
    context_data = retriever_resp.json().get("results", [])

    # Format output for the LLM
    summary = f"""### Market Brief Input Summary

📌 Region Exposure:
- {region} {sector} allocation is {exposure_data['allocation_today']} (was {exposure_data['allocation_yesterday']} yesterday)

📈 Stock Price Movements:
"""
    for ticker in ticker_list:
        if ticker in stock_data:
            stock = stock_data[ticker]
            summary += f"- {ticker.upper()}: {stock.get('change_pct', '?')}% change\n"

    summary += "\n📊 Earnings Surprises:\n"
    for ticker in ticker_list:
        if ticker in earnings_data:
            earnings = earnings_data[ticker]
            summary += f"- {ticker.upper()}: {earnings.get('surprise', 'N/A')}\n"

    summary += "\n🧠 Context for Reasoning (from filings):\n"
    for chunk in context_data:
        summary += f"- {chunk['content'][:200]}...\n"  # show partial content

    return {
        "prompt_input": summary
    }
