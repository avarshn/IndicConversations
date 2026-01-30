import json
import logging
from pathlib import Path
from typing import Dict, Any

import requests

try:    
    current_file = Path(__file__).resolve()

    # Or navigate multiple levels
    PROJECT_DIR = current_file.parents[2]

except:
    PROJECT_DIR = Path.cwd().parent.parent

# print(PROJECT_DIR)

logger = logging.getLogger(__name__)

CACHE_FILE = Path(f"{PROJECT_DIR}/web_search_cache_results/search_cache.json")
logger.info("Cache Location :'%s'", CACHE_FILE)

"""Utility functions for caching Google SERP results from SearchAPI.io.

If the cache file already contains results for a given query, those are
returned immediately. Otherwise, the SearchAPI.io endpoint is called and the
results are persisted for future runs.
"""

def _save_cache(cache: Dict[str, Any]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("w", encoding="utf-8") as fp:
        json.dump(cache, fp, ensure_ascii=False, indent=2)


def _load_cache() -> Dict[str, Any]:
    if CACHE_FILE.exists():
        try:
            with CACHE_FILE.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except json.JSONDecodeError:
            # Corrupted cache → start fresh
            return {}
    return {}


# Fetch API Response

def _fetch_from_api(query: str, api_key: str, engine: str = "google") -> Dict[str, Any]:
    """Call SearchAPI.io and return parsed JSON response."""
    url = "https://www.searchapi.io/api/v1/search"
    params = {"engine": engine, "q": query, "api_key": api_key}
    response = requests.get(url, params=params, timeout=10)
    logger.info(f"Response: {response}")
    response.raise_for_status()
    return response.json()


def get_search_results(query: str, api_key: str, engine: str = "google") -> Dict[str, Any]:
    """Return SERP results for query, using local cache when possible."""
    cache = _load_cache()

    if query in cache:
        logger.info("Using cached SERP results for query: '%s'", query)
        return cache[query]

    logger.info("Fetching SERP results from API for query: '%s'", query)
    fresh_results = _fetch_from_api(query, api_key, engine)
    logger.info(f"Fetched the results") 
    cache[query] = fresh_results
    _save_cache(cache)
    logger.info("Saved results to cache for query: '%s'", query)
    return fresh_results