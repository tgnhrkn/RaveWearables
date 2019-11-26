from modules import ws2812
from time import sleep
from Led import LedStrip
import random

n_leds = 41

leds = LedStrip( 6, n_leds )

leds.set( 0xff, 0xff, 0xff )
leds.display()

def colors ( leds ):
    while True:
        leds.set(90, 0, 0)
        leds.display()
        sleep(1)
        leds.set(0, 90, 0)
        leds.display()
        sleep(1)
           
def driver(leds):
    while True:
        colors(leds)
        sleep( 0.2 )
try:
    driver(leds)
except Exception as e:
    print(e)

