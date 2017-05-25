from scene import Scene
from animation.simple_animations import *
from .widgets import *

class Scene1(Scene):
    def construct(self):
        p = Pear().center()
        a = Apple().next_to(p)
        self.play(ShowCreation(p))
        self.play(ShowCreation(a))
        self.dither()
