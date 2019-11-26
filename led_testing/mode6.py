
from modules import ws2812
from time import sleep
from Led import LedStrip
import random

n_leds = 41

leds = LedStrip( 6, n_leds )

leds.set( 0xff, 0xff, 0xff )
leds.display()

def FadeInOut( red,  green,  blue):
    r = 0
    g = 0
    b = 0
        
    for k in range(255):
        r = int((k/256.0)*red)
        g = int((k/256.0)*green)
        b = int((k/256.0)*blue)
        leds.set(r,g,b)
        leds.display()
  
     
    for k in range(255,0,-2):
        r = int((k/256.0)*red)
        g = int((k/256.0)*green)
        b = int((k/256.0)*blue)
        leds.set(r,g,b)
        leds.display()


def loop():
    while True:
        FadeInOut(0xff, 0x00, 0x00)     # red
        FadeInOut(0xff, 0xff, 0xff)     # white
        FadeInOut(0x00, 0x00, 0xff)     # blue

try:
    loop()
except Exception as e:
    print(e)
