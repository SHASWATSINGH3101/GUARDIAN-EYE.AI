from app.detection import main as detection_main
from pyngrok import ngrok
import threading

# Step 1: Start ngrok tunnel to expose Flask app
http_tunnel = ngrok.connect(5000)
print(f"Public URL: {http_tunnel.public_url}")

# Step 2: Start the detection script in a separate thread
detection_thread = threading.Thread(target=detection_main)
detection_thread.start()
