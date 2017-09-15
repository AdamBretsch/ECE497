#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
import time
bus = smbus.SMBus(1)
address = 0x48
# 0 - Temp
# 1 - config - set bit 1 = 1 for interrupt mode
# 2 - Tlow
# 3 - Thigh
while True:
    temp = bus.read_byte_data(address, 0)
    print (temp, end="\r")
    time.sleep(0.25)
