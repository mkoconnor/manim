from mobject import Mobject
from mobject.vectorized_mobject import VGroup
from mobject.svg_mobject import SVGMobject
from helpers import *
from constants import *

class RunnerPic(SVGMobject):
    CONFIG = {
        "initial_scale_factor" : 0.016
    }
    def __init__(self, phase, **kwargs):
        digest_config(self, kwargs, locals())
        if self.file_name is None:
            self.file_name = "runners/"+self.runner_name+str(self.phase)
        SVGMobject.__init__(self, **kwargs)

        self.init_runner()

def dark_color(color):
    return color_gradient((BLACK, color), 4)[1]
        
class TurtlePic(RunnerPic):
    CONFIG = {
        "runner_name" : "turtle",
    }
    def init_runner(self):

        self.leg1, self.leg2, self.crust, self.head, self.eye \
            = self.submobjects

        self.crust.set_color(GREEN)
        self.head.set_color(LIGHT_BROWN)

        for part in (self.crust, self.head):
            part.set_fill(dark_color(part.color),
                          opacity = 1)

        self.legs = VGroup(self.leg1, self.leg2)
        self.legs.set_stroke(color = LIGHT_BROWN,
                             width = 3*DEFAULT_POINT_THICKNESS)

        self.eye.set_style_data(stroke_width = 0,
                                fill_opacity = 1,
                                fill_color = WHITE)

class RabbitPic(RunnerPic):
    CONFIG = {
        "runner_name" : "rabbit",
    }
    def init_runner(self):

        self.back, self.front_leg, self.back_leg, self.head, self.eye, self.tail \
            = self.submobjects

        self.set_color(LIGHT_BROWN)
        self.set_fill(color = DARK_BROWN, opacity = 1)
        self.tail.set_style_data(stroke_color = WHITE,
                                 fill_color = GREY)
        self.eye.set_style_data(stroke_width = 0,
                                fill_color = WHITE)

class AchilesPic(RunnerPic):
    CONFIG = {
        "initial_scale_factor" : 0.006,
        "runner_name" : "achiles",
    }
    def init_runner(self):

        self.shield, self.body, self.legs, self.arms, \
            self.sword_hilt1, self.sword_hilt2, self.sword, \
            self.head, self.hair, self.eyes \
            = self.submobjects

        self.head.set_fill(color = BLACK, opacity = 1)

        self.sword.set_fill(color = GREY, opacity = 1)
        self.shield.set_fill(color = dark_color(RED), opacity = 1)

