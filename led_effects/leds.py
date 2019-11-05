from modules import ws2812
from time import sleep
import random

n_leds = 57 + 9

leds = ws2812( 6, n_leds )

for i in range( n_leds ):
    leds.set_led( i, (0xff, 0xff, 0xff ) )
leds.display()

def func1( leds ):
    blue = 0
    while True:
        leds.set_led( blue, ( 0xff, 0, 0) )
        blue = (blue + 1) % n_leds
        leds.set_led( blue, (0, 0, 0xff ) )
        leds.display()
        sleep(0.2)

def func2( leds ):
    #initials = [(random.randint(0, 0xff), random.randint(0, 0xff), random.randint(0, 0xff)) for _ in range(n_leds)]
    initials = [ (0, 0, 0) for _ in range(n_leds) ]
    print( initials )
    while True:
        print( "changing" )
        for i in range( len( initials )):
            c_val = initials[i]
            new_val = ( min(0xff, c_val[0] + 1), min( 0xff, c_val[1] + 1 ), min( 0xff, c_val[2] + 1 ) )
            initials[i] = new_val
            leds.set_led(i, new_val)
        leds.display()
        print( "sleeping" )
        sleep(0.4)

def func3( leds ):
    sets = [random.randint(0,2) for _ in range(n_leds)]
    for i, val in enumerate( sets ):
        clr_vals = [0, 0, 0]
        clr_vals[val] = 30
        leds.set_led( i, tuple( clr_vals ) )
    leds.display()

def func4( leds ):
    while True:
        func3(leds)
        sleep( 0.2 )
        
try:
    func4(leds)
except:
    print( "Interrupted" )


