import numpy as np
import cv2
import time
from picamera2 import Picamera2
from threading import Thread, Condition

class PiCameraStream:
    def __init__(self, resolution=(640, 480), framerate=6):
        self.camera = Picamera2()

        # Set the framerate
        self.frame_duration = 1 / framerate

        self.config = self.camera.create_video_configuration(main={"size": resolution})
        print(self.config)
        self.camera.configure(self.config)
        self.frame = None
        self.streaming = False
        self.last_capture_time = 0.0
        self.condition = Condition()

    def start(self):
        print("Camera started.")
        if not self.streaming:
            self.streaming = True
            self.camera.start()
            self.thread = Thread(target=self.update, args=())
            self.thread.start()

    def update(self):
        while self.streaming:
            if time.time() - self.last_capture_time >= self.frame_duration:
                buffer = self.camera.capture_array()
                with self.condition:
                    self.frame = cv2.cvtColor(np.array(buffer), cv2.COLOR_BGR2RGB)
                    self.frame = cv2.flip(self.frame, 0)
                    self.condition.notify_all()

                self.last_capture_time = time.time()

    def get_frame(self):
        with self.condition:
            self.condition.wait()
            frame = self.frame.copy()
            self.frame = None
        return frame
    
    def stop(self):
        self.streaming = False
        self.thread.join()
        self.camera.stop()
