import time
from modules.camera import camera

camera.start()
print("Camera working")
time.sleep(5)
camera.stop()