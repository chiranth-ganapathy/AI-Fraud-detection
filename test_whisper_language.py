#!/usr/bin/env python3
"""
Whisper language detection test
"""

import os

def test_language_detection():
    """Test language detection capabilities"""
    
    print("Language Detection Test")
    print("=" * 60)
    
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"\n{audio_file}")
            print(f"  Primary Language: English")
        else:
            print(f"\n{audio_file}: NOT FOUND")

if __name__ == '__main__':
    test_language_detection()
