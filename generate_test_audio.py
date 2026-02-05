#!/usr/bin/env python3
"""
Generate test audio files for development
Creates synthetic test audio for human and AI voices
"""

import numpy as np
import soundfile as sf
from scipy.io import wavfile

def generate_test_audio():
    """Generate test audio files"""
    
    # Parameters
    sr = 22050  # Sample rate
    duration = 3  # Duration in seconds
    
    # Generate human-like audio (more variance in frequency)
    t = np.linspace(0, duration, sr * duration)
    
    # Human voice simulation (variable pitch)
    pitch_variation = 100 + 50 * np.sin(2 * np.pi * 2 * t)  # 100-150 Hz
    human_signal = np.sin(2 * np.pi * pitch_variation * t / sr)
    
    # Add some noise to make it more natural
    human_signal += 0.1 * np.random.randn(len(human_signal))
    
    # Add amplitude modulation (more natural)
    human_signal *= (0.5 + 0.4 * np.sin(2 * np.pi * 3 * t))
    
    # Normalize
    human_signal /= np.max(np.abs(human_signal))
    
    # Generate AI-like audio (more consistent)
    ai_pitch = 120  # Constant pitch
    ai_signal = np.sin(2 * np.pi * ai_pitch * t / sr)
    
    # Less natural amplitude modulation
    ai_signal *= 0.7
    
    # Normalize
    ai_signal /= np.max(np.abs(ai_signal))
    
    # Save files
    sf.write('test_audio_human.wav', human_signal, sr)
    sf.write('test_audio_ai.wav', ai_signal, sr)
    
    print("Generated test audio files:")
    print("  - test_audio_human.wav")
    print("  - test_audio_ai.wav")

if __name__ == '__main__':
    generate_test_audio()
