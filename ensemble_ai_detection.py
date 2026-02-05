#!/usr/bin/env python3
"""
Ensemble AI Detection System
Combines multiple detection methods for improved accuracy
"""

import os
import numpy as np
import librosa
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def ensemble_detect(audio_file):
    """Ensemble detection using multiple methods"""
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return None
    
    try:
        y, sr = librosa.load(audio_file, sr=None)
        features = extract_audio_features(y, sr)
        
        # Method 1: Pattern-based detection (original)
        result_pattern = analyze_voice_patterns(features)
        
        # Method 2: RMS variance analysis
        rms_frame = librosa.feature.rms(y=y)[0]
        rms_variance = np.var(rms_frame)
        
        if rms_variance < 0.0015:
            ai_score_rms = 0.9  # Classic AI
        elif rms_variance > 0.003:
            ai_score_rms = 0.7  # Potential advanced AI
        else:
            ai_score_rms = 0.1  # Likely human
        
        # Method 3: Spectral analysis
        spec = features.get('spectral_centroid', 0)
        if spec < 1200:
            ai_score_spec = 0.6
        else:
            ai_score_spec = 0.3
        
        # Method 4: Pitch analysis
        pitch = features.get('pitch_std', 0)
        if pitch < 350:
            ai_score_pitch = 0.8  # Classic AI
        elif pitch > 600:
            ai_score_pitch = 0.5  # Could be advanced AI
        else:
            ai_score_pitch = 0.2
        
        # Ensemble voting
        scores = [ai_score_rms, ai_score_spec, ai_score_pitch]
        ensemble_score = np.mean(scores)
        
        return {
            'file': audio_file,
            'pattern_result': result_pattern['classification'],
            'pattern_confidence': result_pattern['confidence'],
            'rms_score': ai_score_rms,
            'spectral_score': ai_score_spec,
            'pitch_score': ai_score_pitch,
            'ensemble_score': ensemble_score,
            'final_classification': 'AI_GENERATED' if ensemble_score > 0.5 else 'HUMAN',
            'metrics': {
                'rms_variance': rms_variance,
                'pitch_std': pitch,
                'spectral_centroid': spec
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Run ensemble detection on all available audio files"""
    print("=" * 80)
    print("ENSEMBLE AI DETECTION ANALYSIS")
    print("=" * 80)
    
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'voice_preview_viraj - rich, confident and expressive.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"\nProcessing: {audio_file}")
            result = ensemble_detect(audio_file)
            
            if result:
                print(f"  Pattern-based: {result['pattern_result']} ({result['pattern_confidence']:.0%})")
                print(f"  Ensemble Score: {result['ensemble_score']:.2%}")
                print(f"  Final Classification: {result['final_classification']}")
                print(f"  Component Scores:")
                print(f"    - RMS Analysis: {result['rms_score']:.2%}")
                print(f"    - Spectral Analysis: {result['spectral_score']:.2%}")
                print(f"    - Pitch Analysis: {result['pitch_score']:.2%}")

if __name__ == '__main__':
    main()
