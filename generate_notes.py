import numpy as np
import wave
import os

# Note frequencies (in Hz)
FREQUENCIES = {
    'C4': 261.63, 'Cs4': 277.18, 'D4': 293.66, 'Ds4': 311.13, 'E4': 329.63,
    'F4': 349.23, 'Fs4': 369.99, 'G4': 392.00, 'Gs4': 415.30, 'A4': 440.00,
    'As4': 466.16, 'B4': 493.88, 'C5': 523.25, 'Cs5': 554.37, 'D5': 587.33
}

SAMPLE_RATE = 44100  # Hz
DURATION = 0.5       # Seconds

def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    return np.int16(tone * 32767)

# Ensure audio directory exists
os.makedirs("audio", exist_ok=True)

for note, freq in FREQUENCIES.items():
    samples = generate_sine_wave(freq, DURATION, SAMPLE_RATE)
    with wave.open(f"audio/{note}.wav", 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(samples.tobytes())

print("✅ Dummy .wav notes generated in /audio folder!")
