import time
from server.app import sio

DESKTOP_SERVER_IP = 'http://192.168.1.95:8080/debrisx'
LAPTOP_SERVER_IP = 'http://192.168.1.68:8080/debrisx'

if __name__ == '__main__':
    sio.connect(DESKTOP_SERVER_IP, transports=['websocket'])
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping client.")
        sio.disconnect()