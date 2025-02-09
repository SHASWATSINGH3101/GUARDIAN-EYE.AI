from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMERGENCY_PHONE_NUMBER
from twilio.rest import Client

import requests
from app.config import MILLIS_API_KEY, MILLIS_AGENT_ID, FROM_PHONE_NUMBER, TO_PHONE_NUMBER


def make_emergency_call(metadata):
    """Make an emergency call using Millis AI with dynamic metadata."""
    try:
        url = "https://api-west.millis.ai/start_outbound_call"
        headers = {
            "Content-Type": "application/json",
            "Authorization": MILLIS_API_KEY
        }
        
        # Include dynamic metadata (Fallback to defaults if missing)
        call_metadata = {
            "emergency": "violence_detected",
            "date_of_incident": metadata.get("date_of_incident", "Unknown"),
            "time_of_incident": metadata.get("time_of_incident", "Unknown"),
            "severity_level": metadata.get("severity_level", "unknown"),
            "detections": metadata.get("detections", 0),
            "confidence": metadata.get("confidence", 0.0)
        }


        
        data = {
            "from_phone": FROM_PHONE_NUMBER,
            "to_phone": TO_PHONE_NUMBER,
            "agent_id": MILLIS_AGENT_ID,
            "metadata": call_metadata,
            "include_metadata_in_prompt": True
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"Emergency call initiated successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error initiating emergency call: {e}")

