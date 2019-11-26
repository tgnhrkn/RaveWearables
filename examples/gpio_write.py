from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO
import time

fpioa = FPIOA()

in_pin = 22
out_pin = 23
fpioa.set_function( in_pin, FPIOA.GPIO6 )
fpioa.set_function( out_pin, FPIOA.GPIO5 )
in_gpio = GPIO(GPIO.GPIO6, GPIO.IN)
out_gpio = GPIO(GPIO.GPIO5, GPIO.OUT)

lcd.init(color=lcd.WHITE)
lcd.draw_string(0,0, "Testing pins 22(in) 23(out)", lcd.BLACK, lcd.WHITE )

count = 100000
zero = True
while True:
    count = count + 1
    if count >= 100000:
        if zero:
            out_gpio.value(0)
            lcd.draw_string(0, 50, "pin 23 output is: %d" % 0, lcd.BLACK, lcd.WHITE )
            lcd.draw_string(0, 100, "pin 22 reads: %d" % in_gpio.value(), lcd.BLACK, lcd.WHITE )
        else:
            out_gpio.value(1)
            lcd.draw_string(0, 50, "pin 23 output is: %d" % 1, lcd.BLACK, lcd.WHITE )
            lcd.draw_string(0, 100, "pin 22 reads: %d" % in_gpio.value(), lcd.BLACK, lcd.WHITE )
        zero = not zero
        count = 0
    
