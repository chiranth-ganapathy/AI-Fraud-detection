#!/usr/bin/env python3
"""
Quick test script for voice detection functionality
"""

import os
import sys
from problem1_voice_detection import detect_voice_type

def quick_test():
    """Run a quick test with available audio files"""
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'voice_preview_viraj - rich, confident and expressive.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    print("Quick Voice Detection Test")
    print("=" * 60)
    
    found_files = 0
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            found_files += 1
            print(f"\nTesting: {audio_file}")
            try:
                result = detect_voice_type(audio_file)
                print(f"  Result: {result['classification']}")
                print(f"  Confidence: {result['confidence']:.0%}")
            except Exception as e:
                print(f"  Error: {e}")
    
    if found_files == 0:
        print("\nNo audio files found. Please provide test audio files.")
        return False
    
    print(f"\n\nTested {found_files} audio file(s)")
    return True

if __name__ == '__main__':
    success = quick_test()
    sys.exit(0 if success else 1)
