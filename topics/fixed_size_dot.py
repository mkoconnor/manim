from geometry import Circle
from mobject.vectorized_mobject import VGroup
from constants import WHITE, ORIGIN

class FixedSizeDot(Circle):
    CONFIG = {
        "radius"       : 0.08,
        "stroke_width" : 0,
        "fill_opacity" : 1.0,
        "color" : WHITE
    }

    def __init__(self, point = ORIGIN, **kwargs):
        self.fake_scale = False
        Circle.__init__(self, **kwargs)
        self.shift(point)
        self.init_colors()
        self.fake_scale = True

    def scale(self, scale_factor, **kwargs):
        if self.fake_scale:
            coor = self.get_center()
            self.move_to(coor * scale_factor)
        else:
            Circle.scale(self, scale_factor, **kwargs)

    def stretch(self, factor, dim):
        coor = self.get_center()
        coor[dim] *= factor
        self.move_to(coor)

        return self

class VGroupPS(VGroup):  # VGroup, Propagate Scale
    def scale(self, scale_factor, **kwargs):
        for submob in self.submobjects:
            submob.scale(scale_factor, **kwargs)

    def stretch(self, factor, dim):
        for submob in self.submobjects:
            submob.stretch(factor, dim)
