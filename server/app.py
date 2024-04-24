from flask import Flask, Response
from picamera2 import Picamera2, Preview
import time
import io

app = Flask(__name__)

def generate_frames():
    camera = Picamera2()
    
    # Use a suitable configuration for still images or low-resolution streaming
    camera_config = camera.create_still_configuration()
    camera.configure(camera_config)
    camera.start()

    try:
        # Allow camera some time to adjust to conditions
        time.sleep(2)
        
        # Continuously capture images
        while True:
            stream = io.BytesIO()
            # Request a JPEG capture
            camera.capture_file(stream, format='jpeg')
            stream.seek(0)
            frame = stream.read()

            # Reset stream for next capture
            stream.seek(0)
            stream.truncate()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
