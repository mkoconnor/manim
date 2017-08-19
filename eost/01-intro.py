#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo

class Chapter1OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 1\\\\ Introduction",
    }

class Chapter1OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "No one shall expel us from the","Paradise","that Cantor has created."
        ],
        "highlighted_quote_terms" : {
            "Paradise" : YELLOW,
        },
        "author" : "David Hilbert"
    }
