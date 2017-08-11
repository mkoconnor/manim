from scene import Scene
from eost.ordinal import *
from topics.runners import *

CIRCLE_DEC = 0.5

def to_spiral(mob):

    x = mob.points[:,0]
    y = mob.points[:,1]
    complex_points = 1j * x \
                     + 1.5 + 0.2*y - CIRCLE_DEC*x/(2*np.pi)
    complex_transformed = np.exp(complex_points)
    mob.points = np.stack([
        complex_transformed.imag,
        complex_transformed.real,
        np.zeros([len(complex_points)]),
    ], axis = 1)

def power_color(power):
    if power == 0: return WHITE
    else: return [YELLOW, ORANGE, RED, PURPLE, BLUE, GREEN][(power-1) % 6]

def color_interpolate(color0, color1, alpha):
    if alpha <= 0: return color0
    if alpha >= 1: return color1
    color0 = color_to_rgb(color0)
    color1 = color_to_rgb(color1)
    return rgb_to_color(interpolate(color0, color1, alpha))

def make_spiral():

    ordinal = []
    i = 0
    #for _ in range(3):
    while True:
        size = np.exp(i*CIRCLE_DEC)
        min_size = (size, size, 0.1)
        thickness = DEFAULT_POINT_THICKNESS / np.sqrt(size)
        if 1 / size < pixel_size or thickness < 0.1: break

        power = i+1
        if power > 5: power = max(3, 2*5-power)

        q = (0.7, 0.7, 0.8)

        cur_ordinal = make_ordinal_power(
            power,
            x0 = i*2*np.pi, x1 = (i+1)*2*np.pi,
            q = q,
            min_size = min_size,
            thickness = thickness,
        )
        subpowers = extract_ordinal_subpowers(cur_ordinal)
        for j,subord in enumerate(reversed(subpowers)):
            for mob in subord:
                mob[0].power = i+1-power+j

        subpowers[0][0].power = i

        ordinal.append(cur_ordinal)
        i += 1

    ordinal = VGroup(*ordinal)
    for mob in ordinal.family_members_with_points():
        mob.darken = (mob.get_center()[0] / (2*np.pi) - mob.power)/5
        mob.set_color(color_interpolate(power_color(mob.power), BLACK, mob.darken))

    return ordinal

def light_key(mobj):
    if hasattr(mobj, "darken"): return mobj.darken
    return 0

class SpiralScene(Scene):
    def construct(self):

        q = (0.7, 0.8, 0.8)

        behind_turtle = make_ordinal_power(1, q=q, x0=-12, x1 = -4, height = 0.5).shift(1.6*UP)

        ahead_turtle = make_ordinal_power(1, q=q, x0=4, x1 = 12, height = 0.5).shift(1.6*UP)
        behind_achiles = make_ordinal_power(2, q=q, x0=-12, x1 = -4, height = 0.5).shift(DOWN)
        ahead_achiles = make_ordinal_power(2, q=q, x0=4, x1 = 12, height = 0.5).shift(DOWN)

        for mob in behind_turtle.family_members_with_points():
            if abs(mob.get_center()[0]) > SPACE_WIDTH+1:
                to_spiral(mob)
        for mob in VGroup(*behind_achiles[:2]).family_members_with_points():
                mob.stretch(0.7, 0)
                mob.shift(UP + 2.5*LEFT)
                to_spiral(mob)

        turtle_ord = make_ordinal_power(1, q=q, height = 0.5).shift(1.6*UP)
        achiles_ord = make_ordinal_power(2, q=q, height = 0.5).shift(DOWN)
        turtle = Turtle().move_to(turtle_ord[0])
        achiles = Achiles(pointer_pos = UP).move_to(achiles_ord[0][0])
        turtle.shift(0.5*DOWN)
        achiles.shift(0.5*UP)
        turtle_desc = TexMobject("\\omega").next_to(turtle_ord[0], DOWN)
        achiles_desc = TexMobject("\\omega^2").next_to(achiles_ord[0][0], UP)

        rect = Rectangle(width = 2*SPACE_WIDTH, height = 2*SPACE_HEIGHT)

        spiral = make_spiral()
        straight_spiral = spiral.copy()
        spiral.apply_to_family(to_spiral)
        straight_spiral.stretch(0.5, 1)
        straight_spiral.shift(ahead_achiles.get_edge_center(RIGHT)
                              - straight_spiral[2][2].get_edge_center(LEFT))

        straight_spiral.submobjects[0] = behind_turtle
        behind_achiles.add_to_back(turtle_ord, ahead_turtle)
        straight_spiral.submobjects[1] = behind_achiles
        straight_spiral[2].submobjects[0] = achiles_ord
        straight_spiral[2].submobjects[1] = ahead_achiles

        spiral.align_data(straight_spiral)
        for src, dest in zip(straight_spiral.family_members_with_points(),
                             spiral.family_members_with_points()):
            src.highlight(dest.color)

        self.add(straight_spiral)

        #self.add(turtle, achiles, turtle_desc, achiles_desc, straight_spiral,
        #         rect)
        #for mob in self.mobjects:
        #    mob.points *= 0.25
        #return

        self.dither()

        self.play(ReplacementTransform(straight_spiral, spiral,
                                       prepare_family = True),
                  order_f = light_key,
                  run_time = 3)

        self.dither()
