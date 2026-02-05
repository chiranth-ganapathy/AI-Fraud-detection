#!/usr/bin/env python3
"""
Integration test for the complete system
"""

import os
import sys

def test_integration():
    """Run integration tests"""
    
    print("=" * 80)
    print("INTEGRATION TEST SUITE")
    print("=" * 80)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: File existence
    print("\nTest 1: Core Files Exist")
    core_files = [
        'problem1_voice_detection.py',
        'problem2_honeypot.py',
        'requirements.txt'
    ]
    
    for f in core_files:
        if os.path.exists(f):
            print(f"  ✓ {f}")
            tests_passed += 1
        else:
            print(f"  ✗ {f}")
            tests_failed += 1
    
    # Test 2: Audio files
    print("\nTest 2: Audio Files Available")
    audio_files = [
        'sample voice 1.mp3',
        'ElevenLabs_2026-02-05T06_26_47_Rachel_pre_sp100_s50_sb75_se0_b_m2.mp3',
        'Standard recording 1.mp3',
        'Standard recording 2.mp3'
    ]
    
    available = 0
    for f in audio_files:
        if os.path.exists(f):
            print(f"  ✓ {f}")
            available += 1
            tests_passed += 1
        else:
            print(f"  ✗ {f}")
            tests_failed += 1
    
    # Test 3: Documentation
    print("\nTest 3: Documentation Files")
    docs = [
        'README.md',
        'DEPLOYMENT.md',
        'PROJECT_STATUS.md'
    ]
    
    for f in docs:
        if os.path.exists(f):
            print(f"  ✓ {f}")
            tests_passed += 1
        else:
            print(f"  ✗ {f}")
            tests_failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print(f"RESULTS: {tests_passed} passed, {tests_failed} failed")
    print("=" * 80)
    
    return tests_failed == 0

if __name__ == '__main__':
    success = test_integration()
    sys.exit(0 if success else 1)
