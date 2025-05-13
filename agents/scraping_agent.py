# agents/scraping_agent.py

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI()

DATA_DIR = "data/filings"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists

def fetch_earnings_surprise(ticker: str):
    """
    Scrape earnings surprise from Finviz.
    Save result as text file in /data/filings/.
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return {"error": f"Failed to fetch data for {ticker}"}

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", class_="snapshot-table2")

    eps_actual = eps_estimate = surprise = "N/A"
    summary_lines = []

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        for i in range(len(cells) - 1):
            key = cells[i].text.strip()
            value = cells[i + 1].text.strip()
            if key == "EPS (ttm)":
                eps_actual = value
            if key == "Earnings":
                surprise = value

    summary = (
        f"Earnings Summary for {ticker}:\n"
        f"EPS Actual: {eps_actual}\n"
        f"Earnings Surprise: {surprise}\n"
    )

    # Save to text file
    with open(os.path.join(DATA_DIR, f"{ticker}.txt"), "w") as f:
        f.write(summary)

    return {
        "ticker": ticker,
        "eps_actual": eps_actual,
        "surprise": surprise,
        "saved_to": f"{DATA_DIR}/{ticker}.txt"
    }

@app.get("/get_earnings_surprise")
def get_earnings(tickers: str):
    results = {}
    for ticker in tickers.split(","):
        results[ticker] = fetch_earnings_surprise(ticker.strip().upper())
    return results
