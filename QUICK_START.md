# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the System

### Option 1: Run Both APIs
```bash
# Terminal 1: Voice Detection API
python problem1_voice_detection.py

# Terminal 2: Honeypot API
python problem2_honeypot.py
```

### Option 2: Using Docker
```bash
docker-compose up
```

## Testing

### Run Comprehensive Test Suite
```bash
python final_comprehensive_test.py
```

### Run Model Validation
```bash
python test_improved_model.py
```

### Analyze Detection Gap
```bash
python analyze_detection_gap.py
```

## API Endpoints

### Voice Detection
```
POST /api/voice-detection
Content-Type: application/json
x-api-key: sk_test_123456789

{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "<base64-encoded-audio>"
}
```

### Health Check
```
GET /health
```

## Voice Sample Testing

Place audio files in the project directory and run:
```bash
python final_comprehensive_test.py
```

Supported formats: MP3, WAV, OGG, M4A

## Key Files

- `problem1_voice_detection.py` - Main detection system
- `problem2_honeypot.py` - Honeypot fraud detection
- `requirements.txt` - Dependencies list
- `test_voice.py` - Voice API tests
- `test_honeypot.py` - Honeypot API tests

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process
taskkill /PID <pid> /F
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Audio Format Issues
Ensure audio files are in supported formats: MP3, WAV, OGG, M4A

## Support Documentation

- README.md - Full user guide
- DEPLOYMENT.md - Deployment instructions
- PROJECT_STATUS.md - Project status
