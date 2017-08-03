from geometry import Cross
from mobject.vectorized_mobject import VMobject
from constants import *

class IconNo(Cross):
    CONFIG = {
        "color" : RED,
    }

class IconYes(VMobject):
    CONFIG = {
        "color" : GREEN,
    }
    def generate_points(self):
        self.set_anchors_and_handles(
            [0.8*LEFT + 0.8*UP,   0.8*LEFT + 0.4*DOWN, RIGHT + 1.1*UP],
            [    LEFT + 0.2*DOWN, 0.6*LEFT + 0.4*DOWN],
            [    LEFT + 0.4*DOWN, ORIGIN],
        )
        self.move_to(ORIGIN)
        self.scale(.35)

class TrianglePointer(VMobject):
    CONFIG = {
        "stroke_width" : 0,
        "fill_opacity" : 1.0,
        "color"  : WHITE,
        "mark_paths_closed" : True,
        "close_new_points" : True,
        "considered_smooth" : False,
        "width"   : 0.2,
        "height"  : 0.2,
    }
    def generate_points(self):
        y, x = self.height, self.width/2.
        self.set_anchor_points([
            ORIGIN,
            ORIGIN + UP*y + LEFT*x,
            ORIGIN + UP*y + RIGHT*x,
        ], mode = "corners")
