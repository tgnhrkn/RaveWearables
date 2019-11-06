from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

test_pin = 16
fpioa = FPIOA()
fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.IN)
lcd.init(color=(0,125,255))
lcd.draw_string(50,120, "Welcome to Teagan's MaixPy!!", lcd.WHITE, lcd.RED )

if test_gpio.value() == 0:
    print( "pin 16 pulled down" )
    while True:
        pass
