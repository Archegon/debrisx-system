import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Motor Pins
EN1_PIN = 23
M1_POS_PIN = 19
M1_NEG_PIN = 26

# Set GPIO direction (IN / OUT)
GPIO.setup(EN1_PIN, GPIO.OUT)
GPIO.setup(M1_POS_PIN, GPIO.OUT)
GPIO.setup(M1_NEG_PIN, GPIO.OUT)

pwm = GPIO.PWM(EN1_PIN, 100)  # Setting PWM at 100 Hz
pwm.start(100)

def test():
    print("Testing in progress...")
    GPIO.output(M1_POS_PIN, True)  # Motor moves in one direction
    GPIO.output(M1_NEG_PIN, False)

try:
    while True:
        test()
        time.sleep(1)  # run the motor for 1 second
        

except KeyboardInterrupt:
    print("Exiting program")
finally:
    pwm.stop()  # Stop the PWM
    GPIO.cleanup()  # This ensures all GPIO pins are freed
