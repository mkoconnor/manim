from helpers import *

from mobject.tex_mobject import *
from mobject.vectorized_mobject import *
from topics.icons import *
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

def make_half_ordinal(ordinal, trunc_down = True):
    for line in ordinal.family_members_with_points():
        if trunc_down: start = line.get_start()
        else: start = line.get_end()
        end = line.get_center()
        line.set_points_as_corners([start, end])
    return ordinal

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
        self.play(Write(title_fin))

        bars_ori = bars
        bars = bars_ori.copy()
        for bar in bars:
            bar.move_to(2*LEFT + 4*RIGHT*random.random())
        bars_sorted = VGroup(*sorted(bars, key = lambda bar: bar.get_center()[0]))
        for i, bar in enumerate(bars_sorted):
            bar.shift(0.5*RIGHT*i)
        bars.center()

        self.dither()
        self.play(ReplacementTransform(bars_ori, bars, path_arc = np.pi*2/3))
        self.dither()

        bars = bars_sorted
        bars_dest = bars.copy()
        bars_dest.arrange_submobjects(buff = 0.5)
        
        self.play(Transform(bars, bars_dest))
        self.dither()

        desc = TexMobject("\\operatorname{type}(X)","=","|X|", "= 5").to_edge(DOWN)
        desc[0].submobject_gradient_highlight(BLUE, YELLOW)
        desc[2].submobject_gradient_highlight(BLUE, YELLOW)
        self.play(Write(VGroup(*desc[:-1])))
        self.dither()
        self.play(Write(desc[-1]))
        self.dither()

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

        for phaseA, phaseB, run_time in zip(ord2_phase[:-1], ord2_phase[1:], [0.7, 1, 0.7]):
            self.play(ReplacementTransform(phaseA, phaseB), run_time = run_time)
        ordinal2 = ord2_phase[-1]

        self.dither()

        desc_A = TexMobject('A').next_to(ordinal1, LEFT, buff = 0.5).set_color(ordinal1.color)
        desc_B = TexMobject('B').next_to(ordinal2, LEFT, buff = 0.5).set_color(ordinal2.color)
        self.play(FadeIn(desc_A), FadeIn(desc_B))

        desc_card = TexMobject("|A|","=","|B|")
        desc_ord = TexMobject("\\operatorname{type}(A)","<","\\operatorname{type}(B)")
        for desc in [desc_card, desc_ord]:
            desc[0].set_color(ordinal1.color)
            desc[2].set_color(ordinal2.color)

        VGroup(desc_card, desc_ord).arrange_submobjects(buff = 3).to_edge(DOWN)

        self.play(Write(desc_card))
        self.dither()

        self.play(Write(desc_ord))
        self.dither()

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
        self.dither(2)

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
        self.dither()

    def try_matching(self, ordinal1, ordinal2, fadeout = True):
        matching = make_ordinal_matching(ordinal1, ordinal2)
        self.play(ShowCreation(matching), submobject_mode = "all_at_once")
        if not fadeout: return matching
        self.dither()
        self.play(FadeOut(matching))


class ApplicationDifference(Scene):
    def construct(self):

        self.tool_color = YELLOW
        self.obj_color = BLUE
        
        title = TextMobject("Different uses")
        title.to_edge(UP)
        line = Line(title.get_edge_center(DOWN) + 0.5*DOWN,
                    SPACE_HEIGHT*DOWN)

        self.play(FadeIn(line), FadeIn(title))
        self.dither()
        card_title = TextMobject("Cardinals","measure","sets")
        ord_title = TextMobject("Ordinals\\\\","extract the essence\\\ of","well-ordered sets")

        for subtitle, part in (card_title, LEFT), (ord_title, RIGHT):
            subtitle[0].set_color(self.tool_color)
            subtitle[2].set_color(self.obj_color)
            target = line.get_start() + part*SPACE_WIDTH/2
            subtitle.shift(target - subtitle.get_edge_center(UP))

        equations = self.make_card_equations(card_title)

        #self.add(card_title, ord_title, equations)
        self.play(FadeIn(card_title))
        self.play(FadeIn(equations, submobject_mode = "lagged_start"), run_time = 3)
        self.dither()

        ordinal_phases = self.make_ord_phases(ord_title)
        self.play(Write(ord_title))
        self.dither()
        ordinal = ordinal_phases[0]
        for subord in ordinal:
            self.play(FadeIn(subord, submobject_mode = "lagged_start"))
        self.dither()
        self.play(ordinal.set_color, self.tool_color)
        self.dither()
        for ord_dest in ordinal_phases[1:]:
            self.play(Transform(ordinal, ord_dest))
        self.dither()

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
        self.dither()

        successor_title = TextMobject("Successor step:","+1").to_corner(UP+LEFT)
        self.change_titles(zero_title, successor_title)

        # 1 -> 4
        
        for bar, desc in zip(underlying_fg, descriptions)[1:5]:
            ord_pic_next = ord_pic.copy()
            ord_pic_next.set_color(BLUE)
            ord_pic_next.add(Line(ORIGIN, 1.5*DOWN).next_to(ord_pic))
            brace_next = self.prepare_brace(ord_pic_next, bar)
            self.play(ReplacementTransform(ord_pic, VMobject(*ord_pic_next[:-1])),
                      ReplacementTransform(brace, brace_next))
            brace = brace_next
            ord_pic = ord_pic_next
            self.play(ShowCreation(ord_pic[-1]),
                      ShowCreation(bar),
                      Write(desc))

        # 5 -> ... <w

        self.play(ShowCreation(VGroup(*descriptions[5:])),
                  ShowCreation(VGroup(*underlying_fg[5:])))
        self.dither()

        # supremum
        
        self.remove(underlying_bg)
        limit_title = TextMobject("Limit step: supremum","of all preceding values")
        limit_title.to_corner(UP+LEFT)
        limit_title[0].set_color(YELLOW)
        self.change_titles(successor_title, limit_title,
                           additional_animations = [
                               FadeOut(brace), FadeOut(ord_pic),
                           ])

        self.dither()
        
        self.play_finite_supremum()

        shift = LEFT*underlying2[0].get_center()
        self.play(VGroup(underlying_fg,
                         underlying2,
                         descriptions).shift, shift)

        # preparation for the next round

        underlying3 = underlying2.copy().next_to(underlying2)
        bar = underlying2[0].copy()
        bar.set_color(YELLOW)
        def make_desc(i):
            tex = "\\omega"
            if i > 0: tex += "+{}".format(i)
            return TexMobject(tex)
        descriptions2 = underlying2.add_descriptions(make_desc,
                                                     direction = UP, size = 0.9)
        descriptions2[0].set_color(YELLOW)

        ord_pic, brace = self.play_infinite_supremum(bar)
        self.remove(bar)
        underlying2[0].set_color(YELLOW)
        #self.add(descriptions2)
        self.dither()
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
                      moving.shift, shift)
            hidden_descs2.shift(shift)

            ord_pic = ord_pic_next
            brace = brace_next

            self.play(ShowCreation(bar_next),
                      ShowCreation(ord_pic[-1]),
                      Write(desc))
            self.remove(bar_next)
            bar.highlight(WHITE)
            shown_descs2.add(desc)
            hidden_descs2.remove(desc)
            self.dither()

        # w+5 -> ... <w+w

        self.dither()

        bar = underlying3[0]
        shift = LEFT*bar.get_center()

        next_descs = hidden_descs2.copy()
        next_descs.shift(shift)
        hidden_descs2.set_fill(opacity = 0)

        moving.remove(underlying2)
        underlying2_dest = underlying2.copy()
        underlying2_dest.shift(shift)
        VGroup(*underlying2_dest[1:]).set_color(WHITE)

        self.play(moving.shift, shift,
                  Transform(hidden_descs2, next_descs),
                  Transform(underlying2, underlying2_dest),
                  FadeOut(ord_pic))

        self.dither()

        self.remove(descriptions, underlying_fg)

        #self.revert_to_original_skipping_status()
        bar = underlying3[0].copy()
        bar.set_color(YELLOW)
        self.play_infinite_supremum2(bar, brace)
        self.dither()
        ww_desc = TexMobject("\\omega+\\omega")
        ww_desc.set_color(YELLOW)
        ww_desc.next_to(bar, UP)
        self.play(Write(ww_desc))
        self.dither()

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
        self.dither()
        shift = RIGHT*(ord2[0].get_center() - ord1[0].get_center())
        self.play(ord1.shift, shift/2,
                  ord2.shift, -shift/2,
                  run_time = 0.5)

        self.dither()
        shift = ord2[0].get_center() - ord1[0].get_center()
        self.play(ord2.shift, -shift/2,
                  ord1.shift, shift/2,
                  run_time = 0.7)
        self.remove(ord2)
        self.dither()
        self.play(FadeOut(ord1))

    def play_infinite_supremum(self, underlying_bar, ord_num = 15):

        supremum = OrdinalOmega().set_color(BLUE)
        brace = self.prepare_brace(supremum, underlying_bar)
        self.play(GrowFromCenter(brace))

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
        self.dither()

        ordinals_dest = ordinals.copy()
        for ordinal in ordinals_dest:
            for i, bar in enumerate(ordinal):
                bar.move_to(supremum[i], coor_mask = RIGHT)

        self.play(Transform(ordinals, ordinals_dest))
        self.dither()
        last_ordinal = supremum.copy()
        last_ordinal.stretch(0,1)
        last_ordinal.shift(DOWN*SPACE_HEIGHT)
        ordinals.add(last_ordinal)
        ordinals_dest = VGroup(*[
            VGroup(*supremum[:len(ordinal)]).copy()
            for ordinal in ordinals
        ])
        self.play(Transform(ordinals, ordinals_dest),
                  ShowCreation(underlying_bar))

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
