import sounddevice as sd
import scipy.io.wavfile as wavfile
import numpy as np

def record_audio(duration=5, sample_rate=16000, filename="output.wav"):
    """
    Record audio and save as WAV file
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Sample rate in Hz (16000 is good for speech)
        filename: Output filename
    """
    print(f"Recording for {duration} seconds...")
    
    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), 
                        samplerate=sample_rate, 
                        channels=1,  # mono
                        dtype='int16')
    
    sd.wait()  # Wait until recording is finished
    print("Recording finished!")
    
    # Save as WAV file
    wavfile.write(filename, sample_rate, audio_data)
    print(f"Audio saved to {filename}")

# Usage
if __name__ == '__main__':    
    record_audio(duration=5, sample_rate=16000, filename="recording.wav")