import os
import time
import ADS1x15
from core.logger import Logger

ADS = ADS1x15.ADS1115(1, 0x48)

class ADCController:
    def __init__(self, i2c_bus=1, address=0x48):
        self.logger = Logger(self.__class__.__name__).get_logger()
        self.logger.info("Initializing ADC Controller")
        self.ADS = ADS1x15.ADS1115(i2c_bus, address)
        self.ADS.setGain(self.ADS.PGA_4_096V)
        self.ADS.setDataRate(self.ADS.DR_ADS111X_128)
        self.ADS.setMode(self.ADS.MODE_CONTINUOUS)

    def read_voltage(self, channel=0):
        try:
            self.ADS.requestADC(channel)
            raw = self.ADS.getValue()
            voltage = self.ADS.toVoltage(raw)
            self.logger.debug(f"Channel {channel} raw value: {raw}, voltage: {voltage:.3f} V")
            return voltage
        except Exception as e:
            self.logger.error(f"Error reading voltage from channel {channel}: {e}")
            return None

if __name__ == "__main__":
    adc = ADCController()
    print(os.path.basename(__file__))
    print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.__version__))

    while True:
        voltage = adc.read_voltage()
        print("{0:.3f} V".format(voltage))
        time.sleep(1)