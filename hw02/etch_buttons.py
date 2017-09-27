#!/usr/bin/env python3
import curses, sys, time, numpy
import Adafruit_BBIO.GPIO as GPIO

button1="GP0_6" # GP0 and 2 user buttons used
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

# setting up the screen output
# TODO: reimplement variable grid
if len(sys.argv) == 3:
  x1 = int(sys.argv[1])
  y1 = int(sys.argv[2])
else:
  x1 = 8
  y1 = 8
y0, x0 = 0, 0
screen = [[' '  for x in range(x1)] for x in range(y1)]
# find screen center and move cursor
yc, xc = int((y1-y0)//2), int((x1-x0)//2)
x,oldx,y,oldy  = xc,xc,xc,xc
quitflag = False

# method called on button push to move cursor
def updatePosition(channel):

    # debounce
    state = GPIO.input(channel)
    time.sleep(0.05)
    if state != GPIO.input(channel):
      return

    global x,y,y1,x1,oldx,oldy,screen,quitflag
    #print("channel = " + channel)
    key = channel
    oldx = x;
    oldy = y;
    if key  == 'PAUSE': # quit
        quitflag = True
    elif key == 'MODE': # clear screen
        print("Clearing screen...")
        screen = [[' '  for x in range(x1)] for x in range(y1)]
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
    screen[oldx][oldy] = 'X'
    screen[x][y] = 'O'

GPIO.add_event_detect(button1, GPIO.RISING, callback=updatePosition) # RISING, FALLING or BOTH
GPIO.add_event_detect(button2, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(button3, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(button4, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(mbutton, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(pbutton, GPIO.FALLING, callback=updatePosition)

# main method run after setup
def main():
    try:
      print("Running..")
      while True:
        if quitflag:
          print("Quitting Etch-a-Sketch, thanks for playing!")
          GPIO.cleanup()
          break
        time.sleep(1)
        #print("Position: "+str(x)+", "+str(y)) 
        screen[oldx][oldy] = 'X'
        screen[x][y] = 'O'
        #print(numpy.matrix(screen))
        format_array(screen)
    except KeyboardInterrupt:
      print(" Cleaning Up")
      GPIO.cleanup()
    GPIO.cleanup()

# array printing method
def format_array(arr):
  for row in arr:
      for element in row:
          print(element, end=" ")
      print('')
  return 

if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch")
   print("Use the 4 buttons to move the cursor, mode key to clear, and pause key to quit")
   if len(sys.argv) == 3 :
     print("You have requested a " + sys.argv[1] + " by " + sys.argv[2] + " grid")
   else:
     print("You have not requested a grid size, so 8 by 8 will be used. To request a grid size see readme")
   input("Press enter to begin playing...")
   main()

