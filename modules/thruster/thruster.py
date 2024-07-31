import RPi.GPIO as GPIO
from time import sleep

class MotorController:
    def __init__(self):
        self.Motor1 = {'EN': 26, 'input1': 20, 'input2': 21}
        self.Motor2 = {'EN': 16, 'input1': 19, 'input2': 13}
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for motor in [self.Motor1, self.Motor2]:
            GPIO.setup(motor['EN'], GPIO.OUT)
            GPIO.setup(motor['input1'], GPIO.OUT)
            GPIO.setup(motor['input2'], GPIO.OUT)

        self.EN1 = GPIO.PWM(self.Motor1['EN'], 100)
        self.EN2 = GPIO.PWM(self.Motor2['EN'], 100)
        self.EN1.start(0)
        self.EN2.start(0)

    def cleanup(self):
        self.EN1.stop()
        self.EN2.stop()
        GPIO.cleanup()

    def forward(self, speed=100, duration=1):
        print("FORWARD MOTION")
        self.set_motor_speed(speed)
        self.set_motor_direction(self.Motor1, GPIO.HIGH, GPIO.LOW)
        self.set_motor_direction(self.Motor2, GPIO.HIGH, GPIO.LOW)
        sleep(duration)
        self.stop()

    def backward(self, speed=100, duration=1):
        print("BACKWARD MOTION")
        self.set_motor_speed(speed)
        self.set_motor_direction(self.Motor1, GPIO.LOW, GPIO.HIGH)
        self.set_motor_direction(self.Motor2, GPIO.LOW, GPIO.HIGH)
        sleep(duration)
        self.stop()

    def turn_left(self, speed=100, duration=1):
        print("TURNING LEFT")
        self.set_motor_speed(speed)
        self.set_motor_direction(self.Motor1, GPIO.LOW, GPIO.HIGH)
        self.set_motor_direction(self.Motor2, GPIO.HIGH, GPIO.LOW)
        sleep(duration)
        self.stop()

    def turn_right(self, speed=100, duration=1):
        print("TURNING RIGHT")
        self.set_motor_speed(speed)
        self.set_motor_direction(self.Motor1, GPIO.HIGH, GPIO.LOW)
        self.set_motor_direction(self.Motor2, GPIO.LOW, GPIO.HIGH)
        sleep(duration)
        self.stop()

    def set_motor_speed(self, speed):
        self.EN1.ChangeDutyCycle(speed)
        self.EN2.ChangeDutyCycle(speed)

    def set_motor_direction(self, motor, input1_state, input2_state):
        GPIO.output(motor['input1'], input1_state)
        GPIO.output(motor['input2'], input2_state)

    def stop(self):
        self.EN1.ChangeDutyCycle(0)
        self.EN2.ChangeDutyCycle(0)
        self.set_motor_direction(self.Motor1, GPIO.LOW, GPIO.LOW)
        self.set_motor_direction(self.Motor2, GPIO.LOW, GPIO.LOW)

if __name__ == "__main__":
    try:
        motor_controller = MotorController()
        
        motor_controller.forward(speed=50, duration=2)
        sleep(1)
        motor_controller.backward(speed=50, duration=2)
        sleep(1)
        motor_controller.turn_left(speed=50, duration=2)
        sleep(1)
        motor_controller.turn_right(speed=50, duration=2)
        
    except KeyboardInterrupt:
        pass
    finally:
        motor_controller.cleanup()
