from sarvamai import SarvamAI
from sarvamai.core.api_error import ApiError

import os

import logging
logger = logging.getLogger(__name__)

_API_KEY = os.getenv("SARVAM_API_KEY")
if not _API_KEY:
    logger.critical("SARVAM_API_KEY environment variable missing")
    raise RuntimeError("SARVAM_API_KEY is not set")


client = SarvamAI(
    api_subscription_key=_API_KEY,
)

def llm_call(messages):
    try:
        response = client.chat.completions(
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    
    except ApiError as e:
        if e.status_code == 400:
            print(f"Bad request: {e.body}")
        elif e.status_code == 403:
            print("Invalid API key. Check your credentials.")
        elif e.status_code == 422:
            print(f"Invalid parameters: {e.body}")
        elif e.status_code == 429:
            print("Rate limit exceeded. Wait and retry.")
        else:
            print(f"Error {e.status_code}: {e.body}")