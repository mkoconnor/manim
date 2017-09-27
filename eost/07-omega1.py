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
from topics.chat_bubbles import Conversation

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer
from topics.objects import BraceDesc, BraceText, Counter
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

import importlib
chapter2 = importlib.import_module('eost.02-size-comparison-countable')
chapter5 = importlib.import_module('eost.05-ordinals')

class CardinalsOrdinalsRecap(chapter2.NotationScene):
    def construct(self):
        self.prepare_overall_picture()
        self.subtitle.to_edge(UP)
        self.add(self.subtitle)
        self.overall_picture.remove(self.finite_brace, self.infinite_brace)
        self.overall_picture.next_to(self.subtitle, DOWN, buff = 1, coor_mask = Y_MASK)
        real_size = TexMobject("|\\mathbb R|")
        real_size.set_color(GREEN)
        real_size.next_to(self.sizes, buff = 1)
        self.sizes.add(real_size)
        self.play(FadeIn(self.sizes))
        self.play(self.countable_brace.creation_anim())
        self.play(self.uncountable_brace.creation_anim())

        ordinal_bg = OrdinalFiniteProd(OrdinalOmega, 3, x1 = 8)
        ordinal_bg.shift(2*DOWN)
        ordinals_title = TextMobject("Ordinals")
        ordinals_title.next_to(ordinal_bg, UP, aligned_edge = LEFT, buff = 0.5)
        ordinal = VGroup(ordinal_bg[0], VGroup(*ordinal_bg[1][:3])).copy()
        ordinal_bg.set_color(DARK_GREY)
        self.play(FadeIn(ordinal_bg), FadeIn(ordinals_title))
        self.play(ShowCreation(ordinal[0]))
        self.play(ShowCreation(ordinal[1]))
        self.dither()
        self.play(FadeOut(self.overall_picture))

        card_sum = TexMobject("\\aleph_0 + \\aleph_0 = \\aleph_0")
        card_prod = TexMobject("\\aleph_0\\cdot\\aleph_0 = \\aleph_0")
        card_sum.next_to(self.subtitle, DOWN)
        card_prod.next_to(card_sum, DOWN)
        card_prod.shift((card_sum[-1].get_center() - card_prod[-1].get_center()) * X_MASK)
        self.play(Write(card_sum))
        self.dither()
        self.play(Write(card_prod))
        self.dither()

        ordinal_dest = ordinal.copy()
        ordinal_bg_dest = ordinal_bg.copy()
        ordinals_title_dest = ordinals_title.copy()
        VGroup(ordinal_bg_dest, ordinal_dest, ordinals_title_dest).shift(0.7*UP)
        ord_type_brace = BraceDesc(ordinal_dest, "\\omega+3")
        self.play(
            Transform(ordinal_bg, ordinal_bg_dest),
            Transform(ordinal, ordinal_dest),
            Transform(ordinals_title, ordinals_title_dest),
            ord_type_brace.creation_anim(),
        )
        bar = ordinal_bg[1][3].copy()
        bar.set_color(BLUE)
        pointer = TrianglePointer(color = BLUE).next_to(bar, UP)
        index_label = ord_type_brace.desc.copy()
        index_label.set_color(BLUE)
        index_label.next_to(pointer, UP)
        self.play(
            ShowCreation(bar),
            FadeIn(pointer),
            FadeIn(index_label),
        )

class SupremumRecap(chapter5.OrdinalByRecursion):
    def construct(self):
        title = TextMobject("Supremum")
        title.to_edge(UP)
        self.add(title)
        
        supremum, _ = self.play_infinite_supremum()
        self.dither()
        self.play(FadeOut(supremum))

class Supremum(Scene):
    def construct(self, fast_play = False):
        #self.force_skipping()
        omega = OrdinalOmega()
        omega_plus_5 = OrdinalSum(OrdinalOmega, 0.75,
                                  lambda **kwargs: OrdinalFinite(5, **kwargs))
        omega_times_3 = OrdinalFiniteProd(OrdinalOmega, 3)
        omega_pow_3 = make_ordinal_power(3, q = (0.7, 0.84, 0.84))
        ordinals = VGroup(omega, omega_plus_5, omega_times_3, omega_pow_3)
        ordinals.stretch(0.4, 1)
        ordinals.arrange_submobjects(DOWN, aligned_edge = LEFT, center = False)
        ordinals.shift(-Y_MASK*ordinals.get_center())
        dots = TexMobject("\\vdots")
        dots.next_to(ordinals, DOWN)

        if fast_play:
            self.add(ordinals, dots)
        else:
            self.play(ShowCreation(omega))
            self.play(ShowCreation(omega_plus_5))
            self.play(ShowCreation(omega_times_3))
            self.play(ShowCreation(omega_pow_3))
            self.play(FadeIn(dots))
            self.dither()

        result = OrdinalFiniteProd(OrdinalOmega, 5, x1 = 8)
        result_stretched = result.copy()
        result_stretched.stretch(omega[0].get_height()
                                 / result_stretched[0][0].get_height(), 1)

        al_omega = result_stretched[0].copy()
        al_omega.shift(omega[0].get_center() - al_omega[0].get_center())

        al_omega_plus_5 = VGroup(result_stretched[0].copy())
        al_omega_plus_5.shift(omega_plus_5[0][0].get_center()
                              - al_omega_plus_5[0][0].get_center())
        al_five = omega_plus_5[1].copy()
        for bar, dest in zip(al_five, result[1]):
            bar.move_to(dest, coor_mask = X_MASK)
        al_omega_plus_5.add(al_five)

        al_omega_times_3 = VGroup(*result_stretched[:3]).copy()
        al_omega_times_3.shift(omega_times_3[0][0].get_center()
                               - al_omega_times_3[0][0].get_center())

        result_in_pow_3 = result_stretched.copy()
        result_in_pow_3.shift(omega_pow_3[0][0][0].get_center()
                              - result_in_pow_3[0][0].get_center())
        al_omega_pow_3 = omega_pow_3.copy()
        al_omega_pow_3.next_to(result_in_pow_3, buff = 0)
        al_omega_pow_3[0].add_to_back(*result_in_pow_3.submobjects)

        al_ordinals = VGroup(al_omega, al_omega_plus_5, al_omega_times_3, al_omega_pow_3)
        if not fast_play: self.dither()
        self.play(ReplacementTransform(ordinals, al_ordinals))

        al_ordinals.remove(al_omega_pow_3)
        al_ordinals.add(result_in_pow_3)
        result_bottom = result.copy()
        result_bottom.stretch(0, 1)
        result_bottom = VGroup(*[result_bottom.copy() for _ in range(5)])
        result_bottom.arrange_submobjects(DOWN, buff = 0.3, center = False)
        result_bottom.to_edge(DOWN, buff = 0)
        al_ordinals.add(result_bottom)

        mrg_omega = result[0].copy()
        mrg_omega_plus_5 = VGroup(result[0], VGroup(*result[1][:5])).copy()
        mrg_omega_times_3 = VGroup(*result[:3]).copy()
        mrg_ordinals = VGroup(
            mrg_omega, mrg_omega_plus_5, mrg_omega_times_3,
            result.copy(), VGroup(result.copy()),
        )
        if not fast_play: self.dither()
        self.play(
            FadeOut(dots),
            ReplacementTransform(al_ordinals, mrg_ordinals),
        )

        self.remove(mrg_ordinals)
        self.add(result)
        if fast_play: return result
        self.dither()
        brace = BraceDesc(result, "\\omega_1", UP)
        self.play(brace.creation_anim())
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("You've said in chapter 5 that taking all ordinals is forbidden.")
        self.dither()
        conversation.add_bubble("We are using just the countable ones.")
        self.dither()

        self.add_foreground_mobjects(conversation.dialog)
        self.play(FadeOut(VGroup(brace, result)))

        omega = OrdinalOmega()
        omega.shift(2*UP)
        self.play(ShowCreation(omega))

class Reorderings(Scene):
    def construct(self):

        self.ordinal_list = VGroup()
        shift = 2*UP
        omega = OrdinalOmega()
        omega.shift(shift)
        omega_ori = omega.copy()

        self.add(omega)

        omega_plus_5 = OrdinalSum(OrdinalOmega, 0.75,
                                  lambda **kwargs: OrdinalFinite(5, **kwargs))
        omega_plus_5.shift(shift)
        omega_src = LimitSubOrdinal(omega[5:])
        five_src = VGroup(*omega[:5])
        self.dither()
        self.play(
            ReplacementTransform(omega_src, omega_plus_5[0]),
            ReplacementTransform(five_src, omega_plus_5[1], path_arc = np.pi/2),
        )
        self.add_to_list(omega_plus_5)
        self.dither()

        omega_times_2 = OrdinalFiniteProd(OrdinalOmega, 2)
        omega_times_2.shift(shift)
        self.play(
            Transform(
                VGroup(
                    LimitSubOrdinal(omega_plus_5[0][0::2]),
                    omega_plus_5[1],
                ),
                VGroup(
                    omega_times_2[0],
                    omega_times_2[1][:5],
                )
            ),
            Transform(
                LimitSubOrdinal(omega_plus_5[0][1::2]),
                LimitSubOrdinal(omega_times_2[1][5:]),
                path_arc = np.pi/2,
            ),
        )
        self.remove(*self.mobjects_from_last_animation)
        self.add(omega_times_2)
        self.add_to_list(omega_times_2)
        self.dither()

        omega = omega_ori
        self.play(
            Transform(omega_times_2[0], LimitSubOrdinal(omega[0::2]),
                      path_arc = np.pi/2),
            Transform(omega_times_2[1], LimitSubOrdinal(omega[1::2]),
                      path_arc = np.pi/2),
        )
        self.add_to_list(omega)
        self.dither()

    def add_to_list(self, ordinal):

        ordinal_dest = ordinal.copy()
        ordinal_dest.set_color(BLUE)
        ordinal_dest.shift(3*DOWN)
        ordinal_list_dest = self.ordinal_list.copy()
        ordinal_list_dest.next_to(ordinal_dest, DOWN, coor_mask = Y_MASK)
        self.play(
            ReplacementTransform(ordinal.copy(), ordinal_dest),
            Transform(self.ordinal_list, ordinal_list_dest),
        )

        self.ordinal_list.add(ordinal_dest)

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

class Omega1Intro(Supremum):
    def construct(self):

        #self.force_skipping()
        supremum = Supremum.construct(self, fast_play = True)

        omega1_brace = BraceDesc(supremum, "\\omega_1", UP)
        self.play(omega1_brace.creation_anim())

        omega1 = Omega1()
        omega1_src = omega1.copy()
        omega1_src[0].highlight(BLACK)
        omega1_src[1].next_to(supremum, buff = 0)
        omega1_src[1].add_to_back(*supremum.submobjects)

        self.dither()
        self.play(
            ReplacementTransform(omega1_src, omega1),
            omega1_brace.shift_brace, omega1,
        )
        self.dither()
        self.revert_to_original_skipping_status()

        countable_point = Dot(2*RIGHT)
        countable_point.set_color(YELLOW)
        countable_arrow = Arrow(
            countable_point.get_center() + DOWN,
            countable_point.get_center(),
        )
        countable_label = TextMobject("a", "countable ordinal")
        countable_label.next_to(countable_arrow, DOWN)

        brace = Brace(Line(omega1.get_corner(LEFT+DOWN),
                           countable_point.get_center()),
                      DOWN)
        brace_label = countable_label.copy()
        brace.put_at_tip(brace_label)

        self.dither()
        self.play(
            FadeIn(countable_label),
            FadeIn(countable_point),
            ShowCreation(countable_arrow),
        )
        self.dither()
        self.play(
            GrowFromCenter(brace),
            ReplacementTransform(countable_label, brace_label),
        )
        self.dither()

        uncountable_brace = Brace(omega1, DOWN)
        uncountable_label = TextMobject("un","countable ordinal",
                                        arg_separator = '')
        uncountable_brace.put_at_tip(uncountable_label)

        self.play(
            Transform(brace, uncountable_brace),
            Transform(brace_label, uncountable_label),
        )
        self.remove(brace_label)
        brace_label = TextMobject("uncountable","ordinal")
        brace.put_at_tip(brace_label)
        self.add(brace_label)

        self.dither()
        uncountable_brace = Brace(Line(countable_point.get_center() + DOWN,
                                       omega1[0].get_edge_center(RIGHT)),
                                  DOWN)
        uncountable_label = TextMobject("uncountable","ordinal")
        uncountable_brace.put_at_tip(uncountable_label)
        uncountable_label[1].highlight(BLACK)
        uncountable_label.shift(uncountable_label.get_center()
                                - uncountable_label[0].get_center())

        self.play(
            Transform(brace, uncountable_brace),
            Transform(brace_label, uncountable_label),
        )
        self.dither()

        omega = OrdinalOmega()
        self.play(
            FadeOut(VGroup(
                omega1, brace, brace_label,
                countable_point, countable_arrow,
            )),
            omega1_brace.change_brace_desc, omega, "\\omega",
        )

class AnalogyOmega(chapter5.OrdinalByRecursion):
    def construct(self):

        omega = OrdinalOmega()
        omega_brace = BraceDesc(omega, "\\omega", UP)
        self.add(omega_brace)
        omega, _ = self.play_infinite_supremum()
        fin_index = 12
        bar = omega[fin_index].copy()
        bar.highlight(YELLOW)
        arrow = Arrow(
            bar.get_edge_center(DOWN) + DOWN,
            bar.get_edge_center(DOWN),
        )
        label = TextMobject("a", "finite ordinal").next_to(arrow, DOWN)

        self.play(
            ShowCreation(bar),
            ShowCreation(arrow),
            FadeIn(label),
        )

        finite_brace = Brace(VGroup(omega[:fin_index]),
                             DOWN)
        brace_label = label.copy()
        finite_brace.put_at_tip(brace_label)

        self.play(
            GrowFromCenter(finite_brace),
            ReplacementTransform(label, brace_label),
        )
        self.dither()

        terminal_segment_brace = BraceText(
            Line(omega[fin_index+1].get_center()+DOWN,
                 omega.get_edge_center(RIGHT)),
            "infinite"
        )
        self.play(terminal_segment_brace.creation_anim())
        self.dither()

        self.play(FadeOut(VGroup(
            finite_brace, brace_label, terminal_segment_brace,
            bar, arrow,
        )))
