import pigpio
import asyncio
from core.logger import Logger

class AngleOutOfRangeError(Exception):
    """Exception raised when the angle is out of the allowed range."""
    pass

class ServoController:
    def __init__(self, pin, min_pulse_width=500, max_pulse_width=2500):
        self.pi = pigpio.pi()
        self.pin = pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.range = max_pulse_width - min_pulse_width
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.logger = Logger(self.__class__.__name__).get_logger()

    async def set_angle(self, angle):
        if angle < 0 or angle > 180:
            self.logger.error(f"Angle {angle} is out of range. Must be between 0 and 180 degrees.")
            raise AngleOutOfRangeError(f"Angle {angle} is out of range. Must be between 0 and 180 degrees.")
        
        # Convert angle (0-180) to pulse width
        pulse_width = self.min_pulse_width + (angle / 180) * self.range
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)
        await asyncio.sleep(0.1)
        self.logger.info(f"Set angle to {angle} degrees (pulse width: {pulse_width} microseconds)")

    async def sweep(self, start_angle=0, end_angle=180, delay=0.05):
        try:
            for angle in range(start_angle, end_angle + 1):  # Move from start to end angle
                await self.set_angle(angle)
                await asyncio.sleep(delay)
            for angle in range(end_angle, start_angle - 1, -1):  # Move back from end to start angle
                await self.set_angle(angle)
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            pass

    async def cleanup(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)  # Turn off the servo
        self.pi.stop()
        self.logger.info("Cleaned up GPIO settings and stopped the servo.")

if __name__ == "__main__":
    servo = ServoController(25)

    print("Starting servo test")

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(servo.sweep())
    except KeyboardInterrupt:
        print("Program stopped")
    except AngleOutOfRangeError as e:
        print(e)
    finally:
        loop.run_until_complete(servo.cleanup())