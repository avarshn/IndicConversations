import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus

from functools import lru_cache
from pymilvus import connections, utility

import logging
logger = logging.getLogger(__name__)


_API_KEY = os.getenv("HF_TOKEN")
if not _API_KEY:
    logger.critical("HF_TOKEN environment variable missing")
    raise RuntimeError("HF_TOKEN is not set")

# Initialize once
@lru_cache(maxsize=1)
def get_embeddings():
    model_name = "sentence-transformers/all-mpnet-base-v2"   # "BAAI/bge-m3"
    model_kwargs = {"device": "cpu"}   # or "cuda"
    encode_kwargs = {"normalize_embeddings": True}

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    return embeddings

# Use everywhere without reloading
def create_load_vector_store(COLLECTION_NAME, URI):
    embedding_model = get_embeddings()  # Uses cached model

    # Check if collection exists
    if utility.has_collection(COLLECTION_NAME):
        print(f"Collection '{COLLECTION_NAME}' exists. Loading...")
        
        # Load existing collection
        vector_store = Milvus(
            embedding_function=embedding_model,
            collection_name=COLLECTION_NAME,
            connection_args={"uri": URI},
        )
    
    # Create New Collection
    else:
        vector_store = Milvus(
            embedding_function=embedding_model,
            collection_name=COLLECTION_NAME,
            connection_args={"uri": URI},
            index_params={"index_type": "FLAT", "metric_type": "L2"},
        )
    return vector_store