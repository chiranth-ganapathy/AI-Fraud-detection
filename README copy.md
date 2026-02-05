# AI Fraud Detection & User Safety - Hackathon Solutions

This repository contains complete solutions for both problem statements in the AI Fraud Detection & User Safety Hackathon.

## 📋 Table of Contents
- [Problem 1: AI Voice Detection](#problem-1-ai-voice-detection)
- [Problem 2: Agentic Honey-Pot](#problem-2-agentic-honey-pot)
- [Installation & Setup](#installation--setup)
- [Deployment Guide](#deployment-guide)
- [Testing](#testing)
- [Architecture](#architecture)

---

## 🎤 Problem 1: AI Voice Detection

### Overview
REST API that detects whether a voice sample is AI-generated or Human across 5 languages (Tamil, English, Hindi, Malayalam, Telugu).

### Features
- ✅ Multi-language support (Tamil, English, Hindi, Malayalam, Telugu)
- ✅ Base64 MP3 audio input
- ✅ Advanced feature extraction using librosa
- ✅ Pattern-based AI detection
- ✅ API key authentication
- ✅ Detailed confidence scores and explanations

### API Endpoint
```
POST /api/voice-detection
```

### Request Format
```bash
curl -X POST https://your-domain.com/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA..."
  }'
```

### Response Format
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.91,
  "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
}
```

### Detection Algorithm

The system uses advanced audio feature extraction:

1. **Spectral Features**: Analyzes frequency distribution patterns
2. **MFCCs**: 20 Mel-frequency cepstral coefficients for voice characteristics
3. **Pitch Analysis**: Detects unnatural pitch consistency in AI voices
4. **Energy Patterns**: Identifies synthetic energy distribution
5. **Temporal Features**: Analyzes voice transitions and variations

**AI Voice Indicators:**
- Low pitch variation (std < 50)
- Uniform spectral patterns
- Consistent energy levels
- Robotic MFCC patterns
- Mechanical transitions

---

## 🕵️ Problem 2: Agentic Honey-Pot

### Overview
AI-powered honeypot that detects scam messages, autonomously engages scammers, and extracts intelligence.

### Features
- ✅ Multi-turn conversation handling
- ✅ Real-time scam detection with confidence scoring
- ✅ Autonomous AI agent with adaptive persona
- ✅ Intelligence extraction (UPI IDs, bank accounts, phone numbers, links)
- ✅ Automatic callback to GUVI evaluation endpoint
- ✅ Session management
- ✅ Pattern-based scam detection

### API Endpoint
```
POST /api/honeypot
```

### Request Format (First Message)
```json
{
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
    "timestamp": "2026-01-21T10:15:30Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

### Response Format
```json
{
  "status": "success",
  "reply": "Why is my account being blocked? I haven't done anything wrong."
}
```

### Scam Detection Patterns

The system detects 6 categories of scam indicators:

1. **Urgency**: "urgent", "immediately", "right now", "expire"
2. **Threats**: "blocked", "suspend", "legal action", "arrest"
3. **Financial**: "bank account", "UPI", "CVV", "OTP", "PIN"
4. **Verification**: "verify", "confirm", "share details"
5. **Rewards**: "won", "prize", "lottery", "free"
6. **Impersonation**: "bank", "government", "police", "official"

**Confidence Scoring:**
- 3+ categories = 85% confidence
- 2 categories = 70% confidence
- High-risk combinations (threats + financial) = 95% confidence

### Agent Behavior

The AI agent operates in 4 stages:

1. **Initial** (Messages 1-2): Shows concern, asks basic questions
2. **Engaged** (Messages 3-6): Shows willingness but hesitation, asks probing questions
3. **Extraction** (Messages 7-12): Pretends to comply while extracting intelligence
4. **Closing** (Messages 12+): Disengages naturally

### Intelligence Extraction

Automatically extracts:
- Bank account numbers
- UPI IDs (username@bank format)
- Phishing URLs
- Phone numbers
- Suspicious keywords

### Final Callback

When engagement ends, the system automatically sends intelligence to:
```
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Local Setup

1. **Clone/Download the code**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
# For both problems
export API_KEY="sk_test_123456789"

# For Problem 1
export PORT=5000

# For Problem 2
export PORT=5001
```

4. **Run Problem 1 (Voice Detection)**
```bash
python problem1_voice_detection.py
```

5. **Run Problem 2 (Honeypot)**
```bash
python problem2_honeypot.py
```

---

## 🌐 Deployment Guide

### Option 1: Heroku Deployment

#### For Problem 1:
```bash
# Create Heroku app
heroku create your-voice-detection-app

# Set environment variables
heroku config:set API_KEY=sk_test_123456789

# Create Procfile
echo "web: gunicorn problem1_voice_detection:app" > Procfile

# Deploy
git add .
git commit -m "Deploy voice detection"
git push heroku main
```

#### For Problem 2:
```bash
# Create Heroku app
heroku create your-honeypot-app

# Set environment variables
heroku config:set API_KEY=sk_test_123456789

# Create Procfile
echo "web: gunicorn problem2_honeypot:app" > Procfile

# Deploy
git add .
git commit -m "Deploy honeypot"
git push heroku main
```

### Option 2: Docker Deployment

Create `Dockerfile-voice`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libsndfile1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY problem1_voice_detection.py .
ENV PORT=5000
CMD gunicorn --bind 0.0.0.0:$PORT problem1_voice_detection:app
```

Create `Dockerfile-honeypot`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY problem2_honeypot.py .
ENV PORT=5001
CMD gunicorn --bind 0.0.0.0:$PORT problem2_honeypot:app
```

Build and run:
```bash
docker build -f Dockerfile-voice -t voice-detection .
docker run -p 5000:5000 -e API_KEY=your_key voice-detection

docker build -f Dockerfile-honeypot -t honeypot .
docker run -p 5001:5001 -e API_KEY=your_key honeypot
```

---

## 🧪 Testing

### Test Problem 1

Create `test_voice.py`:
```python
import requests
import base64

# Read and encode audio file
with open("sample.mp3", "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

response = requests.post(
    "http://localhost:5000/api/voice-detection",
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk_test_123456789"
    },
    json={
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
)

print(response.json())
```

### Test Problem 2

Create `test_honeypot.py`:
```python
import requests
import uuid

session_id = str(uuid.uuid4())

# First message
response1 = requests.post(
    "http://localhost:5001/api/honeypot",
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk_test_123456789"
    },
    json={
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked. Verify immediately.",
            "timestamp": "2026-01-21T10:15:30Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
)

print("Response 1:", response1.json())
```

---

## 📊 Key Features

### Problem 1 Highlights
- **Advanced Audio Analysis**: Uses librosa for professional-grade feature extraction
- **Multi-dimensional Detection**: Analyzes spectral, temporal, and pitch features
- **Language Support**: Works across all 5 required languages
- **High Accuracy**: Pattern-based detection with confidence scoring

### Problem 2 Highlights
- **Intelligent Engagement**: 4-stage conversation strategy
- **Pattern Recognition**: 6 categories of scam indicators
- **Automatic Intelligence Extraction**: Regex-based extraction of sensitive data
- **GUVI Integration**: Automatic callback with final results
- **Adaptive Responses**: Context-aware reply generation

---

## 🔒 Security Best Practices

1. **API Key Management**
   - Store keys in environment variables
   - Never commit keys to version control
   - Use different keys for dev/prod

2. **Input Validation**
   - All inputs validated before processing
   - Base64 decoding errors handled gracefully
   - Proper error messages without leaking info

3. **Rate Limiting** (Recommended for production)
   - Add Flask-Limiter for API rate limiting
   - Prevent abuse and DoS attacks

---

## 🎯 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set API_KEY environment variable
- [ ] Run Problem 1: `python problem1_voice_detection.py`
- [ ] Run Problem 2: `python problem2_honeypot.py`
- [ ] Test with sample requests
- [ ] Deploy to cloud platform
- [ ] Update API URLs in submissions

---

## 📝 File Structure

```
.
├── problem1_voice_detection.py   # Voice detection API
├── problem2_honeypot.py          # Honeypot API
├── requirements.txt              # Dependencies
├── README.md                     # This file
├── test_voice.py                 # Voice API test script
├── test_honeypot.py              # Honeypot API test script
└── Procfile                      # For Heroku deployment
```

---

## 🐛 Troubleshooting

**librosa installation issues:**
```bash
sudo apt-get install libsndfile1
pip install soundfile
```

**Port already in use:**
```bash
# Change port in environment variable
export PORT=5002
```

**Session not found (Problem 2):**
- Sessions are in-memory and reset on restart
- For production, implement Redis or database storage

---

**Good luck with the hackathon! 🚀**
