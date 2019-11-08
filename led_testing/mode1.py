from modules import ws2812
from time import sleep
import random
from Maix import GPIO
from Maix import I2S
from Maix import FFT
import image
import lcd


lcd.init()
fm.register(8,  fm.fpioa.GPIO0)
wifi_en=GPIO(GPIO.GPIO0,GPIO.OUT)
wifi_en.value(0)
fm.register(20,fm.fpioa.I2S0_IN_D0)
fm.register(19,fm.fpioa.I2S0_WS)
fm.register(18,fm.fpioa.I2S0_SCLK)
rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
sample_rate = 38640
rx.set_sample_rate(sample_rate)
img = image.Image()
sample_points = 1024
FFT_points = 512
lcd_width = 320
lcd_height = 240
hist_num = 80 #changeable
hist_width = 1#int(lcd_width / hist_num)#changeable
x_shift = 0

# init LEDs
n_leds = 57 + 9
leds = ws2812( 6, n_leds ) # port 6, # leds
for i in range( n_leds ):
    leds.set_led( i, (0x10, 0x10, 0x10 ) )  # all leds white
leds.display()

def fft_output(led):
    while True:
        audio = rx.record(sample_points)
        FFT_res = FFT.run(audio.to_bytes(),FFT_points)
        FFT_amp = FFT.amplitude(FFT_res)
        img = img.clear()
        x_shift = 0
        for i in range(hist_num):
            if FFT_amp[i] > 240:
                hist_height = 240
                brightness = 255
            else:
                hist_height = FFT_amp[i]
                brightness = FFT_amp[i]
            leds.set_led( i, (brightness, brightness, brightness) )
            img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[255,255,255],2,True)
            x_shift = x_shift + hist_width + 3
        lcd.display(img)
        leds.display()
        

try:
    fft_output(leds)
except:
    print( "Interrupted" )