from mobject import Mobject
from mobject.svg_mobject import SVGMobject
import constants
import os

__all__ = ['Pear', 'Apple']

class Fruit(Mobject):
    def fruit_type(self):
        raise Exception("Define in subclass")

    def __init__(self,color=None):
        fruit_type = self.fruit_type()
        images_dir = os.path.join(
            os.path.dirname(__file__), "images", fruit_type
        )
        # Allow colors to be overridden by the passed in value
        def c(clr):
            if color is None:
                return clr
            else:
                return color
        def load_svg(basename):
            file_name = os.path.join(images_dir,basename)
            svg = SVGMobject(
                file_name = file_name,
                should_center = False
            )
            svg.set_stroke(width=0)
            if 'outline' in basename:
                svg.set_fill(color=c(constants.DARK_BROWN))
            else:
                try:
                    (_fruit,color,ext) = basename.split('-')
                    if ext == "fill.svg":
                        svg.set_fill(color=c(getattr(constants,color.upper())))
                except:
                    pass
            return svg
        svgs = [
            load_svg(basename)
            for basename in os.listdir(images_dir)
            if basename.endswith('svg') and '-' in basename
        ]
        Mobject.__init__(self,*svgs)
        self.center()
        self.scale(0.005)

class Pear(Fruit):
    def fruit_type(self):
        return "pear"

class Apple(Fruit):
    def fruit_type(self):
        return "apple"

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
