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

from src.search.search_api import get_search_results
from src.search.wikipedia_api import WikipediaAPI
from src.log.log_config import setup_logging

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    setup_logging()
    
    # Parser
    parser = argparse.ArgumentParser(description="Web Search")

    # Add arguments
    parser.add_argument("--topic", type=str, help="Topic you want to search")
    
    args = parser.parse_args()

    query = args.topic
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

# Usage
# python src/tasks/task1_data_collection.py --topic "Tourism in India"

# Topics -
# Python language
# Transformers Movie
# ASR Transcription
# Fall of Rome
# Industrial Revolution
# Leonardo da Vinci
# Marie Curie
# Artificial Intelligence
# Quantum Cryptography
# List of Tallest Buildings
