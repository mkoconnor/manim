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
from random import randint
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
            subset = [num for num in subsets_maker[0] if randint(0,1) == 0]
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
        self.play(Write(TextMobject("Transfinite",  " Recursion").to_edge(DOWN)))
        self.dither(2)

class RecursionScene(Scene):

    def construct(self):

        #self.skip_animations = True

        zero_color = GREEN
        succ_color = WHITE
        lim_color = YELLOW
        ordinal_shift = DOWN

        title = TextMobject("Transfinite",  " Recursion").to_edge(DOWN)
        title[0].highlight(DARK_GREY)
        self.add(title)
        naturals = OrdinalOmega()
        naturals[0].set_color(GREEN)
        naturals_desc = naturals.add_descriptions(lambda n: TexMobject(str(n)),
                                                  direction = DOWN, size = 0.5)

        zero_step_title = TextMobject("Zero step: $\\omega$")
        zero_step_title.set_color(zero_color)
        zero_step_title.to_corner(UP+LEFT)
        zero_desc = TexMobject("\\omega")
        zero_desc.next_to(naturals[0], UP)
        zero_desc.set_color(GREEN)

        rec_step_title = TextMobject("Recursive", " step", ": ", "Powerset")
        rec_step_title.set_color(succ_color)
        rec_step_title.to_corner(UP+LEFT)
        rec_step_title.shift(DOWN)

        succ_steps = naturals.to_steps(h_placement = 1)
        succ_steps_desc = naturals.add_descriptions(lambda n: TexMobject("\\mathcal P"))
        succ_steps.set_color(succ_color)
        succ_steps_desc.set_color(succ_color)

        VGroup(naturals, naturals_desc, succ_steps, zero_desc, succ_steps_desc).shift(ordinal_shift)
        for succ_step_desc, succ_step in zip(succ_steps_desc, succ_steps):
            succ_step_desc.next_to(succ_step, UP, buff=succ_step_desc.get_width()*0.7)

        self.play(
            ShowCreation(naturals),
            ShowCreation(naturals_desc))
        self.dither()
        self.play(Write(zero_desc))
        self.play(
            Write(VGroup(*zero_step_title[:-1])),
            ReplacementTransform(zero_desc, zero_step_title[-1]))

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
        succ_step_title = TextMobject("Successor", " step", ": ", "Powerset")
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
        omega_pow2_dest[0][0].set_color(zero_color)

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
        zero_step_q = TextMobject("Zero step?")
        zero_step_q.to_corner(UP+LEFT)
        zero_step_q.set_color(GREEN)
        self.play(Write(zero_step_q))

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

        zero_step_a = TextMobject("Minimal element needed")
        zero_step_a.to_corner(UP+LEFT)
        zero_step_a.set_color(GREEN)
        self.play(
            ReplacementTransform(zero_step_q, zero_step_a)
        )
        self.dither()

        zero_dot = Dot(self.line_start, color = BLUE)
        zero_desc = TexMobject("0")
        zero_desc.next_to(zero_dot, LEFT+DOWN)
        self.play(FadeOut(self.pointer))
        self.play(
            ShowCreation(zero_dot),
            Write(zero_desc),
            Write(real_title[2]),
        )
        zero_step = Line(self.line_start+UP, self.line_start, color = GREEN)
        zero_desc = TexMobject("\\omega").set_color(GREEN)
        zero_desc.next_to(zero_step, UP)
        self.dither()
        self.play(
            Write(zero_desc),
            ShowCreation(zero_step),
        )

        self.dither()
        succ_step_q = TextMobject("Successor"," step?")
        succ_step_q.to_corner(UP+LEFT)
        succ_step_q.set_color(WHITE)
        succ_step_q.next_to(zero_step_a, DOWN, coor_mask = UP)

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

        letter_s = succ_step_q[1][0]
        succ_step_q[1].remove(letter_s)
        succ_step_q[0].add(letter_s)
        succ_step_a = TextMobject("Successors","needed")
        succ_step_a.to_corner(UP+LEFT)
        succ_step_a.set_color(WHITE)
        succ_step_a.next_to(zero_step_a, DOWN, coor_mask = UP)

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

        self.add_foreground_mobjects(zero_step, self.pointer[0])
        self.play(
            Uncreate(lines, submobject_mode = 'lagged_start', lag_factor = 2),
            ShowCreation(dots, submobject_mode = 'lagged_start'),
            FadeOut(real_title),
        )
        self.dither()

        lim_step_q = TextMobject("Limit step?")
        lim_step_q.to_corner(UP+LEFT)
        lim_step_q.set_color(YELLOW)
        lim_step_q.next_to(succ_step_q, DOWN, coor_mask = UP)
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

class OmegaPlusZScene(Scene):

    def construct(self):

        omega = OrdinalOmega(x1 = -1)

        omega2 = omega.copy()
        omega_reversed = omega2.copy()
        omega_reversed.scale([-1,1,1], about_point = omega2[0].get_center())
        Z = VGroup(omega_reversed, omega2)

        omega_plus_Z = VGroup(omega, Z)
        omega_plus_Z.arrange_submobjects()
        omega_plus_Z.center()
        omega_plus_Z.set_color(DARK_GREY)

        self.play(ShowCreation(omega))
        self.dither()
        self.play(
            ShowCreation(omega2),
            ShowCreation(omega_reversed),
        )
        self.dither()
        omega_colorful = omega.copy()
        omega_colorful.set_color(WHITE)
        omega_colorful[0].set_color(GREEN)

        first_step_desc = TexMobject("\\omega")
        first_step_desc.set_color(GREEN)
        first_step_desc.next_to(omega_colorful[0], UP)
        self.play(ShowCreation(omega_colorful[0]), ShowCreation(first_step_desc))
        self.dither()
        self.play(ShowCreation(omega_colorful[1]))
        self.play(ShowCreation(omega_colorful[2]))
        self.play(ShowCreation(VGroup(*omega_colorful[3:])))
        self.dither(5)

        
