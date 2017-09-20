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
x1, y1 = 8, 8
screen = [[' '  for x in range(x1)] for x in range(y1)]
yc, xc = 4, 4
screen[xc][yc] = 'O'
x,oldx,y,oldy  = xc,xc,xc,xc
quitflag = False

# The first byte is GREEN, the second is RED.
def clearDisplay():
   disp = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
   ]
   return disp

display = clearDisplay()
lastx,lasty,index_x,index_y = None,None,4,4


def displayArray(arr): 
   global lastx,lasty,index_x,index_y,display
   disp = clearDisplay()
   for i in range(len(arr)):
      for j in range(len(arr[i])):
         if arr[i][j] == 'X':
           #print("index_x,lastx ",index_x,lastx)
           #if index_x != lastx:
            print("X found at ",i,", ",j)
            index_x = 2*i+1
            print("index_x= ",index_x)
            disp[index_x] += 2**j
            lastx = index_x
            print("disp[index_x]= ", disp[index_x])
         if arr[i][j] == 'O':
           #print("index_y, lasty ",index_y,lasty)
           #if index_y != lasty:
            print("O found at ",i,", ",j)
            index_y = 2*i
            print("index_y= ",index_y)
            disp[index_y] += 2**j
            lasty = index_y
            print("disp[index_y]= ", disp[index_y])            
   return disp

def printArray(arr):
  for row in arr:
      for element in row:
          print(element, end=" ")
      print('')
  return 
 

# method called on button push to move cursor
def updatePosition(channel):

    # debounce ?
    state = GPIO.input(channel)
    time.sleep(0.05)
    if state != GPIO.input(channel):
      return

    global x,y,x1,y1,oldx,oldy,screen,quitflag,display
    #print("channel = " + channel)
    key = channel
    oldx = x;
    oldy = y;
    if key  == 'PAUSE': # quit
        quitflag = True
    elif key == 'MODE': # clear screen
        print("Clearing screen...")
        screen = [[' '  for x in range(y1)] for x in range(x1)]
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
    display = displayArray(screen)
    printArray(screen)
    bus.write_i2c_block_data(matrix, 0, display)
    

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
      printArray(screen)
      display = displayArray(screen)
      while True:
        if quitflag:
          print("Quitting Etch-a-Sketch, thanks for playing!")
          GPIO.cleanup()
          break
        time.sleep(0.5)
        #printArray(screen)
        #displayArray(screen,dis)
        #bus.write_i2c_block_data(matrix, 0, display)
        print("Position: "+str(x)+", "+str(y)) 
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

