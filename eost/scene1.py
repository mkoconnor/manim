from scene import Scene
from animation.simple_animations import *
from .widgets.pear import *

class Scene1(Scene):
    def construct(self):
        p = Pear().center()
        self.play(ShowCreation(p))
        self.dither()
