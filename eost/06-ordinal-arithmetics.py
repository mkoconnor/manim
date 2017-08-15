from scene import Scene
from eost.ordinal import *
from topics.runners import *
from topics.icons import *

class Chapter5Recap(Scene):

    def construct(self):

        ordinal = OrdinalFiniteProd(OrdinalOmega, 2, x1 = 12)
        VGroup(*ordinal[1][3:]).highlight(DARK_GREY)
        ordinal.shift(2*LEFT + DOWN)
        self.play(FadeIn(ordinal))
        self.dither()

        brace_desc = TexMobject("\\omega+3")
        brace = Brace(VGroup(ordinal[0][0], ordinal[1][2]), DOWN)
        brace.put_at_tip(brace_desc)

        self.play(GrowFromCenter(brace), FadeIn(brace_desc))
        self.dither()

        bar = ordinal[1][3].copy().highlight(YELLOW)
        pointer = TrianglePointer(color = YELLOW).next_to(bar, UP)
        pointer_desc = brace_desc.copy().next_to(pointer, UP)
        self.play(ShowCreation(bar),
                  ShowCreation(pointer),
                  FadeIn(pointer_desc))
        self.dither()

        cur_topics = VGroup(
            TextMobject("Addition:", "$\\alpha+\\beta$"),
            TextMobject("Multiplication:", "$\\alpha\\cdot\\beta$"),
        )
        cur_topics.arrange_submobjects(DOWN, aligned_edge=LEFT)
        cur_topics.to_corner(UP+LEFT)

        last_topics = VGroup(
            TextMobject("Successor:", "$\\alpha+1$"),
            TextMobject("Supremum:", "$\\sup_{i\in I}(\\alpha_i)$"),
        )
        last_topics.arrange_submobjects(DOWN, aligned_edge=LEFT)
        last_topics.to_corner(UP+RIGHT)

        for topic in cur_topics.submobjects + last_topics.submobjects:
            topic[1].highlight(BLUE)

        self.play(FadeIn(cur_topics,
                         submobject_mode = "lagged_start"),
                  run_time = 3)
        self.dither()
        self.play(FadeIn(last_topics,
                         submobject_mode = "lagged_start"),
                  run_time = 3)
        self.dither()

        for i in range(1,4):
            pointer_dest = pointer.copy()
            pointer_dest.next_to(ordinal[1][i], UP)
            pointer_desc_dest = TexMobject("\\omega+"+str(i))
            pointer_desc_dest.next_to(pointer_dest, UP)
            self.play(Transform(pointer, pointer_dest),
                      Transform(pointer_desc, pointer_desc_dest))
            self.dither()
        

class Addition(Scene):
    def construct(self):

        self.force_skipping()
        omega = OrdinalOmega(x1 = 2).shift(UP+LEFT)
        omega_desc = TexMobject("\\omega").next_to(omega, UP)
        three = OrdinalFinite(3, x0 = 2).shift(UP+RIGHT)
        three_desc = TexMobject("3").next_to(three, UP)
        omega_g = VGroup(omega, omega_desc)
        three_g = VGroup(three, three_desc)

        VGroup(three, three_desc).highlight(GREEN)
        plus = TexMobject('+')
        plus.move_to((omega.get_edge_center(RIGHT) + three.get_edge_center(LEFT))/2)

        ord_sum = OrdinalSum(OrdinalOmega, 0.75,
                             lambda **kwargs: OrdinalFinite(3, **kwargs))
        ord_sum.shift(2.5*DOWN)
        ord_sum_desc = TexMobject("\\omega+3").next_to(ord_sum, UP)
        ord_sum[1].highlight(GREEN)

        self.play(FadeIn(omega), FadeIn(omega_desc))
        self.play(FadeIn(three), FadeIn(three_desc))
        self.play(Write(plus))
        self.dither()

        self.play(ReplacementTransform(omega.copy(), ord_sum[0]),
                  ReplacementTransform(three.copy(), ord_sum[1]))
        self.play(Write(ord_sum_desc),
                  ord_sum[1].highlight, WHITE)

        self.dither()

        self.play(FadeOut(VGroup(ord_sum, ord_sum_desc)))
        self.revert_to_original_skipping_status()

        omega_g_dest = omega_g.copy().shift(three.get_edge_center(RIGHT)
                                            - omega.get_edge_center(RIGHT))
        three_g_dest = three_g.copy().shift(omega.get_edge_center(LEFT)
                                            - three.get_edge_center(LEFT))
        omega_g_dest.highlight(GREEN)
        three_g_dest.highlight(WHITE)

        plus_dest = plus.copy()
        plus_dest.move_to((three_g_dest[0].get_edge_center(RIGHT)
                           + omega_g_dest[0].get_edge_center(LEFT))/2)
        self.play(Transform(plus, plus_dest, path_arc = -np.pi*0.5),
                  Transform(omega_g, omega_g_dest, path_arc = -np.pi*0.6),
                  Transform(three_g, three_g_dest, path_arc = -np.pi*0.8),
        )
        self.dither()

        ord_sum = OrdinalSum(lambda **kwargs: OrdinalFinite(3, **kwargs),
                             0.25, OrdinalOmega)
        ord_sum.shift(2.5*DOWN)
        ord_sum_desc = TexMobject("3+\\omega", "=\\omega").next_to(ord_sum, UP)
        ord_sum[1].highlight(GREEN)

        self.play(ReplacementTransform(omega.copy(), ord_sum[1]),
                  ReplacementTransform(three.copy(), ord_sum[0]))
        self.play(Write(ord_sum_desc[0]))
        self.dither()

        omega2 = OrdinalOmega()
        ord_sum_dest = VGroup(
            VGroup(*omega2[:3]).copy(),
            LimitSubOrdinal(omega2[3:]).copy(),
        )
        ord_sum_dest.move_to(ord_sum)
        ord_sum_dest.highlight(WHITE)

        self.play(Transform(ord_sum, ord_sum_dest),
                  Write(ord_sum_desc[1]))
        self.dither(3)

class RunnerScene(Scene):

    def transformed_desc(self, mobj, new_str):
        next_desc = TextMobject(":", "$"+new_str+"$")
        next_desc.shift(mobj[0][-1].get_center()
                        - next_desc[0].get_center())
        next_desc.set_color(mobj.color)
        return next_desc[1]

    def transform_desc(self, mobj, new_str):
        next_desc = self.transformed_desc(mobj, new_str)
        return Transform(mobj[1], next_desc)

    def change_desc(self, mobj, new_str):
        self.remove(mobj[1])
        mobj.submobjects[1] = self.transformed_desc(mobj, new_str)
        self.add(mobj[1])

    def runner_step(self, runner, desc, index, bar = None, omega_index = 0):
        if bar is None: bar = self.ordinal[omega_index][index]

        new_str = str(index)

        if omega_index > 0:
            if omega_index == 1: new_str = "\\omega+"+new_str
            else: new_str = "\\omega\\cdot"+str(omega_index)+"+"+new_str
            if index == 0: new_str = new_str[:-2]

        return AnimationGroup(
            runner.step_to(bar),
            self.transform_desc(desc, new_str),
        )

class TurtlesRace(RunnerScene):
    def introduce_turtles(self, animated = True, ord_copies = 2):
        self.ordinal = OrdinalFiniteProd(OrdinalOmega, ord_copies,
                                         x1=-4+8*ord_copies)
        self.ordinal.shift(0.2*LEFT)

        self.gordon = Turtle()
        self.steve = Turtle(pointer_pos = UP)
        self.gordon_desc = TextMobject("Gordon:", '0').to_corner(LEFT+UP)
        self.steve_desc = TextMobject("Steve:", '0').to_corner(LEFT+DOWN)
        self.steve.set_color(YELLOW)

        self.gordon_desc.set_color(self.gordon.color)
        self.steve_desc.set_color(self.steve.color)

        self.add(self.gordon)
        
        self.gordon.move_to(self.ordinal[0][0])
        self.steve.move_to(self.ordinal[0][0])

        self.add(self.ordinal)
        self.steve_index = self.gordon_index = 0
        if animated:
            self.play(self.gordon.run_in(), self.steve.run_in(),
                      FadeIn(self.gordon_desc), FadeIn(self.steve_desc))
        else: self.add(self.gordon, self.steve, self.gordon_desc, self.steve_desc)

    def construct(self):

        #self.force_skipping()
        self.introduce_turtles()
        self.dither()

        self.play(self.steve_step(3))
        self.dither()

        self.play(self.steve_step(next_index = "3+1",
                                  bar = self.ordinal[0][4]),
                  self.gordon_step())
        self.dither()
        self.play(self.transform_desc(self.steve_desc, "4"))
        self.dither()
        self.steve_index = 4

        for _ in range(20):
            self.play(self.steve_step(), self.gordon_step(), run_time = 0.5)
        #self.dither()

        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0, omega_index = 1))
        self.dither(4)
        #self.revert_to_original_skipping_status()
        for _ in range(8):
            self.play(self.gordon_step(omega_index = 1),
                      self.steve_step(next_index = "3+\\omega+"+str(self.gordon_index),
                                      bar = self.ordinal[1][self.gordon_index]),
                      run_time = 0.5)

        steve_desc_dest = self.transformed_desc(self.steve_desc, "3+\\alpha")
        steve_desc_dest.add(
            steve_desc_dest[-1].copy(),
            steve_desc_dest[-1].copy(),
        )
        self.play(
            Transform(self.steve_desc[1], steve_desc_dest),
            self.transform_desc(self.gordon_desc, "\\alpha"),
        )
        self.dither()
        self.play(FadeOut(VGroup(self.steve_desc, self.gordon_desc)))

    def steve_step(self, next_index = None, **kwargs):
        if next_index is not None: self.steve_index = next_index
        else: self.steve_index += 1
        return self.runner_step(self.steve, self.steve_desc, self.steve_index, **kwargs)

    def gordon_step(self, next_index = None, **kwargs):
        if next_index is not None: self.gordon_index = next_index
        else: self.gordon_index += 1
        return self.runner_step(self.gordon, self.gordon_desc, self.gordon_index, **kwargs)

class TurtlesRace2(TurtlesRace):

    def make_question(self):
        question = TexMobject("\\alpha","=","\\omega+\\alpha", "?")
        question[0].set_color(GREEN)
        question[2].set_color(YELLOW)
        question.to_edge(UP)

        return question

    def construct(self):
        self.force_skipping()
        self.introduce_turtles()
        self.dither()
        for _ in range(10):
            self.play(self.steve_step(), self.gordon_step(), run_time = 0.5)

        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0, omega_index = 1))
        self.dither()
        for _ in range(3):
            self.play(self.steve_step(omega_index = 1))
        self.dither()

        formulas = VGroup(
            TexMobject("\\alpha","=","3+\\alpha\\quad", "\\hbox{for infinite $\\alpha$}"),
            TexMobject("\\alpha","<","\\alpha+3"),
        )
        formulas2 = VGroup(
            TexMobject("\\alpha","=","10+\\alpha\\quad", "\\hbox{for infinite $\\alpha$}"),
            TexMobject("\\alpha","<","\\alpha+10"),
        )
        question = self.make_question
        for fs in [formulas, formulas2]:
            for formula in fs:
                formula[0].set_color(GREEN)
                formula[2].set_color(YELLOW)
            fs.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = 0.3)

        formulas.to_edge(UP)
        formulas.shift(RIGHT)
        formulas2.shift(formulas[0][0].get_center() - formulas2[0][0].get_center())

        self.play(Write(formulas[0]))
        self.dither()
        self.play(Write(formulas[1]))
        self.dither()

        self.dither()
        formulas[0][2].add_to_back(formulas[0][2][0].copy())
        formulas[1][2].add(formulas[1][2][-1].copy())
        self.play(ReplacementTransform(formulas, formulas2))
        self.dither()
        formulas_dest = question.copy()
        formulas_dest[2].add_to_back(formulas_dest[2][0].copy())
        self.play(Transform(formulas2[0], formulas_dest),
                  FadeOut(formulas2[1]))
        self.remove(formulas2)
        self.add(question)
        self.dither()

        self.gordon.cur_phase = 1
        self.steve.cur_phase = 1
        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0))
        self.dither()
        for _ in range(9):
            self.play(self.steve_step(omega_index = 1),
                      self.gordon_step(), run_time = 0.5)
        self.revert_to_original_skipping_status()

        self.play(self.steve_step(next_index = "\\omega+\\omega", bar = self.ordinal[1][-1]),
                  self.gordon_step(next_index = 0, omega_index = 1), run_time = 0.5)
        self.dither()


class TurtlesRace3(TurtlesRace2):

    def construct(self):
        self.introduce_turtles(animated = False, ord_copies = 6)
        question = self.make_question()
        self.add(question)
        next_ordinal = OrdinalFiniteProd(OrdinalOmega, 6,
                                         q = (0.8, 0.9, 0.9),
                                         x0 = self.ordinal[0][0].get_center()[0],
                                         x1 = 8)
        next_ordinal.highlight(GREY)
        VGroup(*extract_ordinal_subpowers(next_ordinal)[1]).highlight(YELLOW)

        self.change_desc(self.gordon_desc, "\\omega")
        self.change_desc(self.steve_desc, "\\omega+\\omega")
        self.gordon.move_to(self.ordinal[1])
        self.steve.move_to(self.ordinal[2])

        self.play(
            ReplacementTransform(self.ordinal, next_ordinal),
            self.gordon.move_to, next_ordinal[1],
            self.steve.move_to, next_ordinal[2],
        )
        self.dither()
        self.play(self.transform_desc(self.steve_desc, "\\omega\cdot2"))
        self.dither()

CIRCLE_DECREASE = 0.5

def to_spiral(mob):

    x = mob.points[:,0]
    y = mob.points[:,1]
    complex_points = 1j * x \
                     + 1.5 + 0.2*y - CIRCLE_DECREASE*x/(2*np.pi)
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
    for _ in range(3):
    #while True:
        size = np.exp(i*CIRCLE_DECREASE)
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

        max_x = ahead_turtle[-1].get_center()[0] - SPACE_WIDTH
        for mob in ahead_turtle.family_members_with_points():
            alpha = mob.get_center()[0]
            alpha -= SPACE_WIDTH
            if alpha < 0: continue
            alpha /= max_x
            mob.rotate_in_place(-alpha*np.pi/2)
            mob.move_to(interpolate(1.6*UP + SPACE_WIDTH*RIGHT,
                                    behind_achiles[0][0].get_center(),
                                    alpha))

        turtle_ord = make_ordinal_power(1, q=q, height = 0.5).shift(1.6*UP)
        achiles_ord = make_ordinal_power(2, q=q, height = 0.5).shift(DOWN)
        turtle = Turtle().move_to(ahead_turtle[0])
        achiles = Achiles(pointer_pos = UP).move_to(ahead_achiles[0][0])
        turtle.shift(0.5*DOWN)
        achiles.shift(0.5*UP)
        turtle_desc = TexMobject("\\omega").next_to(turtle_ord[0], DOWN)
        achiles_desc = TexMobject("\\omega^2").next_to(achiles_ord[0][0], UP)

        rect = Rectangle(width = 2*SPACE_WIDTH, height = 2*SPACE_HEIGHT)

        spiral = make_spiral()
        #for runner_dest, bar in [(turtle_dest, spiral[1][1][0]),
        #                         (achiles_dest, spiral[2][1][0][0])]:
        #    runner_dest.scale(np.array([0.35, 2, 1]))
        #    runner_dest.next_to(bar, UP)
        #    to_spiral(runner_dest)

        straight_spiral = spiral.copy()
        spiral.apply_to_family(to_spiral)
        turtle_dest = TrianglePointer(color = GREEN).to_bar(spiral[1][1])
        achiles_dest = TrianglePointer(color = ORANGE).to_bar(spiral[2][1])
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

        self.add(straight_spiral, turtle, achiles)

        #animation = AnimationGroup(
        #    ReplacementTransform(straight_spiral, spiral,
        #                         prepare_family = True),
        #    Transform(straight_spiral[0][2], spiral[0][2], path_arc = np.pi*0.6),
        #    Transform(straight_spiral[0][3], spiral[0][3], path_arc = np.pi*0.6),
        #)
        #animation.update_mobject(0.5)

        #self.add(#turtle, achiles, turtle_desc, achiles_desc,
        #         rect)
        #for mob in self.mobjects:
        #    mob.points *= 0.5
        #return

        self.dither()

        self.play(ReplacementTransform(straight_spiral, spiral,
                                       prepare_family = True),
                  Transform(straight_spiral[0][2], spiral[0][2], path_arc = np.pi*0.6),
                  Transform(straight_spiral[0][3], spiral[0][3], path_arc = np.pi*0.6),
                  ReplacementTransform(turtle, turtle_dest),
                  ReplacementTransform(achiles, achiles_dest),
                  order_f = light_key,
                  run_time = 3)

        self.remove(straight_spiral[0][2], straight_spiral[0][3])
        self.dither()
