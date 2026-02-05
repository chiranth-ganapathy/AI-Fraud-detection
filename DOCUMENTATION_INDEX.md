# Documentation Index

## Project Files Overview

### Core System Files
- **problem1_voice_detection.py** - AI voice detection API (Flask)
- **problem2_honeypot.py** - Fraud detection honeypot API
- **requirements.txt** - Python dependencies

### Test Files
- **test_voice.py** - Voice detection API tests
- **test_honeypot.py** - Honeypot API tests
- **final_comprehensive_test.py** - Full test suite
- **test_improved_model.py** - Model validation
- **compliance_test.py** - Compliance testing

### Analysis & Investigation Scripts
- **improvement_analysis_report.py** - RMS/pitch analysis
- **analyze_detection_gap.py** - Detection gap investigation
- **ensemble_ai_detection.py** - Multi-method ensemble
- **analyze_sample_voice.py** - Sample voice analysis
- **detailed_voice_analysis.py** - Detailed metrics
- **analyze_elevenlabs.py** - ElevenLabs audio analysis
- **analyze_viraj_voice.py** - Viraj voice analysis
- **analyze_standard_recording.py** - Standard recording analysis
- **deep_analysis_sample_voice.py** - Deep analysis
- **comparison_report.py** - Voice comparison
- **statistical_ai_detection.py** - Statistical analysis

### Documentation
- **README.md** - User guide
- **DEPLOYMENT.md** - Deployment instructions
- **PROJECT_STATUS.md** - Project status report
- **CODE_CHANGES.md** - Summary of changes
- **IMPROVEMENT_SUMMARY.md** - Improvements summary
- **IMPROVEMENT_README.md** - Improvements documentation
- **IMPLEMENTATION_COMPLETE.md** - Completion report

### Configuration Files
- **docker-compose.yml** - Docker orchestration
- **Dockerfile.voice** - Voice detection container
- **Dockerfile.honeypot** - Honeypot container
- **Procfile** - Process configuration

### Audio Files
- **sample voice 1.mp3** - Human voice sample
- **ElevenLabs_*.mp3** - AI-generated voice
- **Standard recording 1.mp3** - Standard human recording
- **Standard recording 2.mp3** - Standard human recording
- **test_audio_human.wav** - Synthetic human audio
- **test_audio_ai.wav** - Synthetic AI audio

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run voice API: `python problem1_voice_detection.py`
3. Run honeypot API: `python problem2_honeypot.py`
4. Run tests: `python final_comprehensive_test.py`
5. Analyze audio: `python analyze_detection_gap.py`

## Key Detection Thresholds

- Classic AI: RMS < 0.0015 AND Pitch < 350 Hz
- Advanced AI: RMS > 0.003 AND Pitch > 600 AND Spectral < 1280 AND ZCR < 0.1
- Human: Default (all other cases)

## Support
See individual files for more detailed information.
