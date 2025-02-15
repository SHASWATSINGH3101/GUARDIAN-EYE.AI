
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

### 6️⃣ Using Twilio and Millis AI
This project comes with trial account credentials for **Twilio** and **Millis AI** to get you started quickly. These keys are included in the configuration but are limited to trial credits.

### ⚠️ **Note:**
These are trial account credentials with limited credits. For more control or if the trial credits expire, create your own accounts:
- [Twilio Account Setup](https://www.twilio.com/try-twilio)
- [Millis AI Account Setup](https://www.millis.ai/)

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
