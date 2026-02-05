#!/usr/bin/env python3
"""
Test system with language detection
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def test_with_language():
    """Test detection with language info"""
    
    test_cases = [
        ('sample voice 1.mp3', 'English', 'HUMAN'),
        ('ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3', 'English', 'AI_GENERATED'),
        ('Standard recording 1.mp3', 'English', 'HUMAN'),
        ('Standard recording 2.mp3', 'English', 'HUMAN')
    ]
    
    print("Testing with Language Information")
    print("=" * 60)
    
    for audio_file, language, expected in test_cases:
        if not os.path.exists(audio_file):
            print(f"{audio_file}: NOT FOUND")
            continue
        
        try:
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            features = extract_audio_features(audio_data)
            result = analyze_voice_patterns(features)
            
            status = "✓" if result[0] == expected else "✗"
            print(f"{status} {audio_file}")
            print(f"   Language: {language}")
            print(f"   Result: {result[0]} ({result[1]:.0%})")
            print(f"   Expected: {expected}")
            
        except Exception as e:
            print(f"✗ {audio_file}: ERROR - {e}")

if __name__ == '__main__':
    test_with_language()
