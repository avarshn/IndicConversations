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

def transcribe(audio_bytes):
    response = client.speech_to_text.transcribe(
        file=audio_bytes,
        model="saarika:v2.5",
        language_code="unknown"    # use "unknown" for automatic language detection
    )

    transcribed_text = response.transcript

    return transcribed_text