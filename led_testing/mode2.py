from modules import ws2812
from time import sleep
import random

n_leds = 100

leds = ws2812( 6, n_leds )

for i in range( n_leds ):
    leds.set_led( i, (0xff, 0xff, 0xff ) )
leds.display()

def move (leds)
    moving = 0
    while: moving != n_leds
        for i in range(n_leds):
            if moving == i:
                moving_vals = [0, 0, 0]
                moving_vals[val] = 30
                leds.set_led(i, tuple( moving_vals ))
            else:
                leds.set_led(i, tuple(10, 50, 100))
        leds.display()
        moving = moving + 1
        if (moving == n_leds):
            moving = 0

try:
    move(leds)
except Exception as e:
    print(e)

