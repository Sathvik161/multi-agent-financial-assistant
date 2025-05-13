# 🧠 Multi-Agent Finance Assistant

This project is a modular, open-source multi-agent financial assistant that delivers **spoken market briefs** via a Streamlit UI. It uses LLaMA 3 via Groq, Whisper STT, pyttsx3 TTS, and microservice agents for data ingestion, retrieval, analysis, and orchestration.

## 🧱 Architecture

**Agents:**

- `API Agent` – Real-time financial data via yFinance
- `Scraping Agent` – Earnings surprises scraped from Finviz
- `Retriever Agent` – FAISS vector DB with filing embeddings
- `Analysis Agent` – Combines structured + unstructured data
- `Language Agent` – Generates natural language briefings using LLaMA 3 via Groq
- `Voice Agent` – Converts voice input → query → audio output
- `Orchestrator` – Central router for all agents

**Pipeline:**
```
Voice → Whisper → Analysis + Retrieval → LLaMA 3 → TTS → Voice Output
```

## 🖥️ Run Locally

1. Clone this repo:
```bash
git clone https://github.com/yourname/finance-assistant.git
cd finance-assistant
```

2. Set up `.env` with your Groq API key:
```
GROQ_API_KEY=your_key_here
```

3. Create `data/filings/` directory:
```bash
mkdir -p data/filings
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Launch all agents:
```bash
python launch_all.py
```

6. Start the Streamlit app:
```bash
streamlit run streamlit_app/app.py
```

---

## 🐳 Docker

Build and run the app via Docker:

```bash
docker build -t finance-assistant .
docker run -p 8501:8501 finance-assistant
```

---

## 📦 Directory Structure
```
finance_assistant/
├── agents/
├── data/filings/
├── orchestrator/
├── streamlit_app/
├── launch_all.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 📌 Features

- Microservice architecture (FastAPI)
- LangChain-style RAG with FAISS
- STT (Whisper) + TTS (pyttsx3)
- LLM with Groq-hosted LLaMA 3
- Interactive UI with Streamlit
- Easy to extend or deploy

---

## 📄 License

MIT License
