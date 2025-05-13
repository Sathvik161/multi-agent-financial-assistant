# agents/language_agent.py

from fastapi import FastAPI, Query
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def simple_groq_completion(prompt: str, model="llama3-8b-8192"):
    messages = [
        {"role": "system", "content": "You are a financial assistant. Given a structured market summary, generate a clear, concise spoken report under 100 words."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error contacting Groq API: {e}]"

@app.get("/generate_briefing")
def generate_briefing(query_input: str = Query(...)):
    output = simple_groq_completion(prompt=query_input)
    return {"narrative": output}
