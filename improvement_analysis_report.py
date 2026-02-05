#!/usr/bin/env python3
"""
Improvement Analysis Report for Voice Detection Model
Analyzes RMS variance and other metrics to identify detection gaps
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def analyze_audio_file(filepath):
    """Analyze audio file and return detailed metrics"""
    try:
        y, sr = librosa.load(filepath, sr=None)
        features = extract_audio_features(y, sr)
        result = analyze_voice_patterns(features)
        
        # Add detailed RMS analysis
        rms_frame = librosa.feature.rms(y=y)[0]
        rms_variance = np.var(rms_frame)
        rms_mean = np.mean(rms_frame)
        
        return {
            'file': filepath,
            'classification': result['classification'],
            'confidence': result['confidence'],
            'rms_variance': rms_variance,
            'rms_mean': rms_mean,
            'rms_std': np.std(rms_frame),
            'pitch_std': features.get('pitch_std', 0),
            'spectral_centroid': features.get('spectral_centroid', 0),
            'zero_crossing_rate': features.get('zero_crossing_rate', 0),
        }
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return None

def main():
    """Generate improvement analysis report"""
    print("=" * 80)
    print("VOICE DETECTION IMPROVEMENT ANALYSIS REPORT")
    print("=" * 80)
    
    # List audio files to analyze
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'voice_preview_viraj - rich, confident and expressive.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    results = []
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"\nAnalyzing: {audio_file}")
            result = analyze_audio_file(audio_file)
            if result:
                results.append(result)
                print(f"  Classification: {result['classification']} ({result['confidence']:.0%} confidence)")
                print(f"  RMS Variance: {result['rms_variance']:.6f}")
                print(f"  RMS Mean: {result['rms_mean']:.6f}")
                print(f"  Pitch Std Dev: {result['pitch_std']:.2f} Hz")
                print(f"  Spectral Centroid: {result['spectral_centroid']:.2f} Hz")
                print(f"  Zero Crossing Rate: {result['zero_crossing_rate']:.4f}")
    
    # Analysis and insights
    print("\n" + "=" * 80)
    print("KEY INSIGHTS:")
    print("=" * 80)
    
    if results:
        variances = [r['rms_variance'] for r in results]
        print(f"\nRMS Variance Range: {min(variances):.6f} to {max(variances):.6f}")
        print(f"Mean RMS Variance: {np.mean(variances):.6f}")
        print("\nThreshold Analysis:")
        print(f"  Classic AI (low variance): RMS < 0.0015")
        print(f"  Human speech (high variance): RMS > 0.01")
        print(f"  Advanced AI (moderate-high variance): 0.003 < RMS < 0.01")

if __name__ == '__main__':
    main()
