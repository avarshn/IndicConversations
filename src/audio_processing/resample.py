import librosa
import soundfile as sf
import tempfile
import numpy as np

def ensure_16k_mono_wav(input_bytes):

    # Save incoming bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(input_bytes)
        input_path = tmp.name

    # Read with soundfile
    data, sr = sf.read(input_path)

    # Convert to mono if needed
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Resample only if needed
    if sr != 16000:
        data = librosa.resample(data, orig_sr=sr, target_sr=16000)
        sr = 16000

    # Save final WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as out:
        sf.write(out.name, data, sr)
        return out.name