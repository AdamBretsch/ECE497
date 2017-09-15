#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
import time
import Adafruit_BBIO.GPIO as GPIO

LED1  ="RED"
LED2  ="GREEN" #GP1
TA1   ="GP1_3"
TA2   ="GP1_4"

# Set the GPIO pins:
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(TA1, GPIO.IN)
GPIO.setup(TA2, GPIO.IN)
bus = smbus.SMBus(1)
tmp1 = 0x48
tmp2 = 0x4a
# 0 - Temp
# 1 - config - set bit 1 = 1 for interrupt mode
# 2 - Tlow
# 3 - Thigh
bus.write_byte_data(tmp1, 1, 0x81) #default value was 0x80
bus.write_byte_data(tmp1, 2, 30)
bus.write_byte_data(tmp1, 3, 30)
bus.write_byte_data(tmp2, 1, 0x81) #default value was 0x80
bus.write_byte_data(tmp2, 2, 29)
bus.write_byte_data(tmp2, 3, 29)

while True:
    temp1 = bus.read_byte_data(tmp1, 0)
    temp2 = bus.read_byte_data(tmp2, 0)
    print (temp1,temp2,  end="\r")
   # if GPIO.input(TA1) == 0:
    #  print("Alarm one triggered at ", temp1)
   # if GPIO.input(TA2) == 0:
    #  print("Alarm two triggered at ", temp2)
    time.sleep(0.25)
