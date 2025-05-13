# agents/api_agent.py

from fastapi import FastAPI, Query
from typing import List, Dict
import yfinance as yf

app = FastAPI()

@app.get("/get_stock_data")
def get_stock_data(tickers: List[str] = Query(...)):
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            latest = hist.iloc[-1].to_dict()
            previous = hist.iloc[-2].to_dict()
            change_pct = ((latest['Close'] - previous['Close']) / previous['Close']) * 100

            data[ticker] = {
                "latest_close": latest['Close'],
                "previous_close": previous['Close'],
                "change_pct": round(change_pct, 2)
            }
        except Exception as e:
            data[ticker] = {"error": str(e)}
    return data

@app.get("/get_sector_exposure")
def get_sector_exposure(region: str = "Asia", sector: str = "Technology") -> Dict:
    # Placeholder logic: simulate asset allocation
    allocation_today = 22  # Replace with actual portfolio analytics
    allocation_yesterday = 18
    return {
        "region": region,
        "sector": sector,
        "allocation_today": f"{allocation_today}%",
        "allocation_yesterday": f"{allocation_yesterday}%",
    }
