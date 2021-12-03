

class CodeGenerator:
    from random import choice
    licencia = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    token = "0123456789abcdefghijklmnopqrstuvwxyz"
    def __init__(self, size):
        self.size = size

    def Token(self):
        p = ""
        p = p.join( [self.choice( self.token ) for i in range( self.size )] )
        return p

    def License(self):
        p = ""
        p = p.join( [self.choice( self.licencia ) for i in range( self.size )] )
        return p