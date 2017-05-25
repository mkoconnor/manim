from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from .widgets import *
from animation.simple_animations import *
from animation.transform import *

class NumberLine(Mobject):
    def __init__(self,mobj,n=7):
        unnumbered_mobjs = []
        numbered_mobjs = []

        def make_number_mobj(n):
            text = TextMobject(str(n))
            dot = Dot().next_to(text,direction=DOWN)
            Group(text,dot).center()
            buff = Rectangle(color=BLACK,height=1, width=1.9)
            return Group(buff,text,dot)

        for i in xrange(n):
            copy = mobj.copy()
            unnumbered_mobjs.append(copy)
            number_mobj = make_number_mobj(i)
            number_mobj.next_to(copy,direction=DOWN)
            numbered_mobjs.append(Group(copy,number_mobj))

        last_numbered_mobj = None
        for numbered_mobj in numbered_mobjs:
            if last_numbered_mobj is not None:
                numbered_mobj.next_to(last_numbered_mobj)
            last_numbered_mobj = numbered_mobj
        self.unnumbered_mobjs = unnumbered_mobjs
        self.numbered_mobjs = numbered_mobjs
        Mobject.__init__(self, *numbered_mobjs)

class Scene2(Scene):
    def construct(self):
        # I think the apples and pears look better a little smaller
        # than they did in scene 1
        scale_factor = 0.9
        apple = Apple().scale_in_place(scale_factor)
        pear = Pear().scale_in_place(scale_factor)
        apples = NumberLine(apple).to_edge(UP).to_edge(LEFT)
        pears = NumberLine(pear).to_edge(DOWN).to_edge(LEFT)
        self.play(ShowCreation(apples))
        self.play(ShowCreation(pears))
        self.dither()
