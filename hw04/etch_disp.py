#!/usr/bin/env python3
# Etch a sketch with buttons and 8x8 bicolor led display
# https://www.adafruit.com/product/902

import smbus, time
import Adafruit_BBIO.GPIO as GPIO
import rcpy 
import rcpy.encoder as encoder
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
LED1  ="RED"
LED2  ="GREEN" #GP1
TA1   ="GP1_3"
TA2   ="GP1_4"

tmp1 = 0x48
tmp2 = 0x4a
alarm = 26
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

# Set the GPIO pins:
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(button4, GPIO.IN)
GPIO.setup(pbutton, GPIO.IN)
GPIO.setup(mbutton, GPIO.IN)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(TA1, GPIO.IN)
GPIO.setup(TA2, GPIO.IN)

# set up variable
color = 'H'
x1, y1 = 8, 8
screen = [[' '  for x in range(x1)] for x in range(y1)]
yc, xc = 4, 4
screen[xc][yc] = color
x,oldx,y,oldy  = xc,xc,xc,xc
quitflag = False
lastx,lasty,index_x,index_y = None,None,4,4

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

# The first byte is GREEN, the second is RED.
def clearDisplay():
# method to clear display
   disp = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
   ]
   return disp

def displayArray(arr): 
# convert array data to i2c bus display
   global lastx,lasty,index_x,index_y,display
   disp = clearDisplay()
   for i in range(len(arr)):
      for j in range(len(arr[i])):
         if arr[i][j] == 'X':
           # print("X found at ",i,", ",j)
            index_x = 2*i+1
           # print("index_x= ",index_x)
            disp[index_x] += 2**j
         if arr[i][j] == 'O':
           # print("O found at ",i,", ",j)
            index_y = 2*i
           # print("index_y= ",index_y)
            disp[index_y] += 2**j
         if arr[i][j] == 'H':
            print("H found at ",i,", ",j)
            index_x = 2*i+1
            disp[index_x] += 2**j
            index_y = 2*i
            disp[index_y] += 2**j
                        
   return disp

def printArray(arr):
# method to print array onto console output
  for row in arr:
      for element in row:
          print(element, end=" ")
      print('')
  return 
 

def updatePosition(channel):
# method called on button push to move cursor and update displays
    
    print("Channel pressed: ",channel)
    # debounce ?
    if channel == 'GP0_3' or channel == 'GP0_4' or channel == 'GP0_5' or channel =='GPO_6':
      state = GPIO.input(channel)
      time.sleep(0.05)
      if state != GPIO.input(channel):
        return

    global x,y,x1,y1,oldx,oldy,screen,quitflag,display,color,e2,e3
    #print("channel = " + channel)
    key = channel
    oldx = x;
    oldy = y;
    # check which button pushed, act accordingly
    
    if key  == 'PAUSE': # quit
        quitflag = True
    elif key == 'MODE': # clear screen
        print("Clearing screen...")
        screen = [[' '  for x in range(y1)] for x in range(x1)]
    elif key == 'GP0_6' or key == 'Joy2+': 
        if y > 0:
          y -= 1
    elif key == 'GP0_5' or key == 'Joy2-':
        if y < (y1-1):
          y += 1
    elif key == 'GP0_3' or key == 'Joy3+':
        if x > 0:
          x -= 1
    elif key == 'GP0_4' or key == 'Joy3-':
        if x < (x1-1):
          x += 1
        
    # update displays
    screen[oldx][oldy] = color
    screen[x][y] = 'H'
    display = displayArray(screen)
    printArray(screen)
    bus.write_i2c_block_data(matrix, 0, display)
    print("Position: "+str(x)+", "+str(y))

# event listeners
# RISING, FALLING or BOTH
GPIO.add_event_detect(button1, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(button2, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(button3, GPIO.RISING, callback=updatePosition)
GPIO.add_event_detect(button4, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(mbutton, GPIO.FALLING, callback=updatePosition)
GPIO.add_event_detect(pbutton, GPIO.FALLING, callback=updatePosition)

def main():
# main method run after setup
    global quitflag,color
    try:
      print("Running..")
      # inital display update
      printArray(screen)
      display = displayArray(screen)
      bus.write_i2c_block_data(matrix, 0, display)
      e2old = 0
      e3old = 0
      print("Position: "+str(x)+", "+str(y)) 
      while True:
      # main loop listening for quitflag
        if quitflag:
          print("Quitting Etch-a-Sketch, thanks for playing!")
          bus.write_i2c_block_data(matrix, 0, clearDisplay())
          GPIO.cleanup()
          break
        # read encoders
        e2 = encoder.get(2) 
        e3 = encoder.get(3)
        if e2 > e2old:
            updatePosition('Joy2+')
        elif e2 < e2old:
            updatePosition('Joy2-')
        if e3 > e3old:
            updatePosition('Joy3+')
        elif e3 < e3old:
            updatePosition('Joy3-')
        e2old = encoder.get(2) 
        e3old = encoder.get(3)
        # read temp
        temp1 = bus.read_byte_data(tmp1, 0)
        temp2 = bus.read_byte_data(tmp2, 0)
        # check alarm values
        if GPIO.input(TA1) == 0:
           GPIO.output(LED1,1)
           temp1f = temp1*9/5+32
           print("Alarm one triggered at ", temp1f, " degrees F")
           color = 'X'
        elif GPIO.input(TA2) == 0:
           GPIO.output(LED2,1)
           temp2f = temp2*9/5+32
           print("Alarm two triggered at ", temp2f," degrees F")
           color = 'O'
        else:
           GPIO.output(LED1,0)
           GPIO.output(LED2,0)
           color = 'H'
       
        time.sleep(0.25)
    except KeyboardInterrupt:
          print("Quitting Etch-a-Sketch, thanks for playing!")
          bus.write_i2c_block_data(matrix, 0, clearDisplay())
          GPIO.cleanup()
if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch")
   print("Use the 4 buttons to move the cursor, mode key to clear, and pause key to quit")
   print("Or use the 2 encoders to move the cursor")
   print("Use the tempuarature sensor to change the color, leds show color selected")
   input("Press enter to begin playing...")
   main()
