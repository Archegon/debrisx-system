import time
import socketio
import cv2
import base64
from modules.camera import camera

sio = socketio.Client()

def send_frames():
    print("Sending frames to server.")
    camera.start()
    try:
        time.sleep(2)  # Allow camera some time to adjust
        while True:
            frame = camera.get_frame()
            _, buffer = cv2.imencode('.jpg', frame)  # Compress frame to JPEG
            frame_bytes = buffer.tobytes()  # Convert to bytes
            sio.emit('send_frame', {'frame': base64.b64encode(frame_bytes).decode('utf-8')}, namespace='/debrisx')  # Send as base64 encoded string
            time.sleep(0.0167)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping camera.")
    finally:
        camera.stop()
        sio.disconnect()

@sio.event(namespace='/debrisx')
def connect():
    print("Connected to the server on namespace /debrisx.")
    send_frames()

@sio.event(namespace='/debrisx')
def disconnect():
    print("Disconnected from server on namespace /debrisx")