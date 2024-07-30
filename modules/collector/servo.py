import pigpio
from time import sleep

class ExtendedServo:
    def __init__(self, pi, pin, min_pulse_width=500, max_pulse_width=2500):
        self.pi = pi
        self.pin = pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.range = max_pulse_width - min_pulse_width
        self.pi.set_mode(self.pin, pigpio.OUTPUT)

    def set_angle(self, angle):
        # Convert angle (0-180) to pulse width
        pulse_width = self.min_pulse_width + (angle / 180) * self.range
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)

# Initialize pigpio and the extended servo with GPIO pin 25
pi = pigpio.pi()
servo = ExtendedServo(pi, 25)

print("Starting servo test")

try:
    while True:
        for angle in range(180, -1, -1):  # Move back from 180 to 0 degrees
            servo.set_angle(angle)
            sleep(0.05)  # Increase the delay to smooth the movement
        for angle in range(0, 181, 1):  # Move from 0 to 180 degrees
            servo.set_angle(angle)
            sleep(0.05)  # Increase the delay to smooth the movement
except KeyboardInterrupt:
    print("Program stopped")
finally:
    servo.pi.set_servo_pulsewidth(servo.pin, 0)  # Turn off the servo
    pi.stop()
