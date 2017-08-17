from mobject import Mobject
from mobject.vectorized_mobject import *
from mobject.svg_mobject import SVGMobject
from helpers import *
from constants import *
from animation.simple_animations import *
from animation.transform import *
from topics.icons import TrianglePointer
from topics.geometry import *

class RunnerPic(SVGMobject):
    CONFIG = {
        "initial_scale_factor" : 0.01
    }
    def __init__(self, phase, **kwargs):
        digest_config(self, kwargs, locals())
        if self.file_name is None:
            self.file_name = "runners/"+self.runner_name+str(self.phase)
        SVGMobject.__init__(self, **kwargs)

        self.init_pic()

    def init_pic(self):
        pass

def dark_color(color):
    return color_gradient((BLACK, color), 4)[1]

class TurtlePic(RunnerPic):
    CONFIG = {
        "initial_scale_factor" : 0.007,
        "runner_name" : "turtle",
        "color" : GREEN
    }
    def init_pic(self):

        self.leg1, self.leg2, self.crust, self.head, self.eye \
            = self.submobjects

        self.set_color(self.color)
        self.head.set_color(LIGHT_BROWN)
        self.head.set_fill(dark_color(self.head.color),
                           opacity = 1)

        self.legs = VGroup(self.leg1, self.leg2)
        self.legs.set_stroke(color = LIGHT_BROWN,
                             width = 3*DEFAULT_POINT_THICKNESS)

        self.eye.set_style_data(stroke_width = 0,
                                fill_opacity = 1,
                                fill_color = WHITE)

    def set_color(self, color):
        self.color = color
        self.crust.color = color
        self.crust.set_stroke(color = color)
        self.crust.set_fill(dark_color(self.crust.color),
                            opacity = 1)

class RabbitPic(RunnerPic):
    CONFIG = {
        "runner_name" : "rabbit",
        "color" : LIGHT_BROWN
    }
    def init_pic(self):

        self.back, self.front_leg, self.back_leg, self.head, self.eye, self.tail \
            = self.submobjects

        self.set_color(LIGHT_BROWN)
        self.set_fill(color = DARK_BROWN, opacity = 1)
        self.tail.set_style_data(stroke_color = WHITE,
                                 fill_color = GREY)
        self.eye.set_style_data(stroke_width = 0,
                                fill_color = WHITE)

class AchilesStickmanPic(RunnerPic):
    CONFIG = {
        "initial_scale_factor" : 0.0025,
        "runner_name" : "achiles-stickman",
        "color" : WHITE
    }
    def init_pic(self):

        self.shield, self.body, self.legs, self.arms, \
            self.sword_hilt1, self.sword_hilt2, self.sword, \
            self.head, self.hair, self.eyes \
            = self.submobjects

        self.head.set_fill(color = BLACK, opacity = 1)

        self.sword.set_fill(color = GREY, opacity = 1)
        self.shield.set_fill(color = dark_color(RED), opacity = 1)

class AchilesPic(RunnerPic):
    CONFIG = {
        "initial_scale_factor" : 0.0025,
        "runner_name" : "achiles",
        "color" : ORANGE
    }
    def init_pic(self):

        self.shield, self.helmet, self.legl, self.legr, self.arml, \
            self.body, self.head, self.eyes, self.skirt, self.sword_handle, \
            self.armr, self.sword_blade, self.sword_hilt,  \
            = self.submobjects

        for part in self.submobjects: part.set_color(ORANGE)
        for iron in [self.shield, self.head, self.eyes, self.sword_blade]:
            iron.set_color(WHITE)
        for wood in [self.sword_hilt, self.sword_handle]:
            wood.set_color(GREY)
        self.skirt.set_color(GREEN)
        self.helmet.set_color(RED)

        for part in self.submobjects:
            part.set_fill(dark_color(part.color),
                          opacity = 1)


class Runner(VMobject):
    CONFIG = {
        "phase_gen": None,
        "pointer_pos": DOWN,
        "dist" : 1.1,
    }
    def __init__(self, **kwargs):

        digest_config(self, kwargs, locals())
        VMobject.__init__(self, **kwargs)

        self.phase = [self.phase_gen(i, **kwargs)
                      for i in range(2)]

        self.body = self.phase[0].deepcopy()
        self.cur_phase = 0
        self.color = self.body.color

        self.add(self.body)

        self.pointer = TrianglePointer(color = self.color)
        angle = - np.arctan2(*self.pointer_pos[:2]) + np.pi
        self.pointer.rotate(angle)
        self.pointer.next_to(self.body, self.pointer_pos)

        self.add(self.pointer)

    def set_color(self, color):
        self.color = color
        mob_list = self.phase + [self.body, self.pointer]
        for mob in mob_list:
            mob.set_color(color)

    def move_to(self, mob):

        self.shift(mob.get_edge_center(LEFT) - self.dist*self.pointer_pos
                   - self.pointer.get_edge_center(self.pointer_pos))
        return self

    def step_to(self, mob):
        self.cur_phase = 1-self.cur_phase
        dest = self.deepcopy()
        dest.move_to(mob)
        dest.update_phase()
        return Transform(self, dest)

    def update_phase(self):
        next_body = self.phase[self.cur_phase].copy()
        next_body.move_to(self.body)
        self.body.submobjects = next_body.submobjects

    def run_in(self):
        end = self.body.get_center()
        start = end*UP + (SPACE_WIDTH + self.body.get_width())*LEFT
        animations = [
            Transform(self.body, self.phase[1], rate_func = there_and_back),
            MoveAlongPath(self.body, Line(start, end)),
            FadeIn(self.pointer),
        ]

        return AnimationGroup(*animations, run_time = 1.5)

class Turtle(Runner):
    CONFIG = {
        "phase_gen" : TurtlePic
    }

class Rabbit(Runner):
    CONFIG = {
        "phase_gen" : RabbitPic
    }
    def step_to(self, mob):
        dest = self.deepcopy()
        dest.move_to(mob)
        start = self.body.get_center()
        end = dest.body.get_center()
        animations = [
            Transform(self.body, self.phase[1], rate_func = there_and_back),
            MoveAlongPath(self.body, Line(start, end)),
            Transform(self.pointer, dest.pointer),
        ]

        return AnimationGroup(*animations)


class Achiles(Runner):
    CONFIG = {
        "phase_gen" : AchilesPic
    }
