#!/usr/bin/env python3
"""
Comprehensive test suite for improved voice detection model
Tests all voice types: Human, Classic AI, and Advanced AI
"""

import os
import sys
import base64
from problem1_voice_detection import extract_audio_features, analyze_voice_patterns

def detect_voice_from_file(audio_file, language):
    """Test detection directly from file"""
    try:
        # Read audio file as bytes
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        # Extract features
        features = extract_audio_features(audio_data)
        
        # Analyze patterns
        classification, confidence, explanation = analyze_voice_patterns(features)
        
        return {
            'classification': classification,
            'confidence': confidence,
            'explanation': explanation
        }
    except Exception as e:
        raise Exception(f"Detection failed: {str(e)}")

def test_voice_detection():
    """Test voice detection on all audio types"""
    print("=" * 80)
    print("COMPREHENSIVE VOICE DETECTION TEST")
    print("=" * 80)
    
    test_cases = [
        {
            'file': 'sample voice 1.mp3',
            'expected': 'HUMAN',
            'description': 'Human voice sample',
            'language': 'English'
        },
        {
            'file': 'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
            'expected': 'AI_GENERATED',
            'description': 'ElevenLabs classic AI-generated voice',
            'language': 'English'
        },
        {
            'file': 'voice_preview_viraj - rich, confident and expressive.mp3',
            'expected': 'AI_GENERATED',
            'description': 'Viraj advanced AI-generated voice',
            'language': 'English'
        },
        {
            'file': 'Standard recording 1.mp3',
            'expected': 'HUMAN',
            'description': 'Standard human recording 1',
            'language': 'English'
        },
        {
            'file': 'Standard recording 2.mp3',
            'expected': 'HUMAN',
            'description': 'Standard human recording 2',
            'language': 'English'
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        audio_file = test_case['file']
        expected = test_case['expected']
        description = test_case['description']
        language = test_case['language']
        
        print(f"\n{'=' * 80}")
        print(f"Test: {description}")
        print(f"File: {audio_file}")
        print(f"Language: {language}")
        print(f"Expected: {expected}")
        
        if not os.path.exists(audio_file):
            print(f"❌ FAILED - File not found")
            failed += 1
            continue
        
        try:
            result = detect_voice_from_file(audio_file, language)
            classification = result['classification']
            confidence = result['confidence']
            
            print(f"Result: {classification} ({confidence:.0%} confidence)")
            print(f"Explanation: {result.get('explanation', 'N/A')}")
            
            if classification == expected:
                print(f"✓ PASSED")
                passed += 1
            else:
                print(f"✗ FAILED - Expected {expected}, got {classification}")
                failed += 1
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'=' * 80}")
    print(f"TEST SUMMARY")
    print(f"{'=' * 80}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    print(f"Accuracy: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "N/A")
    
    return failed == 0

if __name__ == '__main__':
    success = test_voice_detection()
    sys.exit(0 if success else 1)
