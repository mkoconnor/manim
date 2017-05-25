from mobject import Mobject, Group
from scene import Scene
from animation.simple_animations import *
from .widgets import *

def in_a_row(mobj,n):
    mobjs = []
    last_mobj = None
    for _ in xrange(n):
        this_mobj = mobj.copy()
        if last_mobj is not None:
            this_mobj.next_to(last_mobj)
        last_mobj = this_mobj
        mobjs.append(this_mobj)
    return mobjs

class Scene1(Scene):
    def construct(self):
        apples = in_a_row(Apple(),5)
        pears = in_a_row(Pear(),4)
        apple_group = Group(*apples).center().to_edge(UP)
        pear_group = Group(*pears).center().to_edge(DOWN)
        self.play(ShowCreation(apple_group))
        self.play(ShowCreation(pear_group))
        self.dither()
