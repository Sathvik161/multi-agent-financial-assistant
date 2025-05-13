# agents/voice_agent.py

from fastapi import FastAPI, File, UploadFile
import whisper
import requests
import os
import tempfile
from gtts import gTTS
from fastapi.responses import FileResponse, Response

app = FastAPI()

stt_model = whisper.load_model("base")


import sys
import os
# Add project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import ANALYSIS_URL, LLM_URL

@app.post("/voice_input")
async def voice_input(audio: UploadFile = File(...)):
    # Save uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_path = tmp_audio.name
        content = await audio.read()
        tmp_audio.write(content)

    # 1. STT
    result = stt_model.transcribe(tmp_path)
    query_text = result["text"]

    # 2. Analysis + LLM
    analysis = requests.get(ANALYSIS_URL, params={"tickers": "TSM,005930.KQ", "query": query_text}).json()
    prompt_input = analysis["prompt_input"]
    llm_response = requests.get(LLM_URL, params={"query_input": prompt_input}).json()
    narration = llm_response.get("narrative", "Could not generate response.")

    # 3. TTS with gTTS
    tts = gTTS(narration)
    audio_output_path = os.path.join(tempfile.gettempdir(), "response.mp3")
    tts.save(audio_output_path)
    

    with open(audio_output_path, "rb") as f:
        audio_bytes = f.read()

    return Response(content=audio_bytes, media_type="audio/mpeg")
