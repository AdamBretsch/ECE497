#!/usr/bin/env python3
import curses, sys, time
import Adafruit_BBIO.GPIO as GPIO

button1="GP0_6"  # PAUSE or MODE
button2="GP0_5"
button3="GP0_4"
button4="GP0_3"


LED1   ="GREEN"
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

# Turn on both LEDs
GPIO.output(LED1, 0)
GPIO.output(LED2, 0)
GPIO.output(LED3, 0)
GPIO.output(LED4, 0)

# Map buttons to LEDs
map = {button1: LED1, button2: LED2, button3: LED3, button4: LED4}

def updateLED(channel):
    print("channel = " + channel)
    state = GPIO.input(channel)
    GPIO.output(map[channel], state)
    print(map[channel] + " Toggled")
    if channel == 'PAUSE': # quit
          break
    elif key == 'MODE': # clear screen
      print("clear screen")
    elif key == 'GP0_6': # TODO fix outside sceen bounds error
        if y > 0:
          y -= 1
    elif key == 'GP0_5':
        if y < y1:
          y += 1
    elif key == 'GP0_4':
        if x > 0:
          x -= 1
    elif key == 'GP0_3':
        if x < x1:
          x += 1
   
print("Running...")

GPIO.add_event_detect(button1, GPIO.BOTH, callback=updateLED) # RISING, FALLING or BOTH
GPIO.add_event_detect(button2, GPIO.BOTH, callback=updateLED)
GPIO.add_event_detect(button3, GPIO.BOTH, callback=updateLED)
GPIO.add_event_detect(button4, GPIO.BOTH, callback=updateLED)

def main():
    # look for arguments
    if len(sys.argv) == 3:
      x1 = int(sys.argv[1])
      y1 = int(sys.argv[2])
    else:
      x1 = 8
      y1 = 8
    #  account for 0 included in numbering
    x1 = x1-1
    y1 = y1-1
    # clear screen
    y0, x0 = 0, 0
    # find screen center and move cursor
    yc, xc = (y1-y0)//2, (x1-x0)//2

    x = xc
    y = yc

    while True:
      time.sleep(100)
      print("Position: "+x+", "+y) 
      except KeyboardInterrupt:
        print("Cleaning Up")
        GPIO.cleanup()
      GPIO.cleanup()

if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch")
   if len(sys.argv) == 3 :
     print("You have requested a " + sys.argv[1] + " by " + sys.argv[2] + " grid")
   else:
     print("You have not requested a grid size, so 8 by 8 will be used. To request a grid size see readme")
   input("Press enter to begin playing...")
   main()
