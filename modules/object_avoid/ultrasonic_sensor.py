import RPi.GPIO as GPIO
import asyncio
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    async def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
 
        # set Trigger after 0.01ms to LOW
        await asyncio.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
 
        StartTime = time.time()
        StopTime = time.time()
 
        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()
 
        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()
 
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
 
        return distance

    async def cleanup(self):
        GPIO.cleanup()

    async def measure_continuously(self, interval=1):
        try:
            while True:
                dist = await self.distance()
                print(f"Measured Distance = {dist:.1f} cm")
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            pass

if __name__ == '__main__':
    try:
        sensor = UltrasonicSensor(trigger_pin=27, echo_pin=17)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(sensor.measure_continuously())
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        loop.run_until_complete(sensor.cleanup())
