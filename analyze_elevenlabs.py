#!/usr/bin/env python3
"""
Analyze ElevenLabs audio
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def analyze_elevenlabs():
    filename = 'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3'
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    print(f"Analyzing: {filename}")
    print("(ElevenLabs AI-Generated Voice)")
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Classification: {result[0]}")
        print(f"Confidence: {result[1]:.0%}")
        print(f"Expected: AI_GENERATED")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    analyze_elevenlabs()
