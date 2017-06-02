#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from topics.objects import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *
import random
from chat_bubbles import Conversation

from eost.ordinal import *
from topics.number_line import NumberLine

import eost.deterministic

def make_p_power(n, start = "\\omega"):
    tex = ("\\mathcal P("*n) + start + (")"*n)
    return TexMobject(tex)

class PowerSetsScene(Scene):

    def construct(self):
        #self.skip_animations = True
        omega_col = GREEN
        p_omega_col = BLUE

        inf_down = 11
        inf_right = 10
        inf_seq = 10
        omega_numbers = VGroup(*[TexMobject(str(n)) for n in range(inf_down)])
        omega_numbers.arrange_submobjects(DOWN)
        omega_rect = SurroundingRectangle(omega_numbers, color = omega_col, buff = MED_SMALL_BUFF)
        omega = VGroup(omega_numbers, omega_rect)
        omega.to_corner(LEFT+UP)
        omega.shift(DOWN)

        up_left, up_right, _, down_left, _ = omega_rect.get_anchors()
        up = (up_left + up_right)/2
        left = [interpolate(up_left, down_left, alpha) for alpha in np.linspace(0,1,2*inf_down)]

        line_left = VMobject(color = omega_rect.color,
                             stroke_width = omega_rect.stroke_width)
        line_left.set_anchor_points([up]+left, mode="corners")
        line_right = line_left.copy()
        line_right.scale([-1,1,1], about_point=up)

        # Draw picture of omega
        self.play(
            ShowCreation(line_left, run_time = 2*DEFAULT_ANIMATION_RUN_TIME),
            ShowCreation(line_right, run_time = 2*DEFAULT_ANIMATION_RUN_TIME),
            Write(omega_numbers),
        )
        self.remove(line_left, line_right)
        self.add(omega_rect)

        subsets = []
        subsets_maker = omega.copy()
        self.play(subsets_maker.shift, 4*RIGHT)

        # Create picture of P(omega)
        for i in range(inf_right):
            subset = [num for num in subsets_maker[0] if random.randint(0,1) == 0]
            subset = VGroup(VGroup(*subset).copy(), subsets_maker[1].copy())
            subsets.append(subset)
            self.add(subset)
            self.play(subsets_maker.shift, 1.2*RIGHT, run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)

        subsets = VGroup(*subsets)
        p_omega_rect = SurroundingRectangle(subsets, color = p_omega_col, buff = MED_SMALL_BUFF)
        p_omega = VGroup(subsets, p_omega_rect)

        self.play(ShowCreation(p_omega_rect))

        # Big '<'
        big_ineq = TexMobject("<")
        big_ineq.scale(2)
        big_ineq.move_to((omega.get_edge_center(RIGHT) + p_omega.get_edge_center(LEFT))/2)

        self.play(Write(big_ineq))
        self.dither()

        # Various descriptions
        p_omega_desc = make_p_power(1)
        p_omega_desc.next_to(p_omega, UP+LEFT)
        p_omega_desc.shift(2*RIGHT)

        omega_desc = p_omega_desc[-2].copy()
        omega_desc.shift(RIGHT*(omega.get_center()[0] - omega_desc.get_center()[0]))

        omega_desc.set_color(omega_col)
        p_omega_desc.set_color(p_omega_col)

        self.play(Write(omega_desc))

        powerset_arrow = Arrow(omega.get_edge_center(RIGHT),
                               subsets[0].get_edge_center(LEFT)+MED_SMALL_BUFF*LEFT)
        powerset_arrow.shift(2*UP)

        powerset_desc = TextMobject("$\\mathcal P$owerset")
        powerset_desc[0].set_color(YELLOW)
        powerset_desc.next_to(powerset_arrow, UP)

        self.play(
            Write(powerset_desc[0]),
            ShowCreation(powerset_arrow),
        )
        self.play(Write(VGroup(*powerset_desc[1:])))
        self.play(
            ReplacementTransform(powerset_desc[0].copy(), p_omega_desc[0], path_arc = -np.pi/3),
            ReplacementTransform(omega_desc.copy(), VGroup(*p_omega_desc[1:])),
        )
        
        # Increasing sequence
        self.ineq = TexMobject("<")
        self.ineq.move_to((omega_desc.get_center() + p_omega_desc[0].get_center())/2)
        self.play(Write(self.ineq))

        self.dither()

        self.ineq_seq_buff = 0.4
        self.ineq_seq = VGroup(omega_desc, self.ineq, p_omega_desc).copy()

        self.ineq_seq.set_color(WHITE)
        self.ineq_seq.arrange_submobjects(
            center = False,
            coor_mask = RIGHT,
            buff = self.ineq_seq_buff,
        )

        self.play(
            ReplacementTransform(
                VGroup(omega_desc, self.ineq, p_omega_desc),
                self.ineq_seq
            ))
        self.dither()

        self.play(
            *map(FadeOut,
                 [omega, p_omega,
                  powerset_desc, powerset_arrow,
                  big_ineq,
                 ]))

        for _ in range(3): self.extend_ineq_seq()

        # integer powers at the center of scene
        self.p_power = None
        self.make_p_power_with_brace(2)
        for exp in range(3, 5): self.make_p_power_with_brace(exp)
        self.make_general_p_power_with_brace(exp)
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("So let's find a big integer!")
        self.dither(3)
        conversation.add_bubble("Integers are too small.")
        self.dither(3)

        ordinal = OrdinalOmega(x0 = -6, x1 = 5, q = (0.8, 0.9, 0.9))
        naturals = ordinal.add_descriptions(lambda n: TexMobject(str(n)),
                                            direction = DOWN, size = 0.5)
        p_powers = ordinal.add_descriptions(make_p_power,
                                            direction = UP)

        for _ in range(len(p_powers) - (len(self.ineq_seq)+1)/2):
            self.extend_ineq_seq(animated = False)
        self.play(*map(FadeOut, [conversation.dialog, self.p_power]+self.ineq_seq[1::2]))
        self.ineq_seq = VGroup(*self.ineq_seq[::2])

        #self.skip_animations = False
        self.play(*map(ShowCreation, [
            naturals, ordinal
        ]))
        self.play(Transform(self.ineq_seq, p_powers))
        self.dither()

    def make_p_power_with_brace(self, exp):
        base = make_p_power(exp)
        brace = Brace(VGroup(*base[:2*exp]))
        desc = TexMobject(str(exp))
        brace.put_at_tip(desc)
        next_p_power = VGroup(base, brace, desc)

        if self.p_power is None:
            next_p_power.shift(1.3*UP)
            self.play(
                Write(base),
                Write(desc),
                GrowFromCenter(brace))

        else:
            last_base, last_brace, last_desc = self.p_power.submobjects
            next_p_power.shift(last_base[0].get_center() - base[2].get_center())
            self.play(
                Write(VGroup(base[0], base[1], base[-1])),
                ReplacementTransform(last_brace, brace),
                ReplacementTransform(last_desc, desc),
            )
            self.remove(last_base)
            self.add(base)

        self.p_power = next_p_power

    def make_general_p_power_with_brace(self, last_exp):
        base = TexMobject("\\mathcal P(\\mathcal P(\cdots\\mathcal P(\omega)\cdots))")
        brace = Brace(VGroup(*base[:9]))
        desc = TexMobject("n")
        brace.put_at_tip(desc)

        last_base, last_brace, last_desc = self.p_power.submobjects
        next_p_power = VGroup(base, brace, desc)
        next_p_power.shift(last_base[2*last_exp].get_center() - base[9].get_center())
        self.play(
            Transform(VGroup(*last_base[:4]), VGroup(*base[:4])),
            Transform(VGroup(*last_base[4:2*(last_exp-1)]), VGroup(*base[4:7])),
            Transform(VGroup(*last_base[-(last_exp-1):-2]), VGroup(*base[-5:-2])),
            Transform(VGroup(*last_base[-2:]), VGroup(*base[-2:])),
            Transform(last_brace, brace),
            Transform(last_desc, desc),
        )
        self.remove(self.p_power, *self.mobjects_from_last_animation)
        self.p_power = next_p_power
        self.add(self.p_power)

    def extend_ineq_seq(self, animated = True):
        n = (len(self.ineq_seq)+1)/2

        next_p_power = make_p_power(n)
        next_ineq = self.ineq.copy()
        next_p_power.shift(self.ineq_seq[-1][-1].get_center() - next_p_power[-1].get_center())

        next_ineq.next_to(
            self.ineq_seq[-1],
            coor_mask = RIGHT,
            buff = self.ineq_seq_buff)

        next_p_power.next_to(
            next_ineq,
            coor_mask = RIGHT,
            buff = self.ineq_seq_buff)

        if animated:
            self.play(ReplacementTransform(self.ineq_seq[-1].copy(), VGroup(*next_p_power[2:-1])))
            self.play(Write(VGroup(next_p_power[0], next_p_power[1], next_p_power[-1], next_ineq)))
        else:
            self.add(next_ineq, next_p_power)

        self.ineq_seq.add(next_ineq, next_p_power)

class FirstLimitStep(Scene):
    def construct(self):

        limit_col = YELLOW

        #self.skip_animations = True

        ordinal = OrdinalOmega(x0 = -6, x1 = 5, q = (0.8, 0.9, 0.9))
        naturals = ordinal.add_descriptions(lambda n: TexMobject(str(n)),
                                            direction = DOWN, size = 0.5)
        p_powers = ordinal.add_descriptions(make_p_power,
                                            direction = UP)
        for i in range(len(p_powers), len(ordinal)):
            p_powers.add(Dot(radius=0))
            p_powers[-1].next_to(ordinal[i], direction = UP, buff=0)

        self.add(ordinal, naturals, p_powers)
        self.dither()

        next_ordinal = OrdinalOmega(q = (0.8, 0.9, 0.9))
        next_ordinal[0].set_color(limit_col)
        ori_center = next_ordinal[0].get_center()
        next_ordinal[0].next_to(ordinal)
        shift = next_ordinal[0].get_center() - ori_center

        def make_U_power(n):
            result = make_p_power(n, start = "U")
            result[-n-1].set_color(limit_col)
            return result

        U_powers = next_ordinal.add_descriptions(make_U_power)
        for i in range(len(U_powers), len(next_ordinal)):
            U_powers.add(Dot(radius=0))
            U_powers[-1].next_to(ordinal[i], direction = UP, buff=0)

        self.play(ReplacementTransform(p_powers.copy(), U_powers[0]))
        self.play(ShowCreation(next_ordinal[0]))
        union_desc = TextMobject("Union").next_to(U_powers[0], UP, buff = LARGE_BUFF)
        self.play(Write(union_desc))

        self.dither()
        
        self.play(VGroup(*self.get_top_level_mobjects()).shift, -shift)
        self.dither()

        #self.skip_animations = False
        ini_segment = 4
        for i in range(1, ini_segment):
            self.play(
                ReplacementTransform(U_powers[i-1].copy(), VGroup(*U_powers[i][2:-1])),
                run_time = 0.5,
            )
            self.play(
                ShowCreation(next_ordinal[i]),
                Write(VGroup(U_powers[i][0], U_powers[i][1], U_powers[i][-1])),
                run_time = 0.5,
            )

        self.play(
            ShowCreation(VGroup(*U_powers[ini_segment:])),
            ShowCreation(VGroup(*next_ordinal[ini_segment:])),
        )

        limit_step = next_ordinal[0].copy()
        limit_step.next_to(next_ordinal)

        limit_step_desc = TexMobject("U_1")
        limit_step_desc.set_color(limit_col)
        limit_step.add_description(limit_step_desc)

        union_desc2 = union_desc.copy()
        union_desc2.next_to(limit_step_desc, UP, buff = LARGE_BUFF)

        self.play(
            Write(union_desc2),
            Succession(
                ReplacementTransform(U_powers.copy(), limit_step_desc),
                ShowCreation(limit_step),
                rate_func = None),
        )

        self.dither(2)
        self.play(Write(TextMobject("Transfinite",  "Recursion").to_edge(DOWN)))
        self.dither(2)

class RecursionScene(Scene):

    def construct(self):

        #self.skip_animations = True

        base_color = GREEN
        succ_color = WHITE
        lim_color = YELLOW
        ordinal_shift = DOWN

        title = TextMobject("Transfinite",  "Recursion").to_edge(DOWN)
        title[0].highlight(DARK_GREY)
        self.add(title)
        naturals = OrdinalOmega()
        naturals[0].set_color(GREEN)
        naturals_desc = naturals.add_descriptions(lambda n: TexMobject(str(n)),
                                                  direction = DOWN, size = 0.5)

        base_case_title = TextMobject("Base case: $\\omega$")
        base_case_title.set_color(base_color)
        base_case_title.to_corner(UP+LEFT)
        base_desc = TexMobject("\\omega")
        base_desc.next_to(naturals[0], UP)
        base_desc.set_color(GREEN)

        rec_step_title = TextMobject("Recursive", " step", ": ", "Powerset", arg_separator = '')
        rec_step_title.set_color(succ_color)
        rec_step_title.to_corner(UP+LEFT)
        rec_step_title.shift(DOWN)

        succ_steps = naturals.to_steps(h_placement = 1)
        succ_steps_desc = naturals.add_descriptions(lambda n: TexMobject("\\mathcal P"))
        succ_steps.set_color(succ_color)
        succ_steps_desc.set_color(succ_color)

        VGroup(naturals, naturals_desc, succ_steps, base_desc, succ_steps_desc).shift(ordinal_shift)
        for succ_step_desc, succ_step in zip(succ_steps_desc, succ_steps):
            succ_step_desc.next_to(succ_step, UP, buff=succ_step_desc.get_width()*0.7)

        self.play(
            ShowCreation(naturals),
            ShowCreation(naturals_desc))
        self.dither()
        self.play(Write(base_desc))
        self.play(
            Write(VGroup(*base_case_title[:-1])),
            ReplacementTransform(base_desc, base_case_title[-1]))

        self.play(Write(rec_step_title))
        self.play(
            ReplacementTransform(rec_step_title[-1].copy(), succ_steps_desc[0]),
            ShowCreation(succ_steps[0]),
        )
        self.play(
            ShowCreation(VGroup(*succ_steps_desc[1:])),
            ShowCreation(VGroup(*succ_steps[1:])),
        )
        self.dither()

        next_ordinal = naturals.copy()
        next_ordinal[0].set_color(lim_color)
        next_ordinal.next_to(naturals)
        self.play(
            title[0].highlight, WHITE, 
            ShowCreation(next_ordinal[0]))

        title[0].highlight(WHITE)
        succ_step_title = TextMobject("Successor", " step", ": ", "Powerset", arg_separator = '')
        succ_step_title.set_color(succ_color)
        lim_step_title = TextMobject("Limit step: Union")
        lim_step_title.set_color(lim_color)

        succ_step_title.next_to(rec_step_title[1])
        lim_step_title.next_to(rec_step_title[1])
        succ_step_title.shift(0.5*UP+RIGHT)
        lim_step_title.shift(0.5*DOWN+RIGHT)

        rec_step_fork = VGroup(*[
            Line(
                rec_step_title[1].get_edge_center(RIGHT) + RIGHT*0.2,
                subtitle.get_edge_center(LEFT) + LEFT*0.2,
            ).set_color(color)
            for subtitle, color in [(succ_step_title, succ_color), (lim_step_title, lim_color)]
        ])


        self.play(
            ShowCreation(rec_step_fork[0]),
            ReplacementTransform(
                VGroup(
                    rec_step_title[0].copy(),
                    rec_step_title[1].copy(),
                    rec_step_title[2],
                    rec_step_title[3]),
                succ_step_title),
        )
        self.dither()
        self.play(
            ShowCreation(rec_step_fork[1]),
            Write(lim_step_title)
        )

        self.play(
            title[0].highlight, DARK_GREY,
            *map(FadeOut, [
                succ_steps, succ_steps_desc, next_ordinal[0],
            ]))

        self.dither(3)
        self.play(
            title[0].highlight, WHITE,
            FadeOut(naturals_desc),
            FadeIn(next_ordinal))

        self.dither(3)
        omega_pow2_src = VGroup(naturals, next_ordinal)


        for _ in range(2):
            next_ordinal = next_ordinal.copy()
            next_ordinal.next_to(omega_pow2_src[-1])
            omega_pow2_src.add(next_ordinal)
            self.play(omega_pow2_src.shift,
                      omega_pow2_src[-2][0].get_center() - next_ordinal[0].get_center())
            self.dither()

        last_bar = next_ordinal[0].copy()
        omega_pow2_dest = make_ordinal_power(2, q=(0.8, 0.9, 0.9), x0 = -6, x1 = 6)
        omega_pow2_dest.shift(ordinal_shift)
        last_bar.next_to(omega_pow2_dest)
        for subord in omega_pow2_dest: subord[0].set_color(lim_color)
        omega_pow2_end = omega_pow2_dest.copy()
        omega_pow2_end.next_to(next_ordinal)
        omega_pow2_src.submobjects += omega_pow2_end.submobjects
        omega_pow2_dest[0][0].set_color(base_color)

        self.play(ReplacementTransform(omega_pow2_src, omega_pow2_dest))
        self.play(ShowCreation(last_bar))
        self.dither()
        #self.skip_animations = False

        self.play(*map(FadeOut, [
            mob for mob in self.get_top_level_mobjects() if mob.get_center()[1] > 0
        ]))
        series = VideoSeries()
        series.to_edge(UP)
        self.play(FadeIn(
            series,
            submobject_mode = "lagged_start",
            run_time = 2
        ))
        ordinal_series = VGroup(*series[3:8])
        ordinal_series_target = ordinal_series.copy()
        ordinal_series_target.shift(DOWN)
        ordinal_series_target.set_color(YELLOW)
        for i, s in enumerate(ordinal_series_target):
            s.remove(s[-1])
            num = TexMobject(str(i+4))
            num.scale(0.7)
            num.move_to(s)
            s.add(num)

        series_brace = Brace(ordinal_series_target)
        self.play(
            Transform(ordinal_series, ordinal_series_target),
            GrowFromCenter(series_brace),
        )

        self.dither(2)

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

class RealsProblems(Scene):

    def construct(self):

        #self.skip_animations = True
        
        elongated = 10
        unit_size = 3
        self.numberline = NumberLine(
            x_min = 0,
            x_max = SPACE_WIDTH*2,
            leftmost_tick = 0.5,
            tick_frequency = 1,
            tick_size = 0.05,
            unit_size = unit_size,
            numbers_with_elongated_ticks = list(range(12))
        )
        self.numberline.add_numbers()
        self.numberline.numbers.shift(0.1*DOWN + 0.5*unit_size*LEFT)

        self.numberline.tick_marks.submobjects.sort(key = lambda tick: tick.get_center()[0])
        self.numberline.tick_marks.remove(self.numberline.tick_marks[0])

        #for tick in self.numberline.tick_marks:
        #    tick.shift(tick.get_end() * DOWN)
        self.numberline.shift(4*LEFT + DOWN)
        self.line_start = np.array(self.numberline.main_line.get_start())
        self.numberline.numbers[0].set_color(BLACK)

        real_title = TexMobject("\mathbb R^+_0")
        real_title.to_edge(RIGHT)
        #real_title.shift()
        self.play(ShowCreation(self.numberline), Write(VGroup(real_title[0], real_title[1])))
        self.dither()
        base_case_q = TextMobject("Base case?")
        base_case_q.to_corner(UP+LEFT)
        base_case_q.set_color(GREEN)
        self.play(Write(base_case_q))

        self.pointer = self.pointer_with_number(2.5)
        self.pointer.set_fill(opacity = 0)
        self.move_pointer(1.25)
        self.dither()
        self.scale_numberline(2)
        self.dither()
        self.move_pointer(0.2)
        self.dither()
        self.scale_numberline(2)
        self.dither()
        self.move_pointer(0.01)

        base_case_a = TextMobject("Minimal element needed")
        base_case_a.to_corner(UP+LEFT)
        base_case_a.set_color(GREEN)
        self.play(
            ReplacementTransform(base_case_q, base_case_a)
        )
        self.dither()

        zero_dot = Dot(self.line_start, color = BLUE)
        zero_desc = TexMobject("0")
        zero_desc.next_to(zero_dot, LEFT)
        self.play(FadeOut(self.pointer))
        self.play(
            ShowCreation(zero_dot),
            Write(zero_desc),
            Write(real_title[2]),
        )
        base_case = Line(self.line_start+UP, self.line_start, color = GREEN)
        base_desc = TexMobject("\\omega").set_color(GREEN)
        base_desc.next_to(base_case, UP)
        self.dither()
        self.play(
            Write(base_desc),
            ShowCreation(base_case),
        )

        self.dither()
        succ_step_q = TextMobject("Successor s","tep?", arg_separator = '')
        succ_step_q.to_corner(UP+LEFT)
        succ_step_q.set_color(WHITE)
        succ_step_q.next_to(base_case_a, DOWN, coor_mask = UP)

        self.play(Write(succ_step_q))

        self.pointer = self.pointer_with_skipped(4)
        self.play(FadeIn(self.pointer[0]))

        self.dither()
        self.play(
            GrowFromCenter(self.pointer[1][0]),
            FadeIn(self.pointer[1][1]),
        )
        self.move_pointer(2, False)
        self.dither()
        self.move_pointer(1, False)
        self.dither()

        succ_step_a = TextMobject("Successors","needed")
        succ_step_a.to_corner(UP+LEFT)
        succ_step_a.set_color(WHITE)
        succ_step_a.next_to(base_case_a, DOWN, coor_mask = UP)

        #self.skip_animations = False
        self.play(
            ReplacementTransform(succ_step_q, succ_step_a),
            FadeOut(self.pointer[1]),
            FadeOut(self.numberline.tick_marks[0]),
        )
        self.dither()

        self.remove(self.numberline)
        lines = VGroup()
        dots = VGroup()
        for i in range(1, 15):
            pos = self.line_start + RIGHT*i
            dots.add(Dot(pos))
            lines.add(Line(pos, pos+LEFT))

        VGroup(lines, dots).highlight(BLUE)
        lines.submobjects.reverse()

        self.add_foreground_mobjects(base_case, self.pointer[0])
        self.play(
            Uncreate(lines, submobject_mode = 'lagged_start', lag_factor = 2),
            ShowCreation(dots, submobject_mode = 'lagged_start'),
            FadeOut(real_title),
        )
        self.dither()

        lim_step_q = TextMobject("Limit step?")
        lim_step_q.to_corner(UP+LEFT)
        lim_step_q.set_color(YELLOW)
        lim_step_q.next_to(succ_step_a, DOWN, coor_mask = UP)
        self.play(Write(lim_step_q))
        self.dither()

    def pointer_with_number(self, x):

        pointer = TrianglePointer()
        pointer.shift(self.numberline.number_to_point(x))
        desc = TexMobject(str(x))
        desc.next_to(pointer, UP)
        result = VGroup(pointer, desc)

        result.number = x

        return result

    def pointer_with_skipped(self, x):
        pointer = TrianglePointer()
        pointer.shift(self.line_start + x*RIGHT)
        p_omega = make_p_power(1)
        p_omega.next_to(pointer, UP)
        skipped_brace = Brace(Line(self.line_start, self.line_start + x*RIGHT), DOWN)
        skipped_desc = TextMobject("skipped")
        skipped_brace.put_at_tip(skipped_desc)

        return VGroup(VGroup(pointer, p_omega), VGroup(skipped_brace, skipped_desc))

    def move_pointer(self, x, with_number = True):

        if with_number: new_pointer = self.pointer_with_number(x)
        else: new_pointer = self.pointer_with_skipped(x)
        self.play(ReplacementTransform(self.pointer, new_pointer))
        self.pointer = new_pointer

    def scale_numberline(self, coef):

        ori_line = self.numberline
        self.numberline = self.numberline.deepcopy()
        self.numberline.scale(coef, about_point = np.array(self.line_start))
        next_pointer = self.pointer_with_number(self.pointer.number)
        self.play(
            ReplacementTransform(ori_line, self.numberline),
            ReplacementTransform(self.pointer, next_pointer),
        )
        self.pointer = next_pointer

def named_brace(brace_base, name, direction = DOWN):
    brace = Brace(brace_base, direction = direction)
    desc = TextMobject(*name)
    brace.put_at_tip(desc)
    return VGroup(brace, desc)

def ini_segment_brace(brace_base, **kwargs):
    return named_brace(brace_base, ("Initial", "segment"), **kwargs)

def term_segment_brace(brace_base, **kwargs):
    return named_brace(brace_base, ("Terminal", "segment"), **kwargs)

class OmegaPlusZScene(Scene):

    def construct(self):

        #self.skip_animations = True

        # Titles
        base_case_a = TextMobject("Minimal element needed")
        base_case_a.to_corner(UP+LEFT)
        base_case_a.set_color(GREEN)

        succ_step_a = TextMobject("Successors","needed")
        succ_step_a.to_corner(UP+LEFT)
        succ_step_a.set_color(WHITE)
        succ_step_a.next_to(base_case_a, DOWN, coor_mask = UP)

        lim_step_q = TextMobject("Limit step?")
        lim_step_q.to_corner(UP+LEFT)
        lim_step_q.set_color(YELLOW)
        lim_step_q.next_to(succ_step_a, DOWN, coor_mask = UP)

        self.add(base_case_a, succ_step_a, lim_step_q)

        # Construct the set
        omega = OrdinalOmega(x1 = -1)

        omega2 = omega.copy()
        omega_reversed = omega2.copy()
        omega_reversed.scale([-1,1,1], about_point = omega2[0].get_center())
        Z = VGroup(omega_reversed, omega2)

        omega_plus_Z = VGroup(omega, Z)
        omega_plus_Z.arrange_submobjects()
        omega_plus_Z.center()
        omega_plus_Z.shift(DOWN)
        omega_plus_Z.set_color(DARK_GREY)

        self.play(ShowCreation(omega))
        self.dither()
        self.play(
            ShowCreation(omega2),
            ShowCreation(omega_reversed),
        )
        self.dither()

        # Fill the initial segment
        omega_colorful = omega.copy()
        omega_colorful.set_color(WHITE)
        omega_colorful[0].set_color(GREEN)

        base_case_desc = TexMobject("\\omega")
        base_case_desc.set_color(GREEN)
        base_case_desc.next_to(omega_colorful[0], UP)
        self.play(ShowCreation(omega_colorful[0]), ShowCreation(base_case_desc))
        self.dither()
        self.play(ShowCreation(omega_colorful[1]))
        self.play(ShowCreation(omega_colorful[2]))
        self.play(ShowCreation(VGroup(*omega_colorful[3:])))
        self.dither()

        self.remove(Z)
        Z.remove(omega2, omega_reversed)
        omega_reversed.remove(omega_reversed[0])
        Z.submobjects = sorted(omega2.submobjects + omega_reversed.submobjects,
                               key = lambda bar: bar.get_center()[0])
        self.add(Z)


        # No place for the limit step
        self.Z = Z
        self.init_skipped(0.7)
        self.dither()
        self.move_skipped(0.3)
        self.dither()
        self.move_skipped(0.1)
        self.dither()

        # Property for the limit step
        lim_step_a = TextMobject("All initial segments have successors")
        lim_step_a.to_corner(UP+LEFT)
        lim_step_a.set_color(YELLOW)
        lim_step_a.next_to(succ_step_a, DOWN, coor_mask = UP)
        self.play(
            ReplacementTransform(lim_step_q, lim_step_a),
            self.highlighted.highlight, DARK_GREY,
            FadeOut(self.pointer),
            FadeOut(self.skipped),
        )
        self.dither()

        # Show initial segment
        self.omega = omega
        self.init_initial()
        for _ in range(2):
            self.add_bar()
            self.dither()
            self.update_ini_segment()

        self.add_bar()
        self.dither()
        self.update_ini_segment(empty = True)
        self.dither()
        self.play(ShowCreation(omega_colorful[0]))
        self.dither()

        well_ordered_title = TextMobject("Well ordered set")
        well_ordered_title.to_edge(UP)
        lim_step_a_target = lim_step_a.copy()
        lim_step_a_target.next_to(well_ordered_title, DOWN, coor_mask = UP)
        self.play(
            FadeOut(base_case_a),
            FadeOut(succ_step_a),
            Transform(lim_step_a, lim_step_a_target),
        )
        self.dither(5)
        self.skip_animations = False
        self.remove(omega)
        self.play(*map(FadeOut, [
            omega_colorful,
            Z,
            base_case_desc,
            self.added_bars,
            self.ini_segment,
        ]))

    def construct_skipped(self, x):

        center_list = [bar.get_center() for bar in self.Z]
        x_list = [c[0] for c in center_list]
        x = interpolate(x_list[0], x_list[-1], x)

        index, _ = max(enumerate([xx for xx in x_list if xx < x]),
                       key=lambda (i,val): val)

        skipped_brace = Brace(Line(center_list[0], center_list[index]))
        skipped_brace.shift(DOWN)
        skipped_desc = TextMobject("skipped")
        skipped_brace.put_at_tip(skipped_desc)

        highlighted = self.Z[index+1]

        pointer = TrianglePointer()
        pointer.shift(x_list[index+1]*RIGHT + (center_list[0][1]+1)*UP)
        pointer_desc = TexMobject('U')
        pointer_desc.next_to(pointer, UP)
        pointer_desc.set_color(YELLOW)

        return VGroup(pointer, pointer_desc), highlighted, VGroup(skipped_brace, skipped_desc)

    def init_skipped(self, x):

        self.pointer, self.highlighted, self.skipped = self.construct_skipped(x)
        self.play(
            self.highlighted.highlight, YELLOW,
            FadeIn(self.pointer),
        )
        self.play(
            GrowFromCenter(self.skipped[0]),
            FadeIn(self.skipped[1]),
        )

    def move_skipped(self, x):

        next_pointer, next_highlighted, next_skipped = self.construct_skipped(x)
        self.play(ReplacementTransform(self.pointer, next_pointer))
        self.pointer = next_pointer

        self.highlighted.highlight(DARK_GREY)
        self.highlighted = next_highlighted
        self.highlighted.highlight(YELLOW)

        self.play(ReplacementTransform(self.skipped, next_skipped))
        self.skipped = next_skipped

    def construct_initial(self, empty = False):
        if empty:
            begin_point = self.omega[0][0].get_end()
            brace_base = Line(begin_point+0.1*LEFT, begin_point+0.4*LEFT)
        elif len(self.added_bars) == 0:
            brace_base = self.omega
        else:
            brace_base = VGroup(self.omega, self.added_bars)

        return ini_segment_brace(brace_base)

    def init_initial(self):
        
        self.added_bars = VGroup()
        self.ini_segment = self.construct_initial()
        self.play(
            GrowFromCenter(self.ini_segment[0]),
            FadeIn(self.ini_segment[1]),
        )

    def add_bar(self):

        next_bar = self.omega[0].copy()

        if len(self.added_bars) == 0:
            next_bar.next_to(self.omega)
            next_bar.set_color(YELLOW)
        else:
            next_bar.next_to(self.added_bars)
            next_bar.set_color(WHITE)

        self.added_bars.add(next_bar)

        Z_target = self.Z.copy()
        Z_target.next_to(next_bar)
        self.play(
            Transform(self.Z, Z_target),
            ShowCreation(next_bar),
        )

    def update_ini_segment(self, empty = False):

        ini_segment_target = self.construct_initial(empty)
        self.play(Transform(self.ini_segment, ini_segment_target))

class WellOrderingCondition(Scene):

    def construct(self):

        #self.skip_animations = True
        well_ordered_title = TextMobject("Well ordered set")
        well_ordered_title.to_edge(UP)

        lim_step_a = TextMobject("All", "initial segments have successors")
        lim_step_a.to_corner(UP+LEFT)
        lim_step_a.set_color(YELLOW)
        lim_step_a.next_to(well_ordered_title, DOWN, coor_mask = UP)

        self.add(lim_step_a)

        any_set = DashedLine(4*LEFT, 4*RIGHT)
        any_set.shift(DOWN)
        any_set_desc = TextMobject("Any set")
        any_set_desc.next_to(any_set, UP)

        self.play(
            ShowCreation(any_set),
            FadeIn(any_set_desc),
        )
        self.dither()

        ini_segment = ini_segment_brace(any_set)
        self.play(
            GrowFromCenter(ini_segment[0]),
            FadeIn(ini_segment[1]),
        )
        self.dither()

        self.play(*map(FadeOut, [
            ini_segment, any_set, any_set_desc
        ]))

        self.dither()
        #self.fill_ordinal(make_ordinal_power(2, q = (0.8, 0.9, 0.9)))
        self.fill_ordinal(OrdinalFiniteProd(OrdinalOmega, 4), one_range = 1)
        self.fill_ordinal(OrdinalFiniteProd(OrdinalOmega, 2), one_range = 1)
        last_ordinal = self.fill_ordinal(OrdinalSum(OrdinalOmega, 0.8,
                                                    lambda **kwargs: OrdinalFinite(5, **kwargs)),
                                         one_range = 0,
                                         remove = False)

        #self.skip_animations = False

        real_condition = TextMobject("All", "proper", "initial segments have successors")
        real_condition.to_corner(UP+LEFT)
        real_condition.set_color(YELLOW)
        real_condition.next_to(well_ordered_title, DOWN, coor_mask = UP)

        proper_src = real_condition[1].copy()
        proper_src.replace(Point(real_condition[1].get_edge_center(LEFT)))
        self.play(
            ReplacementTransform(lim_step_a[0],  real_condition[0]),
            ReplacementTransform(proper_src,     real_condition[1]),
            ReplacementTransform(lim_step_a[-1], real_condition[2]),
        )
        self.dither()
        self.play(Write(well_ordered_title))
        self.dither()

    def fill_ordinal(self, ordinal, remove = True, one_range = 3, omega_range = 1): # omega+k -> omega^2 supported

        ordinal_bg = ordinal.copy()
        ordinal_bg.shift(DOWN)
        ordinal_bg.set_color(DARK_GREY)
        self.add(ordinal_bg)

        ordinal_col = ordinal_bg.copy()
        ordinal_col.set_color(WHITE)

        for subord in ordinal_col:
            subord[0].set_color(YELLOW)
        ordinal_col[0][0].set_color(GREEN)

        self.add(ordinal_bg)

        for i in range(one_range): self.play(ShowCreation(ordinal_col[0][i]))
        self.play(ShowCreation(VGroup(*ordinal_col[0][one_range:])))

        for i in range(1, omega_range):
            if i < len(ordinal_col.submobjects):
                self.play(ShowCreation(ordinal_col[i]))

        if omega_range < len(ordinal_col.submobjects):
            self.play(ShowCreation(VGroup(*ordinal_col[omega_range:])))

        self.remove(ordinal_bg)
        self.dither()
        if remove: self.play(FadeOut(ordinal_col))
        else: return ordinal_col

dec_seq_color = ORANGE

class OmegaSquaredScene(Scene):

    def init_ordinal(self):
        self.brace_list = []
        self.ordinal = make_ordinal_power(2, q=(0.8, 0.9, 0.9), x0 = -4, x1 = 4)
        self.add(self.ordinal)

        self.ordinal.shift(DOWN)
        _, self.lim_bars, self.bars = extract_ordinal_subpowers(self.ordinal)

        self.center_list = [bar.get_center() for bar in self.bars]
        self.x_list = [c[0] for c in self.center_list]
        self.lim_x_list = [bar.get_center()[0] for bar in self.lim_bars]
        self.lim_x_set = set(list(self.lim_x_list))
        self.lim_indices = [self.x_list.index(x) for x in self.lim_x_list]

    def split_at_point(self, x, use_lim = False):

        if use_lim:
            x_list = self.lim_x_list
            indices = self.lim_indices
        else:
            x_list = self.x_list
            indices = range(len(self.x_list))

        x = interpolate(x_list[0], x_list[-1], x)

        index, _ = min([(i,val) for i,val in zip(indices, x_list) if val >= x],
                       key=lambda (i,val): val)

        return index-1, index

    def random_split(self):
        use_lim = (random.random() < 0.4)
        x = random.random()
        return self.split_at_point(x, use_lim)

    def random_dec_seq(self):

        def rand_x():
            return (random.random())

        last, _ = self.split_at_point((rand_x()+1)/2)
        seq = []

        while last != 0:
            if len(seq) == 0 or self.x_list[seq[-1]] - self.x_list[last] > 0.1:
                if random.random() < 0.4: seq.append(last)
            if last in self.lim_x_set:
                last, _ = self.split_at_point(rand_x() * self.x_list[last])
            else: last -= 1

        seq.append(0)

        seq_bars = VGroup(*[self.bars[i] for i in seq]).copy()
        seq_jumps = []
        for i in range(len(seq)-1):
            size = self.x_list[seq[i]] - self.x_list[seq[i+1]]
            stroke_width = max(seq_bars[i].stroke_width, seq_bars[i+1].stroke_width)
            jump = StepCurve(size = size, stroke_width = stroke_width)
            jump.scale((-1,1,1))
            jump.shift(seq_bars[i].get_start())
            seq_jumps.append(jump)

        seq_jumps = VGroup(*seq_jumps)

        seq_bars.set_color(dec_seq_color)
        seq_jumps.set_color(dec_seq_color)

        return seq_bars, seq_jumps, seq

    def construct_ini_brace(self, index, direction = DOWN):
        return ini_segment_brace(Line(self.center_list[0], self.center_list[index]),
                                 direction = direction).shift(direction)

    def construct_term_brace(self, index, direction = DOWN):
        return term_segment_brace(Line(self.center_list[index], self.center_list[-1]),
                                  direction = direction).shift(direction)

    def construct_brace(self, (ini_brace, direction)):
        if ini_brace: return self.construct_ini_brace(self.cur_split[0], direction)
        else: return self.construct_term_brace(self.cur_split[1], direction)

    def add_brace(self, brace_type, show_creation = True):
        brace = self.construct_brace(brace_type)
        if show_creation:
            self.play(
                GrowFromCenter(brace[0]),
                FadeIn(brace[1]),
            )
        self.brace_list.append((brace_type, brace))

        return brace

    def highlight_split(self):
        VGroup(*self.bars[:self.cur_split[1]]).set_color(self.ini_color)
        VGroup(*self.bars[self.cur_split[1]:]).set_color(self.term_color)
    
    def update_split(self, ini_color = WHITE, term_color = DARK_GREY):
        self.play(*[
            Transform(brace, self.construct_brace(brace_type))
            for brace_type, brace in self.brace_list
        ])
        self.highlight_split()

class OmegaSquaredTestSplits(OmegaSquaredScene):

    def construct(self):

        self.init_ordinal()
        self.ini_color = WHITE
        self.term_color = DARK_GREY

        self.cur_split = self.random_split()
        self.add_brace((True, DOWN))
        self.highlight_split()
        self.dither()

        for _ in range(3):
            self.cur_split = self.random_split()
            self.update_split()
            self.dither()

        self.add_brace((False, UP))

        for _ in range(3):
            self.cur_split = self.random_split()
            self.update_split()
            self.dither()

        i = 0
        while True:
            successor = self.bars[self.cur_split[1]].copy()
            successor.highlight(YELLOW)
            self.play(ShowCreation(successor))
            self.dither()

            if i == 3: break
            i += 1

            self.cur_split = self.random_split()
            self.remove(successor)
            self.update_split()

        

class OmegaSquaredTestDecSeq(OmegaSquaredScene):

    def construct(self):

        self.init_ordinal()

        self.ordinal.set_color(DARK_GREY)
        for _ in range(5):
            seq_bars, seq_jumps, seq = self.random_dec_seq()
            self.add(seq_jumps)
            self.play(
                ShowCreation(seq_bars),
                ShowCreation(seq_jumps),
                run_time = 2*DEFAULT_ANIMATION_RUN_TIME,
            )
            self.dither()
            self.remove(seq_bars, seq_jumps)

