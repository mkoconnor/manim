from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from topics.objects import VideoSeries
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo
from topics.objects import BraceText, Counter
import eost.deterministic

class Chapter7OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 7\\\\ Omega One",
    }

class Chapter7OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "From his","paradise","that Cantor with us unfolded, we hold our breath in awe; knowing, we shall","not be expelled."
        ],
        "highlighted_quote_terms" : {
            "paradise" : YELLOW,
            "not be expelled" : GREEN,
        },
        "author" : "David Hilbert"
    }

class GradientLine(Line):
    CONFIG = {
        "segment_num" : 200
    }
    def __init__(self, start, end, *colors, **kwargs):
        self.init_kwargs = kwargs
        Line.__init__(self, start, end, **kwargs)
        self.gradient_highlight(*colors)

    def generate_points(self):
        points = [
            interpolate(self.start, self.end, alpha)
            for alpha in np.linspace(0, 1, self.segment_num)
        ]
        for p1, p2 in zip(points, points[1:]):
            self.add(Line(p1, p2, **self.init_kwargs))

        return self

    def get_start(self):
        if len(self) > 0:
            return self[0].points[0]
        else:
            return self.start

    def get_end(self):
        if len(self) > 0:
            return self[-1].points[-1]
        else:
            return self.end

class Omega1(VMobject):
    def __init__(self):
        VMobject.__init__(self)
        line = GradientLine(2*LEFT, 4*RIGHT, BLACK, WHITE)
        ordinal = LimitOrdinal(lambda **kwargs: OrdinalOmega(**kwargs),
                               q = (0.9, 0.7, 0.8), x0 = -4, x1 = 0)
        self.add(line, ordinal)

class Omega1Picture(Scene):
    def construct(self):

        omega1 = Omega1()

        self.add(omega1)
