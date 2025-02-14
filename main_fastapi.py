# main_fastapi.py

import os
import cv2
import time
from datetime import datetime
from collections import deque
from threading import Thread, Lock
import logging


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles

from app.detection import (
    run_all_models,
    process_alerts,       # Accepts an extra parameter: trigger_call (bool)
    process_review_alert,
    save_video_clip,
    BUFFER_SECONDS,
    SeverityTracker      # Sliding window tracker for severity calculation
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# --------------------------------------------------
# Global Variables & Settings with Locks for Thread Safety
# --------------------------------------------------
detection_status = {
    "level": "NONE",
    "max_confidence": 0.0,
    "detections": 0,
    "last_update": "",
    "alert": "",
    "logs": []  # Stores recent log entries
}
detection_status_lock = Lock()

incident_history = []
incident_history_lock = Lock()

app_settings = {
    "video_save_path": "output",  # Directory where video clips are stored
    "telegram_alert_interval": 10,        # Minimum seconds between successive Telegram alerts
    "emergency_call_interval": 30         # Minimum seconds between successive emergency calls
}

last_telegram_alert_time = 0
last_emergency_call_time = 0

os.makedirs(app_settings["video_save_path"], exist_ok=True)

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Instantiate a global severity tracker with a sliding window (in seconds)
severity_tracker = SeverityTracker(window_size=5)

# --------------------------------------------------
# Detection Frame Generator with Thread-Safe Updates
# --------------------------------------------------
def detection_frame_generator():
    global last_telegram_alert_time, last_emergency_call_time, detection_status, incident_history, severity_tracker

    # Use default camera capture for cross-platform compatibility
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Cannot access the webcam.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    # Buffer for saving video clips when an alert is triggered
    frame_buffer = deque(maxlen=fps * (BUFFER_SECONDS * 2))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.error("Error: Cannot read frame.")
            break

        scaled_frame = frame.copy()
        frame_buffer.append(scaled_frame)

        current_time = time.time()

        # Run all models concurrently on the current frame
        model_results = run_all_models(frame)
        model1_results = model_results.get("model1", [])

        # Update the severity tracker with detections
        for det in model1_results:
            severity_tracker.add_detection(current_time, det["confidence"])

        severity_info = severity_tracker.get_severity()
        severity = severity_info["level"]
        detection_count = severity_info["count"]
        max_conf = severity_info["max_confidence"]

        # Update detection_status safely
        with detection_status_lock:
            detection_status["level"] = severity
            detection_status["max_confidence"] = round(max_conf, 2)
            detection_status["detections"] = detection_count
            detection_status["last_update"] = time.strftime("%H:%M:%S")

        # Draw bounding boxes on the frame for model1 detections
        for det in model1_results:
            x1, y1, x2, y2 = det["box"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        overlay_text = (
            f"Severity: {severity} | "
            f"Confidence: {round(max_conf,2)} | "
            f"Detections: {detection_count} | "
            f"Last Update: {time.strftime('%H:%M:%S')}"
        )
        cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Alert triggering logic with rate limiting and thread-safe updates
        if severity == "HIGH":
            telegram_allowed = (current_time - last_telegram_alert_time) >= app_settings["telegram_alert_interval"]
            call_allowed = (current_time - last_emergency_call_time) >= app_settings["emergency_call_interval"]
            if telegram_allowed or call_allowed:
                video_filename = f"violent_clip_{int(current_time)}.mp4"
                video_path = os.path.join(app_settings["video_save_path"], video_filename)
                saved_path = save_video_clip(frame_buffer, video_path, fps)
                current_dt = datetime.now()
                base_message = (
                    f"🚨 Violent Activity Detected!\n"
                    f"Date: {current_dt.strftime('%Y-%m-%d')}\n"
                    f"Time: {current_dt.strftime('%I:%M %p')}\n"
                    f"Severity: {severity}\n"
                    f"Confidence: {max_conf:.2f}\n"
                    f"Detections: {detection_count}"
                )
                log_entry = f"{current_dt.strftime('%H:%M:%S')} - HIGH alert (Confidence: {max_conf:.2f}, Detections: {detection_count})"
                with detection_status_lock:
                    detection_status["logs"].append(log_entry)
                    if len(detection_status["logs"]) > 10:
                        detection_status["logs"].pop(0)
                extra_info = {
                    "model2": model_results.get("model2", []),
                    "model3": model_results.get("model3", [])
                }
                if telegram_allowed:
                    last_telegram_alert_time = current_time
                if call_allowed:
                    last_emergency_call_time = current_time
                Thread(target=process_alerts, args=(saved_path, base_message, extra_info, call_allowed)).start()
                with incident_history_lock:
                    incident_history.append({
                        "date": current_dt.strftime("%Y-%m-%d"),
                        "time": current_dt.strftime("%H:%M:%S"),
                        "severity": severity,
                        "confidence": round(max_conf, 2),
                        "detections": detection_count,
                        "message": base_message
                    })
                with detection_status_lock:
                    detection_status["alert"] = "High alert triggered: Telegram alert sent" + (", emergency call initiated." if call_allowed else ".")
                # Reset the severity tracker after sending an alert
                severity_tracker.detections.clear()
        elif severity == "MILD":
            if (current_time - last_telegram_alert_time) >= app_settings["telegram_alert_interval"]:
                video_filename = f"violent_clip_{int(current_time)}.mp4"
                video_path = os.path.join(app_settings["video_save_path"], video_filename)
                saved_path = save_video_clip(frame_buffer, video_path, fps)
                current_dt = datetime.now()
                base_message = (
                    f"🚨 Violent Activity Detected!\n"
                    f"Date: {current_dt.strftime('%Y-%m-%d')}\n"
                    f"Time: {current_dt.strftime('%I:%M %p')}\n"
                    f"Severity: {severity}\n"
                    f"Confidence: {max_conf:.2f}\n"
                    f"Detections: {detection_count}"
                )
                log_entry = f"{current_dt.strftime('%H:%M:%S')} - MILD alert (Confidence: {max_conf:.2f}, Detections: {detection_count})"
                with detection_status_lock:
                    detection_status["logs"].append(log_entry)
                    if len(detection_status["logs"]) > 10:
                        detection_status["logs"].pop(0)
                extra_info = {
                    "model2": model_results.get("model2", []),
                    "model3": model_results.get("model3", [])
                }
                last_telegram_alert_time = current_time
                Thread(target=process_review_alert, args=(saved_path, base_message, extra_info)).start()
                with incident_history_lock:
                    incident_history.append({
                        "date": current_dt.strftime("%Y-%m-%d"),
                        "time": current_dt.strftime("%H:%M:%S"),
                        "severity": severity,
                        "confidence": round(max_conf, 2),
                        "detections": detection_count,
                        "message": base_message
                    })
                with detection_status_lock:
                    detection_status["alert"] = "Mild alert triggered: Telegram review alert sent."
                # Reset the severity tracker after sending an alert
                severity_tracker.detections.clear()
            else:
                with detection_status_lock:
                    detection_status["alert"] = ""
        else:
            with detection_status_lock:
                detection_status["alert"] = ""

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
    with detection_status_lock:
        status_copy = detection_status.copy()
    return templates.TemplateResponse("dashboard.html", {"request": request, "status": status_copy})

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(detection_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/status_view", response_class=HTMLResponse)
async def status_view(request: Request):
    with detection_status_lock:
        status_copy = detection_status.copy()
    response = templates.TemplateResponse("status.html", {"request": request, "status": status_copy})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.get("/incidents", response_class=HTMLResponse)
def incidents(request: Request):
    with incident_history_lock:
        incidents_copy = incident_history.copy()
    return templates.TemplateResponse("incidents.html", {"request": request, "incidents": incidents_copy})

@app.get("/settings", response_class=HTMLResponse)
def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "settings": app_settings})

@app.post("/update_settings")
async def update_settings(
    telegram_alert_interval: int = Form(...),
    emergency_call_interval: int = Form(...),
    video_save_path: str = Form(...)
):
    if telegram_alert_interval < 1 or emergency_call_interval < 1:
        return HTMLResponse("Alert intervals must be at least 1 second.", status_code=400)
    app_settings["telegram_alert_interval"] = telegram_alert_interval
    app_settings["emergency_call_interval"] = emergency_call_interval
    app_settings["video_save_path"] = video_save_path
    os.makedirs(video_save_path, exist_ok=True)
    logging.info("Updated settings: %s", app_settings)
    return RedirectResponse(url="/settings", status_code=302)

# --------------------------------------------------
# Running the App:
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_fastapi:app", host="0.0.0.0", port=8000, reload=True)
