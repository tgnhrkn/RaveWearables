import lcd, image

from modules import ws2812
from Led import LedStrip


lcd.init(color=(255, 125, 0))
lcd.draw_string(50,120, "Start", lcd.WHITE, lcd.RED )

strip = LedStrip(6, 9)
lcd.draw_string(50,120, "Middle", lcd.WHITE, lcd.RED )
strip.set( lcd, 255, 255, 255, i=2, display=True )
lcd.draw_string(50,120, "Finish", lcd.WHITE, lcd.RED )



