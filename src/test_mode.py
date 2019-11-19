from Led import LedStrip
from modes import *
from time import sleep

n_leds = 4
driver = LedStrip(6, n_leds )
mode = MoveAcrossMode(driver)
mode.enter_mode()
while True:
    mode.update_mode()
    sleep( 0.2 )

