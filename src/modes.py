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

