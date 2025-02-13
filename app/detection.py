# app/detection.py

import cv2
import os
import time
from datetime import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import re
import requests
from threading import Thread
import torch
import logging

from ultralytics import YOLO
from app.millis_call import make_emergency_call
from app.telegram_alert import send_telegram_video
from app.config import MODEL1_PATH, MODEL2_PATH, MODEL3_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# ------------------------
# Hyperparameter Settings (Centralized)
# ------------------------
HYPERPARAMETERS = {
    "mild_threshold": 0.8,             # If max confidence >= 0.8, HIGH; otherwise, MILD.
    "detection_count_threshold": 20,   # Minimum detections over the sliding window.
    "mild_consecutive_threshold": 5    # Number of consecutive MILD events needed to escalate to HIGH.
}

# ------------------------
# GPU Setup: Load models onto GPU if available
# ------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model1 = YOLO(MODEL1_PATH)
    model1.to(device)
    logging.info("Model1 loaded successfully from %s", MODEL1_PATH)
except Exception as e:
    logging.error("Failed to load Model1: %s", e)

try:
    model2 = YOLO(MODEL2_PATH)
    model2.to(device)
    logging.info("Model2 loaded successfully from %s", MODEL2_PATH)
except Exception as e:
    logging.error("Failed to load Model2: %s", e)

try:
    model3 = YOLO(MODEL3_PATH)
    model3.to(device)
    logging.info("Model3 loaded successfully from %s", MODEL3_PATH)
except Exception as e:
    logging.error("Failed to load Model3: %s", e)

# ------------------------
# BUFFER_SECONDS for video buffering
# ------------------------
BUFFER_SECONDS = 5

# ------------------------
# Model Inference Functions
# ------------------------
def run_model1(frame):
    """Run the primary violence detection model."""
    results = model1(frame)
    detections = []
    for r in results:
        for box in r.boxes:
            conf = box.conf.cpu().item()
            cls = box.cls.cpu().item()
            # Assuming class '1' indicates violence for model1
            if cls == 1:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                detections.append({"confidence": conf, "box": (x1, y1, x2, y2)})
    return detections

def run_model2(frame):
    """Run the lethal object detection model."""
    results = model2(frame)
    info = []
    for r in results:
        for box in r.boxes:
            conf = box.conf.cpu().item()
            cls = box.cls.cpu().item()
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            info.append({"confidence": conf, "box": (x1, y1, x2, y2), "class": cls})
    return info

def run_model3(frame):
    """Run the violence classification model."""
    results = model3(frame)
    info = []
    for r in results:
        for box in r.boxes:
            conf = box.conf.cpu().item()
            cls = box.cls.cpu().item()
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            info.append({"confidence": conf, "box": (x1, y1, x2, y2), "class": cls})
    return info

def run_all_models(frame):
    """Run all three models concurrently and return their outputs."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(run_model1, frame)
        future2 = executor.submit(run_model2, frame)
        future3 = executor.submit(run_model3, frame)
        result1 = future1.result()
        result2 = future2.result()
        result3 = future3.result()
    return {"model1": result1, "model2": result2, "model3": result3}

# ------------------------
# Sliding Window Severity Tracker
# ------------------------
class SeverityTracker:
    def __init__(self, window_size: int):
        self.window_size = window_size  # in seconds
        self.detections = deque()       # Each element is a tuple: (timestamp, confidence)
        self.last_cleanup_time = time.time()
        self.last_detection_time = time.time()
        self.consecutive_mild_count = 0  # Track consecutive MILD events

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

    def get_severity(self) -> dict:
        current_time = time.time()
        self._cleanup_old_detections(current_time)
        count = len(self.detections)
        max_conf = max((conf for _, conf in self.detections), default=0.0)
        
        # Determine severity based on sliding window data
        if count >= HYPERPARAMETERS["detection_count_threshold"]:
            if max_conf >= HYPERPARAMETERS["mild_threshold"]:
                severity = 'HIGH'
            else:
                severity = 'MILD'
        else:
            severity = 'NONE'
        
        # Update consecutive MILD counter and possibly escalate
        if severity == 'HIGH':
            self.consecutive_mild_count = 0
        elif severity == 'MILD':
            self.consecutive_mild_count += 1
            if self.consecutive_mild_count >= HYPERPARAMETERS["mild_consecutive_threshold"]:
                severity = 'HIGH'
                self.consecutive_mild_count = 0
        else:
            self.consecutive_mild_count = 0
        
        return {'level': severity, 'count': count, 'max_confidence': max_conf}

# ------------------------
# Alert Processing Functions
# ------------------------
def process_alerts(saved_path, base_message, extra_info, trigger_call):
    """
    For HIGH severity alerts: enrich the message with extra info from model2 and model3,
    send a Telegram alert, and initiate an emergency call if trigger_call is True.
    """
    extra_text = ""
    if extra_info.get("model2"):
        extra_text += "\nLethal Objects Detected:\n"
        for det in extra_info["model2"]:
            extra_text += f" - Confidence: {det['confidence']:.2f}, Box: {det['box']}\n"
    if extra_info.get("model3"):
        extra_text += "\nViolence Classification:\n"
        for det in extra_info["model3"]:
            extra_text += f" - Confidence: {det['confidence']:.2f}, Class: {det['class']}\n"
    enriched_message = base_message + extra_text
    metadata = send_telegram_video(saved_path, enriched_message)
    logging.info("Extracted Metadata: %s", metadata)
    if trigger_call and metadata:
        Thread(target=make_emergency_call, args=(metadata,)).start()

def process_review_alert(saved_path, base_message, extra_info):
    """
    For MILD severity alerts: send only a review Telegram alert enriched with extra info.
    No emergency call is made.
    """
    extra_text = ""
    if extra_info.get("model2"):
        extra_text += "\nLethal Objects Detected:\n"
        for det in extra_info["model2"]:
            extra_text += f" - Confidence: {det['confidence']:.2f}, Box: {det['box']}\n"
    if extra_info.get("model3"):
        extra_text += "\nViolence Classification:\n"
        for det in extra_info["model3"]:
            extra_text += f" - Confidence: {det['confidence']:.2f}, Class: {det['class']}\n"
    enriched_message = base_message + extra_text
    send_telegram_video(saved_path, enriched_message)

# ------------------------
# Video Saving Helper
# ------------------------
def save_video_clip(frame_buffer: deque, output_path: str, fps: int):
    """Save a clip from the frame buffer to the specified output path."""
    if not frame_buffer:
        logging.warning("Frame buffer is empty, cannot save video clip.")
        return None
    frames = [frame.astype(np.uint8) for frame in frame_buffer]
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        logging.info("Video clip saved successfully at %s", output_path)
        return output_path
    else:
        logging.error("Failed to save a valid video clip at %s", output_path)
        return None
