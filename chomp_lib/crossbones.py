from mobject.svg_mobject import *

__all__ = ['Crossbones']

class Crossbones(SVGMobject):
    def __init__(self):
        SVGMobject.__init__(
            self,
            file_name='/Users/michaeloconnor/Downloads/halloween-skull-and-crossbones.svg',
            initial_scale_factor=0.001,
        )
        self.set_stroke(color=RED,width=0.1)
        self.set_fill(color=RED)
