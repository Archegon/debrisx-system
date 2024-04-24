import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motor1 = {'EN': 19, 'input1': 20, 'input2': 26}
Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)
EN2 = GPIO.PWM(Motor2['EN'], 100)
EN1.start(0)
EN2.start(0)

while True:
    print ("FORWARD MOTION")
    EN1.ChangeDutyCycle(100)
    EN2.ChangeDutyCycle(100)
    GPIO.output(Motor1['input1'], GPIO.HIGH)
    GPIO.output(Motor1['input2'], GPIO.LOW)

    GPIO.output(Motor2['input1'], GPIO.HIGH)
    GPIO.output(Motor2['input2'], GPIO.LOW)
    sleep(0.1)