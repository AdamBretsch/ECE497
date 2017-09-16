#!/usr/bin/env python3
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902

import smbus, time
import Adafruit_BBIO.GPIO as GPIO
bus = smbus.SMBus(1)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

delay = 1; # Delay between images in s

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

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

screen = [[' '  for x in range(8)] for x in range(8)]
# find screen center and move cursor
yc, xc = 4, 4
x,oldx,y,oldy  = xc,xc,xc,xc
quitflag = False

# The first byte is GREEN, the second is RED.
smile = [0x00, 0x3c, 0x00, 0x42, 0x28, 0x89, 0x04, 0xFF,
    0x04, 0x85, 0x28, 0x89, 0x00, 0x42, 0x00, 0x00
]
frown = [0x3c, 0x00, 0x42, 0x00, 0x85, 0x20, 0x89, 0x00,
    0x89, 0x00, 0x85, 0x20, 0x42, 0x00, 0x3c, 0x00
]
neutral = [0x3c, 0x3c, 0x42, 0x42, 0xa9, 0xa9, 0x89, 0x89,
    0x89, 0x89, 0xa9, 0xa9, 0x42, 0x42, 0x3c, 0x3c
]
display = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

def formatArray(arr,disp):
   for i in range(len(arr)):
      for j in range(len(arr[i])):
         if arr[i][j] == 'X':
            index = 2*i+1
            disp[index] += 2**j
         if arr[i][j] == 'O':
            index = 2*i
            disp[index] += 2**j
   return 

formatArray(screen,display)
bus.write_i2c_block_data(matrix, 0, display)

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
        screen = [[' '  for x in range(8)] for x in range(8)]
    elif key == 'GP0_6': 
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
        print("Position: "+str(x)+", "+str(y)) 
        screen[oldx][oldy] = 'X'
        screen[x][y] = 'O'
        formatArray(screen,display)
        bus.write_i2c_block_data(matrix, 0, display)
    except KeyboardInterrupt:
      print(" Cleaning Up")
      GPIO.cleanup()
    GPIO.cleanup()

if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch")
   print("Use the 4 buttons to move the cursor, mode key to clear, and pause key to quit")
   input("Press enter to begin playing...")
   main()

