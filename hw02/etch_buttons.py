#!/usr/bin/env python3
import curses, sys, time, numpy
import Adafruit_BBIO.GPIO as GPIO

button1="GP0_6"  # PAUSE or MODE
button2="GP0_5"
button3="GP0_4"
button4="GP0_3"
pbutton="PAUSE"
mbutton="MODE"

# Set the GPIO pins:
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(button4, GPIO.IN)
GPIO.setup(pbutton, GPIO.IN)
GPIO.setup(mbutton, GPIO.IN)

# TODO: add variable grid
x1 = 8
y1 = 8
screen = [[' '  for x in range(x1)] for x in range(y1)]

x = 4
y =  4

def updatePosition(channel):
    global x; global y; global y1; global x1
    print("channel = " + channel)
    key = channel
    if key  == 'PAUSE': # quit
      print("quit here") # TODO add quit and reset   
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
# TODO: Debounce switch somehow
GPIO.add_event_detect(button1, GPIO.RISING, callback=updatePosition) # RISING, FALLING or BOTH
GPIO.add_event_detect(button2, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(button3, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(button4, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(mbutton, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(pbutton, GPIO.RISING, callback=updatePosition)

def main():
    try:
      print("Running..")
      while True:
        time.sleep(1)
        print("Position: "+str(x)+", "+str(y)) 
        screen[x][y] = 'X'
        #print(numpy.matrix(screen))
        format_array(screen)
    except KeyboardInterrupt:
      print(" Cleaning Up")
      GPIO.cleanup()
    GPIO.cleanup()

def format_array(arr):
  for row in arr:
      for element in row:
          print(element, end=" ")
      print('')
  return 

if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch")
   input("Press enter to begin playing...")
   main()

