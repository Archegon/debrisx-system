import numpy as np
import cv2
import time
from picamera2 import Picamera2
from threading import Thread, Condition

class PiCameraStream:
    def __init__(self, resolution=(640, 480), framerate=24):
        self.camera = Picamera2()

        # Set the framerate
        self.frame_duration = 1 / framerate

        self.config = self.camera.create_preview_configuration(main={"size": resolution})
        self.camera.configure(self.config)
        self.frame = None
        self.streaming = False
        self.last_capture_time = 0
        self.condition = Condition()

    def start(self):
        print("Camera started.")
        if not self.streaming:
            self.streaming = True
            self.camera.start()
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = True  # Ensure the thread will exit with the program
            self.thread.start()

    def update(self):
        while self.streaming:
            current_time = time.time()
            if current_time - self.last_capture_time >= self.frame_duration:
                buffer = self.camera.capture_array()
                with self.condition:
                    self.frame = cv2.cvtColor(np.array(buffer), cv2.COLOR_BGR2RGB)
                    self.frame = cv2.flip(self.frame, 0)
                    self.condition.notify_all()

                self.last_capture_time = time.time()
            time.sleep(0.0001)  # Add a small sleep to prevent high CPU usage

    def get_frame(self):
        with self.condition:
            if self.frame is None:
                self.condition.wait(timeout=self.frame_duration)  # Add a timeout to prevent deadlocks
            frame = self.frame.copy() if self.frame is not None else None
            self.frame = None
        return frame
    
    def stop(self):
        self.streaming = False
        self.thread.join()
        self.camera.stop()
