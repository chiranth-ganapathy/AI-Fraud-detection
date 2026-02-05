#!/usr/bin/env python3
"""
Detect sample voice type
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def detect():
    filename = 'sample voice 1.mp3'
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    print(f"Detecting: {filename}")
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Result: {result[0]} ({result[1]:.0%} confidence)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    detect()
