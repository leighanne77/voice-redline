import wave
import numpy as np

def create_sample_wav():
    """Create a 1-second sample WAV file for testing"""
    # Audio parameters
    duration = 1.0  # seconds
    sample_rate = 44100
    frequency = 440  # Hz (A4 note)

    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    samples = (32767 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

    # Create WAV file
    with wave.open('tests/data/sample_audio.wav', 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes per sample
        wav.setframerate(sample_rate)
        wav.writeframes(samples.tobytes())

if __name__ == "__main__":
    create_sample_wav() 