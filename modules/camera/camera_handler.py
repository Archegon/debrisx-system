from picamera2 import Picamera2
import time
import io

def take_still_image():
    camera = Picamera2()
    
    # Use a suitable configuration for still images or low-resolution streaming
    camera_config = camera.create_still_configuration()
    camera.configure(camera_config)
    camera.start()

    try:
        # Allow camera some time to adjust to conditions
        time.sleep(2)
        stream = io.BytesIO()
        
        # Request a JPEG capture
        camera.capture_file(stream, format='jpeg')
        stream.seek(0)
        frame = stream.read()

        # Reset stream for next capture
        stream.seek(0)
        stream.truncate()
        
        return frame

    finally:
        camera.stop()

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
            
            yield frame

    finally:
        camera.stop()

