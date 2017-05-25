#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *

def geom_seq(ratio, ini_val = 1):
    def f(n):
        return ini_val * (ratio ** n)
    return f

def norm(u):
    return np.sqrt(np.dot(u, u))
def point_dist(x, y):
    return norm(x-y)

class Ordinal(VMobject):
    CONFIG = {
        "thickness" : DEFAULT_POINT_THICKNESS,
        "height"    : 1,
        "x0"        : -4,
        "x1"        : 4,
    }
    def __init__(self, *args, **kwargs):
        VMobject.__init__(self, *args, **kwargs)
        self.ini_size = np.array((self.x1 - self.x0, self.height, self.thickness))

    def to_steps(self):
        return VMobject(*[subord.to_steps() for subord in self.submobjects])

class OrdinalOne(Ordinal):
    def __init__(self, **kwargs):
        Ordinal.__init__(self, **kwargs)

        self.add(Line(self.x0*RIGHT + self.height*UP,
                      self.x0*RIGHT + self.height*DOWN,
                      stroke_width = self.thickness))

    def to_steps(self):
        size = self.x1 - self.x0
        x_dist = size*0.2
        y_dist = size*0.4
        a0 = self.x0*RIGHT + x_dist*RIGHT + y_dist*UP
        a1 = self.x1*RIGHT - x_dist*RIGHT + y_dist*UP
        arc = VMobject(
            stroke_width = self.thickness,
            color = YELLOW
        )
        arc.set_anchors_and_handles(
            [self.x1 * RIGHT, self.x0 * RIGHT], [a1], [a0]
        )

        #if self.x1 - self.x0 > 0.3:
        #    arc.add_tip(0.15*(self.x1 - self.x0))
        return VGroup(arc)

class LimitOrdinal(Ordinal):
    CONFIG = { # (x, height, thickness)
        "min_size"              : np.array((0.0001, 0.0001, 0.0001)),
        "seq"                   : geom_seq(np.array((0.9, 0.95, 0.95))),
        "subord_dec"            : 4
    }
    def __init__(self, SubOrd, **kwargs):
        Ordinal.__init__(self, **kwargs)
        self.SubOrd = SubOrd

        self.n = 0
        while self.add_subordinal(): pass

    def add_subordinal(self, allow_micro = False):
        size = self.ini_size * self.seq(self.n)
        if not allow_micro and self.n > 0 and (size < self.min_size).any(): return False

        (x0, h, t) = size
        x0 = self.x1 - x0
        x1 = (self.ini_size * self.seq(self.n+1))[0]
        x1 = self.x1 - x1

        def subseq(n):
            return ((x0-self.x0)*self.seq(self.subord_dec*n) + (self.x1-x0)*self.seq(n)) / (self.x1-self.x0)

        #subpow = np.array((0.9, 0.95, 0.95))
        #subpow2 = np.array((0.9, 0.95, 0.95))**4
        #subpow = ((x0-self.x0)*subpow2 + (self.x1-x0)*subpow) / (self.x1-self.x0)

        self.submobjects.append(self.SubOrd(
            thickness = t, height = h,
            x0 = x0, x1 = x1,
            order = self.n,
            min_size = np.array((0.01, 0.01, 0.01)),
            seq = subseq,
        ))
        self.n += 1
        return True

    def add_n_more_submobjects(self, n_more):
        for i in range(n_more): self.add_subordinal(True)

class OrdinalOmega(LimitOrdinal):
    def __init__(self, **kwargs):
        LimitOrdinal.__init__(self, OrdinalOne, **kwargs)
