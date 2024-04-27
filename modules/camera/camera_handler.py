from picamera2 import Picamera2
import time
import io

class Camera:
    def __init__(self):
        self.camera = Picamera2()
        self.stream = io.BytesIO()
        self.started = False

    def use_still_config(self):
        if self.started:
            self.stop()

        camera_config = self.camera.create_still_configuration()
        camera_config["main"]["size"] = (640, 480)
        self.camera.configure(camera_config)

    def use_video_config(self):
        camera_config = self.camera.create_video_configuration()
        camera_config["main"]["format"] = "YUV420"  # Use a suitable format for video
        camera_config["main"]["size"] = (640, 480)    # Set desired resolution
        self.camera.configure(camera_config)

    def start(self):
        self.camera.start()
        self.started = True

    def stop(self):
        self.camera.stop()
        self.started = False

    def take_still_image(self):
        self.use_still_config()
        self.start()

        try:
            time.sleep(2)
            self.camera.capture_file(self.stream, format='jpeg')
            self.stream.seek(0)
            frame = self.stream.read()
            return frame
        finally:
            self.stop()

