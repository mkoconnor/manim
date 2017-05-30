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

pixel_size = SPACE_WIDTH*2 / DEFAULT_WIDTH

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

    def make_deeper(self):
        for subord in self.submobjects: subord.make_deeper()

class OrdinalOne(Ordinal):
    def __init__(self, **kwargs):
        Ordinal.__init__(self, **kwargs)
        #print(self.x0 / pixel_size)

        self.add(Line(self.x0*RIGHT + self.height*UP,
                      self.x0*RIGHT + self.height*DOWN,
                      stroke_width = self.thickness))

    def make_deeper(self):
        self.submobjects = [self.copy()]

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

    def add_description(self, desc, size = 0.8, direction = UP, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, **kwargs):
        scale = size*(self.x1 - self.x0) / desc.get_width()
        if scale < 1: desc.scale(scale)
        else: scale = 1
        desc.next_to(self, direction = direction, buff = buff*scale, **kwargs)

class LimitOrdinal(Ordinal):
    CONFIG = {
        "zero_at_fg" : False,
    }
    def __init__(self, SubOrd, q = (0.9, 0.95, 0.95), min_size = (1, 1, 0.1), **kwargs): # (x, height, thickness)
        Ordinal.__init__(self, **kwargs)
        self.SubOrd = SubOrd

        q = np.array(q)
        min_size = np.array(min_size) * np.array((pixel_size, pixel_size, 1))

        ini_size = np.array((self.x1-self.x0, self.height, self.thickness), dtype = float)
        cur_size = np.array(ini_size, dtype = float)

        n = 0
        while True:
            (x, h, t) = cur_size
            if n > 0:
                if (cur_size < min_size).any(): break
                if (last_x - x) < pixel_size*max(t/2, 0.8):
                    cur_size *= q
                    continue

            x1 = x * q[0]
            x0 = self.x1 - x
            x1 = self.x1 - x1

            sub_min_x = (t*q[2])*0.7
            sub_min_size = np.array(min_size)
            if sub_min_size[0] < sub_min_x: sub_min_size[0] = sub_min_x

            self.submobjects.append(
                self.SubOrd(
                    thickness = t,
                    height = h,
                    x0 = x0, x1 = x1,
                    min_size = sub_min_size,
                    q = q,
                    order = n,
                ))

            n += 1
            last_x = x
            cur_size *= q

    def add_n_more_submobjects(self, n_more):
        added = self[-1].copy()
        added.set_stroke(width = 0)
        self.submobjects += [added.copy() for _ in range(n_more)]

class LimitSubOrdinal(LimitOrdinal):
    def __init__(self, sub_list, **kwargs):
        Ordinal.__init__(self, **kwargs)
        self.submobjects = sub_list

class OrdinalOmega(LimitOrdinal):
    def __init__(self, **kwargs):
        LimitOrdinal.__init__(self, OrdinalOne, **kwargs)

    def add_descriptions(self, desc_maker, **kwargs):
        descriptions = []
        for i, subord in enumerate(self.submobjects):
            desc = desc_maker(i)
            subord.add_description(desc, **kwargs)
            descriptions.append(desc)
            if desc.get_height() < pixel_size or desc.get_width() < pixel_size: break

        return VGroup(*descriptions)

def make_ordinal_power(power, **kwargs):
    if power == 0: return OrdinalOne(**kwargs)    
    return LimitOrdinal(lambda **kwargs: make_ordinal_power(power-1, **kwargs),
                        **kwargs)

def extract_ordinal_subpowers(o):
    if type(o) == OrdinalOne: return ([o[0]],)

    result = None
    for subord in o:
        partial = extract_ordinal_subpowers(subord)
        if result is None: result = partial
        else:
            for i, layer in enumerate(result):
                layer += partial[i]

    return ([result[0][0]],)+result
