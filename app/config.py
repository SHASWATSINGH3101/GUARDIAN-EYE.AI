# config.py

# Twilio Configuration
TWILIO_ACCOUNT_SID = "AC3f64e588013f83329ad463ef1ab405a4"
TWILIO_AUTH_TOKEN = "ed429ebfa285606dc7fd1ca547252c8d"
TWILIO_PHONE_NUMBER = "+15674122275"
EMERGENCY_PHONE_NUMBER = "+919140529926"

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875405991:AAGfgB6i1PJWPSBnAZ8VM--mEQ4atM4pRFA"
TELEGRAM_CHAT_ID = "1284776332"

# Flask Server Configuration
FLASK_PORT = 5000

# Millis AI Configuration
MILLIS_API_KEY = "kehJagUujTdQ8WvKS9NqoTvbDpnjhQ4L"
MILLIS_AGENT_ID = "-OIOb-NCvRGe2NcgRNDM"
FROM_PHONE_NUMBER = "+15674122275"  # Your agent's phone number
TO_PHONE_NUMBER = "+919140529926"     # Emergency contact number

# Buffer Optimization Configuration
# This downscale factor is applied to frames before adding them to the buffer.
# A factor of 0.5 will store frames at 50% of the original resolution.
BUFFER_SCALE_FACTOR = 0.98
