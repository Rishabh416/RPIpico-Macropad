import time
from digitalio import *
import analogio
import board

time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

rows = []
for p in [board.GP9, board.GP8, board.GP7, board.GP6]:
    row = DigitalInOut(p)
    row.direction = Direction.OUTPUT
    rows.append(row)

cols = []
for p in [board.GP5, board.GP4, board.GP3, board.GP2]:
    col = DigitalInOut(p)
    col.direction = Direction.INPUT
    col.pull = Pull.DOWN
    cols.append(col)

def getKey():  # Returns -999 or key value
    values = [1,2,3,10, 4,5,6,11, 7,8,9,12, 14,0,15,13]
    val = -999 # Error value for no key press
    for count in range(10): # Try to get key press 10 times
        for r in range(4):  # Rows, one at a time
            rows[r].value = 1 # row HIGH
            for c in range(4): # Test columns, one at a time
                if cols[c].value == 1: # Is column HIGH?
                    p = r * 4 + c      # Pointer to values list
                    val = values[p]
                    count = 11 # This stops looping
            rows[r].value = 0 # row LOW
    time.sleep(0.2) # Debounce
    return val

def macroMap(argument):
    switcher = {
        0: "one",
        1: "one",
        2: "two",
        3: "two",
        4: "two",
        5: "two",
        6: "two",
        7: "two",
        8: "two",
        9: "two",
        10: "two",
        11: "two",
        12: "two",
        13: "two",
        14: "two",
        15: "two",
    }

# loop
while True:
  x = getKey()
  print(x)

  macroMap(x)

