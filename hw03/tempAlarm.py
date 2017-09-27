#!/usr/bin/env python3
# Read a TMP101 sensor, set off console alarm at requested temp

import smbus, time, sys
import Adafruit_BBIO.GPIO as GPIO

# check command line arguments
if len(sys.argv) == 2 :
   alarm = int((float(sys.argv[1])-32)*5/9)
   print("You have requested alarm at " + sys.argv[1] + " degrees F")
else:
     print("You have not requested a temperature so 84 degrees F will be used")
     alarm = 29

# define GPIO values
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
bus.write_byte_data(tmp1, 1, 0x80) #default value was 0x80
bus.write_byte_data(tmp1, 2, alarm)
bus.write_byte_data(tmp1, 3, alarm)
bus.write_byte_data(tmp2, 1, 0x80) #default value was 0x80
bus.write_byte_data(tmp2, 2, alarm)
bus.write_byte_data(tmp2, 3, alarm)

while True:
    # read temp
    temp1 = bus.read_byte_data(tmp1, 0)
    temp2 = bus.read_byte_data(tmp2, 0)
    # check alarm values
    if GPIO.input(TA1) == 0:
       GPIO.output(LED1,1)
       temp1f = temp1*9/5+32
       print("Alarm one triggered at ", temp1f, " degrees F")
    else:
       GPIO.output(LED1,0)
       
    if GPIO.input(TA2) == 0:
       GPIO.output(LED2,1)
       temp2f = temp2*9/5+32
       print("Alarm two triggered at ", temp2f," degrees F")
    else:
       GPIO.output(LED2,0)
       
    time.sleep(0.25)
