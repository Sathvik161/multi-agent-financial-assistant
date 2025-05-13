import streamlit as st
import requests

VOICE_AGENT_URL = "http://localhost:8006/voice_input"
ORCHESTRATOR_URL = "http://localhost:8007/briefing"

st.set_page_config(page_title="📈 Market Brief Assistant", layout="centered")
st.title("🎙️ Morning Market Brief Assistant")

# Backend URLs


# Initialize session state
if "voice_response_ready" not in st.session_state:
    st.session_state.voice_response_ready = False
if "voice_audio_bytes" not in st.session_state:
    st.session_state.voice_audio_bytes = None

query_default = "What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

tab1, tab2 = st.tabs(["🎤 Voice Mode", "⌨️ Text Mode"])

# === Voice Tab ===
with tab1:
    st.subheader("Upload Voice Query")
    audio_file = st.file_uploader("Upload a .wav or .mp3 file", type=["wav", "mp3"])

    if st.button("Submit Voice Query") and audio_file:
        files = {"audio": audio_file}
        response = requests.post(VOICE_AGENT_URL, files=files)

        if response.status_code == 200:
            # Store audio bytes in session state
            st.session_state.voice_audio_bytes = response.content
            st.session_state.voice_response_ready = True
            st.success("✅ Audio ready!")

    if st.session_state.get("voice_response_ready") and st.session_state.get("voice_audio_bytes"):
        st.audio(st.session_state.voice_audio_bytes, format="audio/mp3")

# === Text Tab ===
with tab2:
    st.subheader("Type a Market Query")
    user_query = st.text_area("Ask your question:", value=query_default)
    tickers = st.text_input("Tickers (comma-separated)", "TSM,005930.KQ")

    if st.button("Submit Text Query"):
        try:
            response = requests.get(ORCHESTRATOR_URL, params={"query": user_query, "tickers": tickers})
            if response.status_code == 200:
                data = response.json()
                
                # Display Market Briefing Narrative
                st.markdown("### 📋 Market Briefing")
                st.markdown(data.get("narrative", "No response from LLM."))
            else:
                st.error("❌ Orchestrator did not respond.")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")

