#!/usr/bin/env python3
"""
Analyze language features in audio samples
"""

import os
from problem1_voice_detection import extract_audio_features

def analyze_language_features(audio_file):
    """Analyze language-specific features"""
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Language Analysis: {audio_file}")
    
    try:
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        
        # MFCC analysis (important for language)
        mfcc_means = [v for k, v in features.items() if 'mfcc_' in k and 'mean' in k]
        
        print(f"  MFCC Mean Values: {len(mfcc_means)} coefficients")
        print(f"  Spectral Centroid: {features.get('spectral_centroid_mean', 0):.2f} Hz")
        print(f"  ZCR Mean: {features.get('zcr_mean', 0):.6f}")
        
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
        analyze_language_features(audio_file)
