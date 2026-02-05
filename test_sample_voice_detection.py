#!/usr/bin/env python3
"""
Test sample voice detection
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def test_sample():
    filename = 'sample voice 1.mp3'
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Sample Voice Detection Test")
        print(f"File: {filename}")
        print(f"Result: {result[0]} ({result[1]:.0%} confidence)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_sample()
