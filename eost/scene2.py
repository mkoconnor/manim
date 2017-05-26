from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from .widgets import *
from animation.simple_animations import *
from animation.transform import *
from .matching import get_matching

class NumberLine(Mobject):
    def __init__(self,mobj_creator,direction,n=10):
        unnumbered_mobjs = []
        numbered_mobjs = []

        def make_number_mobj(n):
            text = TextMobject(str(n))
            buff = Rectangle(color=BLACK,height=1, width=1.9)
            return Group(buff,text)

        for i in xrange(n):
            copy = mobj_creator(i)
            unnumbered_mobjs.append(copy)
            number_mobj = make_number_mobj(i)
            number_mobj.next_to(copy,direction=direction)
            numbered_mobjs.append(Group(copy,number_mobj))

        Mobject.__init__(self, *numbered_mobjs)
        self.arrange_submobjects()

class Scene2(Scene):
    def construct(self):
        apples = NumberLine(Apple,direction=UP).to_edge(UP).to_edge(LEFT)
        pears = NumberLine(Pear,direction=DOWN).to_edge(DOWN).to_edge(LEFT)
        self.play(ShowCreation(apples))
        self.play(ShowCreation(pears))
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
