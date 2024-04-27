import time
from server.app import sio

SERVER_IP = 'http://192.168.1.95:8080'

if __name__ == '__main__':
    sio.connect(SERVER_IP)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping client.")
        sio.disconnect()