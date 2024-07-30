import os
import time
import ADS1x15

ADS = ADS1x15.ADS1115(1, 0x48)

print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.__version__))

ADS.setGain(ADS.PGA_4_096V)
ADS.setDataRate(ADS.DR_ADS111X_128)
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(0)                          # First read to trigger

while True :
    raw = ADS.getValue()
    print("{0:.3f} V".format(ADS.toVoltage(raw)))
    time.sleep(1)