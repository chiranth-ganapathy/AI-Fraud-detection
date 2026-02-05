"""
Agentic Honey-Pot for Scam Detection & Intelligence Extraction
Problem Statement 2: AI-powered system that detects and engages scammers
"""

from flask import Flask, request, jsonify
from functools import wraps
import os
import re
import requests
from datetime import datetime, timezone
from collections import defaultdict
import json

app = Flask(__name__)

# Configuration
API_KEY = os.getenv('API_KEY', 'sk_test_123456789')
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Session storage (in production, use Redis or database)
sessions = {}

# Scam detection patterns
SCAM_PATTERNS = {
    'urgency': [
        r'urgent', r'immediately', r'right now', r'within \d+ (hour|minute)',
        r'expire', r'limited time', r'act fast', r'hurry'
    ],
    'threats': [
        r'blocked', r'suspend', r'deactivate', r'freeze', r'lock',
        r'legal action', r'arrest', r'police', r'court', r'fine'
    ],
    'financial': [
        r'bank account', r'credit card', r'debit card', r'upi', r'paytm',
        r'gpay', r'phonepe', r'transaction', r'payment', r'refund',
        r'cvv', r'pin', r'otp', r'account number', r'ifsc'
    ],
    'verification': [
        r'verify', r'confirm', r'validate', r'update.*detail',
        r'share.*detail', r'provide.*information', r'enter.*code'
    ],
    'rewards': [
        r'won', r'prize', r'lottery', r'reward', r'cashback',
        r'free', r'gift', r'bonus', r'offer'
    ],
    'impersonation': [
        r'bank', r'government', r'tax department', r'police',
        r'customer care', r'support team', r'official', r'authorized'
    ]
}

class ScamIntelligence:
    """Class to store extracted intelligence"""
    def __init__(self):
        self.bank_accounts = []
        self.upi_ids = []
        self.phishing_links = []
        self.phone_numbers = []
        self.suspicious_keywords = []
    
    def to_dict(self):
        return {
            "bankAccounts": list(set(self.bank_accounts)),
            "upiIds": list(set(self.upi_ids)),
            "phishingLinks": list(set(self.phishing_links)),
            "phoneNumbers": list(set(self.phone_numbers)),
            "suspiciousKeywords": list(set(self.suspicious_keywords))
        }

class ConversationSession:
    """Manages a conversation session"""
    def __init__(self, session_id):
        self.session_id = session_id
        self.messages = []
        self.scam_detected = False
        self.scam_confidence = 0.0
        self.intelligence = ScamIntelligence()
        self.agent_notes = []
        self.persona = "cautious_user"  # AI agent persona
        self.engagement_stage = "initial"  # initial, engaged, extraction, closing
        
    def add_message(self, sender, text, timestamp):
        self.messages.append({
            "sender": sender,
            "text": text,
            "timestamp": timestamp
        })
    
    def get_message_count(self):
        return len(self.messages)

def require_api_key(f):
    """Decorator to validate API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != API_KEY:
            return jsonify({
                "status": "error",
                "message": "Invalid API key or malformed request"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def detect_scam_intent(message_text, conversation_history):
    """
    Detect if a message is a scam attempt
    Returns: (is_scam, confidence, detected_patterns)
    """
    text_lower = message_text.lower()
    detected_patterns = defaultdict(list)
    
    # Check each pattern category
    for category, patterns in SCAM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                detected_patterns[category].append(pattern)
    
    # Calculate confidence based on pattern matches
    category_matches = len(detected_patterns)
    total_pattern_matches = sum(len(v) for v in detected_patterns.values())
    
    # Scoring logic
    confidence = 0.0
    
    # Multiple categories indicate higher scam probability
    if category_matches >= 3:
        confidence = 0.85
    elif category_matches == 2:
        confidence = 0.70
    elif category_matches == 1:
        confidence = 0.50
    
    # Boost confidence for specific high-risk combinations
    if 'threats' in detected_patterns and 'financial' in detected_patterns:
        confidence = min(0.95, confidence + 0.15)
    
    if 'urgency' in detected_patterns and 'verification' in detected_patterns:
        confidence = min(0.90, confidence + 0.10)
    
    # Check conversation history for escalation patterns
    if len(conversation_history) > 0:
        # Scammers often escalate threats
        recent_messages = [msg['text'].lower() for msg in conversation_history[-3:] 
                          if msg['sender'] == 'scammer']
        if any(re.search(r'urgent|immediately|now', msg) for msg in recent_messages):
            confidence = min(0.95, confidence + 0.05)
    
    is_scam = confidence >= 0.50
    
    return is_scam, confidence, dict(detected_patterns)

def extract_intelligence(text, intelligence):
    """Extract scam-related intelligence from text"""
    
    # Extract bank account numbers (format: XXXX-XXXX-XXXX or similar)
    bank_patterns = [
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4,6}\b',
        r'\b\d{10,18}\b'
    ]
    for pattern in bank_patterns:
        matches = re.findall(pattern, text)
        intelligence.bank_accounts.extend(matches)
    
    # Extract UPI IDs (format: username@bankname)
    upi_pattern = r'\b[\w\.-]+@[\w\.-]+\b'
    upi_matches = re.findall(upi_pattern, text)
    for upi in upi_matches:
        if any(bank in upi.lower() for bank in ['upi', 'paytm', 'gpay', 'phonepe', 'ybl', 'okaxis', 'okhdfcbank']):
            intelligence.upi_ids.append(upi)
    
    # Extract URLs/phishing links
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    intelligence.phishing_links.extend(urls)
    
    # Extract phone numbers
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\d{10}',
        r'\b\d{10}\b'
    ]
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        intelligence.phone_numbers.extend(phones)
    
    # Extract suspicious keywords
    text_lower = text.lower()
    for category, patterns in SCAM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                # Extract the actual matched word
                match = re.search(pattern, text_lower)
                if match:
                    intelligence.suspicious_keywords.append(match.group())

def generate_agent_response(session, scammer_message):
    """
    Generate contextual AI agent response based on conversation stage
    The agent maintains a believable persona and adapts responses
    """
    
    stage = session.engagement_stage
    message_count = session.get_message_count()
    text_lower = scammer_message.lower()
    
    # Stage 1: Initial - Show concern/confusion
    if stage == "initial":
        responses = [
            "Why is my account being blocked? I haven't done anything wrong.",
            "What? I don't understand. What verification are you talking about?",
            "Is this real? How do I know you're from the bank?",
            "I'm worried. Can you explain what's happening?",
            "This seems urgent. What should I do?"
        ]
        
        # Progress to engaged stage after initial response
        session.engagement_stage = "engaged"
        session.agent_notes.append("Initial engagement - showing concern")
        
        # Select response based on message content
        if 'block' in text_lower or 'suspend' in text_lower:
            return responses[0]
        elif 'verify' in text_lower or 'confirm' in text_lower:
            return responses[1]
        else:
            return responses[3]
    
    # Stage 2: Engaged - Ask questions, show willingness but hesitation
    elif stage == "engaged":
        
        # If scammer asks for financial info
        if any(word in text_lower for word in ['upi', 'account', 'card', 'cvv', 'otp', 'pin']):
            responses = [
                "I want to help, but I'm not sure about sharing that. Is there another way?",
                "My account number? I have it somewhere... why do you need it exactly?",
                "I'm a bit nervous sharing this information. Can you verify you're really from the bank first?",
                "Should I share this over message? Isn't that unsafe?"
            ]
            session.engagement_stage = "extraction"
            session.agent_notes.append("Scammer requesting sensitive info - showing hesitation")
            return responses[message_count % len(responses)]
        
        # If scammer sends links
        elif 'http' in text_lower or 'link' in text_lower or 'click' in text_lower:
            session.agent_notes.append("Phishing link detected")
            return "I see a link. Is this safe to click? I've heard about fake websites."
        
        # General engagement
        else:
            responses = [
                "I'm trying to understand. Can you explain more?",
                "What happens if I don't do this right away?",
                "How long do I have to fix this?",
                "Is my money safe? I'm really worried."
            ]
            return responses[message_count % len(responses)]
    
    # Stage 3: Extraction - Pretend to comply while extracting info
    elif stage == "extraction":
        
        # Check if enough intelligence is gathered
        intel_count = (len(session.intelligence.bank_accounts) + 
                      len(session.intelligence.upi_ids) + 
                      len(session.intelligence.phishing_links) + 
                      len(session.intelligence.phone_numbers))
        
        if intel_count >= 3 or message_count >= 12:
            session.engagement_stage = "closing"
            session.agent_notes.append("Sufficient intelligence gathered")
            return "Wait, I'm going to call my bank directly to confirm this. Let me call them."
        
        # Continue extraction
        if 'upi' in text_lower:
            return "My UPI ID? Let me check... but can you tell me your employee ID first?"
        elif 'account' in text_lower:
            return "I have multiple accounts. Which one are you talking about?"
        elif 'otp' in text_lower or 'code' in text_lower:
            return "I haven't received any OTP yet. Where should I look for it?"
        else:
            return "Okay, I'm looking for that information. What will you do with it?"
    
    # Stage 4: Closing - Disengage
    else:
        return "Actually, I'm going to visit the bank branch in person. Thanks anyway."

@app.route('/api/honeypot', methods=['POST'])
@require_api_key
def honeypot_endpoint():
    """
    Main honeypot API endpoint
    Handles incoming messages and orchestrates scam detection and engagement
    """
    try:
        # Validate content type
        if request.content_type != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'sessionId' not in data or 'message' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: sessionId and message"
            }), 400
        
        session_id = data['sessionId']
        message = data['message']
        conversation_history = data.get('conversationHistory', [])
        metadata = data.get('metadata', {})
        
        # Validate message structure
        if 'sender' not in message or 'text' not in message:
            return jsonify({
                "status": "error",
                "message": "Message must contain 'sender' and 'text' fields"
            }), 400
        
        # Get or create session
        if session_id not in sessions:
            sessions[session_id] = ConversationSession(session_id)
        
        session = sessions[session_id]
        
        # Add current message to session
        session.add_message(
            message['sender'],
            message['text'],
            message.get('timestamp', datetime.now(timezone.utc).isoformat())
        )
        
        # Add conversation history if this is continuation
        if conversation_history and len(session.messages) == 1:
            for hist_msg in conversation_history:
                session.add_message(
                    hist_msg['sender'],
                    hist_msg['text'],
                    hist_msg.get('timestamp', datetime.now(timezone.utc).isoformat())
                )
        
        # Detect scam intent
        is_scam, confidence, patterns = detect_scam_intent(
            message['text'],
            conversation_history
        )
        
        # Update session scam detection
        if is_scam and confidence > session.scam_confidence:
            session.scam_detected = True
            session.scam_confidence = confidence
            session.agent_notes.append(f"Scam detected with {confidence:.2f} confidence")
        
        # Extract intelligence from scammer's message
        extract_intelligence(message['text'], session.intelligence)
        
        # Generate agent response
        agent_reply = generate_agent_response(session, message['text'])
        
        # Check if conversation should end
        should_end = (
            session.engagement_stage == "closing" or 
            session.get_message_count() >= 20
        )
        
        # If ending and scam detected, send callback
        if should_end and session.scam_detected:
            send_final_callback(session)
        
        # Return agent response
        return jsonify({
            "status": "success",
            "reply": agent_reply
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Processing error: {str(e)}"
        }), 500

def send_final_callback(session):
    """
    Send final intelligence to GUVI evaluation endpoint
    This is mandatory for evaluation
    """
    try:
        payload = {
            "sessionId": session.session_id,
            "scamDetected": session.scam_detected,
            "totalMessagesExchanged": session.get_message_count(),
            "extractedIntelligence": session.intelligence.to_dict(),
            "agentNotes": " | ".join(session.agent_notes)
        }
        
        # Send POST request to GUVI endpoint
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Log the response
        print(f"Callback sent for session {session.session_id}: {response.status_code}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending callback: {str(e)}")
        return False

@app.route('/api/honeypot/manual-callback', methods=['POST'])
@require_api_key
def manual_callback():
    """
    Manual endpoint to trigger final callback for a session
    Useful for testing or forcing callback
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        
        if not session_id or session_id not in sessions:
            return jsonify({
                "status": "error",
                "message": "Invalid session ID"
            }), 400
        
        session = sessions[session_id]
        success = send_final_callback(session)
        
        return jsonify({
            "status": "success" if success else "error",
            "message": "Callback sent" if success else "Callback failed"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Agentic Honey-Pot API",
        "active_sessions": len(sessions)
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
