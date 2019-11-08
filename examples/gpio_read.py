from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

fpioa = FPIOA()

in_pin = 22 # Actual pin on the Maix
fpioa.set_function( in_pin, FPIOA.GPIO6) # How the k210 gpio6 gets routed to pin 22
in_gpio = GPIO(GPIO.GPIO6, GPIO.IN) # How the k210 knows what GPIO6 should do


lcd.init(color=lcd.WHITE)
lcd.draw_string(0,0, "Testing pin 22 as GPIO6", lcd.BLACK, lcd.WHITE )

while True:
    lcd.draw_string(0, 50, "pin 22 value is: %d" % in_gpio.value(), lcd.BLACK, lcd.WHITE )
