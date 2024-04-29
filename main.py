from server.app import sio

DESKTOP_SERVER_IP = 'http://192.168.1.95:8080'
LAPTOP_SERVER_IP = 'http://192.168.1.68:8080'
LAPTOP_HOTSPOT_SERVER_IP = 'http://192.168.237.96:8080'

if __name__ == '__main__':
    sio.connect(LAPTOP_HOTSPOT_SERVER_IP, transports=['websocket'], namespaces=['/debrisx'])

    try:
        sio.wait()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping client.")
        sio.disconnect()