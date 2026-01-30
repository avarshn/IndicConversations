import argparse

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from src.tasks.task5_rag_pipeline_offline import run_rag_pipeline

import logging
from dotenv import load_dotenv
from src.log.log_config import setup_logging
from pymilvus import connections


logger = logging.getLogger(__name__)


# ---------- ARGPARSE ----------
# Parser
parser = argparse.ArgumentParser(description="Chat with Conversational Agent")

# Add arguments
parser.add_argument("--collection_name", type=str, help="Name of the vector database collection")
parser.add_argument("--uri", type=str, help="Path or URI for the vector database")

args, _ = parser.parse_known_args()

COLLECTION_NAME = args.collection_name
URI = args.uri

# ---------- CACHE CONNECTION ----------
@st.cache_resource
def init_once(uri):
    load_dotenv()
    setup_logging()

    connections.connect(uri=uri)
    return True

# Connect to Milvus, Setup Logging, Load env variables
init_once(URI)


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