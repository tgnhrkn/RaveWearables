from modules import ws2812
from time import sleep
import random
from Led import LedStrip

NUM_LEDS = 41
leds = LedStrip( 6, NUM_LEDS )
heat = [0] * NUM_LEDS
cooldown = 0

def Fire(Cooling, Sparking, SpeedDelay, heat, cooldown):
    # Step 1.  Cool down every cell a little
    for i in range(NUM_LEDS):
        cooldown = random.randint(0, (Cooling * 10) // NUM_LEDS + 2)

        if cooldown > heat[i]: 
            heat[i]=0
        else:
            heat[i]= heat[i] - cooldown


    # Step 2.  Heat from each cell drifts 'up' and diffuses a little
    for k in range(NUM_LEDS - 1, 3, -1): 
        heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 3]) // 3

    # Step 3.  Randomly ignite new 'sparks' near the bottom
    if random.randint(0, 255) < Sparking:
        y = random.randint(0,7)
        heat[y] = heat[y] + random.randint(160,255)
        #heat[y] = random(160,255)


    # Step 4.  Convert heat to LED colors
    for j in range(NUM_LEDS): 
        setPixelHeatColor(j, heat[j])

    leds.display()
    sleep(SpeedDelay)

def setPixelHeatColor(Pixel,  temperature):
    # Scale 'heat' down from 0-255 to 0-191
    t192 = int((temperature/255.0)*191)

    # calculate ramp up from
    heatramp = t192 & 0x3F # 0..63
    heatramp *= 4 # scale up to 0..252

    # figure out which third of the spectrum we're in:
    if t192 > 0x80:                             # hottest
        leds.set(255, 255, heatramp, Pixel)
    elif t192 > 0x40:                           # middle
        leds.set(255, heatramp, 0, Pixel)
    else :                                      # coolest
        leds.set(heatramp, 0, 0, Pixel)


def loop():
    heat = [0] * NUM_LEDS
    while True:
        Fire(55,120,.05,heat, cooldown)

try:
    loop()
except Exception as e:
    print(e)
