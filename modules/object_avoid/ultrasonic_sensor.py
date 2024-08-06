from gpiozero import DistanceSensor
import asyncio
from signal import pause

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, max_distance=4):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=max_distance)
        print(f"Ultrasonic sensor initialized on trigger pin {trigger_pin} and echo pin {echo_pin}")

    async def distance(self):
        distance = self.sensor.distance * 100  # convert to cm
        print(f"Distance measured: {distance:.1f} cm")
        return distance

    async def measure_continuously(self, interval=1, label=None):
        try:
            while True:
                print(f"Starting distance measurement for {label}")
                dist = await self.distance()

                label_text = f"{label}: " if label else ""
                print(f"{label_text}Measured Distance = {dist:.1f} cm")
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            pass

if __name__ == '__main__':
    try:
        sensor1 = UltrasonicSensor(trigger_pin=27, echo_pin=17)
        sensor2 = UltrasonicSensor(trigger_pin=22, echo_pin=10)

        loop = asyncio.get_event_loop()
        tasks = [
            sensor1.measure_continuously(label="Sensor 1"),
            sensor2.measure_continuously(label="Sensor 2")
        ]
        print("Starting asyncio loop")

        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        print("Measurement stopped by User")
