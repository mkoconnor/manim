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

def is_prime(p):
    if p < 2: return False
    if p == 2: return True
    if p%2 == 0: return False
    for d in xrange(3, p//2, 2):
        if p%d == 0: return False
    return True

class LeastInfinite(Scene):
    def setup(self):
        self.shift = 1.1
        shift = self.shift

        self.omega = OrdinalOmega()
        self.omega_brace = BraceDesc(self.omega, "\\omega", UP)
        self.omega.set_color(BLUE)

        self.add(self.omega, self.omega_brace)

        # finite subset

        self.subset_fin = VGroup(self.omega[2:30:3]).copy()
        self.al_subset_fin = VGroup(self.omega[:len(self.subset_fin)]).copy()
        self.shifted_subset_fin = self.subset_fin.copy()
        VGroup(self.al_subset_fin, self.shifted_subset_fin).shift(shift*DOWN)

        self.brace_fin = BraceText(self.al_subset_fin, "finite")

        # infinite subset
        
        self.subset_inf = LimitSubOrdinal([
            bar
            for i, bar in enumerate(self.omega)
            if is_prime(i)
        ]).copy()
        self.al_subset_inf = self.omega.copy()
        self.shifted_subset_inf = self.subset_inf.copy()
        VGroup(self.al_subset_inf, self.shifted_subset_inf).shift(shift*DOWN)
        self.brace_inf = BraceText(self.al_subset_inf, "equal")

    def construct(self):

        shift = self.shift

        # finite subset

        self.play(
            VGroup(self.omega, self.omega_brace).shift, shift*UP,
            Transform(self.subset_fin, self.shifted_subset_fin)
        )
        self.dither()
        self.play(Transform(self.subset_fin, self.al_subset_fin))
        self.dither()

        self.play(self.brace_fin.creation_anim())
        self.dither()

        self.play(FadeOut(VGroup(self.subset_fin, self.brace_fin)))

        # infinite subset

        self.play(Transform(self.subset_inf, self.shifted_subset_inf))
        self.play(Transform(self.subset_inf, self.al_subset_inf))
        self.dither()
       
        self.play(self.brace_inf.creation_anim())
        self.dither()

        self.play(FadeOut(VGroup(self.subset_inf, self.brace_inf)))

        omega1 = Omega1()
        omega1.shift(shift*UP)
        self.play(
            FadeIn(omega1),
            FadeOut(self.omega),
            self.omega_brace.change_brace_desc, omega1, "\\omega_1", 
        )

class LeastUncountable(Scene):
    def setup(self):
        self.shift = 1.1
        shift = self.shift

        self.omega1 = Omega1()
        self.omega1.shift(shift*UP)
        self.omega1_brace = BraceDesc(self.omega1, "\\omega_1", UP)
        self.add(self.omega1, self.omega1_brace)

        # countable subset
        
        omega = OrdinalOmega(x1 = -2)
        omega.stretch(0.5, 1)
        omega.next_to(self.omega1[1])
        self.count_subset = VGroup(
            self.omega1[1][0],
            LimitSubOrdinal([subord[0] for subord in self.omega1[1][1:]]),
        ).copy()
        self.count_subset.add(omega)
        self.al_count_subset = VGroup(self.omega1[1][:3]).copy()
        self.shifted_count_subset = self.count_subset.copy()
        VGroup(
            self.al_count_subset,
            self.shifted_count_subset
        ).shift(2*shift*DOWN)
        omega.stretch_in_place(0, 1)

        self.count_brace = BraceText(self.al_count_subset, "countable")

    def construct(self):

        #self.force_skipping()
        shift = self.shift

        # countable subset
        
        self.dither()
        self.play(Transform(self.count_subset, self.shifted_count_subset))
        self.dither()
        self.play(Transform(self.count_subset, self.al_count_subset))
        self.dither()
        self.play(self.count_brace.creation_anim())
        self.dither()

        self.play(FadeOut(VGroup(self.count_brace, self.count_subset)))

        # uncountable subset
        
        unc_initial = LimitSubOrdinal([subord[0] for subord in self.omega1[1]])
        unc_initial = unc_initial.copy()
        unc_line = DashedLine(self.omega1[0].get_edge_center(LEFT),
                              self.omega1[0].get_edge_center(RIGHT))
        unc_line.gradient_highlight(BLACK, WHITE)
        start_x = unc_initial.get_edge_center(RIGHT)[0]
        unc_line.submobjects = filter(
            lambda l: l.get_edge_center(LEFT)[0] > start_x,
            unc_line.submobjects
        )
        unc_subset = VGroup(unc_initial, unc_line)
        self.play(VGroup(unc_initial, unc_line).shift, 2*shift*DOWN)
        self.revert_to_original_skipping_status()
        self.dither()

        al_unc_subset = Omega1().shift(shift*DOWN)
        al_unc_line, al_unc_initial = al_unc_subset
        ini_index = 9
        al_unc_line_parts = []

        # split gradient line to larger parts
        line_len = (unc_line[2].get_center() - unc_line[1].get_center())[0]
        remaining = len(unc_line) - (ini_index+1) - 1
        next_split = al_unc_line.get_edge_center(LEFT)[0]
        for grad_part in al_unc_line:
            if remaining > 0 and grad_part.get_center()[0] >= next_split:
                next_split += line_len
                al_unc_line_parts.append([])
            al_unc_line_parts[-1].append(grad_part)
        al_unc_line_parts = VGroup(al_unc_line_parts)

        self.play(
            Transform(
                VGroup(unc_line[ini_index+1:]),
                al_unc_line_parts,
            ),
            Transform(unc_initial, al_unc_initial[0]),
            Transform(
                VGroup(unc_line[:ini_index]),
                VGroup(al_unc_initial[1:ini_index+1]),
            ),
            Transform(
                unc_line[ini_index],
                VGroup(unc_initial[ini_index+1:]),
            )
        )
        self.dither()
        self.remove(*self.mobjects_from_last_animation)
        unc_subset = al_unc_subset
        self.add(unc_subset)

        unc_brace = BraceText(unc_subset, "equal")
        self.play(unc_brace.creation_anim())
        self.dither()

        cardinality = TexMobject("|","\\omega_1", "|=\\aleph_1")
        cardinality.shift(self.omega1_brace.desc.get_center()
                          - cardinality[1].get_center())
        cardinality.remove(cardinality[1])
        self.play(Write(cardinality))
        self.dither()

class ContinuumHypothesis(Scene):
    def construct(self):

        title = TextMobject("Continuum Hypothesis").to_edge(UP)
        question = TextMobject("Is $|\mathbb R|$ the smallest uncountable cardinality?")
        question.shift(DOWN)

        self.add(title)
        cardinalities = TexMobject("0, 1, 2, \ldots","\\aleph_0",
                                   "\\aleph_1","=","|\\mathbb R|","?")
        cardinalities.set_color(GREEN)
        cardinalities[1].next_to(cardinalities[0], coor_mask = X_MASK, buff = 1)
        VGroup(cardinalities[2:]).next_to(cardinalities[1], coor_mask = X_MASK, buff = 0.5)
        cardinalities.next_to(title, DOWN)
        count_brace = BraceText(VGroup(cardinalities[:2]), "countable")
        self.play(
            count_brace.creation_anim(),
            *map(FadeIn, [
                cardinalities[0], cardinalities[1], cardinalities[4]
            ])
        )
        self.play(Write(question))

        arrow_end = (cardinalities[1].get_center() + cardinalities[4].get_center())/2
        arrow = Arrow(arrow_end+DOWN, arrow_end)

        why_not_answer = TextMobject("Why anything\\\\ should be here?",
                                 alignment="\\raggedright")
        why_not_answer.next_to(arrow, DOWN, aligned_edge = LEFT)
        why_not_answer.shift(0.5*LEFT)

        self.dither()
        self.play(ShowCreation(arrow), FadeIn(why_not_answer))

        self.dither()
        self.play(FadeOut(VGroup(arrow, why_not_answer)))
        why_answer = VGroup(cardinalities[3], cardinalities[5])
        why_answer.set_color(WHITE)
        self.play(Write(cardinalities[2])) # omega1
        self.play(Write(why_answer))

        omega1 = Omega1()
        make_half_ordinal(omega1[1])
        reals = NumberLine(x_min = -4, x_max = 4)
        reals.set_color(WHITE)

        reals.to_edge(DOWN)
        omega1.next_to(reals, UP, buff = 2)
        self.dither()
        self.play(FadeOut(question))
        self.play(FadeIn(reals), FadeIn(omega1))

        positions_num = 50
        positions = np.expand_dims(np.linspace(-4, 4, positions_num), 1) * RIGHT
        positions_real = positions + reals.get_edge_center(UP) + UP*0.1
        positions_omega1 = positions + omega1.get_edge_center(DOWN) + DOWN*0.1
        positions_omega1 = list(positions_omega1)
        random.shuffle(positions_omega1)

        matching = VGroup([
            Line(start, end)
            for start, end in zip(positions_omega1, positions_real)
        ])
        matching.set_color(BLUE)
        self.play(ShowCreation(
            matching,
            submobject_mode = "all_at_once",
        ))
        self.dither()
        self.play(FadeOut(matching))

class UnboundedOmega(LeastInfinite):
    def construct(self):

        VGroup(
            self.omega, self.omega_brace, self.subset_inf
        ).shift(self.shift*UP)
        
        subset_ori = self.subset_inf.copy()
        subset = self.subset_inf

        self.play(Transform(subset, self.shifted_subset_inf))
        self.play(Transform(subset, self.al_subset_inf))

        self.dither()
        self.play(Transform(subset, self.shifted_subset_inf))
        self.dither()

        self.subset = subset
        self.brace = None
        self.show_terminal_brace(-2)
        self.dither()
        self.show_terminal_brace(0)
        self.dither()
        self.show_terminal_brace(2)
        self.dither()

        self.play(
            FadeOut(self.brace),
            subset.highlight, BLUE,
        )
        unbounded = TextMobject("unbounded")
        unbounded.next_to(subset, DOWN)
        self.play(FadeIn(unbounded))
        self.dither()

        self.play(
            FadeOut(VGroup(unbounded, subset)),
            FadeIn(self.al_subset_fin),
        )
        subset = self.al_subset_fin
        self.play(
            self.brace_fin.creation_anim(),
        )
        self.play(
            Transform(subset, self.shifted_subset_fin),
            self.brace_fin.shift_brace, self.shifted_subset_fin,
        )
        bar = subset[-1].copy()
        bar.highlight(YELLOW)
        self.play(ShowCreation(bar))
        term_part = VGroup([
            p
            for p in self.omega
            if p.get_center()[0] > bar.get_center()[0]
        ])
        brace = Brace(term_part, DOWN)
        label = TextMobject("unused")
        label.next_to(brace, DOWN, aligned_edge = LEFT)
        bar = bar.copy()
        self.play(bar.shift, 2*self.shift*UP)
        term_part.highlight(WHITE)
        self.play(
            GrowFromCenter(brace),
            FadeIn(label),
        )
        self.dither()

    def show_terminal_brace(self, pos):
        line = Line(pos*RIGHT, 4*RIGHT)
        line.shift((1+self.shift)*DOWN)

        next_brace = Brace(line, DOWN)
        if self.brace is None:
            self.play(GrowFromCenter(next_brace))
        else:
            self.play(ReplacementTransform(self.brace, next_brace))
        self.brace = next_brace

        for bar in self.subset:
            if bar.get_center()[0] < pos: bar.highlight(DARK_GREY)
            else: bar.highlight(BLUE)

class UnboundedOmega1(LeastUncountable):
    def construct(self):

        #self.force_skipping()
        
        subset = self.al_count_subset
        self.play(FadeIn(subset))
        self.dither()
        self.play(self.count_brace.creation_anim())
        self.dither()
        self.play(
            Transform(subset, self.shifted_count_subset),
            self.count_brace.shift_brace, self.shifted_count_subset,
        )
        self.dither()

        supremum = Line(ORIGIN, DOWN).next_to(subset, buff = 0)
        supremum.set_color(YELLOW)
        self.play(ShowCreation(supremum))

        self.dither()

        identity = TexMobject("\\aleph_0\\cdot\\aleph_0 = \\aleph_0")
        identity.next_to(supremum, buff = 1)
        self.play(FadeIn(identity))

        supremum_in_ori = supremum.copy()
        supremum_in_ori.move_to(self.omega1, coor_mask = Y_MASK)
        self.dither()
        self.play(ReplacementTransform(supremum.copy(), supremum_in_ori))

        self.dither()
        self.play(FadeOut(identity))
        brace_base = Line(
            supremum_in_ori.get_edge_center(DOWN),
            self.omega1[0].get_edge_center(RIGHT),
        )
        brace_unused = BraceText(brace_base, "unused")
        self.play(brace_unused.creation_anim())

        self.dither()
        self.play(FadeOut(VGroup(
            brace_unused, subset, supremum, supremum_in_ori, self.count_brace
        )))

        seq = OrdinalOmega(x0 = -1, x1 = 2)
        seq.set_color(GREEN)
        seq.stretch(0.5, 1)
        seq.shift(self.shift*UP)
        self.play(ShowCreation(seq))

        supremum.next_to(seq, buff = 0)
        self.dither()
        self.play(ShowCreation(supremum))

        self.dither()
        self.play(FadeOut(VGroup(seq, supremum)))

        seq = OrdinalOmega(x0 = -1, x1 = 4)
        seq.set_color(GREEN)
        seq.stretch(0.5, 1)
        seq.shift(self.shift*UP)
        self.play(ShowCreation(seq))

        self.revert_to_original_skipping_status()
        self.dither()
        self.omega1.add(seq)
        stretched_omega1 = self.omega1.copy()
        stretched_omega1.stretch_about_point(
            0.6, 0,
            self.omega1.get_edge_center(LEFT)
        )
        added_line = Line(
            stretched_omega1.get_edge_center(RIGHT),
            self.omega1.get_edge_center(RIGHT),
            color = WHITE
        )
        self.add(added_line)
        supremum.move_to(added_line.get_edge_center(LEFT))

        brace_unc = BraceText(VGroup(supremum, added_line), "uncountable")
        brace_src = brace_unc.brace.copy()
        brace_src.stretch_about_point(0,0,added_line.get_edge_center(RIGHT))

        self.play(
            Transform(self.omega1, stretched_omega1),
            ReplacementTransform(brace_src, brace_unc.brace),
            FadeIn(brace_unc.desc),
        )
        self.play(ShowCreation(supremum))
        self.dither()

class SemiOpen(VMobject):
    def __init__(self, left = LEFT, right = RIGHT, color = BLUE, dot_radius = 0.1, **kwargs):
        VMobject.__init__(self,
            Dot(left, radius = dot_radius, color = color),
            Line(left, right, color = color),
            VGroup(
                Dot(right, radius = dot_radius, color = color),
                Dot(right, radius = 0.6*dot_radius, color = BLACK),
            ),
            **kwargs
        )

    @property
    def first_point(self): return self.submobjects[0]
    @property
    def line(self): return self.submobjects[1]
    @property
    def second_point(self): return self.submobjects[2]

class IntervalMul(Scene):
    def construct(self):

        # self.force_skipping()
        
        # left-closed, right-open, two intervals
        
        interval1 = SemiOpen()
        interval2 = interval1.copy()
        VGroup(interval1, interval2).arrange_submobjects(buff = 1)
        self.play(
            FadeIn(interval1),
            FadeIn(interval2),
        )
        self.dither()

        self.play(
            interval1.move_to, LEFT,
            interval2.move_to, RIGHT,
        )
        self.remove(interval1.second_point)
        self.play(interval2.first_point.scale_in_place, 0)

        interval = SemiOpen(2*LEFT, 2*RIGHT)
        self.remove(interval1, interval2)
        self.add(interval)
        self.dither()
        interval_dest = SemiOpen(LEFT, RIGHT)
        self.play(Transform(interval, interval_dest))
        self.dither()
        self.play(FadeOut(interval))

        interval1 = SemiOpen()
        interval2 = interval1.copy()
        VGroup(interval1, interval2).arrange_submobjects(buff = 1)
        for interval in [interval1, interval2]:
            interval.stretch_in_place(-1, 0)

        # left-open, right-closed, two intervals

        self.play(
            FadeIn(interval1),
            FadeIn(interval2),
        )
        self.dither()

        self.play(
            interval2.move_to, RIGHT,
            interval1.move_to, LEFT,
        )
        self.remove(interval2.second_point)
        self.play(interval1.first_point.scale_in_place, 0)

        interval = SemiOpen(2*RIGHT, 2*LEFT)
        self.remove(interval1, interval2)
        self.add(interval)
        self.dither()
        interval_dest = SemiOpen(RIGHT, LEFT)
        self.play(Transform(interval, interval_dest))
        self.dither()

        # left-open, right-closed, omega

        omega = OrdinalOmega()
        omega.highlight(DARK_GREY)
        interval_copies = []
        for bar in omega:
            interval_copy = SemiOpen(RIGHT*bar.x1, RIGHT*bar.x0,
                                     dot_radius = 0.1*bar.height)
            interval_copies.append(interval_copy)

        final_interval = SemiOpen(RIGHT*omega.x0, RIGHT*omega.x1)
        interval_copies.reverse()
        interval_copies = VGroup(interval_copies)
        VGroup(omega, interval_copies, final_interval).shift(UP)

        self.play(
            FadeIn(omega),
            interval.shift, 0.8*DOWN,
        )
        interval_copies_src = interval_copies.copy()
        for interval_copy in interval_copies_src:
            interval_copy.scale_in_place(0)
        self.play(ReplacementTransform(interval_copies_src, interval_copies))
        to_shrink = []
        for interval_copy in interval_copies:
            self.remove(interval_copy.second_point)
            to_shrink.append(interval_copy.first_point)

        self.add(interval_copies[-1].second_point)
        to_shrink = VGroup(to_shrink)
        to_shrink_ori = to_shrink.copy()
        shrinked = to_shrink.copy()
        for dot in shrinked: dot.scale_in_place(0)
        self.play(
            Transform(to_shrink, shrinked),
            UnapplyMethod(final_interval.second_point.scale_in_place, 0),
            run_time = 0.5,
        )
        self.remove(interval_copies)
        self.add(final_interval.line,
                 interval_copies[-1].second_point)
        self.add_foreground_mobjects(final_interval.second_point)

        self.dither()

        # left-closed, right-open, omega

        self.play(Rotate(interval, in_place = True))

        self.dither()

        self.play(
            Transform(to_shrink, to_shrink_ori),
            run_time = 0.5,
        )

        interval_copies_dest = interval_copies.copy()
        bg, bg_dest, fg, fg_dest = [], [], [], []
        for interval_copy_dest in interval_copies_dest:
            interval_copy_dest.scale_in_place(-1)
            bg_dest += [interval_copy_dest.line, interval_copy_dest.second_point]
            fg_dest.append(interval_copy_dest.first_point)
        for interval_copy in interval_copies:
            bg += [interval_copy.line, interval_copy.second_point]
            fg.append(interval_copy.first_point)

        bg, bg_dest, fg, fg_dest = map(VGroup, (bg, bg_dest, fg, fg_dest))

        self.remove(final_interval)
        self.add_foreground_mobjects(final_interval.second_point)
        self.play(
            Transform(
                bg, bg_dest,
                path_arc = np.pi
            ),
            Transform(
                fg, fg_dest,
                path_arc = np.pi
            ),
        )
        self.remove(bg)
        self.add(final_interval)

        shrinked = to_shrink.copy()
        for dot in shrinked: dot.scale_in_place(0)

        self.play(
            Transform(to_shrink, shrinked),
            run_time = 0.5,
        )

        self.dither()

        # left-closed, right-open, omega*2

        interval_template = interval # some renaming
        interval = final_interval

        omega_cdot_2 = OrdinalFiniteProd(OrdinalOmega, 2)
        omega_cdot_2.set_color(DARK_GREY)

        intervals2 = [
            SemiOpen(RIGHT*ordinal.x0, RIGHT*ordinal.x1)
            for ordinal in omega_cdot_2[0], omega_cdot_2[1][0], omega_cdot_2[1][1], omega_cdot_2
        ]
        intervals2.append(SemiOpen(RIGHT*omega_cdot_2.x0, RIGHT*omega_cdot_2[1][1].x1))
        VGroup(omega_cdot_2, intervals2).shift(UP)

        self.dither()
        self.play(
            ReplacementTransform(omega, omega_cdot_2[0]),
            Transform(interval, intervals2[0]),
        )
        self.revert_to_original_skipping_status()
        self.dither()

        self.remove_foreground_mobjects(interval.second_point)
        interval2_1_src = intervals2[1].copy()
        interval2_1_src.set_color(BLACK).shift(RIGHT)
        self.play(
            ShowCreation(omega_cdot_2[1][0]),
            Animation(interval),
            ReplacementTransform(interval2_1_src, intervals2[1])
        )
        self.remove(interval.second_point)
        interval.line.scale_about_point(1.1, interval.line.get_edge_center(LEFT))
        self.play(intervals2[1].first_point.scale_in_place, 0, run_time = 0.5)
        self.dither()

        interval2_2_src = intervals2[2].copy()
        interval2_2_src.set_color(BLACK).shift(RIGHT)
        self.play(
            ShowCreation(omega_cdot_2[1][1]),
            Animation(intervals2[1]),
            ReplacementTransform(interval2_2_src, intervals2[2])
        )
        self.remove(interval, intervals2[1], intervals2[2])
        interval = intervals2[4]
        self.add(interval)
        self.play(intervals2[2].first_point.scale_in_place, 0, run_time = 0.5)
        self.remove(intervals2[2].first_point)
        self.dither()

        self.play(
            FadeIn(VGroup(omega_cdot_2[1][2:]),
                   submobject_mode = "lagged_start"),
            Transform(interval, intervals2[3]),
        )
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("Shouldn't the result be longer than the first factor?")
        self.dither()
        conversation.add_bubble("Interval is not well-ordered.")
        self.dither()

        self.play(FadeOut(VGroup(omega_cdot_2, interval, conversation.dialog)))

class LongLine(Scene):
    def construct(self):

        self.force_skipping()

        interval_template = SemiOpen()
        interval_template.shift(0.8*DOWN)
        self.add(interval_template)

        omega1 = Omega1().shift(UP)

        self.play(FadeIn(omega1))
        self.dither()
        omega1_start = OrdinalFiniteProd(
            lambda **kwargs: OrdinalOmega(q = (0.7, 0.84, 0.84), **kwargs), 4, x1 = 8
        ).shift(UP)
        omega1_dest = omega1.copy().next_to(omega1_start, buff = 0)
        omega1_dest[1].add_to_back(*omega1_start)

        omega1_dest.set_color(GREY)
        self.play(Transform(omega1, omega1_dest))
        self.remove(omega1)
        self.add(omega1_start)

        intervals = []
        for subord in omega1_start:
            for bar in subord:
                intervals.append(SemiOpen(
                    UP + RIGHT*bar.x0, UP + RIGHT*bar.x1,
                    radius = 0.1*bar.height,
                ))
        intervals = VGroup(intervals)
        intervals_outside = VGroup([interval_template.copy() for _ in range(20)])
        intervals_outside.arrange_submobjects()
        intervals_outside.next_to(intervals)
        self.play(
            ReplacementTransform(VGroup(interval_template.copy()), intervals),
            ReplacementTransform(VGroup(interval_template), intervals_outside),
        )

        to_shrink = []
        self.remove(intervals[0].second_point)
        for interval in intervals[1:]:
            to_shrink.append(interval.first_point)
            self.remove(interval.second_point)
        to_shrink = VGroup(to_shrink)
        shrinked = to_shrink.copy()
        for dot in shrinked: dot.scale_in_place(0)

        self.play(Transform(to_shrink, shrinked), run_time = 0.5)
        self.remove(intervals)
        interval = SemiOpen(omega1_start.get_edge_center(LEFT),
                            omega1_start.get_edge_center(RIGHT))
        self.add(interval)


        title = TextMobject("Long Line").to_edge(UP)
        self.play(Write(title))


        self.dither()

        self.ordinal = omega1_start
        self.brace = None
        self.show_initial_brace(-1.5)
        self.dither()
        self.show_initial_brace(2.5)
        self.dither()
        self.show_initial_brace(4.5)
        self.dither()

        line = Line(-4*RIGHT, 10*RIGHT)
        next_brace = Brace(line, DOWN).highlight(BLACK)
        self.add_foreground_mobjects(interval)
        self.play(
            FadeOut(self.ordinal),
            Transform(self.brace, next_brace),
        )
        self.remove(next_brace)
        self.remove_foreground_mobjects(interval)

        # sequence and supremum

        self.revert_to_original_skipping_status()
        seq_start = OrdinalFiniteProd(OrdinalOne, 8, x0 = 0, x1 = 8, height = 0.5)
        seq_dest = OrdinalOmega(height = 0.5, x0 = -1.5)
        seq_g = VGroup(seq_start, seq_dest)
        seq_g.shift(UP)
        seq_g.set_color(GREEN)
        seq = seq_dest.copy().next_to(seq_start, buff = 1)
        seq.add_to_back(*seq_start)
        for bar in seq_start:
            self.play(ShowCreation(bar), run_time = 0.4)
        self.dither()
        self.play(Transform(seq, seq_dest))

        supremum = Line(ORIGIN, DOWN, color = YELLOW).next_to(seq)
        self.play(ShowCreation(supremum))
        self.dither()
        self.play(FadeOut(VGroup(seq, supremum)))

    def show_initial_brace(self, pos):
        line = Line(-4*RIGHT, pos*RIGHT)

        next_brace = Brace(line, DOWN)
        if self.brace is None:
            self.play(GrowFromCenter(next_brace))
        else:
            self.play(ReplacementTransform(self.brace, next_brace))
        self.brace = next_brace

        for bar in self.ordinal.family_members_with_points():
            if bar.get_center()[0] < pos: bar.highlight(WHITE)
            else: bar.highlight(DARK_GREY)

class NextChapter(Scene):
    def construct(self):

        conversation = Conversation(self, start_answer = True)

        conversation.add_bubble("Is there a set of all sets?")
        conversation.add_bubble("Sure, why shouldn't be?")
        self.dither()
        conversation.add_bubble("What about the set of all sets not containing themselves?")
        self.dither()
        conversation.add_bubble("Just discard some elements of the previous one?")
        self.dither()
        conversation.add_bubble("Does such a set contain itself?")
        conversation.add_bubble("Oops...")
