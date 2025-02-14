# 2222  # app/config.py

import os

# Twilio Configuration - Ensure you set these in your environment variables.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")
EMERGENCY_PHONE_NUMBER = os.environ.get("EMERGENCY_PHONE_NUMBER", "")

# Telegram Configuration - Set these securely in your environment.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Flask Server Configuration (if applicable)
FLASK_PORT = int(os.environ.get("FLASK_PORT", 5000))

# Millis AI Configuration - Set these via environment variables.
MILLIS_API_KEY = os.environ.get("MILLIS_API_KEY", "")
MILLIS_AGENT_ID = os.environ.get("MILLIS_AGENT_ID", "")
FROM_PHONE_NUMBER = os.environ.get("FROM_PHONE_NUMBER", "")  # Agent's phone number
TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER", "")     # Emergency contact number

# Buffer Optimization Configuration
BUFFER_SCALE_FACTOR = float(os.environ.get("BUFFER_SCALE_FACTOR", "0.98"))

# Model Paths - Update these environment variables with the correct paths for your models.
MODEL1_PATH = os.environ.get("")
MODEL2_PATH = os.environ.get("")
MODEL3_PATH = os.environ.get("")
