import time
import socketio
import cv2
import base64
from modules.camera import camera

sio = socketio.Client()

def send_frames():
    camera.start()
    try:
        time.sleep(2)  # Allow camera some time to adjust
        while True:
            frame = camera.get_frame()
            _, buffer = cv2.imencode('.jpg', frame)  # Compress frame to JPEG
            frame_bytes = buffer.tobytes()  # Convert to bytes
            sio.emit('send_frame', {'frame': base64.b64encode(frame_bytes).decode('utf-8')})  # Send as base64 encoded string
            time.sleep(0.06)
    except KeyboardInterrupt:
        camera.stop()
    finally:
        camera.stop()
        sio.disconnect()

@sio.event
def connect():
    print("Connected to the server.")
    send_frames()

@sio.event
def disconnect():
    print("Disconnected from server")