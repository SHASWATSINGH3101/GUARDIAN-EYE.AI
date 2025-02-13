
# GUARDIAN-EYE.AI

![Guardian-Eye.AI](https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI/blob/main/assets/oie_jpg.png)

## Overview
**Guardian-Eye.AI** is an AI-powered surveillance system designed to enhance public safety by detecting violent activities in real-time. Using **computer vision and deep learning**, this system integrates with existing surveillance infrastructure to identify threats, send alerts, and enable **rapid response** to critical incidents.

## Key Features
- ✅ **Real-Time Violence Detection** – Utilizes **YOLO (You Only Look Once)** for high-speed and accurate detection.
- ✅ **FastAPI-Powered Backend** – Provides a **lightweight, efficient API** for both web and mobile integration.
- ✅ **Live Video Streaming** – Streams processed video with detected threats **overlaid on the feed**.
- ✅ **Incident Logging** – Automatically records **date, time, severity, and detection confidence** for review.
- ✅ **Automated Alerts** – Sends **real-time alerts via Telegram** and triggers emergency calls using **Millis AI/Twilio**.
- ✅ **Configurable Settings** – Adjust alert thresholds, detection confidence, and contact details via an intuitive web dashboard.
- ✅ **Intelligent Alert Escalation** – Triggers review alerts for MILD cases and automatically escalates to HIGH severity if 5 consecutive MILD detections occur.
- ✅ **Web Dashboard (HTMX + FastAPI)** – Provides a responsive UI with **live status updates** and incident history.

---

## Services Used
- **YOLO (Ultralytics)** – For real-time object detection and violence recognition.
- **FastAPI** – Backend framework for handling API requests and responses.
- **HTMX** – Enables dynamic UI updates without a full page reload.
- **OpenCV** – Processes video frames for real-time analysis.
- **Twilio** – Sends emergency phone alerts in case of detected violence.
- **Telegram API** – Delivers real-time alerts to predefined chat groups.
- **Millis AI** – Automates emergency call initiation based on AI analysis.

---

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI.git
cd GUARDIAN-EYE.AI
```

### 2️⃣ Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
To avoid exposing sensitive credentials, create a \`.env\` file and add:
```ini
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
MILLIS_API_KEY=your_api_key
MILLIS_AGENT_ID=your_agent_id
FROM_PHONE_NUMBER=your_from_phone_number
TO_PHONE_NUMBER=your_emergency_number
MODEL1_PATH=path/to/model1/best.pt
MODEL2_PATH=path/to/model2/best.pt
MODEL3_PATH=path/to/model3/best.pt
BUFFER_SCALE_FACTOR=0.98
```

### 5️⃣ Run the Application
```bash
uvicorn main_fastapi:app --reload
```

---

## Usage

### Access the Web Dashboard
Once the server is running, open your browser and visit:
```
http://127.0.0.1:8000/
```

### Key Endpoints
| Endpoint           | Description                                                |
|--------------------|------------------------------------------------------------|
| `/`                | Dashboard showing live detection, alerts, and logs         |
| `/video_feed`      | Streams the processed video feed                           |
| `/status_view`     | Returns the current detection status (updated via HTMX)    |
| `/incidents`       | Displays incident history                                  |
| `/settings`        | Allows users to update system settings                     |
| `/update_settings` | API endpoint to modify alert thresholds, detection confidence, and more |

### Triggering Alerts
- **Violence Detection Above Threshold:**  
  - The system saves a video clip of the incident.
  - Sends a Telegram alert with incident details.
  - Initiates an emergency call (if enabled) via Millis AI/Twilio.
- **MILD vs. HIGH Alerts:**  
  - A **MILD alert** triggers a review alert.
  - If 5 consecutive MILD detections occur, the alert escalates to **HIGH severity**.

---

## Roadmap / Future Enhancements 🚀
- **Multi-Camera Support** – Monitor multiple locations simultaneously.
- **Face Recognition** – Identify known offenders.
- **Cloud Storage Integration** – Securely store incident videos online.
- **WebSockets for Real-Time Updates** – Reduce polling and improve UI performance.
- **Mobile App** – Extend functionality to mobile devices.

---

## Contributing
We welcome contributions! To improve Guardian-Eye.AI, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request!

---

## License
This project is licensed under the **MIT License**.

---

## Contact
For inquiries or support, connect via:
- 💬 **Discord:** shaswat_singh
