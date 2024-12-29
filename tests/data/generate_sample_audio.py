import wave
import numpy as np

def create_sample_wav(filename="sample_audio.wav", duration=1.0, sample_rate=16000):
    """Generate a sample WAV file for testing"""
    # Generate a simple sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    data = np.sin(2 * np.pi * 440 * t)
    scaled = np.int16(data * 32767)
    
    # Create WAV file
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(scaled.tobytes())

if __name__ == "__main__":
    create_sample_wav() 