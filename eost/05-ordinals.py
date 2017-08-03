from helpers import *

from mobject.tex_mobject import *
from mobject.vectorized_mobject import *
from topics.icons import TrianglePointer
from topics.chat_bubbles import Conversation
from eost.widgets import *

from animation.transform import *
from animation.simple_animations import *

import random
import eost.deterministic

from eost.ordinal import *

from topics.common_scenes import OpeningQuote

class Chapter5OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "All that is actually completely","trivial.\\\\","What is difficult is to","realize","it.",
        ],
        "highlighted_quote_terms" : {
            "trivial.\\\\" : GREEN,
            "realize" : YELLOW,
        },
        "author" : "unnamed math professor"
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
        self.dither()
        for i in range(2):
            for bar in self.ordinal1_fg[i][:2]:
                self.play(ShowCreation(bar), run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
            self.play(ShowCreation(VGroup(*self.ordinal1_fg[i][2:])))
        self.dither()

        self.prepare_ord2(OrdinalOmega())

        self.play(FadeIn(self.ordinal2_bg))
        for bar in self.ordinal2_fg[:3]:
            self.play(ShowCreation(bar), run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
        self.play(ShowCreation(VGroup(*self.ordinal2_fg[3:])))

        self.dither()

        self.play(*map(FadeOut, [self.ordinal1_fg, self.ordinal2_fg]))
        self.dither()

        ordinal1_fg_al = self.ordinal1_fg[0].copy()
        ordinal1_fg_al.align_data(self.ordinal2_fg)

        for bar1, bar2, run_time, dither_time in\
            zip(ordinal1_fg_al[:3], self.ordinal2_fg[:3], (1,1,0.5), (1,0,0)):

            self.play(ShowCreation(bar1),
                      ShowCreation(bar2),
                      run_time = run_time*DEFAULT_ANIMATION_RUN_TIME)
            self.dither(dither_time)

        self.play(ShowCreation(VGroup(*ordinal1_fg_al[3:])),
                  ShowCreation(VGroup(*self.ordinal2_fg[3:])))
        self.dither()

        self.remove(self.ordinal2_bg)
        self.play(*map(FadeOut, [ordinal1_fg_al, self.ordinal2_fg]))

        self.prepare_ord2(OrdinalFiniteProd(OrdinalOmega, 2))

        self.play(FadeIn(self.ordinal2_bg))
        ordinal2_fg_al = self.ordinal2_fg[0].copy()
        ordinal2_fg_al.align_data(self.ordinal1_fg[0])
        ordinal2_fg_al = VGroup(ordinal2_fg_al,
                                VGroup(*self.ordinal2_fg[1][:5]))
        
        self.play_both(self.ordinal1_fg, ordinal2_fg_al)
        self.dither()

        self.remove(self.ordinal1_bg)
        self.play(*map(FadeOut, [self.ordinal1_fg, ordinal2_fg_al]))

        self.prepare_ord1(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.play(FadeIn(self.ordinal1_bg))

        self.ordinal1_fg.align_data(self.ordinal2_fg)
        self.play_both(self.ordinal1_fg, self.ordinal2_fg)
        self.dither()

        #self.revert_to_original_skipping_status()

        self.play(Uncreate(VGroup(*self.ordinal1_fg[1][3:]), clean_up_alpha = 0),
                  Uncreate(VGroup(*self.ordinal2_fg[1][3:]), clean_up_alpha = 0),
        )
        self.dither()

        pointer1 = TrianglePointer(color = RED).next_to(self.ordinal1_fg[1][3], UP)
        self.ordinal1_fg[1][3].set_color(RED)
        self.play(*map(ShowCreation, [pointer1, self.ordinal1_fg[1][3]]))

        self.dither()
        pointer2 = TrianglePointer(color = RED).scale(-1).next_to(self.ordinal2_fg[1][3], DOWN)
        self.ordinal2_fg[1][3].set_color(RED)
        self.play(*map(ShowCreation, [pointer2, self.ordinal2_fg[1][3]]))

        self.dither()

        self.remove(self.ordinal1_bg, self.ordinal2_bg)
        self.add(self.ordinal1_fg, self.ordinal2_fg)
        VGroup(*self.ordinal1_fg[1][4:]).set_color(DARK_GREY)
        VGroup(*self.ordinal2_fg[1][4:]).set_color(DARK_GREY)
        ordinal2_dest = self.ordinal1_fg.copy()
        ordinal2_dest.shift(2.8*DOWN)
        self.play(Transform(self.ordinal2_fg, ordinal2_dest),
                  pointer2.next_to, ordinal2_dest[1][3], DOWN)
        self.dither()
        ordinal_dest = self.ordinal1_fg.copy()
        VGroup(*ordinal_dest[1][1:]).highlight(WHITE)
        self.play(FadeOut(pointer1), FadeOut(pointer2),
                  Transform(self.ordinal1_fg, ordinal_dest.copy()),
                  Transform(self.ordinal2_fg, ordinal_dest))
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(ordinal_dest)

        ordinal_numbers_title = TextMobject("Ordinal numbers").to_edge(DOWN)
        self.play(Write(ordinal_numbers_title))
        self.play(FadeOut(ordinal_dest))

    def play_both_simple(self, o1, o2, one_range = 2):
        for bar1, bar2 in zip(o1[:one_range], o2[:one_range]):
            self.play(ShowCreation(bar1),
                      ShowCreation(bar2),
                      run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
        self.play(ShowCreation(VGroup(*o1[one_range:])),
                  ShowCreation(VGroup(*o2[one_range:])))

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
        self.dither()
        
        self.ordinal1.align_data(self.ordinal2)
        self.make_matching()
        self.play(ShowCreation(self.matching[0]))
        self.play(ShowCreation(self.matching[1]))
        self.dither()

        type_comparison = TexMobject("\\operatorname{type}(A)",
                                     "=",
                                     "\\operatorname{type}(B)")
        type_comparison.next_to(ordinal_numbers_title, UP, buff = 0.5)
        type_comparison[0].set_color(RED)
        type_comparison[2].set_color(YELLOW)

        self.play(Write(type_comparison))
        self.dither()

        o_ord2 = self.ordinal2
        o_matching = self.matching
        self.make_ord2(OrdinalSum(OrdinalOmega, 0.6, OrdinalOmega))
        self.ordinal1.align_data(self.ordinal2)
        self.make_matching()
        self.play(ReplacementTransform(o_matching, self.matching),
                  ReplacementTransform(o_ord2, self.ordinal2))
        self.dither()

        self.play(*map(FadeOut, [self.matching, self.ordinal2, type_comparison[1]]))

        self.make_ord2(OrdinalSum(OrdinalOmega, 0.8,
                                  lambda **kwargs: OrdinalFinite(5, **kwargs)))
        self.play(FadeIn(self.ordinal2))
        self.dither()

        self.ordinal1[0].align_data(self.ordinal2[0])
        self.make_matching()

        self.play(ShowCreation(self.matching[0]))
        self.play(ShowCreation(self.matching[1]))
        self.dither()

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

        self.dither()

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
        self.dither()

        fruit_match = make_ordinal_matching(apples, pears)
        self.play(ShowCreation(fruit_match))

        self.dither()
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
        self.dither()

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
        self.dither()

    def make_matching(self):
        self.matching = make_ordinal_matching(self.ordinal1, self.ordinal2)
    def make_ord1(self, ordinal):
        self.ordinal1 = self.make_half_ordinal(ordinal, trunc_down = True)
        self.ordinal1.set_color(RED)
        self.ordinal1.shift(UP)
    def make_ord2(self, ordinal):
        self.ordinal2 = self.make_half_ordinal(ordinal, trunc_down = False)
        self.ordinal2.set_color(YELLOW)
        #self.ordinal2.shift(UP)
    def make_half_ordinal(self, ordinal, trunc_down = True):
        for line in ordinal.family_members_with_points():
            if trunc_down: start = line.get_start()
            else: start = line.get_end()
            end = line.get_center()
            line.set_points_as_corners([start, end])
        return ordinal
