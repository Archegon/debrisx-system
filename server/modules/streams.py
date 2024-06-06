import io
import threading
import time
from fastapi import APIRouter
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform

api_router = APIRouter()

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def get_frame(self):
        with self.condition:
            self.condition.wait_for(lambda: self.frame is not None)
            frame = self.frame
            self.frame = None
        return frame

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class PiCameraStream:
    def __init__(self, resolution=(640, 480), framerate=12):
        self.resolution = resolution
        self.fps = framerate
        self.output = StreamingOutput()
        self.camera = Picamera2()
        self.stop_stream = True
        self.configure_camera()
        self.frame_count = 0
        self.start_time = None

    def configure_camera(self):
        frame_duration = int((1 / self.fps) * 1000000)  # Convert to microseconds and cast to int
        self.config = self.camera.create_video_configuration(
            main={"size": self.resolution},
            transform=Transform(vflip=True, hflip=True),
            controls={"FrameDurationLimits": [frame_duration, frame_duration]}
        )
        self.camera.configure(self.config)

    def start(self):
        if self.stop_stream:
            self.stop_stream = False
            print("Streaming started")
            self.start_time = time.time()
            self.frame_count = 0
            self.camera.start_recording(JpegEncoder(), FileOutput(self.output))

    def stop(self):
        if self.stop_stream:
            self.camera.stop_recording()
            print("Streaming stopped")
            self.stop_stream = True

    def generate_frames(self):
        try:
            while not self.stop_stream:
                frame = self.output.get_frame()

                if frame is None:
                    continue

                self.frame_count += 1
                self.calculate_and_print_fps()

                yield (b'--FRAME\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + f'{len(frame)}'.encode() + b'\r\n'
                       b'\r\n' + frame + b'\r\n')
        finally:
            # Cleanup when the client disconnects
            self.stop()

    def calculate_and_print_fps(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1:
            fps = self.frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            self.frame_count = 0
            self.start_time = time.time()