from modules import ws2812

class LedStrip():
    
    def __init__( self, pin, n ):
        self.n = n
        self.data = [ (0, 0, 0) for _ in range( self.n ) ]
        self.leds = ws2812( pin, self.n )

    def set( self, r, g, b, idx=None, display=False ):
        if idx is not None:
            self.data[idx] = ( r, g, b )
        else:
            for i in range(self.n):
                self.data[i] = (r, g, b)
        
        if display:
            self._update( idx=idx )

    def _update( self, idx=None ):
        if idx is not None:
            self.leds.set_led( idx, self.data[idx] )
        else:
            for i in range( self.n ):
                self.leds.set_led( i, self.data[i] )
        self.leds.display()

    def display( self ):
        self._update()

    def clear( self ):
        self.set( 0, 0, 0, display=True )

    def max( self ):
        self.set( 255, 255, 255, display=True )

class FadingStrip( LedStrip ):

    def __init__( self, pin, n):
        super().__init__( pin, n )
    
    def set( self, r, g, b, idx=None, display=False ):
        def fade( cval, setval ):
            if setval >= cval:
                return setval
            else:
                drop = cval - setval
                perc = setval / 255
                perc = 1.0 - (perc/3)
                drop_amt = perc * drop

                return cval - int( drop_amt)
            
        if idx is not None:
            cr, cg, cb = self.data[idx]
            self.data[idx] = ( fade( cr, r), fade( cg, g), fade( cb, b) )
        else:
            for i in range(self.n):
                cr, cg, cb = self.data[i]
                self.data[i] = ( fade( cr, r), fade( cg, g), fade( cb, b) )

        if display:
            self._update( idx )

class LowPowerStrip( LedStrip ):
    def __init__( self, pin, n ):
        super().__init__( pin, n )

    def set( self, r, g, b, idx=None, display=False ):
        r = min( 50, r )
        g = min( 50, g )
        b = min( 50, b )

        super().set( r, g, b, idx, display )

class LowRangeStrip( FadingStrip ):
    def __init__( self, pin, n ):
        super().__init__( pin, n )

    def set( self, r, g, b, idx=None, display=False ):
        def translate( cur, bh, nh ):
            perc = cur / bh
            return int(perc * nh)
             
        r = translate( r, 255, 50 )
        g = translate( g, 255, 50 )
        b = translate( b, 255, 50 )

        super().set( r, g, b, idx, display )




        
        
