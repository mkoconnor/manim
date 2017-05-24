from mobject import Mobject
from mobject.svg_mobject import SVGMobject
from constants import *

__all__ = ['Pear']

def load_svg(basename):
    import os
    file_name = os.path.join(
        os.path.dirname(__file__),
        "images", "pear", basename + ".svg"
    )
    return SVGMobject(
        file_name=file_name,
        should_center=False
    )

class Pear(Mobject):
    def __init__(self):
        outline = load_svg("pear-outline").set_stroke(color=DARK_BROWN,width=0)
        outline.set_fill(color=DARK_BROWN)
        yellow_fill = load_svg("pear-yellow-fill").set_fill(color=YELLOW)
        yellow_fill.set_stroke(width=0)
        green_fill = load_svg("pear-green-fill").set_fill(color=GREEN)
        green_fill.set_stroke(width=0)
        Mobject.__init__(self,outline,yellow_fill,green_fill)
        self.center()
        self.scale(0.01)
