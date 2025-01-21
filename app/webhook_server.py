from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/call", methods=["GET", "POST"])
def call():
    """Responds to Twilio with the message to be spoken."""
    response = VoiceResponse()
    response.say("This is an emergency call. Violent activity has been detected. Please send help immediately.", voice='alice')
    response.hangup()  # End the call
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
