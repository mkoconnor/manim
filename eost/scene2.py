from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from .widgets import *
from animation.simple_animations import *
from animation.transform import *
from .matching import get_matching
import deterministic

from .ordinal import *

def fruit_omega(Fruit):
    class NumberOrdinal(OrdinalOne):
        def __init__(self, **kwargs):
            Ordinal.__init__(self,**kwargs)
            fruit = Fruit(random.randint(0,5))
            center = (self.x0 + self.x1) / 2.0
            fruit.shift((center - fruit.get_center()[0],0,0))
            fruit.scale_to_fit_width((self.x1 - self.x0) * 0.7)
            if fruit.get_height() > self.height:
                fruit.scale_to_fit_height(self.height)
            self.add(fruit)

    class OrdinalOmega(LimitOrdinal):
        def __init__(self, **kwargs):
            LimitOrdinal.__init__(self, NumberOrdinal, **kwargs)
    return OrdinalOmega()

def number_submobjects(mobj,direction):
    zero = TexMobject("0")
    zero.next_to(mobj.submobjects[0],direction=direction)
    submobjs = [zero]
    for i in xrange(1,5):
        submobj = TexMobject(str(i))
        submobj.next_to(submobjs[-1])
        submobj.shift((mobj.submobjects[i].get_center()[0]-submobj.get_center()[0],0,0))
        submobjs.append(submobj)
    dots = TexMobject("\\cdots").next_to(submobjs[-1])
    submobjs.append(dots)
    return Group(*submobjs)

class Scene2(Scene):
    def construct(self):
        apples = fruit_omega(Apple).center()
        apple_numbers = number_submobjects(apples,direction=UP)
        Group(apples,apple_numbers).to_edge(UP)
        self.play(ShowCreation(apples),Write(apple_numbers))
        pears = fruit_omega(Pear).center()
        pear_numbers = number_submobjects(pears,direction=DOWN)
        Group(pears,pear_numbers).to_edge(DOWN)
        self.play(ShowCreation(pears), Write(pear_numbers))
        self.dither()
        matching = get_matching(
            Group(*apples.submobjects[:-1]),
            Group(*pears.submobjects[:-1])
        )
        self.play(ShowCreation(matching))
        self.dither()
        one_extra_apple = get_matching(
            Group(*apples.submobjects[1:]),
            Group(*pears.submobjects[:-1])
        )
        self.play(Transform(matching,one_extra_apple))
        self.dither()
        one_extra_pear = get_matching(
            Group(*apples.submobjects[:-1]),
            Group(*pears.submobjects[1:])
        )
        self.play(Transform(matching,one_extra_pear))
        self.dither()
