import requests
import os
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_video(video_path: str, message: str):
    """Send a video clip to Telegram."""
    try:
        # Send the message first
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
        response.raise_for_status()

        # Send the video
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
            print("Telegram video alert sent successfully.")
        else:
            print(f"Error: Video file is invalid or empty: {video_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram alert: {e}")
    except Exception as e:
        print(f"Unexpected error sending Telegram alert: {e}")
