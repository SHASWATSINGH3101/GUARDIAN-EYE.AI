# app/__init__.py

"""
This module initializes the Guardian Eye AI application package.
It explicitly imports necessary components to maintain a clean namespace.
"""

from .config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    EMERGENCY_PHONE_NUMBER,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    FLASK_PORT,
    MILLIS_API_KEY,
    MILLIS_AGENT_ID,
    FROM_PHONE_NUMBER,
    TO_PHONE_NUMBER,
    BUFFER_SCALE_FACTOR,
    MODEL1_PATH,
    MODEL2_PATH,
    MODEL3_PATH
)
from .detection import (
    run_all_models,
    SeverityTracker,
    BUFFER_SECONDS,
    process_alerts,
    process_review_alert,
    save_video_clip
)
from .millis_call import make_emergency_call
from .telegram_alert import send_telegram_video, extract_metadata_from_message
