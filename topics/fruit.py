from mobject import Mobject
from mobject.svg_mobject import SVGMobject
from helpers import *
from eost import deterministic

import constants
import os

__all__ = ['Pear', 'Apple']

class Fruit(SVGMobject):
    CONFIG = {
        "initial_scale_factor" : 0.0016
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs, locals())
        if self.file_name is None:
            self.file_name = "fruit/"+self.fruit_type
        SVGMobject.__init__(self, **kwargs)
        self[1].set_color(LIGHT_BROWN)
        self.set_color(self.color)

    def set_color(self, color):
        self.color = color
        self[0].set_stroke(color = color)
        self[0].set_fill(color = color_gradient((BLACK, color), 4)[1], opacity = 1)

color_indices='ABCDE'

def get_color(base_color,color,color_index):
    if color is not None:
        return color
    if color_index is None:
        import random
        color_index = random.randint(0,len(color_indices))
    return getattr(
        constants,
        base_color + "_" + color_indices[color_index % len(color_indices)]
    )

class Pear(Fruit):
    CONFIG = {
        "fruit_type" : "pear",
    }

    def __init__(self,color_index=None,color=None,**kwargs):
        self.color=get_color(base_color="YELLOW",color=color,color_index=color_index)
        Fruit.__init__(self,**kwargs)

class Apple(Fruit):
    CONFIG = {
        "fruit_type" : "apple",
    }

    def __init__(self,color_index=None,color=None,**kwargs):
        self.color=get_color(base_color="RED",color=color,color_index=color_index)
        Fruit.__init__(self,**kwargs)
