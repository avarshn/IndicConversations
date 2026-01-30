import os
import sys

from pathlib import Path

try:    
    current_file = Path(__file__).resolve()

    # Or navigate multiple levels
    PROJECT_DIR = current_file.parents[2]

except:
    PROJECT_DIR = Path.cwd().parent.parent

sys.path.insert(0, str(PROJECT_DIR))        # Don't use -> sys.path.append(PROJECT_DIR)
# print(PROJECT_DIR)

import logging

import argparse
from dotenv import load_dotenv
from pymilvus import connections

from src.log.log_config import setup_logging
from src.asr.asr_api import transcribe
from src.translate.translate_api import translate
from src.vector_db.initialize_db import create_load_vector_store
from src.llm.llm_api import llm_call
from src.llm.prompt import get_prompt

def run_rag_pipeline(audio_bytes, output_lang, COLLECTION_NAME, URI):
    # Transcribe
    user_said = transcribe(audio_bytes)

    # Translate to English
    translated_text_query = translate(user_said)

    # Load Vector DB
    vector_store = create_load_vector_store(COLLECTION_NAME, URI)

    # Retrieve the top-2 closest chunks from the Vector Database for your question
    retrieved_docs = vector_store.similarity_search(translated_text_query, k=2)

    sources = set()
    context = "Context:\n\n"
    for doc in retrieved_docs:
        context = context + doc.page_content + "\n\n"
        
        # Get Source URL
        sources.add(doc.metadata["source"])

    # Prompt
    prompt = get_prompt(context = context, question= translated_text_query, output_lang = output_lang)

    messages = [
        {"role" : "user", "content" : prompt}
    ]

    response_text = llm_call(messages)


    with open("response.txt", "w") as fout:
        fout.write(response_text)

    return user_said, response_text, sources


# Usage
# python src/tasks/task5_rag_pipeline_offline.py --audio_file "./sample/test1_rag_pipeline.wav"
if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    setup_logging()

    load_dotenv()

    # Parser
    parser = argparse.ArgumentParser(description="Chat with Conversational Agent")

    # Add arguments
    parser.add_argument("--audio_file", type=str, help="Path of audio file, that stores user's query")
    parser.add_argument("--collection_name", type=str, default="wikipedia_docs", help="Name of the vector database collection")
    parser.add_argument("--uri", type=str, default=f"{PROJECT_DIR}/db/milvus_example.db", help="Path or URI for the vector database")

    args = parser.parse_args()

    audio_file_path = args.audio_file
    COLLECTION_NAME = args.collection_name
    URI = args.uri

    # Connect to Milvus
    connections.connect(uri=URI)
    
    audio_bytes = open(audio_file_path, "rb")
    user_query, response_text, sources = run_rag_pipeline(audio_bytes, "English", COLLECTION_NAME, URI)

    print("User Query :\n", user_query)
    print("\n")
    print("Response :\n", response_text)