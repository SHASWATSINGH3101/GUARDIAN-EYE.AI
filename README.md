
<img src="https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI/blob/main/assets/logo-modified.png" alt="Guardian-Eye.AI" width="350">

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
- A working webcam (or adjust the code for a different video source)
- [Git LFS](https://git-lfs.github.com/) – **Required for downloading large model files.** Make sure Git LFS is installed before cloning the model repository.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI.git
cd GUARDIAN-EYE.AI
```

### 2️⃣ Download Pre-trained Models
Models are hosted on Hugging Face. To download them:
```bash
git lfs install
git clone https://huggingface.co/SHASWATSINGH3101/GAURDIAN_EYE_AI
```
After cloning, update the model paths in your `app/config.py`:
```python
MODEL1_PATH = "GAURDIAN_EYE_AI/model1/best.pt"
MODEL2_PATH = "GAURDIAN_EYE_AI/model2/best.pt"
MODEL3_PATH = "GAURDIAN_EYE_AI/model3/best.pt"
```

### 3️⃣ Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Setting up Telegram Alerts
1. Create a new bot on Telegram using [BotFather](https://t.me/BotFather).
2. Get your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
3. Update the following in your configuration (e.g., in `app/config.py`):
    ```python
    TELEGRAM_BOT_TOKEN = "your_bot_token_here"
    TELEGRAM_CHAT_ID = "your_chat_id_here"
    ```
Use this video to get your bot's TELEGRAM_CHAT_ID:- 
[Chat ID Tutorial](https://youtu.be/l5YDtSLGhqk?si=5C7r3xK4WJFJNBx3)

### 6️⃣ Using Twilio and Millis AI
For full functionality and control, you must create your own accounts and update your configuration with your personal credentials.

### ⭐Note:-

- Make sure to get your emergency number verfied through the twillio dashboard.

 ### Twilio:
Sign up for an account at Twilio and obtain your:
  ```
  TWILIO_ACCOUNT_SID
  TWILIO_AUTH_TOKEN
  TWILIO_PHONE_NUMBER
  ```
 ### Millis AI:
Sign up for an account at Millis AI and obtain your:
  ```
  MILLIS_API_KEY
  MILLIS_AGENT_ID 
  FROM_PHONE_NUMBER 
  TO_PHONE_NUMBER 
  ```
Update your  `app/config.py` with your personal credentials:

```python 
TWILIO_ACCOUNT_SID = "your_account_sid_here"
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_PHONE_NUMBER = "your_twilio_number_here"

MILLIS_API_KEY = "your_millis_api_key_here"
MILLIS_AGENT_ID = "your_agent_id_here"
FROM_PHONE_NUMBER = "your_twilio_number_here"
TO_PHONE_NUMBER = "your_emergency_number_here"

```
- Voice AI Agent Prompt for Millis AI:

  To configure the Millis AI voice agent for reporting violent incidents, use the following prompt:

  ```yaml
  You are a violent incident reporting AI agent. Follow these steps during calls:

  Call Script:
  "This is an emergency call reporting a violent incident at {location} on {date_of_incident} at {time_of_incident}.
  The severity level is {severity_level}, with {detections} cases detected.
  The detection confidence is {confidence}%."

  {If applicable, include additional information:}

  Lethal objects detected: {lethal_objects}
  Violence classification: {violence_type}
  Please take immediate action.

  Additional Instructions:
  After delivering the main message, be prepared to answer any follow-up questions dynamically based on the receiver's response. Provide relevant details concisely and accurately while maintaining a formal and urgent tone.

  Note:
  - Be polite and professional with the receiver.
  - Ensure that the information is delivered clearly and accurately.
  - Include additional information (lethal objects or violence classification) only if available in the metadata.

  ```
## Other resources
- [Twillio docs](https://www.twilio.com/docs)
- [Millis_ai docs](https://docs.millis.ai/introduction)

### 7️⃣ Run the Application
```bash
uvicorn main_fastapi:app --reload
```

### Troubleshooting Tips
- **Git LFS Issues:** Ensure Git LFS is installed before cloning the model repository.
- **Webcam Access:** If you encounter errors accessing your webcam, verify that your system permissions are correctly set or modify the video source in the code.
- **Port Conflicts:** If the server does not start, ensure port 8000 (or the port specified in your configuration) is not in use or adjust the command accordingly.
- **Dependency Conflicts:** Use a virtual environment to prevent package conflicts.

---

## License
This project is licensed under the **MIT License**.

---
## Citing the project

To cite this repository in publications:

```bibtex
@misc{GUARDIAN-EYE.AI,
  author = {SHASWATSINGH3101,Siddharth-sahu-21, Nikhilverma-codes},
  title = {GUARDIAN-EYE.AI},
  year = {2025},
  howpublished = {\url{https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI}},
  note = {GitHub repository},
}
```
---

## Contact
For inquiries or support, connect via:
- 💬 **Discord:** shaswat_singh
