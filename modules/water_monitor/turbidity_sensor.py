import asyncio
import time
from modules.adc.adc_controller import ADCController
from core.logger import Logger

class TurbiditySensor:
    def __init__(self, adc_channel=2):
        self.logger = Logger(self.__class__.__name__).get_logger()
        self.adc = ADCController()
        self.adc_channel = adc_channel
        self.logger.info("Turbidity Sensor initialized")

    def read_turbidity(self):
        try:
            voltage = self.adc.read_voltage(self.adc_channel)
            if voltage is None:
                self.logger.error("Failed to read voltage from ADC")
                return None

            # Convert voltage to turbidity value
            turbidity_value = self.voltage_to_turbidity(voltage)
            self.logger.debug(f"Voltage: {voltage:.3f} V, Turbidity: {turbidity_value:.2f} NTU")
            return turbidity_value
        except Exception as e:
            self.logger.error(f"Error reading turbidity: {e}")
            return None

    def voltage_to_turbidity(self, voltage):
        # Convert voltage to turbidity value based on the sensor's characteristics
        # Assuming that the sensor outputs a voltage range of 0-4.5V corresponding to 0-3000 NTU
        max_voltage = 4.5
        max_turbidity = 3000

        # Linear mapping from voltage to turbidity
        turbidity_value = (voltage / max_voltage) * max_turbidity
        return turbidity_value

    async def cleanup(self):
        await self.adc.cleanup()
        self.logger.info("Cleaned up ADC settings.")

if __name__ == "__main__":
    turbidity_sensor = TurbiditySensor()
    try:
        while True:
            turbidity = turbidity_sensor.read_turbidity()
            if turbidity is not None:
                print(f"Turbidity: {turbidity:.2f} NTU")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        asyncio.run(turbidity_sensor.cleanup())
