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

    def to_steps(self, **kwargs):
        return VMobject(*[subord.to_steps(**kwargs) for subord in self.submobjects])

    def make_deeper(self):
        for subord in self.submobjects: subord.make_deeper()

    def fix_x1(self):
        for subord0, subord1 in zip(self.submobjects, self.submobjects[1:]):
            subord0.x1 = subord1.x0

class StepCurve(VMobject):
    CONFIG = {
        "x_handle"      : 0.2,
        "y_handle"      : 0.4,
        "start"         : ORIGIN,
        "end"           : RIGHT,
    }
    def __init__(self, **kwargs):
        digest_locals(self)
        VMobject.__init__(self, **kwargs)

    def generate_points(self):
        a0 = self.start
        a1 = self.end
        x_dist = a1[0] - a0[0]
        y_dist = a1[1] - a0[1]
        h0 = interpolate(a0, a1, self.x_handle) + self.y_handle*abs(x_dist)*UP
        h1 = interpolate(a1, a0, self.x_handle) + self.y_handle*abs(x_dist)*UP
        #self.add(Dot(h0))
        #self.add(Dot(h1))
        self.set_anchors_and_handles(
            [a0, a1], [h0], [h1]
        )

def seq_to_jumps(bars, color = WHITE):

    jumps = []
    for i in range(len(bars)-1):
        stroke_width = max(bars[i].stroke_width, bars[i+1].stroke_width)
        jump = StepCurve(
            start = bars[i].get_edge_center(UP), 
            end = bars[i+1].get_edge_center(UP),
            stroke_width = stroke_width)
        jump.set_color(color)
        jumps.append(jump)

    return VGroup(*jumps)

class OrdinalObj(Ordinal):
    CONFIG = {
        "pos" : ORIGIN,
    }
    def __init__(self, obj, **kwargs):
        Ordinal.__init__(self, **kwargs)
        obj.scale(self.height)
        obj.set_stroke(width = self.thickness)
        obj.shift(self.x0*RIGHT - obj.get_critical_point(self.pos))

        self.add(obj)

    def make_deeper(self):
        self.submobjects = [self.copy()]

    def to_steps(self, h_placement = 0):

        step = StepCurve(
            start = self.x0*RIGHT + h_placement*self.height*UP,
            end = self.x1*RIGHT + h_placement*self.height*UP,
            stroke_width = self.thickness)
        step.shift(self.get_center() - RIGHT*self.x0)

        #if self.x1 - self.x0 > 0.3:
        #    arc.add_tip(0.15*(self.x1 - self.x0))
        return VGroup(step)

    def add_description(self, desc, size = 0.8, direction = UP, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, **kwargs):
        scale = size*(self.x1 - self.x0) / desc.get_width()
        if scale < 1: desc.scale(scale)
        else: scale = 1
        desc.next_to(self, direction = direction, buff = buff*scale, **kwargs)

class OrdinalOne(OrdinalObj):
    def __init__(self, **kwargs):
        OrdinalObj.__init__(self, Line(UP, DOWN), **kwargs)

class OrdinalSum(Ordinal):
    def __init__(self, *args, **kwargs):
        Ordinal.__init__(self, **kwargs)

        prev_x = self.x0
        args += (1,)
        for SubOrd, x1 in zip(args[::2], args[1::2]):
            x1 = interpolate(self.x0, self.x1, x1)

            kwargs['x0'] = prev_x
            kwargs['x1'] = x1
            self.add(SubOrd(**kwargs))

            prev_x = x1

class OrdinalFiniteProd(Ordinal):
    def __init__(self, SubOrd, prod, **kwargs):
        Ordinal.__init__(self, **kwargs)

        x_list = np.linspace(self.x0, self.x1, prod+1)
        x0_list = x_list[:-1]
        x1_list = x_list[1:]
        for x0, x1 in zip(x0_list, x1_list):
            kwargs['x0'] = x0
            kwargs['x1'] = x1
            self.add(SubOrd(**kwargs))

class OrdinalFinite(OrdinalFiniteProd):
    def __init__(self, num, **kwargs):
        OrdinalFiniteProd.__init__(self, OrdinalOne, num, **kwargs)

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

    def add_descriptions(self, desc_maker, **kwargs):
        descriptions = []
        for i, subord in enumerate(self.submobjects):
            desc = desc_maker(i)
            subord.add_description(desc, **kwargs)
            descriptions.append(desc)
            if desc.get_height() < pixel_size or desc.get_width() < pixel_size: break

        return VGroup(*descriptions)

class LimitSubOrdinal(LimitOrdinal):
    def __init__(self, sub_list, **kwargs):
        Ordinal.__init__(self, **kwargs)
        self.submobjects = sub_list

class OrdinalOmega(LimitOrdinal):
    def __init__(self, **kwargs):
        LimitOrdinal.__init__(self, OrdinalOne, **kwargs)

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

def make_ordinal_matching(o1, o2):
    if not isinstance(o1, Ordinal):
        return Line(o1.get_edge_center(DOWN) + 0.05*DOWN,
                    o2.get_edge_center(UP) + 0.05*UP,
                    stroke_width = (o1.stroke_width + o2.stroke_width) / 2,
                    #stroke_width = max(o1.stroke_width, o2.stroke_width),
        )

    else: return VGroup(*[
            make_ordinal_matching(sub_o1, sub_o2)
            for sub_o1, sub_o2 in zip(o1, o2)
    ])

def make_half_ordinal(ordinal, trunc_down = True):
    for line in ordinal.family_members_with_points():
        if trunc_down: start = line.get_start()
        else: start = line.get_end()
        end = line.get_center()
        line.set_points_as_corners([start, end])
    return ordinal

