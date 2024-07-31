import asyncio
import time
import pigpio
from core.logger import Logger
from modules.adc.adc_controller import ADCController
from modules.collector.servo import ServoController
from modules.object_avoid.ultrasonic_sensor import UltrasonicSensor
from modules.thruster import MotorController
from modules.water_monitor.tds_sensor import TDSSensor
from modules.water_monitor.turbidity_sensor import TurbiditySensor

class RCBoatController:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get_logger()
        self.logger.info("Initializing RC Boat Controller")
        self.pi = pigpio.pi()

        # Initialize components
        self.servo_controller = ServoController(pi=self.pi, pin=25)
        self.ultrasonic_sensor_1 = UltrasonicSensor(trigger_pin=27, echo_pin=17)
        self.ultrasonic_sensor_2 = UltrasonicSensor(trigger_pin=22, echo_pin=10)
        self.tds_sensor = TDSSensor(adc_channel=0)
        self.turbidity_sensor = TurbiditySensor(adc_channel=1)
        self.motor_controller = MotorController()

    async def read_sensors(self):
        try:
            distance_1 = await self.ultrasonic_sensor_1.distance()
            distance_2 = await self.ultrasonic_sensor_2.distance()
            tds = self.tds_sensor.read_tds()
            turbidity = self.turbidity_sensor.read_turbidity()
            self.logger.info(f"Distance_1: {distance_1:.2f} cm, Distance_2: {distance_2:.2f} cm, TDS: {tds:.2f} ppm, Turbidity: {turbidity:.2f} NTU")
            return distance_1, distance_2, tds, turbidity
        except Exception as e:
            self.logger.error(f"Error reading sensors: {e}", exc_info=True)
            return None, None, None

    async def control_servo(self, angle):
        try:
            await self.servo_controller.set_angle(angle)
            self.logger.info(f"Servo angle set to {angle}")
        except Exception as e:
            self.logger.error(f"Error controlling servo: {e}", exc_info=True)

    async def cleanup(self):
        await self.servo_controller.cleanup()
        await self.ultrasonic_sensor.cleanup()
        await self.tds_sensor.cleanup()
        await self.turbidity_sensor.cleanup()
        self.logger.info("Cleaned up all components.")

if __name__ == "__main__":
    rc_boat_controller = RCBoatController()

    async def main():
        try:
            while True:
                await rc_boat_controller.read_sensors()
                await rc_boat_controller.control_servo(90)  # Example: set servo to 90 degrees
                await asyncio.sleep(1)  # Delay between readings and control actions
        except KeyboardInterrupt:
            print("Program stopped by User")
        except Exception as e:
            rc_boat_controller.logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            await rc_boat_controller.cleanup()

    asyncio.run(main())
