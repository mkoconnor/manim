from geometry import Cross
from mobject.vectorized_mobject import VMobject
from constants import *
from helpers import *
from topics.geometry import Line, Circle
from animation.simple_animations import Uncreate
from mobject.tex_mobject import TexMobject

class IconNo(Cross):
    CONFIG = {
        "color" : RED,
    }

class IconYes(VMobject):
    CONFIG = {
        "color" : GREEN,
    }
    def generate_points(self):
        self.set_anchors_and_handles(
            [0.8*LEFT + 0.8*UP,   0.8*LEFT + 0.4*DOWN, RIGHT + 1.1*UP],
            [    LEFT + 0.2*DOWN, 0.6*LEFT + 0.4*DOWN],
            [    LEFT + 0.4*DOWN, ORIGIN],
        )
        self.move_to(ORIGIN)
        self.scale(.35)

class TrianglePointer(VMobject):
    CONFIG = {
        "stroke_width" : 0,
        "fill_opacity" : 1.0,
        "color"  : WHITE,
        "mark_paths_closed" : True,
        "close_new_points" : True,
        "considered_smooth" : False,
        "width"   : 0.2,
        "height"  : 0.2,
    }
    def generate_points(self):
        y, x = self.height, self.width/2.
        self.set_anchor_points([
            ORIGIN,
            ORIGIN + UP*y + LEFT*x,
            ORIGIN + UP*y + RIGHT*x,
        ], mode = "corners")

    def to_bar(self, bar, buff = 0.1):
        while not isinstance(bar, Line):
            bar = bar[0]
        start = bar.get_start()
        end = bar.get_end()
        buff = (start-end)*0.1
        self.rotate(angle_of_vector(end-start) + np.pi/2)
        self.shift(start - self.points[0] + buff)

        return self

class Counter(Circle):
    CONFIG = {
        "stroke_color" : GREY,
        "fill_color"   : DARK_GREY,
        "fill_opacity" : 0.5,
    }
    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)
        self.rotate(np.pi/2)
        
    def count_from(self, start, scene):
        scene.add(self)
        for n in reversed(range(1,start+1)):
            white = self.copy()
            white.set_fill(opacity = 0)
            white.highlight(WHITE)
            number = TexMobject(str(n))
            number.move_to(self)
            number.scale_to_fit_height(self.get_height()/2)
            scene.add(number)
            scene.play(Uncreate(white))
            scene.remove(number)
        scene.remove(self)

class MirekOlsakLogo(VMobject):

    def __init__(self, camera):
        VMobject.__init__(self)

        stroke = 20
        factor = sum(PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_shape"]) / sum(camera.pixel_shape)
        stroke /= factor
        self.add(Circle())
        h1, h2, x = 1, 1.5, 0.5
        y = -np.sqrt(1-x**2)+h1
        self.add(Line([-x, y, 0], [-x, y-h1, 0]))
        self.add(Line([0, 1, 0], [0, 1-h2, 0]))
        self.add(Line( [x, y, 0],  [x, y-h1, 0]))

        self.set_stroke(color = "#00ffff", width = stroke)
        self.to_corner(RIGHT+DOWN)
