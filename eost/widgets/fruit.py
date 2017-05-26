from mobject import Mobject
from mobject.svg_mobject import SVGMobject
from helpers import *

import constants
import os

__all__ = ['Pear', 'Apple']

class Fruit(SVGMobject):

    def __init__(self, **kwargs):
        digest_config(self, kwargs, locals())
        file_name = os.path.join(
            os.path.dirname(__file__), "images", self.fruit_type+".svg"
        )
        SVGMobject.__init__(self, file_name = file_name, **kwargs)
        self.scale(0.0012)
        self[1].set_color(WHITE)
        self.set_color(self.color)

    def set_color(self, color):
        self.color = color
        self[0].set_stroke(color = color)
        self[0].set_fill(color = color_gradient((BLACK, color), 4)[1], opacity = 1)

class Pear(Fruit):
    CONFIG = {
        "fruit_type" : "pear",
        "color"      : YELLOW,
    }

class Apple(Fruit):
    CONFIG = {
        "fruit_type" : "apple",
        "color"      : RED,
    }
