from mobject.svg_mobject import *
from animation.transform import *

__all__ = ['SmileyGuy']

class SmileyGuy(SVGMobject):
    def set_stroke_and_fill(self,cls,color):
        cls.set_stroke(color=color,width=1.5)
        cls.set_fill(color=color)

    def load_svg(self,file_name,color):
        c = SVGMobject(
            file_name=file_name,
            initial_scale_factor=self.scale_factor
        )
        self.set_stroke_and_fill(c,color)
        return c

    def __init__(self,color=WHITE,scale_factor=0.015):
        self.scale_factor = scale_factor
        self.color=color
        SVGMobject.__init__(
            self,
            file_name='/Users/michaeloconnor/Downloads/Untitled-3.svg',
            initial_scale_factor=scale_factor,
        )
        self.set_stroke_and_fill(self,color=color)

    def transform_to(self,file_name):
        new_face = self.load_svg(file_name,color=self.color)
        return Transform(self,new_face.replace(self,stretch=True))

    def neutral(self):
        return self.transform_to('/Users/michaeloconnor/Downloads/Untitled-3.svg')

    def open_mouth(self):
        return self.transform_to('/Users/michaeloconnor/Downloads/Untitled-4.svg')
    def toothy_grin(self):
        return self.transform_to('/Users/michaeloconnor/Downloads/Untitled-5.svg')

    def tilde_face(self):
        return self.transform_to('/Users/michaeloconnor/Downloads/Untitled-6.svg')

    def v_face(self):
        return self.transform_to('/Users/michaeloconnor/Downloads/Untitled-7.svg')

    def easy_scale(self,by):
        c = self.copy()
        c.scale(scale_factor=by,about_point=c.get_center())
        return Transform(self,c)

    def scale_up(self):
        return self.easy_scale(by=1.2)

    def scale_down(self):
        return self.easy_scale(by=1/1.2)
