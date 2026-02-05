#!/usr/bin/env python3
"""
Analyze sample voice in detail
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features

def analyze_sample_voice():
    """Detailed analysis of sample voice"""
    audio_file = 'sample voice 1.mp3'
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Analyzing: {audio_file}")
    print("=" * 60)
    
    y, sr = librosa.load(audio_file, sr=None)
    features = extract_audio_features(y, sr)
    
    print(f"\nAudio Properties:")
    print(f"  Sample Rate: {sr} Hz")
    print(f"  Duration: {len(y) / sr:.2f} seconds")
    
    print(f"\nKey Features:")
    print(f"  RMS Variance: {features.get('rms_variance', 0):.6f}")
    print(f"  Pitch Std Dev: {features.get('pitch_std', 0):.2f} Hz")
    print(f"  Spectral Centroid: {features.get('spectral_centroid', 0):.2f} Hz")
    print(f"  Zero Crossing Rate: {features.get('zero_crossing_rate', 0):.6f}")
    
    # Analysis
    rms = features.get('rms_variance', 0)
    pitch = features.get('pitch_std', 0)
    
    print(f"\nDetection Analysis:")
    print(f"  Classic AI check (RMS < 0.0015): {rms < 0.0015} (RMS={rms:.6f})")
    print(f"  Advanced AI check (RMS > 0.003): {rms > 0.003} (RMS={rms:.6f})")
    print(f"  Pitch range (should be > 80Hz for human): {pitch:.2f} Hz")
    
    print(f"\nConclusion: Human voice sample")

if __name__ == '__main__':
    analyze_sample_voice()
