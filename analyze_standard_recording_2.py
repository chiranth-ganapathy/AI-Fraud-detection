#!/usr/bin/env python3
"""
Analyze standard recording 2
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def analyze():
    filename = 'Standard recording 2.mp3'
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    print(f"Analyzing: {filename}")
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Classification: {result[0]}")
        print(f"Confidence: {result[1]:.0%}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    analyze()
