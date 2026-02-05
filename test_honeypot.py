# -*- coding: utf-8 -*-
"""
Test script for Problem 2: Agentic Honey-Pot API
Simulates a complete scam conversation
"""

import requests
import uuid
from datetime import datetime, timedelta
import time

class HoneypotTester:
    def __init__(self, api_url="http://localhost:5001", api_key="sk_test_123456789"):
        self.api_url = api_url
        self.api_key = api_key
        self.session_id = str(uuid.uuid4())
        self.conversation_history = []
        
    def send_message(self, scammer_text, delay=1):
        """Send a message to the honeypot API"""
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        payload = {
            "sessionId": self.session_id,
            "message": {
                "sender": "scammer",
                "text": scammer_text,
                "timestamp": timestamp
            },
            "conversationHistory": self.conversation_history.copy(),
            "metadata": {
                "channel": "SMS",
                "language": "English",
                "locale": "IN"
            }
        }
        
        print(f"\n{'='*70}")
        print(f"SCAMMER: {scammer_text}")
        print(f"{'='*70}")
        
        try:
            response = requests.post(
                f"{self.api_url}/api/honeypot",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key
                },
                json=payload,
                timeout=10
            )
            
            result = response.json()
            
            if result.get("status") == "success":
                agent_reply = result.get("reply", "")
                print(f"AGENT: {agent_reply}")
                
                # Add both messages to history
                self.conversation_history.append({
                    "sender": "scammer",
                    "text": scammer_text,
                    "timestamp": timestamp
                })
                
                self.conversation_history.append({
                    "sender": "user",
                    "text": agent_reply,
                    "timestamp": timestamp
                })
                
                time.sleep(delay)
                return agent_reply
            else:
                print(f"ERROR: {result.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return None
    
    def run_scam_scenario(self, scenario_name, messages):
        """Run a complete scam scenario"""
        print(f"\n{'#'*70}")
        print(f"# SCENARIO: {scenario_name}")
        print(f"# Session ID: {self.session_id}")
        print(f"{'#'*70}")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n[Message {i}/{len(messages)}]")
            reply = self.send_message(msg)
            if reply is None:
                print("Stopping scenario due to error")
                break
        
        print(f"\n{'='*70}")
        print(f"SCENARIO COMPLETED")
        print(f"Total messages exchanged: {len(self.conversation_history)}")
        print(f"{'='*70}")

def test_health_check(api_url="http://localhost:5001"):
    """Test health check endpoint"""
    print("\n" + "="*70)
    print("HEALTH CHECK")
    print("="*70)
    
    try:
        response = requests.get(f"{api_url}/health")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Status: {result.get('status')}")
        print(f"Service: {result.get('service')}")
        print(f"Active Sessions: {result.get('active_sessions')}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def test_invalid_api_key(api_url="http://localhost:5001"):
    """Test with invalid API key"""
    print("\n" + "="*70)
    print("TESTING INVALID API KEY")
    print("="*70)
    
    try:
        response = requests.post(
            f"{api_url}/api/honeypot",
            headers={
                "Content-Type": "application/json",
                "x-api-key": "invalid_key"
            },
            json={
                "sessionId": "test-session",
                "message": {
                    "sender": "scammer",
                    "text": "Test message",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                "conversationHistory": []
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 401:
            print("[OK] Invalid API key correctly rejected")
        else:
            print("[FAIL] Expected 401 status code")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Scam scenarios
BANK_FRAUD_SCENARIO = [
    "Your bank account will be blocked in 2 hours due to suspicious activity.",
    "To prevent blocking, you must verify your account immediately.",
    "Please share your bank account number and UPI ID for verification.",
    "We need your account number: XXXX-XXXX-XXXX format",
    "Also provide your registered mobile number and UPI ID like name@upi",
    "Click this link to verify: http://fake-bank-verify.com/urgent",
    "If you don't verify now, your account will be frozen permanently.",
    "Share your OTP code that we just sent to your phone.",
    "Final warning: Share details within 10 minutes or lose access to funds."
]

UPI_SCAM_SCENARIO = [
    "Congratulations! You've won ₹50,000 cashback from Paytm!",
    "To claim your prize, verify your UPI ID immediately.",
    "What is your UPI ID? Format: yourname@paytm",
    "Great! Now share your mobile number linked to this UPI.",
    "We're sending you a verification code. Share it when you receive.",
    "The code will expire in 5 minutes. Please hurry!",
    "Send your bank account number to transfer the cashback."
]

PHISHING_SCENARIO = [
    "URGENT: Your tax refund of ₹15,000 is pending.",
    "Government portal link: http://tax-refund-india.com/claim",
    "Enter your PAN card and bank details on this official site.",
    "This is from Income Tax Department. Verify immediately.",
    "Your refund will be cancelled if not claimed within 24 hours."
]

IMPERSONATION_SCENARIO = [
    "This is Police Cyber Crime Department.",
    "Your bank account is involved in suspicious transactions.",
    "Legal action will be taken unless you cooperate immediately.",
    "Share your account details for investigation.",
    "Transfer ₹5,000 to this UPI ID for verification: cybercrime@paytm",
    "This is official police business. Share your phone number."
]

if __name__ == "__main__":
    api_url = "http://localhost:5001"
    api_key = "sk_test_123456789"
    
    print("="*70)
    print("AGENTIC HONEY-POT API - TEST SUITE")
    print("="*70)
    
    # Health check
    test_health_check(api_url)
    
    # Test invalid API key
    test_invalid_api_key(api_url)
    
    # Choose scenario
    print("\n" + "="*70)
    print("SELECT SCENARIO TO TEST:")
    print("="*70)
    print("1. Bank Fraud (9 messages)")
    print("2. UPI Scam (7 messages)")
    print("3. Phishing (5 messages)")
    print("4. Police Impersonation (6 messages)")
    print("5. All scenarios")
    
    choice = input("\nEnter choice (1-5) or press Enter for scenario 1: ").strip()
    
    if not choice:
        choice = "1"
    
    scenarios = {
        "1": ("Bank Account Fraud", BANK_FRAUD_SCENARIO),
        "2": ("UPI Cashback Scam", UPI_SCAM_SCENARIO),
        "3": ("Tax Refund Phishing", PHISHING_SCENARIO),
        "4": ("Police Impersonation", IMPERSONATION_SCENARIO)
    }
    
    if choice == "5":
        # Run all scenarios
        for key, (name, messages) in scenarios.items():
            tester = HoneypotTester(api_url, api_key)
            tester.run_scam_scenario(name, messages)
            time.sleep(2)
    elif choice in scenarios:
        name, messages = scenarios[choice]
        tester = HoneypotTester(api_url, api_key)
        tester.run_scam_scenario(name, messages)
    else:
        print("Invalid choice")
    
    print("\n" + "="*70)
    print("TESTS COMPLETED")
    print("="*70)
    print("\nNote: The final intelligence should be automatically sent to:")
    print("https://hackathon.guvi.in/api/updateHoneyPotFinalResult")
