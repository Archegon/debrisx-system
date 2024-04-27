import time
import cv2
from flask import Flask, Response
from modules.camera import camera
from modules.object_detection.tensorflow_handler import process_image

app = Flask(__name__)

def generate_frames():
    camera.start()

    try:
        # Allow camera some time to adjust to conditions
        time.sleep(2)
        
        # Continuously capture images
        while True:
            frame = camera.get_frame()
            frame = process_image(frame)
            _, buffer = cv2.imencode('.jpg', frame)  # Encode frame as JPEG

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    except KeyboardInterrupt:
        camera.stop()
    finally:
        camera.stop()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Return a simple webpage with the video stream embedded
    return Response('<html><body><img src="/video_feed"></body></html>')
