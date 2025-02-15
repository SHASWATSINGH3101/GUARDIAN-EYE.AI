# 2222  # app/config.py

import os

# Twilio Configuration - Ensure you set these in your environment variables.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC3f64e588013f83329ad463ef1ab405a4")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "ed429ebfa285606dc7fd1ca547252c8d")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+15674122275")
EMERGENCY_PHONE_NUMBER = os.environ.get("EMERGENCY_PHONE_NUMBER", "Add yours")

# Telegram Configuration - Set these securely in your environment.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "Add yours")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "Add yours")

# Flask Server Configuration (if applicable)
FLASK_PORT = int(os.environ.get("FLASK_PORT", 5000))

# Millis AI Configuration - Set these via environment variables.
MILLIS_API_KEY = os.environ.get("MILLIS_API_KEY", "3spNq9LeArjRRkgW3UXnynyxVBQ6xFU2")
MILLIS_AGENT_ID = os.environ.get("MILLIS_AGENT_ID", "-OIjPEnOJK__QQwSbXVp")
FROM_PHONE_NUMBER = os.environ.get("FROM_PHONE_NUMBER", "+15674122275")  # Agent's phone number
TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER", "Add yours")     # Emergency contact number

# Buffer Optimization Configuration
BUFFER_SCALE_FACTOR = float(os.environ.get("BUFFER_SCALE_FACTOR", "0.98"))

# Model Paths - Update these environment variables with the correct paths for your models.
MODEL1_PATH = os.environ.get("MODEL1_PATH", "Add yours")
MODEL2_PATH = os.environ.get("MODEL2_PATH", "Add yours"
MODEL3_PATH = os.environ.get("MODEL3_PATH", "Add yours")
