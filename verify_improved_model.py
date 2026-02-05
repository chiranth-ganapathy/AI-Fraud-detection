#!/usr/bin/env python3
"""
Verify improved model functionality
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def verify():
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3'
    ]
    
    print("Verifying Improved Model")
    print("=" * 60)
    
    for audio_file in audio_files:
        if not os.path.exists(audio_file):
            print(f"{audio_file}: NOT FOUND")
            continue
        
        try:
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            features = extract_audio_features(audio_data)
            result = analyze_voice_patterns(features)
            
            print(f"✓ {audio_file}: {result[0]}")
            
        except Exception as e:
            print(f"✗ {audio_file}: ERROR - {e}")

if __name__ == '__main__':
    verify()
