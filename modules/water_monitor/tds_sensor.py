from modules.adc.adc_controller import ADCController
from core.logger import Logger

class TDSSensor:
    def __init__(self, adc_channel=0):
        self.logger = Logger(self.__class__.__name__).get_logger()
        self.adc = ADCController()
        self.adc_channel = adc_channel
        self.logger.info("TDS Sensor initialized")

    def read_tds(self):
        try:
            voltage = self.adc.read_voltage(self.adc_channel)
            if voltage is None:
                self.logger.error("Failed to read voltage from ADC")
                return None

            # Convert voltage to TDS value
            tds_value = self.voltage_to_tds(voltage)
            self.logger.debug(f"Voltage: {voltage:.3f} V, TDS: {tds_value:.2f} ppm")
            return tds_value
        except Exception as e:
            self.logger.error(f"Error reading TDS: {e}")
            return None

    def voltage_to_tds(self, voltage):
        # Not done
        conversion_factor = 500.0
        tds_value = voltage * conversion_factor
        return tds_value

    async def cleanup(self):
        await self.adc.cleanup()
        self.logger.info("Cleaned up ADC settings.")

if __name__ == "__main__":
    tds_sensor = TDSSensor()
    try:
        while True:
            tds = tds_sensor.read_tds()
            print(f"TDS: {tds:.2f} ppm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        asyncio.run(tds_sensor.cleanup())
