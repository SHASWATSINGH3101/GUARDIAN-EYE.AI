from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMERGENCY_PHONE_NUMBER
from twilio.rest import Client

import requests
from app.config import MILLIS_API_KEY, MILLIS_AGENT_ID, FROM_PHONE_NUMBER, TO_PHONE_NUMBER

def make_emergency_call():
    try:
        url = "https://api-west.millis.ai/start_outbound_call"
        headers = {
            "Content-Type": "application/json",
            "Authorization": MILLIS_API_KEY
        }
        data = {
            "from_phone": FROM_PHONE_NUMBER,
            "to_phone": TO_PHONE_NUMBER,
            "agent_id": MILLIS_AGENT_ID,
            "metadata": {
                "emergency": "violence_detected",
                "location": "Lucknow, Uttar Pradesh, India"
            },
            "include_metadata_in_prompt": True
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"Emergency call initiated successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error initiating emergency call: {e}")
