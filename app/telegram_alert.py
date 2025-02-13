# app/telegram_alert.py

import requests
import os
import re
import logging
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def extract_metadata_from_message(message: str):
    """
    Extracts metadata from the Telegram alert message.
    Expected metadata includes:
      - Date of incident
      - Time of incident
      - Severity level
      - Detections count (if provided)
      - Confidence level
    """
    metadata = {}
    date_match = re.search(r"Date: ([\d-]+)", message)
    time_match = re.search(r"Time: ([\d:]+ [APMapm]+)", message)
    severity_match = re.search(r"Severity: (\w+)", message)
    detections_match = re.search(r"Detections: (\d+)", message)
    confidence_match = re.search(r"Confidence: ([\d.]+)", message)

    if date_match:
        metadata["date_of_incident"] = date_match.group(1)
    if time_match:
        metadata["time_of_incident"] = time_match.group(1)
    if severity_match:
        metadata["severity_level"] = severity_match.group(1).upper()
    if detections_match:
        metadata["detections"] = int(detections_match.group(1))
    if confidence_match:
        metadata["confidence"] = float(confidence_match.group(1))
    return metadata

def send_telegram_video(video_path: str, message: str):
    """
    Sends a Telegram text message and video clip.
    Returns metadata extracted from the message.
    """
    metadata = extract_metadata_from_message(message)
    try:
        # Send text message
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
        response.raise_for_status()
        logging.info("Telegram text message sent successfully.")

        # Send video if the file exists and is valid
        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            video_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
            with open(video_path, "rb") as video_file:
                files = {"video": ("video.mp4", video_file, "video/mp4")}
                response = requests.post(
                    video_url,
                    data={"chat_id": TELEGRAM_CHAT_ID},
                    files=files,
                    timeout=30
                )
                response.raise_for_status()
            logging.info("Telegram video alert sent successfully.")
        else:
            logging.error("Error: Video file is invalid or empty: %s", video_path)
    except requests.exceptions.RequestException as e:
        logging.error("Error sending Telegram alert: %s", e)
    except Exception as e:
        logging.error("Unexpected error sending Telegram alert: %s", e)

    return metadata
