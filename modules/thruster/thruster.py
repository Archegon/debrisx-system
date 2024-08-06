from gpiozero import Motor
from time import sleep
from core.logger import Logger

class MotorController:
    def __init__(self):
        # Initialize motors
        self.motor1 = Motor(forward=20, backward=13, enable=26, pwm=True)  # Motor 1 pins
        self.motor2 = Motor(forward=19, backward=21, enable=16, pwm=True)  # Motor 2 pins
        print("Motors initialized")

    def cleanup(self):
        # Stop the motors and clean up resources
        self.motor1.stop()
        self.motor2.stop()
        print("Motors cleaned up")

    def forward(self, speed=1, duration=1):
        print("FORWARD MOTION")
        self.motor1.forward(speed)
        self.motor2.forward(speed)
        sleep(duration)
        self.stop()

    def backward(self, speed=1, duration=1):
        print("BACKWARD MOTION")
        self.motor1.backward(speed)
        self.motor2.backward(speed)
        sleep(duration)
        self.stop()

    def turn_left(self, speed=1, duration=1):
        print("TURNING LEFT")
        self.motor1.backward(speed)
        self.motor2.forward(speed)
        sleep(duration)
        self.stop()

    def turn_right(self, speed=1, duration=1):
        print("TURNING RIGHT")
        self.motor1.forward(speed)
        self.motor2.backward(speed)
        sleep(duration)
        self.stop()

    def stop(self):
        print("Stopping motors")
        self.motor1.stop()
        self.motor2.stop()

if __name__ == "__main__":
    try:
        motor_controller = MotorController()
        
        motor_controller.forward(speed=1, duration=2)
        sleep(1)
        motor_controller.backward(speed=1, duration=2)
        sleep(1)
        motor_controller.turn_left(speed=1, duration=2)
        sleep(1)
        motor_controller.turn_right(speed=1, duration=2)
        
    except KeyboardInterrupt:
        pass
    finally:
        motor_controller.cleanup()
