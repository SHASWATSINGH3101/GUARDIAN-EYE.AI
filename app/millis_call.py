# app/millis_call.py

import requests
import logging
from app.config import MILLIS_API_KEY, MILLIS_AGENT_ID, FROM_PHONE_NUMBER, TO_PHONE_NUMBER

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def make_emergency_call(metadata):
    """
    Initiates an emergency call using Millis AI, enriched with metadata.
    The metadata should include:
      - date_of_incident
      - time_of_incident
      - severity_level
      - detections
      - confidence
      - additional_info (optional extra details)
    """
    try:
        url = "https://api-west.millis.ai/start_outbound_call"
        headers = {
            "Content-Type": "application/json",
            "Authorization": MILLIS_API_KEY
        }
        
        # Build call metadata dynamically.
        call_metadata = {
            "emergency": "violence_detected",
            "date_of_incident": metadata.get("date_of_incident", "Unknown"),
            "time_of_incident": metadata.get("time_of_incident", "Unknown"),
            "severity_level": metadata.get("severity_level", "unknown"),
            "detections": metadata.get("detections", 0),
            "confidence": metadata.get("confidence", 0.0),
            "additional_info": metadata.get("additional_info", ""),
            "location": "Lucknow, Uttar Pradesh"  # Static location (can be made dynamic)
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
        logging.info("Emergency call initiated successfully: %s", response.json())
    except requests.exceptions.RequestException as e:
        logging.error("Error initiating emergency call: %s", e)
