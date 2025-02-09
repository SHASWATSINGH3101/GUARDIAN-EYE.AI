import cv2
import os
import time
from ultralytics import YOLO
from datetime import datetime
import requests
from threading import Thread
import numpy as np
from collections import deque
from typing import List, Dict
from app.millis_call import make_emergency_call  # Import Twilio call function
import re
import requests

# ------------------------
# Hyperparameters / Configurations
# ------------------------

# Model path
MODEL_PATH = "X:\\VS_CODE\\_HACKATHON\\_IPYNB\\best model\\archive\\best (6).pt"

# Output directory for video clips
OUTPUT_DIR = "X:\\VS_CODE\\_HACKATHON\\datasets\\Real Life Violence Dataset\\out"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Telegram credentials
TOKEN = "7875405991:AAGfgB6i1PJWPSBnAZ8VM--mEQ4atM4pRFA"
CHAT_ID = "1284776332"

# Severity assessment configuration
SEVERITY_WINDOW = 30  # Time window in seconds for severity assessment
SEVERITY_THRESHOLDS = {'low': 1, 'medium': 2, 'high': 3}

# Video buffer configuration (seconds before and after the event)
BUFFER_SECONDS = 5

# Twilio Call configuration
CALL_INTERVAL = 5  # Interval in seconds to make a call after violence detection

# ------------------------
# Model and Helpers
# ------------------------

model = YOLO(MODEL_PATH)

# Video buffer configuration
BUFFER_SIZE = 30  # Buffer size (FPS * BUFFER_SECONDS)
frame_buffer = deque(maxlen=BUFFER_SIZE)


class SeverityTracker:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.detections = deque()
        self.last_cleanup_time = time.time()
        self.last_detection_time = time.time()

    def add_detection(self, timestamp: float, confidence: float):
        self.detections.append((timestamp, confidence))
        self.last_detection_time = timestamp

        current_time = time.time()
        if current_time - self.last_cleanup_time >= 1.0:
            self._cleanup_old_detections(current_time)
            self.last_cleanup_time = current_time

    def _cleanup_old_detections(self, current_time: float):
        while self.detections and (current_time - self.detections[0][0]) > self.window_size:
            self.detections.popleft()
        if current_time - self.last_detection_time > 5.0:
            self.detections.clear()

    def get_severity(self) -> Dict:
        current_time = time.time()
        self._cleanup_old_detections(current_time)

        if not self.detections:
            return {'level': 'none', 'count': 0, 'avg_confidence': 0}

        count = len(self.detections)
        avg_confidence = sum(conf for _, conf in self.detections) / count

        if count >= SEVERITY_THRESHOLDS['high']:
            level = 'high'
        elif count >= SEVERITY_THRESHOLDS['medium']:
            level = 'medium'
        elif count >= SEVERITY_THRESHOLDS['low']:
            level = 'low'
        else:
            level = 'none'

        return {'level': level, 'count': count, 'avg_confidence': avg_confidence}


# Save video clip
def save_video_clip(frame_buffer: deque, output_path: str, fps: int):
    if not frame_buffer:
        return None
    frames = [frame.astype(np.uint8) for frame in frame_buffer]
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    return output_path if os.path.exists(output_path) and os.path.getsize(output_path) > 0 else None


# Send Telegram video alert
def send_telegram_video(video_path: str, message: str):
    metadata = extract_metadata_from_message(message)
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=5).raise_for_status()

        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            video_url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
            with open(video_path, "rb") as video_file:
                files = {"video": ("video.mp4", video_file, "video/mp4")}
                requests.post(video_url, data={"chat_id": CHAT_ID}, files=files, timeout=30).raise_for_status()
            print("Telegram video alert sent successfully.")

    except Exception as e:
        print(f"Error sending Telegram alert: {e}")

    return metadata


# Extract metadata from message
def extract_metadata_from_message(message: str):
    """Extracts metadata from the Telegram alert message."""
    metadata = {}

    date_match = re.search(r"Date: ([\d-]+)", message)
    time_match = re.search(r"Time: ([\d:]+ [APMampm]+)", message)  # Capture AM/PM
    severity_match = re.search(r"Severity: (\w+)", message)
    detections_match = re.search(r"Detections: (\d+)", message)
    confidence_match = re.search(r"Confidence: ([\d.]+)%", message)

    if date_match:
        metadata["date_of_incident"] = date_match.group(1)
    if time_match:
        metadata["time_of_incident"] = time_match.group(1)
    if severity_match:
        metadata["severity_level"] = severity_match.group(1).lower()  # Convert to lowercase
    if detections_match:
        metadata["detections"] = int(detections_match.group(1))  # Convert to integer
    if confidence_match:
        metadata["confidence"] = float(confidence_match.group(1))  # Convert to float

    return metadata




# Run alerts in a separate thread to prevent blocking webcam feed
def process_alerts(saved_path, message):
    """Runs Telegram alert and emergency call in a separate thread."""
    metadata = send_telegram_video(saved_path, message)
    print("Extracted Metadata:", metadata)  # Debugging: Ensure metadata is correct
    if metadata:
        Thread(target=make_emergency_call, args=(metadata,)).start()



# Main function
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    frame_buffer = deque(maxlen=fps * (BUFFER_SECONDS * 2))
    severity_tracker = SeverityTracker(SEVERITY_WINDOW)

    last_report_time = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame.")
                break
            frame_buffer.append(frame.copy())
            results = model(frame)
            current_time = time.time()
            violence_detected = False

            for r in results:
                for box in r.boxes:
                    conf = box.conf.cpu().item()
                    cls = box.cls.cpu().item()
                    if cls == 1 and conf > 0.70:
                        violence_detected = True
                        severity_tracker.add_detection(current_time, conf)
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            severity = severity_tracker.get_severity()
            if violence_detected and severity['level'] == 'high' and (current_time - last_report_time) >= CALL_INTERVAL:
                last_report_time = current_time
                video_path = os.path.join(OUTPUT_DIR, f"violent_clip_{int(current_time)}.mp4")
                if saved_path := save_video_clip(frame_buffer, video_path, fps):
                    current_time = datetime.now()
                    current_time = datetime.now()
                    message = (
                        f"🚨 Violent Activity Detected!\n"
                        f"Date: {current_time.strftime('%Y-%m-%d')}\n"
                        f"Time: {current_time.strftime('%I:%M %p')}\n"  # 12-hour format with AM/PM
                        f"Severity: {severity['level'].upper()}\n"
                        f"Detections: {severity['count']}\n"
                        f"Confidence: {severity['avg_confidence']:.2f}%"
                    )


                    Thread(target=process_alerts, args=(saved_path, message)).start()

            cv2.putText(frame, f"Severity: {severity['level'].upper()} ({severity['count']} detections)", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Webcam Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
