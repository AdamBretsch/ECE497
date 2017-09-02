#! /usr/bin/python
import sys, select
def main():
  row = 8
  col = 8
  screen = [[' ' for x in range(col)] for x in range(row)]
  screen[4][4] = 'X'
  printArray(screen)

def printArray(A):
  for row in A:
    for val in row:
      print '{:4}'.format(val),
    print
  return;

main()
