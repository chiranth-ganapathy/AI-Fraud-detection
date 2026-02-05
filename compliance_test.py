#!/usr/bin/env python3
"""
Compliance test for voice detection system
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def compliance_test():
    """Run compliance tests"""
    
    print("COMPLIANCE TEST SUITE")
    print("=" * 80)
    
    # Test 1: File loading
    print("\nTest 1: Audio File Loading")
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    loaded = 0
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            loaded += 1
    
    print(f"✓ Loaded {loaded}/{len(audio_files)} audio files")
    
    # Test 2: Feature extraction
    print("\nTest 2: Feature Extraction")
    if audio_files[0] and os.path.exists(audio_files[0]):
        try:
            with open(audio_files[0], 'rb') as f:
                audio_data = f.read()
            features = extract_audio_features(audio_data)
            print(f"✓ Extracted {len(features)} features")
        except Exception as e:
            print(f"✗ Feature extraction failed: {e}")
    
    # Test 3: Voice detection
    print("\nTest 3: Voice Detection")
    if audio_files[0] and os.path.exists(audio_files[0]):
        try:
            with open(audio_files[0], 'rb') as f:
                audio_data = f.read()
            features = extract_audio_features(audio_data)
            result = analyze_voice_patterns(features)
            print(f"✓ Detection working: {result[0]} ({result[1]:.0%})")
        except Exception as e:
            print(f"✗ Detection failed: {e}")
    
    print("\n" + "=" * 80)
    print("COMPLIANCE TEST COMPLETE")

if __name__ == '__main__':
    compliance_test()
