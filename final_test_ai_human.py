#!/usr/bin/env python3
"""
Final AI/Human detection test
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def final_test():
    """Final comprehensive detection test"""
    
    print("=" * 80)
    print("FINAL AI/HUMAN DETECTION TEST")
    print("=" * 80)
    
    test_cases = [
        ('sample voice 1.mp3', 'HUMAN', 'Human Voice Sample'),
        ('ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3', 'AI_GENERATED', 'ElevenLabs AI Voice'),
        ('Standard recording 1.mp3', 'HUMAN', 'Standard Recording 1'),
        ('Standard recording 2.mp3', 'HUMAN', 'Standard Recording 2')
    ]
    
    passed = 0
    failed = 0
    
    for audio_file, expected, description in test_cases:
        print(f"\n{description}")
        print(f"File: {audio_file}")
        print(f"Expected: {expected}")
        
        if not os.path.exists(audio_file):
            print(f"❌ FAILED - File not found")
            failed += 1
            continue
        
        try:
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            features = extract_audio_features(audio_data)
            result = analyze_voice_patterns(features)
            
            classification = result[0]
            confidence = result[1]
            
            print(f"Result: {classification} ({confidence:.0%} confidence)")
            
            if classification == expected:
                print(f"✓ PASSED")
                passed += 1
            else:
                print(f"✗ FAILED")
                failed += 1
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"FINAL RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)

if __name__ == '__main__':
    final_test()
