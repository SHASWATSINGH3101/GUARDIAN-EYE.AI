![image (3)](https://github.com/SHASWATSINGH3101/GUARDIAN-EYE.AI/blob/main/assets/oie_jpg.png)


# GUARDIAN-EYE.AI

## Overview
**Guardian-Eye.AI** is an AI-powered surveillance system designed to enhance public safety by detecting violent activities in real-time. Using **computer vision and deep learning**, this system integrates with existing surveillance infrastructure to identify threats, send alerts, and enable **rapid response** to critical incidents.

## Key Features
✅ **Real-Time Violence Detection** – Uses **YOLO** (You Only Look Once) for high-speed and accurate detection.  
✅ **FastAPI-Powered Backend** – Ensures a **lightweight, efficient API** for web and mobile integration.  
✅ **Live Video Streaming** – Streams processed video with detected threats **overlaid on the feed**.  
✅ **Incident Logging** – Automatically records **date, time, severity, and detection confidence** for review.  
✅ **Automated Alerts** – Sends **real-time alerts via Telegram & emergency calls (Millis AI/Twilio)**.  
✅ **Configurable Settings** – Users can **adjust alert thresholds, detection confidence, and contact details**.  
✅ **Web Dashboard (HTMX + FastAPI)** – Provides a responsive UI with **live status updates**.  

---

## Installation & Setup

### **Prerequisites**
Ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/guardian-eye.ai.git
cd guardian-eye.ai
```

### **2️⃣ Set Up a Virtual Environment** (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
To avoid exposing sensitive credentials, create a `.env` file and add:
```ini
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
MILLIS_API_KEY = your Api key
MILLIS_AGENT_ID = your agent ID
TO_PHONE_NUMBER = your emergency number
```

### **5️⃣ Run the Application**
```bash
uvicorn main_fastapi:app --reload
```

---

## Usage

### **1️⃣ Access the Web Dashboard**
Once the server is running, open a browser and visit:
```
http://127.0.0.1:8000/
```

### **2️⃣ Key Endpoints**
| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard showing live detection and alerts |
| `/video_feed` | Streams the processed video feed |
| `/status_view` | Returns the current detection status (HTMX) |
| `/incidents` | Displays incident history |
| `/settings` | Allows users to update system settings |
| `/update_settings` | API to modify alert thresholds, confidence, etc. |

### **3️⃣ Trigger Alerts**
- If violence is detected **above the threshold**, Guardian-Eye.AI will:
  - **Save a video clip** of the incident.
  - **Send a Telegram alert** with details.
  - **Trigger an emergency call** if enabled.

---

## Roadmap / Future Enhancements 🚀
🔹 **Multi-Camera Support** – Monitor multiple locations simultaneously.  
🔹 **Face Recognition** – Identify known offenders.  
🔹 **Cloud Storage Integration** – Store incident videos securely online.  
🔹 **WebSockets for Real-Time Updates** – Reduce polling and improve UI performance.  
🔹 **Mobile App** – Extend functionality to mobile devices.  

---

## Contributing
We welcome contributions! If you'd like to improve Guardian-Eye.AI, follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request!

---

## License
This project is licensed under the **MIT License**. Feel free to modify and distribute!

---

## Contact
For any inquiries or support, reach out via:
📧 Email: your.email@example.com  
💬 Telegram: @yourhandle  

