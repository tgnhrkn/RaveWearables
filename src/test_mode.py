from Led import LedStrip
from modes import *
from time import sleep


n_leds = 41
driver = LedStrip(6, n_leds )
mode = MusicFFT(driver)
mode.enter_mode()
while True:
    mode.update_mode()
    

