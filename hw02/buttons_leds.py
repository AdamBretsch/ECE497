#!/usr/bin/env python3
import time
import Adafruit_BBIO.GPIO as GPIO

button1="GP0_6"  # GP0 for buttons
button2="GP0_5"
button3="GP0_4"
button4="GP0_3"


LED1   ="GREEN" #GP1 for leds
LED2   ="RED"
LED3   ="GP1_4"
LED4   ="GP1_3"

# Set the GPIO pins:
GPIO.setup(LED1,    GPIO.OUT)
GPIO.setup(LED2,    GPIO.OUT)
GPIO.setup(LED3,    GPIO.OUT)
GPIO.setup(LED4,    GPIO.OUT)
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(button4, GPIO.IN)

# Turn on LEDs to default state
GPIO.output(LED1, 0)
GPIO.output(LED2, 1)
GPIO.output(LED3, 0)
GPIO.output(LED4, 1)

# Map buttons to LEDs
map = {button1: LED1, button2: LED2, button3: LED3, button4: LED4}

def updateLED(channel):
    print("channel = " + channel)
    state = GPIO.input(channel)
    GPIO.output(map[channel], state)
    print(map[channel] + " Toggled")

print("Running...")

GPIO.add_event_detect(button1, GPIO.BOTH, callback=updateLED) # RISING, FALLING or BOTH
GPIO.add_event_detect(button2, GPIO.BOTH, callback=updateLED)
GPIO.add_event_detect(button3, GPIO.BOTH, callback=updateLED)
GPIO.add_event_detect(button4, GPIO.BOTH, callback=updateLED)

try:
    while True:
        time.sleep(100)   # Let other processes run

except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()
