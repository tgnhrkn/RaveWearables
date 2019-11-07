from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

fpioa = FPIOA()

test_pin = 16
fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.IN)

lcd.init(color=LCD.WHITE)
lcd.draw_string(0,0, "Welcome to Teagan's MaixPy!", lcd.BLACK, lcd.WHITE )
if test_gpio.value() == 0:
    print( "pin 16 pulled down" )
    lcd.draw_string( 50, 180, "Pin 16 pulled down", lcd.BLACK, lcd.WHITE )
    while True:
        pass
