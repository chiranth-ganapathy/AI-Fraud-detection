#!/usr/bin/env python3
"""
Analyze detection gap for Viraj audio
Investigates why Viraj audio might not be detected as AI-generated
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def deep_analyze_viraj():
    """Deep analysis of Viraj audio detection gap"""
    audio_file = 'voice_preview_viraj - rich, confident and expressive.mp3'
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print("=" * 80)
    print("VIRAJ AUDIO DEEP ANALYSIS")
    print("=" * 80)
    
    try:
        y, sr = librosa.load(audio_file, sr=None)
        features = extract_audio_features(y, sr)
        result = analyze_voice_patterns(features)
        
        print(f"\nBasic Classification:")
        print(f"  Result: {result['classification']}")
        print(f"  Confidence: {result['confidence']:.0%}")
        print(f"  Explanation: {result['explanation']}")
        
        # Detailed metrics
        print(f"\nDetailed Audio Metrics:")
        print(f"  RMS Variance: {features.get('rms_variance', 0):.6f}")
        print(f"  Pitch Std Dev: {features.get('pitch_std', 0):.2f} Hz")
        print(f"  Spectral Centroid: {features.get('spectral_centroid', 0):.2f} Hz")
        print(f"  Spectral Rolloff: {features.get('spectral_rolloff', 0):.2f} Hz")
        print(f"  Zero Crossing Rate: {features.get('zero_crossing_rate', 0):.6f}")
        print(f"  MFCC Mean: {features.get('mfcc_mean', 0):.4f}")
        
        # Analysis
        print(f"\nDetection Gap Analysis:")
        rms = features.get('rms_variance', 0)
        pitch = features.get('pitch_std', 0)
        spec = features.get('spectral_centroid', 0)
        
        print(f"  Classic AI threshold (RMS < 0.0015): {rms < 0.0015}")
        print(f"  Advanced AI threshold (RMS > 0.003): {rms > 0.003}")
        print(f"  Pitch characteristic (Pitch > 600): {pitch > 600}")
        print(f"  Spectral control (Spectral < 1280): {spec < 1280}")
        
        if rms > 0.003 and pitch > 600:
            print(f"\n  -> LIKELY ADVANCED AI: High RMS + High Pitch (deceptively natural)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    deep_analyze_viraj()
