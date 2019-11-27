from modules import ws2812
from time import sleep
import random
from Led import LedStrip

NUM_LEDS = 46
leds = LedStrip( 6, NUM_LEDS ) 

def rainbowCycle():
  c = [0] * 3
  i = 0
  j = 0

  for j in range(256 * 5) : # 5 cycles of all colors on wheel
    for i in range(NUM_LEDS): 
        Wheel(c, ((i * 256 // NUM_LEDS) + j) & 255)
        leds.set(c[0], c[1], c[2], i)
    leds.display()


def Wheel(c, WheelPos ):
 
    if WheelPos < 85:
        c[0] = WheelPos * 3
        c[1] = 255 - WheelPos * 3
        c[2] = 0
    elif WheelPos < 170:
        WheelPos = WheelPos - 85
        c[0] = 255 - WheelPos * 3
        c[1] = 0
        c[2] = WheelPos * 3
    else :
        WheelPos = WheelPos - 170
        c[0] = 0
        c[1] = WheelPos * 3
        c[2] = 255 - WheelPos * 3

def loop():
    while True:
        rainbowCycle()

try:
    loop()
except Exception as e:
    print(e)