#!/usr/bin/env python3
"""
Test the improved voice detection model
Validates all detection paths
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns, detect_voice_type

def test_improved_model():
    """Test improved detection model"""
    print("Testing improved voice detection model...\n")
    
    audio_files = [
        ('sample voice 1.mp3', 'HUMAN'),
        ('ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3', 'AI_GENERATED'),
        ('voice_preview_viraj - rich, confident and expressive.mp3', 'AI_GENERATED'),
        ('Standard recording 1.mp3', 'HUMAN'),
        ('Standard recording 2.mp3', 'HUMAN')
    ]
    
    correct = 0
    total = 0
    
    for audio_file, expected in audio_files:
        if not os.path.exists(audio_file):
            print(f"Skipping {audio_file} (not found)")
            continue
        
        total += 1
        result = detect_voice_type(audio_file)
        classification = result['classification']
        confidence = result['confidence']
        
        status = "✓" if classification == expected else "✗"
        if classification == expected:
            correct += 1
        
        print(f"{status} {audio_file}")
        print(f"  Expected: {expected}, Got: {classification} ({confidence:.0%})")
    
    print(f"\nAccuracy: {correct}/{total} ({100*correct/total:.0f}%)")

if __name__ == '__main__':
    test_improved_model()
