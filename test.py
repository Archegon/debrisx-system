from server_2.app import app, output

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform

DESKTOP_SERVER_IP = 'http://192.168.1.95:8080'
LAPTOP_SERVER_IP = 'http://192.168.1.68:8080'
LAPTOP_HOTSPOT_SERVER_IP = 'http://192.168.237.96:8080'

FPS_12 = (83333, 83333)
FPS_30 = (33333, 33333)

if __name__ == '__main__':
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (640, 480)},
                                               transform=Transform(vflip=True, hflip=True),
                                               controls={
                                                   "FrameDurationLimits": FPS_12
                                               })
    picam2.configure(config)
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        picam2.stop_recording()