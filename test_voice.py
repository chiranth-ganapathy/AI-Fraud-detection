# -*- coding: utf-8 -*-
"""
Test script for Problem 1: AI Voice Detection API
"""

import requests
import base64
import sys

def test_voice_detection(audio_file_path, language="English", api_url="http://localhost:5000", api_key="sk_test_123456789"):
    """
    Test the voice detection API
    
    Args:
        audio_file_path: Path to MP3 audio file
        language: One of Tamil, English, Hindi, Malayalam, Telugu
        api_url: API endpoint URL
        api_key: API key for authentication
    """
    
    try:
        # Read and encode audio file
        print(f"Reading audio file: {audio_file_path}")
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        print(f"Audio size: {len(audio_data)} bytes")
        print(f"Base64 size: {len(audio_base64)} characters")
        
        # Make API request
        print(f"\nSending request to {api_url}/api/voice-detection")
        print(f"Language: {language}")
        
        response = requests.post(
            f"{api_url}/api/voice-detection",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key
            },
            json={
                "language": language,
                "audioFormat": "mp3",
                "audioBase64": audio_base64
            },
            timeout=30
        )
        
        # Print response
        print(f"\nStatus Code: {response.status_code}")
        print("\n" + "="*60)
        print("API RESPONSE:")
        print("="*60)
        
        result = response.json()
        
        if result.get("status") == "success":
            print(f"[OK] Status: {result['status']}")
            print(f"[OK] Language: {result['language']}")
            print(f"[OK] Classification: {result['classification']}")
            print(f"[OK] Confidence Score: {result['confidenceScore']}")
            print(f"[OK] Explanation: {result['explanation']}")
        else:
            print(f"[FAIL] Error: {result.get('message', 'Unknown error')}")
        
        print("="*60)
        
        return result
        
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_file_path}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {api_url}")
        print("Make sure the server is running!")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def test_invalid_api_key(audio_file_path, api_url="http://localhost:5000"):
    """Test with invalid API key"""
    print("\n" + "="*60)
    print("Testing Invalid API Key:")
    print("="*60)
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
        
        response = requests.post(
            f"{api_url}/api/voice-detection",
            headers={
                "Content-Type": "application/json",
                "x-api-key": "invalid_key"
            },
            json={
                "language": "English",
                "audioFormat": "mp3",
                "audioBase64": audio_base64
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 401:
            print("[OK] Invalid API key correctly rejected")
        else:
            print("[FAIL] Invalid API key should return 401")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def test_health_check(api_url="http://localhost:5000"):
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check:")
    print("="*60)
    
    try:
        response = requests.get(f"{api_url}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Check if audio file path is provided
    if len(sys.argv) < 2:
        print("Usage: python test_voice.py <audio_file_path> [language] [api_url] [api_key]")
        print("\nExample:")
        print("  python test_voice.py sample.mp3")
        print("  python test_voice.py sample.mp3 Tamil")
        print("  python test_voice.py sample.mp3 English http://localhost:5000")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "English"
    api_url = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:5000"
    api_key = sys.argv[4] if len(sys.argv) > 4 else "sk_test_123456789"
    
    # Run tests
    print("="*60)
    print("AI VOICE DETECTION API - TEST SUITE")
    print("="*60)
    
    # Test 1: Health check
    test_health_check(api_url)
    
    # Test 2: Valid request
    result = test_voice_detection(audio_file, language, api_url, api_key)
    
    # Test 3: Invalid API key
    test_invalid_api_key(audio_file, api_url)
    
    print("\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)
