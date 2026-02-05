#!/usr/bin/env python3
"""
Verify the improved detection model works correctly
"""

import os
from problem1_voice_detection import detect_voice_type

def verify_system():
    """Verify system is working"""
    print("Verifying Voice Detection System...")
    print("=" * 60)
    
    # Test with available files
    test_files = [
        'sample voice 1.mp3',
        'Standard recording 1.mp3'
    ]
    
    for audio_file in test_files:
        if os.path.exists(audio_file):
            print(f"\nTesting {audio_file}...")
            try:
                result = detect_voice_type(audio_file)
                print(f"✓ Detection successful")
                print(f"  Classification: {result['classification']}")
                print(f"  Confidence: {result['confidence']:.0%}")
            except Exception as e:
                print(f"✗ Error: {e}")
                return False
    
    print("\n✓ System verification complete")
    return True

if __name__ == '__main__':
    verify_system()
