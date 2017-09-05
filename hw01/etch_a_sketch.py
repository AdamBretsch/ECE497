#!/usr/bin/env python3
import curses, sys


def main(scr):
    if len(sys.argv) == 3:
      x1 = int(sys.argv[1])
      y1 = int(sys.argv[2])
    else:
      x1 = 8
      y1 = 8
    #  account for 0 included in numbering
    x1 = x1-1
    y1 = y1-1
    scr.clear()
    y0, x0 = 0, 0

    yc, xc = (y1-y0)//2, (x1-x0)//2

    scr.move(yc, xc)

    scr.refresh()

    x = xc
    y = yc
    ch = 'X'

    while True:

      key = scr.getkey()
      if key == 'q':
          break
      elif key == 'z':
          scr.clear()
          scr.move(x,y)
          ch = ' '
	 # TODO Fix screen clearing for multiple types
      elif key == 'KEY_UP':
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
	 # TODO: add multiple key types, ch = ?

      scr.addstr(ch)
      scr.move(y, x)
      scr.refresh()
      ch = 'X'

if __name__ == "__main__":
   print("Welcome to Etch-A-Sketch! Move with the arrow keys, press z to clear and q to quit")
   if len(sys.argv) == 3 :
     print("You have requested a " + sys.argv[1] + " by " + sys.argv[2] + " grid")
   else:
     print("You have not requested a grid size, so 8 by 8 will be used. To request a grid size see readme")
   input("Press enter to begin playing...")
   curses.wrapper(main)
