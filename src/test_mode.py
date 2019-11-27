from Led import LedStrip
from modes import *
from time import sleep


n_leds = 45
driver = LedStrip(6, n_leds )
mode = RainbowCycle(driver)
mode.enter_mode()
while True:
    mode.update_mode()
    

