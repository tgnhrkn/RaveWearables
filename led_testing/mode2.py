from modules import ws2812
from time import sleep
import random

n_leds = 41

leds = ws2812( 6, n_leds )


for i in range( n_leds ):
    leds.set_led( i, (0x10, 0x10, 0x10 ) )
leds.display()

def move ( leds ):
    index = 0
    while True:
        leds.set_led( index, ( 0xff, 0xff, 0xff) )
        index = (index + 1) % n_leds
        leds.set_led( index, (0, 0, 0xff ) )
        leds.display()
        sleep(0.2)
    
def driver(leds):
    while True:
        move(leds)
        sleep( 0.2 )
try:
    move(leds)
except Exception as e:
    print(e)

