import serial
import time

def read_gps():
    # Open serial port
    ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)  # Change to /dev/ttyAMA0 if needed
    
    try:
        while True:
            # Read a line from the GPS module
            line = ser.readline().decode('ascii', errors='replace')
            print(line.strip())
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    read_gps()
