from time import sleep
import random
from Led import LedStrip
import math

NUM_LEDS = 41
leds = LedStrip( 6, NUM_LEDS )


def RunningLights( red,  green,  blue,  WaveDelay):
    Position = 0
 
    for j in range(NUM_LEDS * 2):
        Position = Position + 1
        for i in range(NUM_LEDS): 
            leds.set(int(((math.sin(i+Position) * 127 + 128)/255)*red), int(((math.sin(i+Position) * 127 + 128)/255)*green), int(((math.sin(i+Position) * 127 + 128)/255)*blue), i)
        leds.display()
        sleep(WaveDelay)


def loop():
    RunningLights(0xff,0,0, 10)        # red
    RunningLights(0xff,0xff,0xff, 10)  # white
    RunningLights(0,0,0xff, 10)        # blue

try:
    loop()
except Exception as e:
    print(e)