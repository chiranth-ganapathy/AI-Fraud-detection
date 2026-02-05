#!/usr/bin/env python3
"""
Test ElevenLabs audio detection
"""

import os
from problem1_voice_detection import detect_voice_type

def test_elevenlabs():
    """Test ElevenLabs audio"""
    audio_file = 'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3'
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Testing: {audio_file}")
    result = detect_voice_type(audio_file)
    
    print(f"Classification: {result['classification']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Expected: AI_GENERATED")
    
    if result['classification'] == 'AI_GENERATED':
        print("✓ PASSED")
    else:
        print("✗ FAILED")

if __name__ == '__main__':
    test_elevenlabs()
