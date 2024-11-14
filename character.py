from common import Vecter2

class Character2D():
    def __init__(self):
        self.center=Vecter2(0,0)
        self.image=None 

    def set_pos(self,x=0,y=0):
        self.center.x=x
        self.center.y=y

    def set_pos_delta(self,dx=0,dy=0):
        self.center.x+=dx
        self.center.y+=dy


