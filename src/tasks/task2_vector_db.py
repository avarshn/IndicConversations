import sys
import os
from pathlib import Path
import logging

# Set Project Directory
try:    
    current_file = Path(__file__).resolve()

    # Or navigate multiple levels
    PROJECT_DIR = current_file.parents[1]

except:
    PROJECT_DIR = Path.cwd().parent

sys.path.insert(0, str(PROJECT_DIR))        # Don't use -> sys.path.append(PROJECT_DIR)
# print(PROJECT_DIR)

from src.vector_db.doc_chunking import get_chunks, merge_small_documents_with_metadata
from src.vector_db.initialize_db import create_load_vector_store
from src.log.log_config import setup_logging

from dotenv import load_dotenv
load_dotenv()
from pymilvus import connections

from huggingface_hub import login

# Login - Required for Embedding Model - From HuggingFace
login(token=os.environ['HF_TOKEN'])

logger = logging.getLogger(__name__)
setup_logging()

source_url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
filename = f"{PROJECT_DIR}/wikipedia_pages/Python_(programming_language)_wikipedia.txt"

COLLECTION_NAME = "wikipedia_docs"
URI = f"{PROJECT_DIR}/db/milvus_example.db"   #   "http://localhost:19530"

# Read the text file
with open(filename, "r") as fout:
    content = fout.read()

# Content Chunking
all_chunks = get_chunks(content, source_url)
chunks = merge_small_documents_with_metadata(all_chunks, min_size=150)

# Connect to Milvus
connections.connect(uri=URI)

# Load / Initialize Vector Store
vector_store = create_load_vector_store(COLLECTION_NAME, URI)

# Add chunks to Vector DB
vector_store.add_documents(chunks)