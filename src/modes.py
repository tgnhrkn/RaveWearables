class Mode():
    
    def __init__( self, ledstrip ):
        self.strip = ledstrip

    def enter_mode( self ):
        self.strip.max()

    def update_mode( self ):
        pass

class MoveAcrossMode( Mode ):

    def __init__( self, ledstrip ):
        super().__init__( ledstrip )
        self.index = 0

    def update_mode( self ):
        self.strip.set( 0xff, 0, 0, idx=self.index )
        self.index = (self.index + 1) % self.strip.n
        self.strip.set( 0, 0 , 0xff, idx=self.index )
        self.strip.display()

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

