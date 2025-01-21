from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMERGENCY_PHONE_NUMBER
from twilio.rest import Client

def make_emergency_call():
    try:
        # Twilio credentials
        ACCOUNT_SID = ''
        AUTH_TOKEN = ''
        FROM_PHONE_NUMBER = ''
        TO_PHONE_NUMBER = ''

        # Create a Twilio client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Call API to initiate the call
        call = client.calls.create(
            to=TO_PHONE_NUMBER,
            from_=FROM_PHONE_NUMBER,
            twiml='<Response><Say>hello this is a test call.</Say></Response>'
        )

        print(f"Call initiated successfully: {call.sid}")
        
    except Exception as e:
        print(f"Error during Twilio call: {e}")

    except Exception as e:
        print(f"Error while making the call: {str(e)}")
