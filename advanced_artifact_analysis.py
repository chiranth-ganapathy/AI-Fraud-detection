#!/usr/bin/env python3
"""
Advanced artifact analysis for AI voice detection
Identifies subtle AI-specific patterns
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def advanced_analysis(audio_file):
    """Perform advanced artifact analysis"""
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    try:
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Advanced Analysis: {audio_file}")
        print(f"Classification: {result[0]}")
        print(f"Confidence: {result[1]:.0%}")
        
        # Detailed feature analysis
        print(f"\nFeature Analysis:")
        for key, value in sorted(features.items())[:20]:
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Analyze all audio files
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            advanced_analysis(audio_file)
            print("=" * 60)
