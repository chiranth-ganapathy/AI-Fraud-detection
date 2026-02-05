#!/usr/bin/env python3
"""
Deep analysis of sample voice
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def deep_analyze():
    filename = 'sample voice 1.mp3'
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    print(f"Deep Analysis: {filename}")
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Classification: {result[0]}")
        print(f"Confidence: {result[1]:.0%}")
        print(f"Detailed Metrics:")
        
        # Show some key features
        for key in sorted(features.keys())[:10]:
            print(f"  {key}: {features[key]:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    deep_analyze()
