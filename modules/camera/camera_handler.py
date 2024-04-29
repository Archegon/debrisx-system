import numpy as np
import cv2
from picamera2 import Picamera2
from threading import Thread, Condition

class PiCameraStream:
    def __init__(self, resolution=(640, 480)):
        self.camera = Picamera2()
        self.config = self.camera.create_preview_configuration(main={"size": resolution})
        self.camera.configure(self.config)
        self.frame = None
        self.streaming = False
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
            buffer = self.camera.capture_array()
            with self.condition:
                self.frame = cv2.cvtColor(np.array(buffer), cv2.COLOR_BGR2RGB)
                self.frame = cv2.flip(self.frame, 0)
                self.condition.notify_all()

    def get_frame(self):
        with self.condition:
            self.condition.wait()
            frame = self.frame.copy()
        return frame
    
    def stop(self):
        self.streaming = False
        self.thread.join()
        self.camera.stop()
