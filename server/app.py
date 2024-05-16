import time
import cv2
import base64
import socketio
import psutil
from modules.camera import camera

sio = socketio.Client()

connected_namespaces = {}

def send_frames():
    print("Sending frames to server.")
    camera.start()
    time.sleep(2)

    try: 
        while True:
            frame = camera.get_frame()
            _, buffer = cv2.imencode('.jpg', frame)  # Compress frame to JPEG
            frame_bytes = buffer.tobytes()  # Convert to bytes
            client_sendtime = time.time()

            data = {
                'frame': base64.b64encode(frame_bytes).decode('utf-8'),
                'client_sendtime': client_sendtime
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
    connected_namespaces['/debrisx'] = True
    sio.emit("start_latency_test", {'start_test': True}, namespace="/debrisx")
    send_frames()

@sio.event(namespace='/debrisx')
def disconnect():
    print("Disconnected from server on namespace /debrisx")

@sio.event(namespace='/debrisx')
def test_latency(data):
    if connected_namespaces['/debrisx']:
        print("Latency test received.")
        sio.emit('latency_response', {
            'server_time': data['server_time']
        }, namespace='/debrisx')

@sio.event(namespace='/debrisx')
def frame_latency(data):
    current_time = time.time()
    latency = round((current_time - data['client_sendtime']) * 1000, 1)
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    print(f"Frame Latency: {latency} ms | Cpu Usage: {cpu_usage}% | Memory Usage: {memory_usage}%")
