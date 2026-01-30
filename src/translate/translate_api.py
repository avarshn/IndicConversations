from sarvamai import SarvamAI
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

def translate(input_text):

    response = client.text.translate(
        input= input_text,           # limit 1000 chars for mayura:v1 model
        source_language_code="auto",
        target_language_code="en-IN",
        speaker_gender="Female",
        mode="modern-colloquial",   # best for hinglish input, chatbot use cases
        model="mayura:v1",         # "sarvam-translate:v1" does not support modern colloquial
        numerals_format="international",
    )

    translated_text = response.translated_text

    return translated_text