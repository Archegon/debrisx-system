import time
import cv2
import base64
from modules.camera import camera
from .app import sio

def send_frames():
    print("Sending frames to server.")
    camera.start()
    time.sleep(2)  # Allow camera some time to adjust

    try: 
        while True:
            frame = camera.get_frame()
            
            if frame is None:
                continue
            
            _, buffer = cv2.imencode('.jpg', frame)  # Compress frame to JPEG
            frame_bytes = buffer.tobytes()  # Convert to bytes

            data = {
                'frame': base64.b64encode(frame_bytes).decode('utf-8'),
            }
            sio.emit('send_frame', data, namespace='/debrisx')  # Send as base64 encoded string
    except KeyboardInterrupt:
        print("Interrupted by user, stopping camera.")
    finally:
        camera.stop()
        sio.disconnect()

@sio.event(namespace='/debrisx')
def connect():
    print("Connected to the server on namespace /debrisx.")

@sio.event(namespace='/debrisx')
def disconnect():
    print("Disconnected from server on namespace /debrisx")

@sio.event(namespace='/debrisx')
def ready(data):
    print(data['message'])
    sio.emit("start_latency_test", {'start_test': True}, namespace="/debrisx")
    send_frames()

@sio.event(namespace='/debrisx')
def test_latency(data):
    print("Latency test received.")
    client_time = time.time()
    sio.emit('latency_response', {
        'client_time': client_time,
        'server_time': data['server_time']
    }, namespace='/debrisx')