import os
import cv2
import time
from collections import deque
from datetime import datetime
from threading import Thread

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ultralytics import YOLO

# Import functions and classes from your code base.
from app.detection import (
    save_video_clip,
    process_alerts,
    SeverityTracker,
    # These variables are defined in your detection.py:
    MODEL_PATH,
    OUTPUT_DIR,
    CALL_INTERVAL,
    BUFFER_SECONDS,
    SEVERITY_WINDOW,
)
# (Your detection.py already makes sure OUTPUT_DIR exists.)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Global Variables & Settings
# --------------------------------------------------

# This dictionary holds data for the status panel.
# Note the new "announcement" field.
detection_status = {
    "level": "NONE",
    "count": 0,
    "avg_confidence": 0.0,
    "last_update": "",
    "alert": "",
    "announcement": ""
}

# Incident history – each alert record will be appended here.
incident_history = []

# Settings that you can adjust via the UI.
app_settings = {
    "alert_threshold": 3,          # Minimum number of detections required to trigger an alert.
    "min_confidence_threshold": 0.70,  # Minimum confidence (as a fraction) for a detection to count.
    "alert_interval": 5,           # Minimum seconds between successive alerts.
    "emergency_contact": "+919140529926",
    "telegram_chat_id": "1284776332"
}

# Variable to track when the last alert was sent.
last_alert_time = 0

# Load your YOLO model.
model = YOLO(MODEL_PATH)

# --------------------------------------------------
# FastAPI App Setup
# --------------------------------------------------

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --------------------------------------------------
# Detection Frame Generator (UI Integration)
# --------------------------------------------------
def detection_frame_generator():
    """
    This generator continuously captures frames from the webcam,
    runs your YOLO detection (with your actual detection logic),
    overlays bounding boxes, status info, and announcement messages,
    and yields JPEG-encoded frames.
    """
    global last_alert_time
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Adjust the flag if needed.
    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        return

    # Determine FPS and set up a frame buffer.
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    frame_buffer = deque(maxlen=fps * (BUFFER_SECONDS * 2))
    severity_tracker = SeverityTracker(SEVERITY_WINDOW)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        # Add current frame to the buffer.
        frame_buffer.append(frame.copy())

        # Run YOLO detection on the current frame.
        results = model(frame)
        current_time = time.time()
        violence_detected = False

        # Process detections.
        for r in results:
            for box in r.boxes:
                conf = box.conf.cpu().item()  # e.g., 0.85
                cls = box.cls.cpu().item()    # assuming class 1 indicates violence
                if cls == 1 and conf > app_settings["min_confidence_threshold"]:
                    violence_detected = True
                    severity_tracker.add_detection(current_time, conf)
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Retrieve the current severity information.
        severity = severity_tracker.get_severity()  # returns a dict with keys: level, count, avg_confidence
        detection_status["level"] = severity["level"].upper()
        detection_status["count"] = severity["count"]
        detection_status["avg_confidence"] = round(severity["avg_confidence"], 2)
        detection_status["last_update"] = time.strftime("%H:%M:%S")

        # Trigger an alert if conditions are met.
        if (violence_detected and 
            severity["count"] >= app_settings["alert_threshold"] and 
            (current_time - last_alert_time) >= app_settings["alert_interval"]):
            
            last_alert_time = current_time
            video_path = os.path.join(OUTPUT_DIR, f"violent_clip_{int(current_time)}.mp4")
            if (saved_path := save_video_clip(frame_buffer, video_path, fps)):
                current_dt = datetime.now()
                message = (
                    f"🚨 Violent Activity Detected!\n"
                    f"Date: {current_dt.strftime('%Y-%m-%d')}\n"
                    f"Time: {current_dt.strftime('%I:%M %p')}\n"
                    f"Severity: {severity['level'].upper()}\n"
                    f"Detections: {severity['count']}\n"
                    f"Confidence: {severity['avg_confidence']:.2f}%"
                )
                # Set the announcement text.
                detection_status["announcement"] = "Alert triggered! Sending alert messages and initiating calls..."
                # Call your alert functions (e.g., Telegram alert, emergency call) in a new thread.
                Thread(target=process_alerts, args=(saved_path, message)).start()
                # Record this incident.
                incident_history.append({
                    "date": current_dt.strftime("%Y-%m-%d"),
                    "time": current_dt.strftime("%H:%M:%S"),
                    "severity": severity["level"].upper(),
                    "detections": severity["count"],
                    "confidence": round(severity["avg_confidence"], 2),
                    "alert_message": message
                })

        # Automatically clear the announcement after 3 seconds.
        if time.time() - last_alert_time > 3:
            detection_status["announcement"] = ""

        # Overlay detection info on the frame.
        overlay_text = (
            f"Severity: {detection_status['level']} "
            f"({detection_status['count']} detections) | "
            f"Confidence: {detection_status['avg_confidence']}% | "
            f"Last Update: {detection_status['last_update']}"
        )
        cv2.putText(frame, overlay_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        # If an announcement is set, display it.
        if detection_status.get("announcement", ""):
            cv2.putText(frame, detection_status["announcement"], (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# --------------------------------------------------
# FastAPI Endpoints
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page showing the live feed, detection status, and alerts."""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/video_feed")
def video_feed():
    """Endpoint that streams the processed webcam feed."""
    return StreamingResponse(
        detection_frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/status_view", response_class=HTMLResponse)
def status_view(request: Request):
    """Returns an HTML snippet (used by HTMX) with the current detection status."""
    return templates.TemplateResponse("status.html", {"request": request, "status": detection_status})

@app.get("/incidents", response_class=HTMLResponse)
def incidents(request: Request):
    """Incident history page."""
    return templates.TemplateResponse("incidents.html", {"request": request, "incidents": incident_history})

@app.get("/settings", response_class=HTMLResponse)
def settings(request: Request):
    """Settings panel page to adjust alert thresholds, contact info, etc."""
    return templates.TemplateResponse("settings.html", {"request": request, "settings": app_settings})

@app.post("/update_settings")
async def update_settings(
    alert_threshold: int = Form(...),
    min_confidence_threshold: float = Form(...),
    alert_interval: int = Form(...),
    emergency_contact: str = Form(...),
    telegram_chat_id: str = Form(...)
):
    app_settings["alert_threshold"] = alert_threshold
    app_settings["min_confidence_threshold"] = min_confidence_threshold
    app_settings["alert_interval"] = alert_interval
    app_settings["emergency_contact"] = emergency_contact
    app_settings["telegram_chat_id"] = telegram_chat_id

    print("Updated settings:", app_settings)
    return RedirectResponse(url="/settings", status_code=302)

# --------------------------------------------------
# Running the App:
# --------------------------------------------------
# Run using:
#   uvicorn main_fastapi:app --reload
