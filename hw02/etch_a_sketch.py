#!/usr/bin/env python3
import curses, sys

def main(scr):
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
    scr.clear()
    y0, x0 = 0, 0
    # find screen center and move cursor
    yc, xc = (y1-y0)//2, (x1-x0)//2
    scr.move(yc, xc)
    scr.refresh()

    x = xc
    y = yc
    ch = 'X'
    lastch = 'X'
    while True:
      # check key input
      key = scr.getkey()
      if key == 'q': # quit
          break
      elif key == 'z': # clear screen
          scr.clear()
          scr.move(x,y)
          oldch = ch
          ch = '	'
      elif key == 'KEY_UP': # TODO fix outside sceen bounds error
        if y > 0:
          y -= 1
      elif key == 'KEY_DOWN':
        if y < y1:
          y += 1
      elif key == 'KEY_LEFT':
        if x > 0:
          x -= 1
      elif key == 'KEY_RIGHT':
        if x < x1:
          x += 1
      else: # set cursor to new charactor if no other action
         oldch = ch
         ch = key

      scr.addstr(ch)
      scr.move(y, x)
      scr.refresh()
      if ch == '	':
        ch = oldch # make sure ch is reset

if __name__ == "__main__":
   # pregame instructions
   print("Welcome to Etch-A-Sketch! Move with the arrow keys, press z to clear and q to quit")
   print("All other keys can be used to change the cursor")
   if len(sys.argv) == 3 :
     print("You have requested a " + sys.argv[1] + " by " + sys.argv[2] + " grid")
   else:
     print("You have not requested a grid size, so 8 by 8 will be used. To request a grid size see readme")
   input("Press enter to begin playing...")
   # using wrapper makes setup much easier
   curses.wrapper(main)
