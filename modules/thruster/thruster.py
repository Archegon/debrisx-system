import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Motor1 = {'EN': 26, 'input1': 20, 'input2': 21}
Motor2 = {'EN': 16, 'input1': 19, 'input2': 13}

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)
EN2 = GPIO.PWM(Motor2['EN'], 100)
EN1.start(0)
EN2.start(0)

try:
    while True:
        print("FORWARD MOTION")

        # Ramp up the duty cycle from 0% to 100%
        for dc in range(0, 101, 5):  # Increment by 5% steps
            EN1.ChangeDutyCycle(dc)
            EN2.ChangeDutyCycle(dc)
            GPIO.output(Motor1['input1'], GPIO.HIGH)
            GPIO.output(Motor1['input2'], GPIO.LOW)
            GPIO.output(Motor2['input1'], GPIO.HIGH)
            GPIO.output(Motor2['input2'], GPIO.LOW)
            sleep(0.05)  # Short delay for smooth ramp up

        # Hold at 100% for a moment
        sleep(1)

        # Ramp down the duty cycle from 100% to 0%
        for dc in range(100, -1, -5):  # Decrement by 5% steps
            EN1.ChangeDutyCycle(dc)
            EN2.ChangeDutyCycle(dc)
            GPIO.output(Motor1['input1'], GPIO.HIGH)
            GPIO.output(Motor1['input2'], GPIO.LOW)
            GPIO.output(Motor2['input1'], GPIO.HIGH)
            GPIO.output(Motor2['input2'], GPIO.LOW)
            sleep(0.05)  # Short delay for smooth ramp down

        # Hold at 0% for a moment
        sleep(1)

except KeyboardInterrupt:
    # Cleanup GPIO settings before exiting
    EN1.stop()
    EN2.stop()
    GPIO.cleanup()
