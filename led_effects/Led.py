from modules import ws2812

class LedStrip():
    
    def __init__( self, pin, n ):
        self.n = n
        self.data = [ [0, 0, 0] for _ in range( self.n ) ]
        self.leds = ws2812( pin, self.n )

    def set( self, lcd, r, g, b, i=None, display=False ):
        lcd.draw_string(50,120, "enter .set", lcd.WHITE, lcd.RED )
        if i is not None:
            pxl = self.data[i]
            pxl[0] = r
            pxl[1] = g
            pxl[2] = b
        else:
            for pxl in self.data:
                pxl[0] = r
                pxl[1] = g
                pxl[2] = b
        
        lcd.draw_string(50,120, "before update", lcd.WHITE, lcd.RED )
        if display:
            self._update( lcd, i )
        lcd.draw_string(50,120, "after update", lcd.WHITE, lcd.RED )

    def _update( self, lcd, i=None ):
        lcd.draw_string(50,120, "enter update", lcd.WHITE, lcd.RED )
        if i is not None:
            self.leds.set_led( i, self.data[i] )
        else:
            for i in range( self.n ):
                self.leds.set_led( i, self.data[i] )
        lcd.draw_string(50,120, "before display", lcd.WHITE, lcd.RED )
        self.leds.display()
        lcd.draw_string(50,120, "after display", lcd.WHITE, lcd.RED )

    def display( self ):
        self._update()

    def clear( self ):
        self.set( 0, 0, 0, display=True )

    def max( self ):
        self.asdf( 255, 255, 255, i=2, display=True )

class FadingStrip( LedStrip ):

    def __init__( self ):
        pass
    
    def set( self, r, g, b, i=None, display=False ):
        def fade( data, clr, val ):
            if val > data[clr]:
                data[clr] = val
            else:
                data[clr] = data[clr] - 1
            
        if i is not None:
            pxl = self.data[i]
            fade( pxl, 0, r )
            fade( pxl, 1, g )
            fade( pxl, 2, b )
        else:
            for pxl in self.data:
                fade( pxl, 0, r )
                fade( pxl, 1, g )
                fade( pxl, 2, b )

        if display:
            self._update( i )

        
        
