import os
import sys

from pathlib import Path

# Set Project Directory
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
from huggingface_hub import login
from pymilvus import connections

from src.search.search_api import get_search_results
from src.search.wikipedia_api import WikipediaAPI
from src.log.log_config import setup_logging

from src.vector_db.doc_chunking import get_chunks, merge_small_documents_with_metadata
from src.vector_db.initialize_db import create_load_vector_store
from src.log.log_config import setup_logging

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    setup_logging()
    
    # Parser
    parser = argparse.ArgumentParser(description="Web Search")

    # Add arguments
    parser.add_argument("--topic", type=str, help="Topic you want to search")
    parser.add_argument("--collection_name", type=str, default="wikipedia_docs", help="Name of the vector database collection")
    parser.add_argument("--uri", type=str, default=f"{PROJECT_DIR}/db/wiki.db", help="Path or URI for the vector database")
    
    args = parser.parse_args()

    query = args.topic
    COLLECTION_NAME = args.collection_name
    URI = args.uri

    logger.info("Topic / Query : '%s'", query)

    # Reformat Query - To search within Wikipedia only
    query = f"site:wikipedia.org {query}"

    # Load Search API Key
    load_dotenv()  # reads variables from a .env file and sets them in os.environ

    # Get Top WikiPedia Link
    top_results = get_search_results(query, api_key = os.environ["SEARCH_API_KEY"])
    for result in top_results['organic_results']:
        if 'wikipedia.org' in result['link']:
            top_ranked_url = result['link']
            break

    # Scrape Wikipedia URL and Save Text content
    wiki = WikipediaAPI()

    parsed_webpage = wiki.get_page_content(top_ranked_url)

    title = parsed_webpage['title']
    title = title.replace(" ", "_")

    output_file = f"{PROJECT_DIR}/wikipedia_pages/{title}_wikipedia.txt"

    # Open file to write
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{parsed_webpage['title']}\n\n")
        f.write(parsed_webpage['content'])
        
    logger.info(f"\nSaved to '%s'", output_file)

    # Login - Required for Embedding Model - From HuggingFace
    login(token=os.environ['HF_TOKEN'])

    source_url = top_ranked_url
    filename = output_file

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


# Usage
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "Tourism in India" --collection_name "wiki_docs" --uri "/tmp/wiki.db"
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "Tourism in India"
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "Python language"
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "Fall of Rome"
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "Industrial Revolution"
# python src/tasks/task_1_2_data_collection_ingestion.py --topic "List of Tallest Buildings"