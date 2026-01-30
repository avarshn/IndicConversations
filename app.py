import streamlit as st
from streamlit_mic_recorder import mic_recorder
from src.tasks.task5_rag_pipeline_offline import run_rag_pipeline

import logging
from dotenv import load_dotenv
from src.log.log_config import setup_logging
from pymilvus import connections

COLLECTION_NAME = "wikipedia_docs"
URI = "./db/milvus_example.db"


logger = logging.getLogger(__name__)
setup_logging()

load_dotenv()

# Connect to Milvus
connections.connect(uri=URI)

# ---------- STREAMLIT UI ----------

st.set_page_config(page_title="Voice RAG Chatbot")

st.title("🎤 Voice-enabled Multilingual RAG Chatbot (on Wikipedia Data)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

st.divider()

# ---------- Language selection ----------
output_lang = st.selectbox(
    "Select output language:",
    options=["English", "Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Punjabi"],
    index=1,  # default Hindi
)

audio = mic_recorder(
    start_prompt="🎤 Press to Speak",
    stop_prompt="⏹️ Stop",
    just_once=True,
    format="webm"
)

# When audio received
if audio:
    with st.spinner("Processing..."):

        query, answer, sources = run_rag_pipeline(audio['bytes'], output_lang, COLLECTION_NAME, URI)

    # Format sources
    if sources:
        source_text = "\n\n**Sources:**\n" + "\n".join(
            f"- {s}" for s in sources
        )
        answer = answer + source_text

    # Save messages
    st.session_state.messages.append(("user", query))
    st.session_state.messages.append(("assistant", answer))

    st.rerun()