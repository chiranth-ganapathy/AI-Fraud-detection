#!/usr/bin/env python3
"""
Detailed voice analysis for all sample files
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def analyze_all_voices():
    """Analyze all available voice files"""
    
    print("=" * 80)
    print("DETAILED VOICE ANALYSIS REPORT")
    print("=" * 80)
    
    audio_files = [
        ('sample voice 1.mp3', 'Human Sample'),
        ('ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3', 'ElevenLabs AI'),
        ('voice_preview_viraj - rich, confident and expressive.mp3', 'Viraj Advanced AI'),
        ('Standard recording 1.mp3', 'Standard Human 1'),
        ('Standard recording 2.mp3', 'Standard Human 2')
    ]
    
    for filepath, description in audio_files:
        if not os.path.exists(filepath):
            print(f"\n{description}: FILE NOT FOUND")
            continue
        
        print(f"\n{'=' * 80}")
        print(f"{description}")
        print(f"File: {filepath}")
        print(f"{'=' * 80}")
        
        try:
            y, sr = librosa.load(filepath, sr=None)
            features = extract_audio_features(y, sr)
            result = analyze_voice_patterns(features)
            
            print(f"\nClassification: {result['classification']}")
            print(f"Confidence: {result['confidence']:.0%}")
            print(f"Explanation: {result.get('explanation', 'N/A')}")
            
            print(f"\nDetailed Metrics:")
            print(f"  RMS Variance: {features.get('rms_variance', 0):.6f}")
            print(f"  Pitch Std Dev: {features.get('pitch_std', 0):.2f} Hz")
            print(f"  Spectral Centroid: {features.get('spectral_centroid', 0):.2f} Hz")
            print(f"  Spectral Rolloff: {features.get('spectral_rolloff', 0):.2f} Hz")
            print(f"  Zero Crossing Rate: {features.get('zero_crossing_rate', 0):.6f}")
            print(f"  MFCC Mean: {features.get('mfcc_mean', 0):.4f}")
            
        except Exception as e:
            print(f"Error analyzing: {e}")

if __name__ == '__main__':
    analyze_all_voices()
