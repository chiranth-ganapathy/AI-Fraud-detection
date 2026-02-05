#!/usr/bin/env python3
"""
Comparison report for voice detection
"""

import os
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def compare_voices():
    """Compare all voice samples"""
    
    audio_files = [
        ('sample voice 1.mp3', 'Human Sample'),
        ('ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3', 'ElevenLabs AI'),
        ('Standard recording 1.mp3', 'Standard Human 1'),
        ('Standard recording 2.mp3', 'Standard Human 2')
    ]
    
    print("=" * 80)
    print("VOICE COMPARISON REPORT")
    print("=" * 80)
    
    results = []
    for filepath, label in audio_files:
        if not os.path.exists(filepath):
            print(f"\n{label}: FILE NOT FOUND")
            continue
        
        try:
            with open(filepath, 'rb') as f:
                audio_data = f.read()
            
            features = extract_audio_features(audio_data)
            result = analyze_voice_patterns(features)
            
            results.append({
                'label': label,
                'classification': result[0],
                'confidence': result[1],
                'features': features
            })
            
            print(f"\n{label}:")
            print(f"  Classification: {result[0]} ({result[1]:.0%})")
            
        except Exception as e:
            print(f"\n{label}: ERROR - {e}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    for r in results:
        status = "✓" if r['classification'] else "✗"
        print(f"{status} {r['label']}: {r['classification']} ({r['confidence']:.0%})")

if __name__ == '__main__':
    compare_voices()
