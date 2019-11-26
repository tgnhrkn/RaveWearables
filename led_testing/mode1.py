from modules import ws2812
from time import sleep
import random
from Maix import GPIO
from Maix import I2S
from Maix import FFT

fm.register(20,fm.fpioa.I2S0_IN_D0)
fm.register(19,fm.fpioa.I2S0_WS)
fm.register(18,fm.fpioa.I2S0_SCLK)
rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
sample_rate = 38640
rx.set_sample_rate(sample_rate)
sample_points = 1024
FFT_points = 512
hist_num = 41 #changeable
hist_width = 1#int(lcd_width / hist_num)#changeable
x_shift = 0

# init LEDs
n_leds = 41
leds = ws2812( 6, n_leds ) # port 6, # leds

for i in range( n_leds ):
    leds.set_led( i, (0x10, 0x10, 0x10 ) )  # all leds white
leds.display()

def fft_output( leds ):
    while True:
        audio = rx.record(sample_points)
        FFT_res = FFT.run(audio.to_bytes(),FFT_points)
        FFT_amp = FFT.amplitude(FFT_res)
        interval = int(hist_num/n_leds)
        count = 0
        for i in range(0, hist_num, interval):
            if FFT_amp[i] > 240:
                hist_height = 240
                brightness = 255 / 5
            else:
                hist_height = FFT_amp[i]
                brightness =  FFT_amp[i]
            leds.set_led( count, (35, brightness, 10) )
            count = count + 1
        leds.display()


try:
    fft_output( leds )
except Exception as e:
    print(e)