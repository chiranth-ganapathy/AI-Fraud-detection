#!/usr/bin/env python3
"""
Analyze standard recordings
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def analyze_standard_recording(filename, label):
    """Analyze a standard recording"""
    
    if not os.path.exists(filename):
        print(f"{label}: File not found")
        return
    
    print(f"\n{label}: {filename}")
    print("=" * 60)
    
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        
        features = extract_audio_features(audio_data)
        result = analyze_voice_patterns(features)
        
        print(f"Classification: {result[0]}")
        print(f"Confidence: {result[1]:.0%}")
        print(f"Explanation: {result[2]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    analyze_standard_recording('Standard recording 1.mp3', 'Standard Recording 1')
    analyze_standard_recording('Standard recording 2.mp3', 'Standard Recording 2')
