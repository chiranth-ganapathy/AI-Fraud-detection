#!/usr/bin/env python3
"""
Statistical AI detection analysis
"""

import os
import numpy as np
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def statistical_analysis(audio_file):
    """Statistical analysis for AI detection"""
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    try:
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        # Statistical measures
        feature_values = list(features.values())
        
        print(f"Statistical Analysis: {audio_file}")
        print(f"Classification: {result[0]} ({result[1]:.0%})")
        print(f"Feature Statistics:")
        print(f"  Mean: {np.mean(feature_values):.4f}")
        print(f"  Std Dev: {np.std(feature_values):.4f}")
        print(f"  Min: {np.min(feature_values):.4f}")
        print(f"  Max: {np.max(feature_values):.4f}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    for audio_file in audio_files:
        statistical_analysis(audio_file)
        print("=" * 60)
