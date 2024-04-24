from picamera2 import Picamera2

def capture_image():
    picam2 = Picamera2()
    # Use a simple configuration that doesn't involve DRM
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)
    picam2.start()
    picam2.capture_file("test.jpg")

if __name__ == "__main__":
    capture_image()
