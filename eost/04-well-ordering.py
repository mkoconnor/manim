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
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *
from random import randint
from chat_bubbles import Conversation

from eost.ordinal import *

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
            coor_mask = np.array([1,0,0]),
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
            coor_mask = np.array([1,0,0]),
            buff = self.ineq_seq_buff)

        next_p_power.next_to(
            next_ineq,
            coor_mask = np.array([1,0,0]),
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
        self.play(Write(TextMobject("Transfinite Recursion").to_edge(DOWN)))
        self.dither(2)
