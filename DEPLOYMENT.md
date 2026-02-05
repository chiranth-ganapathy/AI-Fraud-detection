# Deployment Guide - AI Fraud Detection Hackathon

## Quick Deployment Options

### Option 1: Local Development (Fastest)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export API_KEY="sk_test_123456789"

# Run Problem 1 (Terminal 1)
python problem1_voice_detection.py

# Run Problem 2 (Terminal 2)
python problem2_honeypot.py
```

**URLs:**
- Voice Detection: http://localhost:5000
- Honeypot: http://localhost:5001

---

### Option 2: Docker (Recommended)

```bash
# Build and run both services
docker-compose up --build

# Or run individually:
docker build -f Dockerfile.voice -t voice-api .
docker run -p 5000:5000 -e API_KEY=your_key voice-api

docker build -f Dockerfile.honeypot -t honeypot-api .
docker run -p 5001:5001 -e API_KEY=your_key honeypot-api
```

---

### Option 3: Heroku (For Public Access)

#### Problem 1 Deployment:

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-voice-detection-app

# Set environment variables
heroku config:set API_KEY=sk_test_123456789

# Create Procfile (already included)
# Contents: web: gunicorn problem1_voice_detection:app

# Add buildpacks
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python

# Create Aptfile for system dependencies
echo "libsndfile1" > Aptfile

# Deploy
git init
git add .
git commit -m "Deploy voice detection"
git push heroku main

# Check logs
heroku logs --tail
```

**Your API URL:** `https://your-voice-detection-app.herokuapp.com`

#### Problem 2 Deployment:

```bash
# Create second app
heroku create your-honeypot-app

# Set environment variables
heroku config:set API_KEY=sk_test_123456789

# Update Procfile to use problem2
# Contents: web: gunicorn problem2_honeypot:app

# Deploy
git add .
git commit -m "Deploy honeypot"
git push heroku main
```

**Your API URL:** `https://your-honeypot-app.herokuapp.com`

---

### Option 4: Render.com (Alternative to Heroku)

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** voice-detection-api (or honeypot-api)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** 
     - For Problem 1: `gunicorn problem1_voice_detection:app`
     - For Problem 2: `gunicorn problem2_honeypot:app`
   - **Environment Variables:**
     - `API_KEY` = `sk_test_123456789`
     - `PORT` = Leave empty (Render sets this automatically)

6. Click "Create Web Service"

---

### Option 5: AWS EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv libsndfile1 -y

# Clone your code
git clone your-repo-url
cd your-repo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Set environment variables
export API_KEY="sk_test_123456789"

# Run with gunicorn (for production)
gunicorn --bind 0.0.0.0:5000 --workers 2 problem1_voice_detection:app &
gunicorn --bind 0.0.0.0:5001 --workers 2 problem2_honeypot:app &

# Or use systemd service (better for production)
sudo nano /etc/systemd/system/voice-detection.service
```

**Systemd service file:**
```ini
[Unit]
Description=Voice Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/your-repo
Environment="PATH=/home/ubuntu/your-repo/venv/bin"
Environment="API_KEY=sk_test_123456789"
Environment="PORT=5000"
ExecStart=/home/ubuntu/your-repo/venv/bin/gunicorn --bind 0.0.0.0:5000 problem1_voice_detection:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable voice-detection
sudo systemctl start voice-detection
sudo systemctl status voice-detection

# Configure security group to allow ports 5000 and 5001
```

---

### Option 6: Google Cloud Run

```bash
# Install Google Cloud SDK
# Then:

# For Problem 1
gcloud run deploy voice-detection \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=sk_test_123456789 \
  --port 5000 \
  --command "gunicorn" \
  --args "problem1_voice_detection:app"

# For Problem 2
gcloud run deploy honeypot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=sk_test_123456789 \
  --port 5001 \
  --command "gunicorn" \
  --args "problem2_honeypot:app"
```

---

## Testing Your Deployment

### Test Voice Detection API:

```bash
# Replace YOUR_URL with your deployed URL
export API_URL="https://your-app.herokuapp.com"

curl -X POST $API_URL/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "BASE64_STRING_HERE"
  }'
```

### Test Honeypot API:

```bash
curl -X POST $API_URL/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked. Verify now.",
      "timestamp": "2026-01-21T10:15:30Z"
    },
    "conversationHistory": []
  }'
```

---

## Important Notes

### For Problem 1 (Voice Detection):
- Ensure `libsndfile1` is installed on the server
- Set appropriate timeout for audio processing (120s recommended)
- Increase worker memory if handling large audio files

### For Problem 2 (Honeypot):
- Session storage is in-memory (resets on restart)
- For production, implement Redis or database
- Ensure callback URL is reachable: `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

### Security:
- Always use HTTPS in production
- Rotate API keys regularly
- Implement rate limiting for production
- Monitor logs for suspicious activity

---

## Troubleshooting

### Heroku Issues:

**"Application error" on startup:**
```bash
heroku logs --tail
# Check for missing dependencies or port issues
```

**Timeout errors:**
```bash
# Increase timeout in Procfile
web: gunicorn --timeout 120 problem1_voice_detection:app
```

### Docker Issues:

**Build fails for voice detection:**
```bash
# Ensure system dependencies are installed
# Check Dockerfile.voice has apt-get install libsndfile1
```

**Port already in use:**
```bash
# Change port mapping
docker run -p 5002:5000 voice-api
```

### General Issues:

**"Invalid API key":**
- Check environment variable is set correctly
- Verify x-api-key header is included in request

**"librosa not found":**
```bash
pip install librosa soundfile
# On Ubuntu/Debian:
sudo apt-get install libsndfile1
```

---

## Performance Optimization

### For High Traffic:

1. **Increase workers:**
```bash
gunicorn --workers 4 --threads 2 problem1_voice_detection:app
```

2. **Add Redis for session storage (Problem 2):**
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

3. **Implement caching:**
```python
from functools import lru_cache
```

4. **Use load balancer for multiple instances**

---

## Monitoring

### Health Checks:
```bash
# Voice Detection
curl http://your-url:5000/health

# Honeypot
curl http://your-url:5001/health
```

### Logs:
```bash
# Heroku
heroku logs --tail --app your-app-name

# Docker
docker logs -f container-name

# Systemd
sudo journalctl -u voice-detection -f
```

---

## Submission Checklist

- [ ] APIs deployed and publicly accessible
- [ ] Health check endpoints working
- [ ] API key authentication enabled
- [ ] Tested with sample requests
- [ ] Problem 1: Returns correct JSON format
- [ ] Problem 2: Sends callback to GUVI endpoint
- [ ] URLs documented and shared
- [ ] No hard-coded secrets in code
- [ ] Logs reviewed for errors

---

## Quick Reference

**Default API Key:** `sk_test_123456789` (Change this!)

**Endpoints:**
- Voice Detection: `POST /api/voice-detection`
- Honeypot: `POST /api/honeypot`
- Health: `GET /health`

**Required Headers:**
- `Content-Type: application/json`
- `x-api-key: YOUR_API_KEY`

---

Good luck with deployment! 🚀
