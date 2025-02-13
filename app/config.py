# app/config.py

import os

# Twilio Configuration - Ensure you set these in your environment variables.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxx")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "your_auth_token")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+156741222")
EMERGENCY_PHONE_NUMBER = os.environ.get("EMERGENCY_PHONE_NUMBER", "+9191405299")

# Telegram Configuration - Set these securely in your environment.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "your_telegram_chat_id")

# Flask Server Configuration (if applicable)
FLASK_PORT = int(os.environ.get("FLASK_PORT", 5000))

# Millis AI Configuration - Set these via environment variables.
MILLIS_API_KEY = os.environ.get("MILLIS_API_KEY", "your_millis_api_key")
MILLIS_AGENT_ID = os.environ.get("MILLIS_AGENT_ID", "your_millis_agent_id")
FROM_PHONE_NUMBER = os.environ.get("FROM_PHONE_NUMBER", "+156741222")  # Agent's phone number
TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER", "+9191405299")     # Emergency contact number

# Buffer Optimization Configuration
BUFFER_SCALE_FACTOR = float(os.environ.get("BUFFER_SCALE_FACTOR", "0.98"))

# Model Paths - Update these environment variables with the correct paths for your models.
MODEL1_PATH = os.environ.get("MODEL1_PATH", "path/to/model1/best.pt")
MODEL2_PATH = os.environ.get("MODEL2_PATH", "path/to/model2/best.pt")
MODEL3_PATH = os.environ.get("MODEL3_PATH", "path/to/model3/best.pt")
