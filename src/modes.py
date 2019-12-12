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
        self.low = 0
        self.high = 4
        self.count = 0
        self.baseColor = [0, 0, 0]
        self.movingColor = [0, 0, 0]
        self.selectBase = random.randint(1, 3)
        self.selectMoving = random.randint(1, 3)
        while self.selectBase == self.selectMoving:
            self.selectMoving = random.randint(1, 3)

        self.setBase()
        self.setMoving()
        
    def enter_mode( self ):
        self.strip.set( 0xff, 0, 0)

    def update_mode( self ):
        self.strip.set(self.baseColor[0], self.baseColor[1], self.baseColor[2])
        for i in range (self.low, self.high):
            self.strip.set( self.movingColor[0], self.movingColor[1], self.movingColor[2], idx=i)
        self.low = (self.low + 1) % self.strip.n
        self.count = self.count + 1
        self.high = (self.high + 1) % self.strip.n
        self.strip.display()
        if self.count == self.strip.n:
            self.count = 0
            self.selectBase = random.randint(1, 3)
            self.selectMoving = random.randint(1, 3)
            while self.selectBase == self.selectMoving:
                self.selectMoving = random.randint(1, 3)
            
            self.setBase()
            self.setMoving()
    
    def setMoving(self):
        if self.selectMoving == 1:
            self.movingColor = [random.randint(200, 0xff), random.randint(0, 50), random.randint(0, 50)]
        if self.selectMoving == 2:
            self.movingColor = [random.randint(0, 50), random.randint(200, 0xff), random.randint(0, 50)]
        if self.selectMoving == 3:
            self.movingColor = [random.randint(0, 50), random.randint(0, 50), random.randint(200, 0xff)]
    
    def setBase(self):
        if self.selectBase == 1:
            self.baseColor = [random.randint(200, 0xff), random.randint(0, 50), random.randint(0, 50)]
        if self.selectBase == 2:
            self.baseColor = [random.randint(0, 50), random.randint(200, 0xff), random.randint(0, 50)]
        if self.selectBase == 3:
            self.baseColor = [random.randint(0, 50), random.randint(0, 50), random.randint(200, 0xff)]
        

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
                brightness = 255
            else:
                hist_height = FFT_amp[i]
                brightness = FFT_amp[i]
            
            r,g,b = 0,0,0
                
            if brightness < 5 and brightness > 2:
                g = 50
            if brightness >= 5 and brightness < 20:
                g = 200 + brightness
                r = 200 + brightness
            if brightness >= 20:
                r = 200 + brightness
            self.strip.set(r,g,b, count)
            count = count + 1
        self.strip.display()

class SideFFT( Mode ):
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

        self.c = [0] * 3
        self.j = 0

        self.rain_vals = []
        for i in range( self.strip.n ):
            c = [0,0,0]
            self.Wheel( c, ((i * 256 // self.strip.n ) + 0 ) & 255 )
            self.rain_vals.append(c)

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
            
    def update_mode( self ):
        audio = self.rx.record(self.sample_points)
        FFT_res = FFT.run(audio.to_bytes(),self.FFT_points)
        FFT_amp = FFT.amplitude(FFT_res)
        interval = (self.hist_num//self.strip.n)
        total = 0
        for i in range(0, 20):
            total = total + min( 255, FFT_amp[i] )

        avg = total / 20
        if avg > 50:
            avg = 50
        else:
            avg = int( avg )

        perc = avg / 50
        n_lit = int(perc * self.strip.n)
        for i in range(n_lit):
            rv = self.rain_vals[i]
            self.strip.set(rv[0],rv[1],rv[2],i)
        for i in range(n_lit,self.strip.n):
            self.strip.set(0,0,0,i)
        self.strip.display()


class RedGreenSwitch (Mode):

    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.count = 0

    def enter_mode( self ):
        self.count = 0
        self.strip.set( 255, 0, 0, display=True)

    def update_mode( self ):
        self.count = self.count + 1
        if self.count == 120:
            self.count = 0
        if self.count == 0:
            self.strip.set( 255, 0, 0, display=True )

        if self.count == 60:
            self.strip.set( 0, 255, 0, display=True )
        

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
                self.strip.max()
            else:
                self.strip.clear()
        
        self.count = self.count + 1
        sleep(0.01)

class RunningLights(Mode):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.red = 0xff
        self.green = 0xff
        self.blue = 0xff
        self.WaveDelay = 10
        self.j = 0

    def enter_mode( self ):
        self.j = 0

    def update_mode( self ):
        Position = self.j + 1
        for i in range(self.strip.n): 
            self.strip.set(int(((math.sin(i+Position) * 127 + 128)/255)*self.red), int(((math.sin(i+Position) * 127 + 128)/255)*self.green), int(((math.sin(i+Position) * 127 + 128)/255)*self.blue), i)
        self.strip.display()

        self.j = self.j + 1
        if self.j == self.strip.n * 2:
            self.j = 0
        sleep(self.WaveDelay/300)

class RainbowCycle(Mode):
    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.c = [0] * 3
        self.j = 0

    def enter_mode( self ):
        self.j = 0
        
    def update_mode( self ):
        
        for i in range( self.strip.n ):
            self.Wheel(self.c, ((i * 256 // self.strip.n) + self.j) & 255)
            self.strip.set(self.c[0], self.c[1], self.c[2], i)
        self.strip.display()

        self.j = self.j + 1
        if self.j == 256*5:
            self.j = 0

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
