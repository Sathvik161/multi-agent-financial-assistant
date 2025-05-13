#  AI Tool Usage Log

This document details all prompts, AI-generated code, and model parameters used to build the Multi-Agent Finance Assistant.

---

## 🤖 LLM Used
**Model:** LLaMA 3 8B  
**Provider:** Groq Inference API  
**Mode:** Chat (OpenAI-compatible)  
**Temperature:** 0.7  
**Top-p:** 1.0  
**Max Tokens:** 1024

---

##  Prompts Used for Code Generation

### Language Agent Prompt
```text
You are a financial assistant. Given a structured market summary, generate a clear, concise spoken report under 100 words. Highlight: region allocation, stock price change, and earnings surprises with sentiment.
```

---

## 🛠️ Code Assistance via AI

### 1. `api_agent.py`
- Prompt: "Write a FastAPI endpoint using yfinance to return % change and historical close for given tickers."

### 2. `scraping_agent.py`
- Prompt: "Scrape earnings surprise using BeautifulSoup from Finviz and save to local text files for RAG ingestion."

### 3. `retriever_agent.py`
- Prompt: "Use FAISS and SentenceTransformer to index documents from `data/filings` and serve top-k chunks."

### 4. `analysis_agent.py`
- Prompt: "Fetch from multiple microservices (API, scraper, retriever), format the results into a single text summary."

### 5. `language_agent.py`
- Prompt: "Use Groq Python SDK to call LLaMA 3 with structured summary and return LLM output."

### 6. `voice_agent.py`
- Prompt: "Build Whisper STT and pyttsx3 TTS FastAPI pipeline that accepts audio, returns transcribed + spoken result."

### 7. `orchestrator.py`
- Prompt: "Route a query through analysis agent and language agent and return final narrative."

---

## ⚙ Notes

- Whisper (openai/whisper) model used for STT
- pyttsx3 used for offline TTS
- Each agent is modularized and exposed via FastAPI for clarity and orchestration

