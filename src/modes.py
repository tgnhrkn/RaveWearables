from time import sleep
import random
from Maix import GPIO
from Maix import I2S
from Maix import FFT
from fpioa_manager import *
import math

class Mode():
    def __init__( self, ledstrip ):
        self.strip = ledstrip

    def enter_mode( self ):
        self.strip.max()

    def update_mode( self ):
        pass

class MoveAcross( Mode ):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.index = 0
        
    def enter_mode( self ):
        self.strip.set( 0xff, 0, 0)

    def update_mode( self ):
        self.strip.set( 0xff, 0, 0, idx=self.index )
        self.index = (self.index + 1) % self.strip.n
        self.strip.set( 0, 0 , 0xff, idx=self.index )
        self.strip.display()
        sleep(0.1)
        

class MusicFFT (Mode):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        fm.register(20,fm.fpioa.I2S0_IN_D0)
        fm.register(19,fm.fpioa.I2S0_WS)
        fm.register(18,fm.fpioa.I2S0_SCLK)
        self.rx = I2S(I2S.DEVICE_0)
        self.rx.channel_config(self.rx.CHANNEL_0, self.rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
        self.sample_rate = 38640
        self.rx.set_sample_rate(self.sample_rate)
        self.sample_points = 1024
        self.FFT_points = 512
        self.hist_num = 90     #changeable
        
    def update_mode( self ):
        audio = self.rx.record(self.sample_points)
        FFT_res = FFT.run(audio.to_bytes(),self.FFT_points)
        FFT_amp = FFT.amplitude(FFT_res)
        interval = (self.hist_num//self.strip.n)
        count = 0
        for i in range(0, self.hist_num, interval):
            if FFT_amp[i] > 240:
                hist_height = 240
                brightness = 255 / 5
            else:
                hist_height = FFT_amp[i]
                brightness =  FFT_amp[i]
            self.strip.set(35, brightness, 10, count)
            count = count + 1
        self.strip.display()


class RedGreenSwitch (Mode):

    def __init__( self, ledstrip ):
        super().__init__( ledstrip )


    def update_mode( self ):
        self.strip.set(90, 0, 0)
        self.strip.display()
        sleep(1)
        self.strip.set(0, 90, 0)
        self.strip.display()
        sleep(1)

class OffMode( Mode ):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )

    def enter_mode( self ):
        self.strip.clear()

class FlashMode( Mode ):  
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.mode = 0
        self.count = 0

    def enter_mode( self ):
        self.strip.max()
        self.mode = 1
        self.count = 0

    def update_mode( self ):
        if self.count == 10:
            self.count = 0
            self.mode = 1 if self.mode == 0 else 0

            if self.mode == 1:
                self.strip.set( 50, 50, 50, display=True )
            else:
                self.strip.set( 0, 0, 0, display=True )
        
        self.count = self.count + 1
        sleep(0.01)

class RunningLights(Mode):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.red = 0xff
        self.green = 0xff
        self.blue = 0xff
        self.WaveDelay = 10

    def update_mode( self ):
        Position = 0
        for j in range(self.strip.n * 2):
            Position = Position + 1
            for i in range(self.strip.n): 
                self.strip.set(int(((math.sin(i+Position) * 127 + 128)/255)*self.red), int(((math.sin(i+Position) * 127 + 128)/255)*self.green), int(((math.sin(i+Position) * 127 + 128)/255)*self.blue), i)
            self.strip.display()
            sleep(self.WaveDelay/300)

class RainbowCycle(Mode):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.c = [0] * 3
        
    def update_mode( self ):
        i = 0
        j = 0

        for j in range(256 * 5): # 5 cycles of all colors on wheel
            for i in range(self.strip.n): 
                self.Wheel(self.c, ((i * 256 // self.strip.n) + j) & 255)
                self.strip.set(self.c[0], self.c[1], self.c[2], i)
            self.strip.display()

    def Wheel(self, c, WheelPos ):
        if WheelPos < 85:
            c[0] = WheelPos * 3
            c[1] = 255 - WheelPos * 3
            c[2] = 0
        elif WheelPos < 170:
            WheelPos = WheelPos - 85
            c[0] = 255 - WheelPos * 3
            c[1] = 0
            c[2] = WheelPos * 3
        else :
            WheelPos = WheelPos - 170
            c[0] = 0
            c[1] = WheelPos * 3
            c[2] = 255 - WheelPos * 3