import time
from digitalio import *
import analogio
import board

import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

keyboard = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

i2c = busio.I2C (scl=board.GP17, sda=board.GP16)
display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group()
display.show(splash)
color_bitmap = displayio.Bitmap(128, 64, 1) 
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF 

slider = analogio.AnalogIn(board.GP26)
joystickHor = analogio.AnalogIn(board.GP27)
joystickVer = analogio.AnalogIn(board.GP28)

def range_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

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
        0: keyboard.send(Keycode.F20),
        1: "one",
        2: "two",
        3: "two",
        4: "two",
        5: "two",
        6: "two",
        7: "two",
        8: "two",
        9: "two",
        10: keyboard.send(Keycode.F21),
        11: keyboard.send(Keycode.F22),
        12: keyboard.send(Keycode.F23),
        13: keyboard.send(Keycode.F24),
        14: "two",
        15: "two",
    }

prevVol = 0

# loop
while True:
    x = getKey()
    print(x)
    macroMap(x)
    
    print(joystickVer.value)
    print(joystickHor.value)
    mouse.move(
        x=range_map(joystickHor.value, 0, 65535, -10, 10),
        y=range_map(joystickVer.value, 0, 65535, -10, 10),
    )

    inner_bitmap = displayio.Bitmap(118, 54, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
    splash.append(inner_sprite)

    volume = range_map(slider.value, 0, 65535, 0, 100)
    print(volume)

    if volume > prevVol:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif volume < prevVol:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    
    text_area = label.Label(
        terminalio.FONT, text="Volume:" + str(volume), color=0xFFFFFF, x=28, y=64 // 2 - 1
    )
    splash.append(text_area)
    display.refresh()

    prevVol = volume

