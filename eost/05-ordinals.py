# coding: utf-8

from helpers import *

from mobject.tex_mobject import *
from mobject.vectorized_mobject import *
from topics.number_line import NumberLine
from topics.icons import *
from topics.chat_bubbles import Conversation
from topics.fruit import *

from animation.transform import *
from animation.simple_animations import *

import random
import eost.deterministic

from eost.ordinal import *

from topics.common_scenes import OpeningTitle, OpeningQuote

class Chapter5OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 5\\\\ Ordinal Numbers",
    }
class Chapter5OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "All of this is actually completely","trivial.\\\\","It is just difficult to","comprehend","it.",
        ],
        "highlighted_quote_terms" : {
            "trivial.\\\\" : GREEN,
            "comprehend" : YELLOW,
        },
        "author" : "from Mathematical Analysis lecture"
    }

class SimultaneousRecursion(Scene):
    def construct(self):
        #self.force_skipping()
        
        title = TextMobject("Well ordered sets")
        title.to_edge(UP)
        
        self.add(title)

        self.prepare_ord1(OrdinalSum(OrdinalOmega, 0.8,
                                     lambda **kwargs: OrdinalFinite(5, **kwargs)))

        self.play(FadeIn(self.ordinal1_bg))

        self.wait_to(3.5)
        for i in range(2):
            for bar in self.ordinal1_fg[i][:2]:
                self.play(ShowCreation(bar), run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
            self.play(ShowCreation(VGroup(*self.ordinal1_fg[i][2:])))

        self.wait_to(8)
        self.prepare_ord2(OrdinalOmega())

        self.play(FadeIn(self.ordinal2_bg))
        for bar in self.ordinal2_fg[:3]:
            self.play(ShowCreation(bar), run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
        self.play(ShowCreation(VGroup(*self.ordinal2_fg[3:])))

        self.wait_to(26)
        self.play(*map(FadeOut, [self.ordinal1_fg, self.ordinal2_fg]))

        ordinal1_fg_al = self.ordinal1_fg[0].copy()
        ordinal1_fg_al.align_data(self.ordinal2_fg)

        self.wait_to(33.2)
        for bar1, bar2, run_time, wait_time in\
            zip(ordinal1_fg_al[:3], self.ordinal2_fg[:3], (1,1,0.5), (36, 38.9, 39.6)):

            self.play(ShowCreation(bar1),
                      ShowCreation(bar2),
                      run_time = run_time*DEFAULT_ANIMATION_RUN_TIME)
            self.wait_to(wait_time)

        self.play(ShowCreation(VGroup(*ordinal1_fg_al[3:])),
                  ShowCreation(VGroup(*self.ordinal2_fg[3:])))

        self.wait_to(49)

        self.remove(self.ordinal2_bg)
        self.play(*map(FadeOut, [ordinal1_fg_al, self.ordinal2_fg]))

        self.prepare_ord2(OrdinalFiniteProd(OrdinalOmega, 2))

        self.play(FadeIn(self.ordinal2_bg), run_time = 0.5)
        ordinal2_fg_al = self.ordinal2_fg[0].copy()
        ordinal2_fg_al.align_data(self.ordinal1_fg[0])
        ordinal2_fg_al = VGroup(ordinal2_fg_al,
                                VGroup(*self.ordinal2_fg[1][:5]))
        
        self.play_both(self.ordinal1_fg, ordinal2_fg_al)
        self.wait_to(54)

        self.remove(self.ordinal1_bg)
        self.play(*map(FadeOut, [self.ordinal1_fg, ordinal2_fg_al]))

        self.prepare_ord1(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.play(FadeIn(self.ordinal1_bg))

        self.ordinal1_fg.align_data(self.ordinal2_fg)
        self.play_both(self.ordinal1_fg, self.ordinal2_fg)
        self.dither()

        self.wait_to(60 + 3)
        #self.revert_to_original_skipping_status()

        self.play(Uncreate(VGroup(*self.ordinal1_fg[1][3:]), clean_up_alpha = 0),
                  Uncreate(VGroup(*self.ordinal2_fg[1][3:]), clean_up_alpha = 0),
        )
        self.dither()

        pointer1 = TrianglePointer(color = RED).next_to(self.ordinal1_fg[1][3], UP)
        self.ordinal1_fg[1][3].set_color(RED)
        self.play(*map(ShowCreation, [pointer1, self.ordinal1_fg[1][3]]))

        self.wait_to(60 + 6.5)
        pointer2 = TrianglePointer(color = RED).scale(-1).next_to(self.ordinal2_fg[1][3], DOWN)
        self.ordinal2_fg[1][3].set_color(RED)
        self.play(*map(ShowCreation, [pointer2, self.ordinal2_fg[1][3]]))

        self.wait_to(60 + 11)

        self.remove(self.ordinal1_bg, self.ordinal2_bg)
        self.add(self.ordinal1_fg, self.ordinal2_fg)
        VGroup(*self.ordinal1_fg[1][4:]).set_color(DARK_GREY)
        VGroup(*self.ordinal2_fg[1][4:]).set_color(DARK_GREY)
        ordinal2_dest = self.ordinal1_fg.copy()
        ordinal2_dest.shift(2.8*DOWN)
        self.play(Transform(self.ordinal2_fg, ordinal2_dest),
                  pointer2.next_to, ordinal2_dest[1][3], DOWN)
        self.wait_to(60 + 14)
        ordinal_dest = self.ordinal1_fg.copy()
        VGroup(*ordinal_dest[1][1:]).highlight(WHITE)
        self.play(FadeOut(pointer1), FadeOut(pointer2),
                  Transform(self.ordinal1_fg, ordinal_dest.copy()),
                  Transform(self.ordinal2_fg, ordinal_dest))
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(ordinal_dest)

        self.wait_to(60 + 21)
        ordinal_numbers_title = TextMobject("Ordinal numbers").to_edge(DOWN)
        self.play(Write(ordinal_numbers_title))
        self.wait_to(60 + 27)
        self.play(FadeOut(ordinal_dest))

    def play_both_simple(self, o1, o2, one_range = 2):
        for bar1, bar2 in zip(o1[:one_range], o2[:one_range]):
            self.play(ShowCreation(bar1),
                      ShowCreation(bar2),
                      run_time = 0.4*DEFAULT_ANIMATION_RUN_TIME)
        self.play(ShowCreation(VGroup(*o1[one_range:])),
                  ShowCreation(VGroup(*o2[one_range:])), run_time = 0.7)

    def play_both(self, o1, o2):
        for o1_part, o2_part in zip(o1, o2):
            self.play_both_simple(o1_part, o2_part)

    def prepare_ord1(self, ordinal):
        self.ordinal1_bg, self.ordinal1_fg = self.prepare_ord(ordinal.shift(1.2*UP))
    def prepare_ord2(self, ordinal):
        self.ordinal2_bg, self.ordinal2_fg = self.prepare_ord(ordinal.shift(1.6*DOWN))
    def prepare_ord(self, ordinal):
        ordinal_bg = ordinal.copy()
        ordinal_fg = ordinal
        ordinal_bg.set_color(DARK_GREY)
        if len(ordinal) > 2: ordinal_fg[0].set_color(GREEN)
        else:
            ordinal_fg[0][0].set_color(GREEN)
            ordinal_fg[1][0].set_color(YELLOW)
        return ordinal_bg, ordinal_fg

def make_matching(o1, o2):
    matching = []
    for line1, line2 in zip(self.ordinal1.family_members_with_points(),
                            self.ordinal2.family_members_with_points()):
        m_line = Line(line1.get_end() + 0.05*DOWN,
                      line2.get_end() + 0.05*UP,
                      stroke_width = (line1.stroke_width + line2.stroke_width)/2,
                      color = WHITE)
        matching.append(m_line)

    self.matching = VGroup(*matching)

def one_apple_ord(**kwargs):
    return OrdinalObj(Apple().scale(0.6), pos = DOWN, **kwargs)

def one_pear_ord(**kwargs):
    return OrdinalObj(Pear().scale(0.6), pos = UP, **kwargs)

class OrdinalMatching(Scene):
    def construct(self):
        #self.force_skipping()

        title = TextMobject("Well ordered sets").to_edge(UP)
        ordinal_numbers_title = TextMobject("Ordinal numbers").to_edge(DOWN)
        self.add(title, ordinal_numbers_title)

        self.make_ord1(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.make_ord2(OrdinalSum(OrdinalOmega, 0.5, OrdinalOmega))

        desc1 = TexMobject("A").highlight(RED).next_to(self.ordinal1, LEFT, buff = 1)
        desc2 = TexMobject("B").highlight(YELLOW).next_to(self.ordinal2, LEFT, buff = 1)

        self.play(*map(FadeIn, [self.ordinal1, self.ordinal2, desc1, desc2]))
        self.wait_to(3)

        self.ordinal1.align_data(self.ordinal2)
        self.make_matching()
        self.play(ShowCreation(self.matching[0]))
        self.play(ShowCreation(self.matching[1]))
        self.wait_to(7)

        type_comparison = TexMobject("\\operatorname{type}(A)",
                                     "=",
                                     "\\operatorname{type}(B)")
        type_comparison.next_to(ordinal_numbers_title, UP, buff = 0.5)
        type_comparison[0].set_color(RED)
        type_comparison[2].set_color(YELLOW)

        self.play(Write(type_comparison))
        self.wait_to(15.5)

        o_ord2 = self.ordinal2
        o_matching = self.matching
        self.make_ord2(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.ordinal1.align_data(self.ordinal2)
        self.make_matching()
        self.play(ReplacementTransform(o_matching, self.matching),
                  ReplacementTransform(o_ord2, self.ordinal2))
        self.wait_to(19.8)

        self.play(*map(FadeOut, [self.matching, self.ordinal2, type_comparison[1]]))

        self.make_ord2(OrdinalSum(OrdinalOmega, 0.8,
                                  lambda **kwargs: OrdinalFinite(5, **kwargs)))
        self.play(FadeIn(self.ordinal2))
        self.dither()

        self.ordinal1[0].align_data(self.ordinal2[0])
        self.make_matching()

        self.play(ShowCreation(self.matching[0]))
        self.play(ShowCreation(self.matching[1]))
        self.wait_to(25.2)

        o_ord2 = self.ordinal2
        o_matching = self.matching

        self.make_ord2(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.ordinal1[0].align_data(self.ordinal2[0])
        self.ordinal2[1].submobjects = self.ordinal2[1].submobjects[:5]
        self.matching = make_ordinal_matching(self.ordinal1, self.ordinal2)
        self.play(ReplacementTransform(o_matching, self.matching),
                  ReplacementTransform(o_ord2, self.ordinal2))
        ineq = TexMobject('>').move_to(type_comparison[1])
        self.play(Write(ineq))

        self.wait_to(34)

        o_matching = self.matching
        o_ord1 = self.ordinal1
        o_ord2 = self.ordinal2
        self.make_ord1(OrdinalOmega(x0 = -4.5, x1 = 5, height = 0.8))
        self.make_ord2(OrdinalOmega(x0 = -4.5, x1 = 5, height = 0.8))
        self.ordinal1.shift(1.8*UP)
        self.ordinal2.shift(2*UP)

        self.make_matching()
        match_adding = o_matching[0][-1].copy()
        match_adding.set_stroke(width = 0)
        o_matching[0].submobjects += [match_adding.copy()
                                      for _ in range(len(self.matching) - len(o_matching[0]))]

        line_dest = Line(SPACE_WIDTH*RIGHT, SPACE_WIDTH*LEFT)
        line = line_dest.copy()
        line.shift(SPACE_HEIGHT*DOWN)

        ordinals_title_dest = ordinal_numbers_title.copy()
        ordinals_title_dest.next_to(line_dest, UP)
        ordinals_title_dest.shift(LEFT)

        type_comparison_dest = type_comparison.copy()
        type_comparison.submobjects[1] = ineq
        type_comparison_dest.next_to(ordinals_title_dest, buff = 0.5)

        title_dest = title.copy()
        title_dest.shift(UP)

        desc1_dest = desc1.copy().next_to(self.ordinal1, LEFT, buff = 0.5)
        desc2_dest = desc2.copy().next_to(self.ordinal2, LEFT, buff = 0.5)

        ord1_extra = o_ord1[1].copy().next_to(self.ordinal1, buff = 2.5)
        ord2_extra = o_ord2[1].copy().next_to(self.ordinal2, buff = 2.5)
        matching_extra = o_matching[1].copy().next_to(self.matching, buff = 2.5)

        bottom_screen = VGroup()

        apples = LimitOrdinal(one_apple_ord, x0 = -4.5, x1 = 5)
        pears = LimitOrdinal(one_pear_ord, x0 = -4.5, x1 = 5)
        apples.shift(2*DOWN)
        pears.shift(3*DOWN)
        apples_desc = TexMobject('A').set_color(RED)
        pears_desc = TexMobject('B').set_color(YELLOW)
        apples_desc.next_to(apples, LEFT, buff = 0.5)
        pears_desc.next_to(pears, LEFT, buff = 0.5)

        bottom_screen.add(*list(reversed(apples.submobjects))+list(reversed(pears.submobjects)))
        bottom_screen.add(apples_desc, pears_desc)
        cardinal_title = TextMobject("Cardinal numbers")
        cardinal_comparison = TexMobject("|A|","=","|B|")
        cardinal_comparison[0].set_color(RED)
        cardinal_comparison[2].set_color(YELLOW)
        cardinal_title.next_to(line_dest, DOWN)
        cardinal_title.shift(LEFT)
        cardinal_comparison.next_to(line_dest, DOWN)
        cardinal_comparison.shift(RIGHT*(type_comparison_dest.get_center() -
                                         cardinal_comparison.get_center()))
        bottom_screen.add(cardinal_title, cardinal_comparison)
        
        bottom_screen_dest = bottom_screen.copy()
        bottom_screen.shift(SPACE_HEIGHT*DOWN)

        self.play(ReplacementTransform(o_ord1, VGroup(self.ordinal1, ord1_extra)),
                  ReplacementTransform(o_ord2, VGroup(self.ordinal2, ord2_extra)),
                  ReplacementTransform(o_matching, VGroup(self.matching, matching_extra)),
                  Transform(ordinal_numbers_title, ordinals_title_dest),
                  Transform(type_comparison, type_comparison_dest),
                  Transform(desc1, desc1_dest),
                  Transform(desc2, desc2_dest),
                  Transform(title, title_dest),
                  Transform(line, line_dest),
                  Transform(bottom_screen, bottom_screen_dest),
        )
        self.wait_to(46)

        fruit_match = make_ordinal_matching(apples, pears)
        self.play(ShowCreation(fruit_match))

        self.wait_to(53.5)
        apples_dest = LimitSubOrdinal(apples[:-1]).copy()
        apple = apples[0]
        apple_dest = apple.copy()
        apple_dest.next_to(apples, coor_mask = RIGHT)
        apples = LimitSubOrdinal(apples[1:])
        for app_ord, app_ord_ori in zip(apples_dest, apples):
            app_ord[0].set_color(app_ord_ori[0].color)

        fruit_match_dest = make_ordinal_matching(apples_dest, LimitSubOrdinal(pears[1:]))
        fruit_match_dest.add_to_back(make_ordinal_matching(apple_dest, pears[0]))
        apples.submobjects.reverse()
        apples_dest.submobjects.reverse()

        self.play(Transform(apples, apples_dest),
                  Transform(apple, apple_dest, path_arc = -np.pi/5),
                  Transform(fruit_match, fruit_match_dest),
        )
        self.wait_to(60 + 7.4)
        self.play(
            ordinal_numbers_title.set_fill, None, 1,
            type_comparison.set_fill, None, 1,
            cardinal_title.set_fill, None, 0.3,
            cardinal_comparison.set_fill, None, 0.3,
        )
        self.wait_to(60 + 13)

        #self.revert_to_original_skipping_status()
        for f in [lambda x: x + np.sin(np.pi*3*x)/(np.pi*3.5),
                  lambda x: x - np.sin(np.pi*5*x)/(np.pi*5.5),
                  lambda x: x]:
            ord1_dest = self.ordinal1.copy()
            for bar in ord1_dest:
                x = bar.x0
                x -= self.ordinal1.x1
                x /= (self.ordinal1.x0 - self.ordinal1.x1)
                x = f(x)
                x *= (self.ordinal1.x0 - self.ordinal1.x1)
                x += self.ordinal1.x1
                bar.shift(RIGHT*(x - bar.get_center()[0]))
            matching_dest = make_ordinal_matching(ord1_dest, self.ordinal2)
            self.play(Transform(self.ordinal1, ord1_dest),
                      Transform(self.matching, matching_dest))
        self.wait_to(60 + 20)

    def make_matching(self):
        self.matching = make_ordinal_matching(self.ordinal1, self.ordinal2)
    def make_ord1(self, ordinal):
        self.ordinal1 = make_half_ordinal(ordinal, trunc_down = True)
        self.ordinal1.set_color(RED)
        self.ordinal1.shift(UP)
    def make_ord2(self, ordinal):
        self.ordinal2 = make_half_ordinal(ordinal, trunc_down = False)
        self.ordinal2.set_color(YELLOW)
        #self.ordinal2.shift(UP)

class FiniteOrInfinite(Scene):

    def construct(self):

        #self.force_skipping()
        bars = VGroup(*[
            Line(1.4*UP, ORIGIN, color = color)
            for color in color_gradient((BLUE, YELLOW), 5)
        ])
        bars.arrange_submobjects(buff = 0.5)
        self.add(bars)

        title_fin = TextMobject("Finite well-ordered sets").to_edge(UP)
        self.play(Write(title_fin), run_time = 2)

        bars_ori = bars
        bars = bars_ori.copy()
        for bar in bars:
            bar.move_to(2*LEFT + 4*RIGHT*random.random())
        bars_sorted = VGroup(*sorted(bars, key = lambda bar: bar.get_center()[0]))
        for i, bar in enumerate(bars_sorted):
            bar.shift(0.5*RIGHT*i)
        bars.center()

        self.wait_to(2.3)
        self.play(ReplacementTransform(bars_ori, bars, path_arc = np.pi*2/3))
        self.wait_to(5)

        bars = bars_sorted
        bars_dest = bars.copy()
        bars_dest.arrange_submobjects(buff = 0.5)
        
        self.play(Transform(bars, bars_dest))
        self.wait_to(10)

        desc = TexMobject("\\operatorname{type}(X)","=","|X|", "= 5").to_edge(DOWN)
        desc[0].submobject_gradient_highlight(BLUE, YELLOW)
        desc[2].submobject_gradient_highlight(BLUE, YELLOW)
        self.play(Write(VGroup(*desc[:-1])))
        self.wait_to(15)
        self.play(Write(desc[-1]))
        self.wait_to(17.5)

        title_inf = TextMobject("Infinite well-ordered sets").to_edge(UP)
        self.play(ReplacementTransform(VMobject(VMobject(*title_fin[:2]), VMobject(*title_fin[2:])),
                                       VMobject(VMobject(*title_inf[:3]), VMobject(*title_inf[3:]))),
                  FadeOut(bars), FadeOut(desc))


        main_h = 1.2
        main_shift = 0.8
        ordinal1 = make_half_ordinal(OrdinalOmega(height = main_h))
        ordinal1.shift(main_shift*UP)
        ordinal1.set_color(YELLOW)
        ordinal2 = ordinal1.copy()
        ordinal2.set_color(BLUE)
        ordinal2.stretch(-1, 1)
        self.play(FadeIn(ordinal1), FadeIn(ordinal2))

        rearr_shift = 0.7*UP
        ord2_phase = [None]*4

        ord2_phase[3] = make_half_ordinal(OrdinalFiniteProd(OrdinalOmega, 2, height = main_h),
                                          trunc_down = False)
        ord2_phase[3].set_color(ordinal2.color)
        ord2_phase[3].shift(main_shift*DOWN)

        ord2_phase[0] = VGroup(LimitSubOrdinal(ordinal2[::2]), LimitSubOrdinal(ordinal2[1::2]))
        ord2_phase[1] = ord2_phase[0].copy()
        ord2_phase[1][0].shift(rearr_shift)
        ord2_phase[1][1].shift(-rearr_shift)
        ord2_phase[2] = ord2_phase[3].copy()
        ord2_phase[2][0].shift(rearr_shift)
        ord2_phase[2][1].shift(-rearr_shift)

        self.wait_to(19.5)
        for phaseA, phaseB, run_time in zip(ord2_phase[:-1], ord2_phase[1:], [0.7, 1, 0.7]):
            self.play(ReplacementTransform(phaseA, phaseB), run_time = run_time)
        ordinal2 = ord2_phase[-1]

        self.wait_to(25)

        desc_A = TexMobject('A').next_to(ordinal1, LEFT, buff = 0.5).set_color(ordinal1.color)
        desc_B = TexMobject('B').next_to(ordinal2, LEFT, buff = 0.5).set_color(ordinal2.color)
        self.play(FadeIn(desc_A), FadeIn(desc_B))

        desc_card = TexMobject("|A|","=","|B|")
        desc_ord = TexMobject("\\operatorname{type}(A)","<","\\operatorname{type}(B)")
        for desc in [desc_card, desc_ord]:
            desc[0].set_color(ordinal1.color)
            desc[2].set_color(ordinal2.color)

        VGroup(desc_card, desc_ord).arrange_submobjects(buff = 3).to_edge(DOWN)

        self.play(Write(desc_card), run_time = 1.5)
        self.wait_to(27.5)

        self.play(Write(desc_ord), run_time = 2.5)
        self.wait_to(30)

        desc_ord_ori = desc_ord.copy()
        self.play(desc_ord.highlight, DARK_GREY)
        ord1_al = ordinal1.copy()
        ord2_al = ordinal2[1].copy()
        ord1_al.align_data(ord2_al)
        self.try_matching(ord1_al, ord2_al)

        ord1_al = Ordinal(LimitSubOrdinal(ordinal1[7:]).copy(), Ordinal(*ordinal1[:7]))
        ord2_al = ordinal2.copy()
        ord1_al[0].align_data(ord2_al[0])
        self.try_matching(ord1_al, ord2_al)

        ord1_al = Ordinal(LimitSubOrdinal(ordinal1[::2]).copy(),
                          LimitSubOrdinal(ordinal1[1::2]).copy())
        ord2_al = ordinal2.copy()
        ord1_al.align_data(ord2_al)
        matching = self.try_matching(ord1_al, ord2_al, fadeout = False)

        icon_confirmed = IconYes().next_to(desc_card)
        self.play(ShowCreation(icon_confirmed))
        desc_card.add(icon_confirmed)
        #self.wait_to(36.5)

        desc_cadr_ori = desc_card.copy()
        self.play(desc_card.highlight, DARK_GREY,
                  Transform(desc_ord, desc_ord_ori),
                  FadeOut(matching),
        )

        ord1_al = ordinal1.copy()
        ord2_al = ordinal2[0].copy()
        ord1_al.align_data(ord2_al)
        matching = make_ordinal_matching(ord1_al, ord2_al)
        for match_line in matching[:3]:
            self.play(ShowCreation(match_line), run_time = 0.5)
        self.play(ShowCreation(VGroup(*matching[3:])))
        self.dither()
        
        icon_confirmed = IconYes().next_to(desc_ord)
        self.play(ShowCreation(icon_confirmed))
        self.wait_to(47)

    def try_matching(self, ordinal1, ordinal2, fadeout = True):
        matching = make_ordinal_matching(ordinal1, ordinal2)
        self.play(
            ShowCreation(matching),
            submobject_mode = "all_at_once",
            run_time = 0.8
        )
        if not fadeout: return matching
        self.dither(0.7)
        self.play(FadeOut(matching), run_time = 0.5)


class ApplicationDifference(Scene):
    def construct(self):

        self.tool_color = YELLOW
        self.obj_color = BLUE
        
        title = TextMobject("Different uses")
        title.to_edge(UP)
        line = Line(title.get_edge_center(DOWN) + 0.5*DOWN,
                    SPACE_HEIGHT*DOWN)

        self.play(FadeIn(line), FadeIn(title))
        card_title = TextMobject("Cardinals","measure","sets")
        ord_title = TextMobject("Ordinals\\\\","extract the essence\\\ of","well-ordered sets")

        for subtitle, part in (card_title, LEFT), (ord_title, RIGHT):
            subtitle[0].set_color(self.tool_color)
            subtitle[2].set_color(self.obj_color)
            target = line.get_start() + part*SPACE_WIDTH/2
            subtitle.shift(target - subtitle.get_edge_center(UP))

        equations = self.make_card_equations(card_title)

        #self.add(card_title, ord_title, equations)
        self.wait_to(6)
        self.play(FadeIn(card_title))
        self.wait_to(8.2)
        self.play(FadeIn(equations, submobject_mode = "lagged_start"), run_time = 3)
        self.wait_to(15.5)

        ordinal_phases = self.make_ord_phases(ord_title)
        self.play(Write(ord_title))
        self.dither()
        ordinal = ordinal_phases[0]
        for subord in ordinal:
            self.play(FadeIn(subord, submobject_mode = "lagged_start"))
        self.wait_to(33)
        self.play(ordinal.set_color, self.tool_color)
        self.wait_to(43)
        for ord_dest in ordinal_phases[1:]:
            self.play(Transform(ordinal, ord_dest))
        self.wait_to(51.5)

    def make_card_equations(self, title):

        objects = ["\omega", "\\mathbb Z", "\\mathbb Q", "\\mathbb R", "\\mathcal P(\omega)"]
        sizes = ["\\aleph_0"]*3 + ["\\mathfrak c"]*2
        equations = VGroup(*[
            TexMobject("|"+obj+"|", "=", size)
            for obj, size in zip(objects, sizes)
        ])
        for equation in equations:
            equation.shift(-equation[1].get_center())
            equation[0].set_color(self.obj_color)
            equation[2].set_color(self.tool_color)
        equations.arrange_submobjects(DOWN, coor_mask = UP)

        target = title.get_edge_center(DOWN)
        target[1] = (target[1] - SPACE_HEIGHT)/2
        equations.move_to(target)

        return equations

    def make_ord_phases(self, title):

        q1 = (0.9, 0.95, 0.95)
        q2 = (0.8, 0.9, 0.9)
        q3 = (0.7, 0.8, 0.8)
        settings = ((0.5, q2, q2), (0.6, q1, q3), (0.4, q2, q1), (0.5, q2, q2))

        ordinal_phases = VGroup(*[
            OrdinalSum(lambda **kwargs: OrdinalOmega(q = qA, **kwargs),
                       split,
                       lambda **kwargs: OrdinalOmega(q = qB, **kwargs),
                       x0 = 0, x1 = 5,
            )
            for split, qA, qB in settings
        ])
        ordinal_phases.set_color(self.tool_color)
        ordinal_phases[0].set_color(self.obj_color)

        target = title.get_edge_center(DOWN)
        target[1] = (target[1] - SPACE_HEIGHT)/2
        ordinal_phases.move_to(target)

        return ordinal_phases

def make_omega_desc(i):
    tex = "\\omega"
    if i > 0: tex += "+{}".format(i)
    return TexMobject(tex)

class OrdinalByRecursion(Scene):

    def construct(self):

        #self.force_skipping()

        underlying_bg = OrdinalOmega().shift(UP)
        underlying_fg = underlying_bg.copy()
        underlying_bg.set_color(DARK_GREY)
        underlying_fg[0].set_color(GREEN)
        underlying2 = underlying_bg.copy()
        underlying2.next_to(underlying_bg)

        self.add(underlying_bg, underlying2)

        zero_title = TextMobject("Zero case:","0").to_corner(UP+LEFT)
        zero_title.set_color(GREEN)
        self.wait_to(6.7)
        self.play(Write(zero_title))

        descriptions = underlying_fg.add_descriptions(lambda i: TexMobject(str(i)),
                                                      direction = UP, size = 0.5)

        # step 0
        
        descriptions[0].set_color(GREEN)
        self.play(ShowCreation(underlying_fg[0]),
                  ReplacementTransform(zero_title[1].copy(), descriptions[0]))

        ord_pic = VMobject()
        brace = self.prepare_brace(ord_pic, underlying_fg[0])
        self.play(GrowFromCenter(brace))
        self.wait_to(20.4)

        successor_title = TextMobject("Successor step:","+1").to_corner(UP+LEFT)
        self.change_titles(zero_title, successor_title)

        # 1 -> 4

        self.wait_to(29.1)
        for bar, desc in zip(underlying_fg, descriptions)[1:5]:
            ord_pic_next = ord_pic.copy()
            ord_pic_next.set_color(BLUE)
            ord_pic_next.add(Line(ORIGIN, 1.5*DOWN).next_to(ord_pic))
            brace_next = self.prepare_brace(ord_pic_next, bar)
            self.play(ReplacementTransform(ord_pic, VMobject(*ord_pic_next[:-1])),
                      ReplacementTransform(brace, brace_next), run_time = 0.5)
            brace = brace_next
            ord_pic = ord_pic_next
            self.play(ShowCreation(ord_pic[-1]),
                      ShowCreation(bar),
                      Write(desc))

        # 5 -> ... <w

        self.play(ShowCreation(VGroup(*descriptions[5:])),
                  ShowCreation(VGroup(*underlying_fg[5:])))
        self.wait_to(36.4)

        # supremum
        
        self.remove(underlying_bg)
        limit_title = TextMobject("Limit step: ordinal union","of all preceding values")
        limit_title.to_corner(UP+LEFT)
        limit_title[0].set_color(YELLOW)
        self.change_titles(successor_title, limit_title,
                           additional_animations = [
                               FadeOut(brace), FadeOut(ord_pic),
                           ])

        self.wait_to(40.5)

        self.play_finite_supremum()

        shift = LEFT*underlying2[0].get_center()
        self.play(VGroup(underlying_fg,
                         underlying2,
                         descriptions).shift, shift)

        # preparation for the next round

        underlying3 = underlying2.copy().next_to(underlying2)
        bar = underlying2[0].copy()
        bar.set_color(YELLOW)
        descriptions2 = underlying2.add_descriptions(make_omega_desc,
                                                     direction = UP, size = 0.9)
        descriptions2[0].set_color(YELLOW)

        self.wait_to(60 + 13)
        ord_pic, brace = self.play_infinite_supremum(bar, waits = (60+16.5, 60+18))
        self.remove(bar)
        underlying2[0].set_color(YELLOW)
        #self.add(descriptions2)
        self.wait_to(60 + 19.7)
        self.play(Write(descriptions2[0]))

        # w -> w + 5
        self.dither()

        shown_descs2 = VGroup(descriptions2[0])
        hidden_descs2 = VGroup(*descriptions2[1:])
        moving = VGroup(underlying_fg,
                        underlying2,
                        descriptions,
                        shown_descs2,
                        underlying3)
        self.wait_to(60 + 30.3)
        for bar, desc in zip(underlying2, descriptions2)[1:5]:
            shift = LEFT*bar.get_center()
            ord_pic_next = ord_pic.copy()
            ord_pic_next[-1].set_color(BLUE)
            ord_pic_next.add(Line(ORIGIN, 1.5*DOWN).next_to(ord_pic))
            bar_next = bar.copy()
            bar_next.set_color(WHITE)
            bar_next.shift(shift)
            brace_next = self.prepare_brace(ord_pic_next, bar_next)
            self.play(ReplacementTransform(ord_pic, VMobject(*ord_pic_next[:-1])),
                      ReplacementTransform(brace, brace_next),
                      moving.shift, shift, run_time = 0.5)
            hidden_descs2.shift(shift)

            ord_pic = ord_pic_next
            brace = brace_next

            self.play(ShowCreation(bar_next),
                      ShowCreation(ord_pic[-1]),
                      Write(desc), run_time = 0.5)
            self.remove(bar_next)
            bar.highlight(WHITE)
            shown_descs2.add(desc)
            hidden_descs2.remove(desc)
            #self.dither()

        # w+5 -> ... <w+w

        self.wait_to(60 + 34.3)

        bar = underlying3[0]
        shift = LEFT*bar.get_center()

        next_descs = hidden_descs2.copy()
        next_descs.shift(shift)
        hidden_descs2.set_fill(opacity = 0)

        underlying2_dest = underlying2.copy()
        underlying2_dest.shift(shift)
        VGroup(*underlying2_dest[1:]).set_color(WHITE)

        self.play(moving.shift, shift,
                  Transform(hidden_descs2, next_descs),
                  Transform(underlying2, underlying2_dest),
                  FadeOut(ord_pic))

        moving.add(hidden_descs2)
        self.dither()

        #self.remove(descriptions, underlying_fg)
        #self.revert_to_original_skipping_status()
        bar = underlying3[0].copy()
        bar.set_color(YELLOW)
        ord_pic = self.play_infinite_supremum2(bar, brace)
        self.wait_to(60 + 40)
        ww_desc = TexMobject("\\omega+\\omega")
        ww_desc.set_color(YELLOW)
        ww_desc.next_to(bar, UP)
        self.play(Write(ww_desc))
        moving.add(ww_desc, bar)
        self.wait_to(60 + 50.5)

        moving.remove(descriptions, underlying_fg)
        moving2 = VGroup(descriptions, underlying_fg)
        shift2 = 1 - SPACE_WIDTH - underlying_fg[0].get_center()[0]
        shift = shift2 - DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        #print(shift)
        self.play(moving.shift, RIGHT*shift,
                  moving2.shift, RIGHT*shift2,
                  FadeOut(brace), FadeOut(ord_pic), FadeOut(limit_title))
        

    def prepare_brace(self, mobj, bar):

        left = mobj.get_corner(UP+LEFT) + 0.1*LEFT
        right = mobj.get_corner(UP+RIGHT) + 0.1*RIGHT
        if right[0] - left[0] < 0.5:
            mid = (left+right)/2
            left = mid+0.25*LEFT
            right = mid+0.25*RIGHT
        strut = Line(left, right)
        brace = Brace(strut, UP).set_color(BLUE)
        target = bar.get_center()+DOWN
        Group(brace,mobj).shift(target - brace.get_tip())

        return brace

    def change_titles(self, tit_old, tit_new, additional_animations = (), baseline = 0.7):
        tit_old_dest = tit_old.copy()
        tit_new_dest = tit_new.copy()
        tit_old_dest.shift(UP * baseline)
        tit_new.shift(DOWN * baseline)
        tit_old_dest.set_fill(opacity = 0)
        tit_new.set_fill(opacity = 0)
        self.play(Transform(tit_old, tit_old_dest),
                  Transform(tit_new, tit_new_dest),
                  *additional_animations)
        self.remove(tit_old)

    def play_finite_supremum(self):
        ord1 = VGroup(*[Line(ORIGIN, DOWN) for _ in range(7)])
        ord1.arrange_submobjects(RIGHT, buff = 0.4)
        ord1.set_color(BLUE)
        ord1.shift(DOWN)

        ord2 = VGroup(*[Line(ORIGIN, DOWN) for _ in range(4)])
        ord2.arrange_submobjects(RIGHT, buff = 0.4)
        ord2.set_color(WHITE)

        ord2.next_to(ord1, DOWN, buff = 0.2)
        self.play(ShowCreation(VGroup(ord1, ord2)))
        self.wait_to(47)
        shift = RIGHT*(ord2[0].get_center() - ord1[0].get_center())
        self.play(ord1.shift, shift/2,
                  ord2.shift, -shift/2,
                  run_time = 0.5)

        self.wait_to(55.5)
        shift = ord2[0].get_center() - ord1[0].get_center()
        self.play(ord2.shift, -shift/2,
                  ord1.shift, shift/2,
                  run_time = 0.7)
        self.remove(ord2)
        self.wait_to(60 + 9)
        self.play(FadeOut(ord1))

    def play_infinite_supremum(self, underlying_bar = None, ord_num = 15, waits = None):

        supremum = OrdinalOmega().set_color(BLUE)
        if underlying_bar is not None:
            brace = self.prepare_brace(supremum, underlying_bar)
            self.play(GrowFromCenter(brace))
        else:
            brace = None

        ordinals = VGroup(*[
            VGroup(*[
                Line(ORIGIN, DOWN*min(0.4, 0.8/(1.3**i)))
                for _ in range(i)
            ])
            for i in range(1, ord_num+1)
        ])

        ordinals.set_color(BLUE)
        for ordinal in ordinals:
            ordinal.arrange_submobjects(RIGHT, buff = 0.4)
        for ord1, ord2, i in zip(ordinals[:-1], ordinals[1:], range(ord_num-1)):
            ord2.next_to(ord1, DOWN, buff = min(0.2, 0.4/(1.3**i)))

        ordinals.to_edge(DOWN, buff = 0)

        self.play(ShowCreation(ordinals))
        if waits is not None: self.wait_to(waits[0])

        ordinals_dest = ordinals.copy()
        for ordinal in ordinals_dest:
            for i, bar in enumerate(ordinal):
                bar.move_to(supremum[i], coor_mask = RIGHT)

        self.play(Transform(ordinals, ordinals_dest))
        if waits is not None: self.wait_to(waits[1])
        last_ordinal = supremum.copy()
        last_ordinal.stretch(0,1)
        last_ordinal.shift(DOWN*SPACE_HEIGHT)
        ordinals.add(last_ordinal)
        ordinals_dest = VGroup(*[
            VGroup(*supremum[:len(ordinal)]).copy()
            for ordinal in ordinals
        ])
        animations = [Transform(ordinals, ordinals_dest)]
        if underlying_bar is not None: animations.append(ShowCreation(underlying_bar))
        self.play(*animations)

        self.remove(ordinals)
        self.add(supremum)

        return supremum, brace

    def play_infinite_supremum2(self, underlying_bar, brace, ord_num = 15):

        supremum = OrdinalFiniteProd(OrdinalOmega, 2).set_color(BLUE)

        ordinals = []
        for row in range(ord_num):
            h = min(0.4, 0.8/(1.3**(row+1)))
            ordinals.append(VGroup(
                OrdinalOmega(x0 = supremum[0].x0, x1 = supremum[0].x1, height = h/2),
                VGroup(*[
                    Line(ORIGIN, UP*h).move_to(bar)
                    for bar in supremum[1][:row]
                ])
            ))
        ordinals = VGroup(*ordinals)

        ordinals.set_color(BLUE)
        for ord1, ord2, i in zip(ordinals[:-1], ordinals[1:], range(ord_num-1)):
            ord2.next_to(ord1, DOWN, buff = min(0.2, 0.4/(1.3**i)), coor_mask = UP)

        ordinals.to_edge(DOWN, buff = 0)
        supremum.next_to(brace, DOWN, coor_mask = UP)

        self.play(FadeIn(ordinals))
        self.dither()

        last_ordinal = supremum.copy()
        last_ordinal.stretch(0,1)
        last_ordinal.shift(DOWN*SPACE_HEIGHT)
        ordinals.add(last_ordinal)
        ordinals_dest = VGroup(*[
            VGroup(VGroup(*supremum[0][:len(ordinal[0])]).copy(),
                   VGroup(*supremum[1][:len(ordinal[1])]).copy())
            for ordinal in ordinals
        ])
        self.play(Transform(ordinals, ordinals_dest),
                  ShowCreation(underlying_bar))

        self.remove(ordinals)
        self.add(supremum)

        return supremum

class OrdinalRoles(Scene):
    def construct(self):
        ord1 = OrdinalOmega()
        ord1.to_edge(LEFT, buff = 1)
        ord1.shift(UP)
        desc1 = ord1.add_descriptions(lambda i: TexMobject(str(i)),
                                      direction = UP, size = 0.5)
        ord2 = ord1.copy()
        ord2.next_to(ord1, buff = 0)
        desc2 = ord2.add_descriptions(make_omega_desc,
                                      direction = UP, size = 0.9)
        ord1[0].set_color(GREEN)
        desc1[0].set_color(GREEN)
        ord2[0].set_color(YELLOW)
        desc2[0].set_color(YELLOW)
        self.add(ord1, ord2, desc1, desc2)

        ordinals_title = TextMobject("ordinals")
        order_types_title = TextMobject("order types of well ordered sets")
        indices_title = TextMobject("indices of a","well ordering")

        roles = VGroup(order_types_title, indices_title)
        roles.arrange_submobjects(DOWN, aligned_edge=LEFT)
        roles.next_to(ordinals_title, buff = 1.5)
        connections = VGroup(*[
            Line(ordinals_title.get_edge_center(RIGHT)+0.2*RIGHT,
                 role.get_edge_center(LEFT)+0.2*LEFT)
            for role in roles
        ])
        title = VGroup(ordinals_title, connections, roles)
        title.center()
        title.to_edge(DOWN)

        #self.force_skipping()

        self.wait_to(10)
        self.play(FadeIn(ordinals_title))

        self.wait_to(17.5)
        for con, role in zip(connections, roles):
            self.play(ShowCreation(con), Write(role))
            self.wait_to(20.8, assert_positive = False)

        pointer = TrianglePointer(color = BLUE).next_to(ord2[3], UP, buff = 0.3)
        pointer_desc = desc2[3]
        pointer_desc_target = TexMobject("\\omega+3")
        pointer_desc_target.set_color(BLUE)
        pointer_desc_target.next_to(pointer, UP)
        desc2.remove(desc2[3])
        self.wait_to(26.5)
        self.play(
            FadeOut(desc1), FadeOut(desc2),
            Transform(pointer_desc, pointer_desc_target),
            FadeIn(pointer)
        )
        self.dither()
        steps1 = ord1.to_steps().shift(UP)
        steps1.remove()
        steps1_ori = LimitSubOrdinal(ord1[1:])
        ord1_bg = ord1.copy()
        ord1_bg.set_color(DARK_GREY)
        self.add(ord1_bg, ord1, ord2)
        self.wait_to(31.2)
        self.play(ReplacementTransform(
            steps1_ori, steps1,
            submobject_mode = "one_at_a_time",
            run_time = 1.8*DEFAULT_ANIMATION_RUN_TIME,
            rate_func = rush_into,
        ))
        self.wait_to(33)

        steps2 = seq_to_jumps(ord2[:4])
        steps2_ori = Ordinal(*ord2[1:4])
        ord2_bg = ord2.copy()
        ord2_bg.set_color(DARK_GREY)
        self.add(ord2_bg, ord2)
        self.play(ReplacementTransform(
            steps2_ori, steps2,
            submobject_mode = "one_at_a_time"
        ))
        successor = ord2_bg[3].copy()
        successor.set_color(BLUE)
        self.play(ShowCreation(successor),
                  *map(FadeOut, ord2[4:]))
        self.wait_to(44.5)

        steps1_dest = ord1_bg.copy().set_color(WHITE)
        steps2_dest = VGroup(*ord2_bg[:3]).copy().set_color(WHITE)
        self.play(
            Transform(steps1, steps1_dest),
            Transform(steps2, steps2_dest),
        )
        self.brace = Brace(VGroup(steps1, steps2), DOWN)
        self.brace_desc = pointer_desc.copy()
        self.brace_desc.set_color(WHITE)
        self.brace.put_at_tip(self.brace_desc)
        self.wait_to(50.5)
        self.play(GrowFromCenter(self.brace),
                  FadeIn(self.brace_desc))
        self.remove(ord1, ord2, steps1, steps2)
        ord1 = ord1_bg
        ord2 = ord2_bg
        ord1.highlight(WHITE)
        VGroup(*ord2[:3]).highlight(WHITE)
        self.all_bars = VGroup(ord1, ord2)
        self.wait_to(60 + 2.7)
        self.play(*map(FadeOut, [successor, pointer, pointer_desc]))

        self.move_brace(ord1[:4], TextMobject("four"))
        self.wait_to(60 + 12)

        last_bar = ord1[3].copy().set_color(ORANGE)
        lb_pointer = TrianglePointer(color = ORANGE).next_to(last_bar, UP)
        lb_desc = TextMobject("fourth").next_to(lb_pointer, UP).set_color(ORANGE)
        self.play(
            ShowCreation(last_bar),
            FadeIn(lb_pointer),
            FadeIn(lb_desc)
        )
        self.add_foreground_mobjects(last_bar)
        self.wait_to(60 + 17.3)
        self.move_brace(ord1, TexMobject("\\omega"))
        self.wait_to(60 + 21.7)
        self.move_brace(ord1[:4], TexMobject("4"))
        successor = ord1[4].copy().highlight(BLUE)
        pointer = TrianglePointer(color = BLUE).next_to(successor, UP)
        pointer_desc = TexMobject("4").next_to(pointer, UP).set_color(BLUE)

        self.wait_to(60 + 23.7)
        self.play(
            Uncreate(last_bar),
            ShowCreation(successor),
            ReplacementTransform(lb_desc, pointer_desc),
            ReplacementTransform(lb_pointer, pointer),
        )
        self.wait_to(60 + 34.5)

        self.play(order_types_title.highlight, YELLOW)
        self.wait_to(60 + 37.1)
        self.play(
            order_types_title.highlight, WHITE,
            indices_title.highlight, YELLOW,
        )

        self.wait_to(2*60 + 1.5)

        indices_title2 = TextMobject("indices of a","universal","well ordering")
        indices_title2.shift(indices_title[0].get_center() - indices_title2[0].get_center())
        indices_title2.set_color(YELLOW)
        indices_title2_src = VGroup(
            indices_title[0],
            indices_title2[1].copy(),
            indices_title[1],
        )
        indices_title2_src[1].next_to(indices_title2[0])
        indices_title2_src[1].scale(0, about_point = indices_title2_src[1].get_edge_center(LEFT))
        self.play(ReplacementTransform(indices_title2_src, indices_title2))
        self.wait_to(2*60 + 6)

        arrows = VGroup(*[
            Arrow(ORIGIN, 2*UP + i*1.0*RIGHT)
            for i in range(3)
        ])
        arrows.shift(ordinals_title.get_edge_center(UP) + 0.2*UP - arrows[0].get_start())
        self.play(
            ord1.highlight, WHITE,
            ord2.highlight, WHITE,
            *map(FadeOut, [
                self.brace,
                self.brace_desc,
                pointer,
                pointer_desc,
                successor
            ]) + map(ShowCreation, arrows)
        )
        #self.revert_to_original_skipping_status()
        self.wait_to(2*60 + 11.5)
        ord_pow = make_ordinal_power(2, q=(0.8, 0.9, 0.9), x1 = 7)
        ord_pow.shift(ord1[0].get_center() - ord_pow[0][0].get_center())
        ord_pow_extra = VGroup(*ord_pow[1:3]).copy().next_to(ord_pow, buff = 0)
        ord_pow_all = VGroup(ord_pow, ord_pow_extra)
        ord_pow_all_src = ord_pow_all.copy()
        ord_pow_all_src.next_to(ord2, buff = 0)
        ord_pow_src = ord_pow_all_src[0]
        ord_pow_src.add_to_back(ord1, ord2)
        
        self.play(ReplacementTransform(
            ord_pow_all_src, ord_pow_all,
            prepare_families = True,
        ))
        self.wait_to(2*60 + 29.5)

    def move_brace(self, bars, desc):
        bars = VGroup(*bars)
        brace = Brace(bars, DOWN)
        brace.put_at_tip(desc)
        self.play(
            ReplacementTransform(self.brace, brace),
            ReplacementTransform(self.brace_desc, desc),
        )
        self.brace = brace
        self.brace_desc = desc
        self.all_bars.highlight(DARK_GREY)
        bars.highlight(WHITE)

class SupremumRecap(OrdinalByRecursion):
    def construct(self):
        title = TextMobject("Ordinal Union", "$=$","Supremum")
        title.to_edge(UP)
        self.add(title[0])
        
        supremum, _ = self.play_infinite_supremum(waits = (5.5, 6.9))
        self.wait_to(11.3)
        self.play(Write(VGroup(title[1:])))
        self.wait_to(17.5)
        self.play(
            FadeOut(supremum),
            VGroup(title[:2]).highlight, DARK_GREY,
        )

class SupremumReal(Scene):
    def construct(self):
        #self.force_skipping()
        title = TextMobject("Ordinal Union", "$=$","Supremum")
        VGroup(title[:2]).highlight(DARK_GREY)
        title.to_edge(UP)
        self.add(title)

        numberline = NumberLine(color = DARK_BLUE)
        self.play(ShowCreation(numberline))
        self.wait_to(2)

        edges = [-2.5, 2.5]
        points = [
            numberline.number_to_point(x)
            for x in edges
        ]
        dots = VGroup(*[
            Dot(p)
            for p in points
        ])
        texts = [str(x) for x in edges]
        descs = VGroup(*[
            TexMobject(t).next_to(d, UP)
            for t, d in zip(texts, dots)
        ])
        segment = VGroup(dots[0], Line(*points), dots[1])
        main_desc = TexMobject("[" + ",".join(texts) + "]")
        main_desc.next_to(segment, UP, buff = 1)
        main_desc_closed = main_desc.copy()
        self.play(ShowCreation(segment),
                  Write(descs),
                  Write(main_desc))
        self.wait_to(6)

        maximum_desc = TextMobject("maximum").move_to(points[1]+2*DOWN)
        arrow = Arrow(maximum_desc.get_edge_center(UP), points[1])
        arrow_backup = arrow.copy()

        self.play(FadeIn(maximum_desc),
                  ShowCreation(arrow))
        self.wait_to(12.5)
        self.play(Uncreate(arrow))

        main_desc_open = TexMobject("(" + ",".join(texts) + ")")
        main_desc_open.shift(main_desc[1].get_center() - main_desc_open[1].get_center())
        dots_ori = dots.copy()
        dots_erased = dots.copy()
        dots_erased.shift(0.5*DOWN)
        dots_erased.set_fill(opacity = 0)

        self.play(Transform(dots, dots_erased))
        self.play(Transform(main_desc, main_desc_open))

        segment.remove(*dots)
        self.wait_to(16.3)

        no = TextMobject("no m")
        no.shift(maximum_desc[0].get_center() - no[-1].get_center())
        no.remove(no[-1])
        maximum_desc.add_to_back(no)
        self.play(Write(no))
        
        self.wait_to(18.7)
        dot_out = Dot(points[1], color = DARK_BLUE)
        self.play(ShowCreation(dot_out), FocusOn(points[1]))

        #self.revert_to_original_skipping_status()
        self.wait_to(27)
        supremum_desc = TextMobject("supremum")
        supremum_desc.shift(maximum_desc[-1].get_center() - supremum_desc[-1].get_center())
        self.play(ReplacementTransform(maximum_desc, supremum_desc))
        arrow = arrow_backup.copy()
        self.play(ShowCreation(arrow))
        self.wait_to(33)
        self.play(*map(FadeOut, [arrow, supremum_desc]))
        self.play(Transform(dots, dots_ori),
                  Transform(main_desc, main_desc_closed))
        #self.wait_to(34.5)
        eq_maximum = TextMobject("$=$ maximum")
        eq_maximum.next_to(supremum_desc, DOWN)
        self.play(
            FadeIn(supremum_desc),
            FadeIn(eq_maximum),
            ShowCreation(arrow),
        )
        self.wait_to(37)

        self.play(*map(FadeOut, [arrow, supremum_desc, eq_maximum]))
        self.play(Transform(dots, dots_erased),
                  Transform(main_desc, main_desc_open))
        self.wait_to(40.5)
        self.play(
            FadeIn(supremum_desc),
            ShowCreation(arrow),
        )
        self.wait_to(44)

        self.play(*map(FadeOut, [
            numberline, dot_out, segment, descs, main_desc, supremum_desc, arrow
        ]))

class SupremumIndices(Scene):
    def construct(self):
        #self.force_skipping()
        title = TextMobject("Ordinal Union", "$=$","Supremum")
        VGroup(title[:2]).highlight(DARK_GREY)
        title.to_edge(UP)
        self.add(title)

        ord1 = OrdinalOmega()
        ord1.shift(LEFT + UP)
        ord1.set_color(DARK_GREY)
        ord2 = ord1.copy()
        ord2.next_to(ord1)

        self.play(
            FadeIn(VGroup(ord1, ord2)),
            title.highlight, WHITE,
        )
        set1 = VGroup(ord1[2], ord1[4]).copy().highlight(WHITE)
        self.wait_to(5)
        self.play(ShowCreation(set1))
        desc = self.show_supremum(set1[-1], with_maximum = True)

        self.wait_to(10.3)
        self.play(FadeOut(desc))

        set2 = VGroup(*ord1[6::2]).copy().highlight(WHITE)
        self.play(ShowCreation(set2))
        desc = self.show_supremum(ord2[0], with_maximum = False)
        self.wait_to(14)

    def show_supremum(self, bar, with_maximum = False):
        point = bar.get_edge_center(DOWN)
        supremum_desc = TextMobject("supremum")
        supremum_desc.move_to(point+2*DOWN)
        arrow = Arrow(supremum_desc.get_edge_center(UP), point)

        stuff = VGroup(supremum_desc, arrow)
        animations = [FadeIn(supremum_desc), ShowCreation(arrow)]
        if with_maximum:
            eq_maximum = TextMobject("$=$ maximum").next_to(supremum_desc, DOWN)
            animations.append(FadeIn(eq_maximum))
            stuff.add(eq_maximum)

        self.play(*animations)

        return stuff
