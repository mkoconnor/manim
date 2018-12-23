#!/usr/bin/env python
# coding: utf-8

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
from topics.fruit import Apple
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.chat_bubbles import Conversation, ChatBubble

import random
import itertools
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer, IconYes, IconNo
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic

import importlib

class Chapter13OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 13\\\\Axiom of Choice",
    }

class Chapter13OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "To choose one sock from each of infinitely many pairs of","socks","requires the Axiom of Choice, but for","shoes","the Axiom is not needed.",
        ],
        "socks" : GREEN,
        "shoes" : YELLOW,
        "author" : "Bertrand Russell"
    }

class AxiomRecallSelExt(Scene):
    def construct(self):

        title = TextMobject("Axioms").to_edge(UP)
        self.play(UnapplyMethod(title.behind_edge, UP))

        dots = VGroup(Dot() for _ in range(8)).arrange_submobjects(buff = 0.5)
        icons = []
        subset_dots = []

        for dot in dots:
            if random.random() < 0.5: icon = IconNo()
            else:
                icon = IconYes()
                subset_dots.append(dot)

            icon.scale(0.5)
            icons.append(icon.next_to(dot, UP))

        subset_dots = VGroup(subset_dots).copy()
        icons = VGroup(icons)

        rect = SurroundingRectangle(VGroup(dots, icons), buff = 0.3)
        VGroup(dots, subset_dots, icons, rect).to_edge(LEFT).shift(1.0*UP)

        selection_title = TextMobject("Selection").next_to(rect, UP)

        #self.wait_to(5)
        self.play(
            Write(selection_title),
            ShowCreation(rect),
            FadeIn(dots),
        )
        self.play(ShowCreation(icons))
        #self.wait_to(8.2)

        subset_dots.save_state()
        subset_dots.shift(1.5*DOWN)
        subset_rect = SurroundingRectangle(subset_dots, buff = 0.3)

        self.play(MoveFromSaved(subset_dots))
        self.play(ShowCreation(subset_rect))

        #self.wait_to(11)

        subset = VGroup(subset_dots, subset_rect)
        subset2 = subset.copy()
        subset2_dots, subset2_rect = subset2
        subset2_dots.save_state()
        subset2.shift(1.5*DOWN)

        subsets = VGroup(subset, subset2)
        eq = TexMobject('=').move_to(subsets)
        ext_title = TextMobject("Extensionality").next_to(subsets)
        
        self.play(FadeIn(ext_title, submobject_mode = "lagged_start"))

        #self.wait_to(14)
        self.play(MoveFromSaved(subset2_dots))
        self.play(ShowCreation(subset2_rect))
        self.play(Write(eq))

        emptyset = Square(color = YELLOW, side_length = 0.5)
        x = Dot()
        singleton = VGroup(x.copy(), SurroundingRectangle(x, buff = 0.2))
        y = Dot().next_to(x, buff = 0.2)
        pair = VGroup(x.copy(), y.copy(), SurroundingRectangle(VGroup(x,y), buff = 0.2))
        small_sets_label = TextMobject("Existence\\\\Pair")
        small_sets = VGroup(small_sets_label, emptyset, singleton, pair).arrange_submobjects(DOWN)
        small_sets.to_edge(RIGHT, buff = 2)

        #self.wait_to(20.5)
        self.play(FadeIn(small_sets_label, submobject_mode = "lagged_start"))
        self.play(FadeIn(VGroup(small_sets[1:]), submobject_mode = "lagged_start"))

        #self.wait_to(30)
        self.dither(2)
        self.play(FadeOut(VGroup(
            subsets, eq,
            dots, rect, icons,
            ext_title, selection_title,
            small_sets,
        )))

chapter4 = importlib.import_module('eost.04-well-ordering')

class AxiomRecallBigSet(Scene):
    def construct(self):

        title = TextMobject("Axioms").to_edge(UP)
        self.add(title)

        omega = OrdinalOmega(q=(0.8, 0.9, 0.9)).shift(LEFT)
        omega[0].highlight(GREEN)
        p_powers = omega.add_descriptions(chapter4.make_p_power,
                                          direction = UP)
        for i,label in enumerate(p_powers):
            label[-i-1].highlight(GREEN)

        naturals = VGroup(TexMobject(str(i)) for i in range(20))
        naturals.arrange_submobjects(buff = 0.5)
        nat_rect = SurroundingRectangle(naturals, buff = 0.2, color = GREEN)
        inf_ax = TextMobject("Infinity").next_to(nat_rect, DOWN, aligned_edge = LEFT)
        VGroup(naturals, nat_rect, inf_ax).to_corner(DOWN+LEFT)

        self.play(
            FadeIn(inf_ax),
            FadeIn(naturals, submobject_mode = "lagged_start"),
            ShowCreation(nat_rect),
        )

        #self.wait_to(4.5)

        self.play(ReplacementTransform(nat_rect.copy(), p_powers[0]))
        self.play(ShowCreation(omega[0]))
        #self.add(omega, p_powers)

        powerset_ax = TextMobject("Powerset").next_to(p_powers[0], UP, buff = 0.5)
        powerset_ax.to_edge(LEFT)

        ##self.wait_to(6.5)
        self.play(FadeIn(powerset_ax))

        #self.play(ReplacementTransform(p_powers[0][0].copy(), p_powers[1][-2]))
        #self.play(
        #    Write(VGroup(p_powers[1][:-2], p_powers[1][-1])),
        #    ShowCreation(omega[1]),
        #)
        print(self.current_scene_time)
        for i in range(1,3):
            self.play(
                ShowCreation(omega[i]),
                FadeIn(VGroup(p_powers[i][:2], p_powers[i][-1])),
                ReplacementTransform(p_powers[i-1].copy(), VGroup(p_powers[i][2:-1])),
            )
        print(self.current_scene_time)
        self.play(
            ShowCreation(VGroup(omega[i+1:])),
            ShowCreation(VGroup(p_powers[i+1:])),
        )
        #self.wait_to(11)

        replacement_ax = TextMobject("Replacement")
        replacement_ax.next_to(powerset_ax.get_corner(DOWN+LEFT), UP+RIGHT)
        replacement_ax.save_state()
        powerset_ax.save_state()
        powerset_ax.shift(UP)
        powerset_ax.set_fill(opacity = 0)
        replacement_ax.shift(DOWN)
        replacement_ax.set_fill(opacity = 0)

        self.play(replacement_ax.restore, MoveFromSaved(powerset_ax))

        #self.wait_to(13.5)
        rect = SurroundingRectangle(VGroup(p_powers, omega[-1].copy().scale_in_place(0)), color = GREEN)
        
        self.play(ReplacementTransform(nat_rect, rect))

        union_bar = omega[0].copy().highlight(YELLOW)
        union_label = TextMobject("Union").highlight(YELLOW).next_to(union_bar, UP)
        VGroup(union_bar, union_label).next_to(rect, coor_mask = X_MASK)

        union_src = []
        for p_power in p_powers: union_src += p_power.submobjects
        union_src = VGroup(union_src).copy()

        #self.wait_to(16.5)
        self.play(ReplacementTransform(union_src, union_label))
        self.play(ShowCreation(union_bar))

        #self.wait_to(26)
        self.dither(2)
        self.play(FadeOut(VGroup(
            naturals, inf_ax,
            omega, p_powers, rect,
            replacement_ax, union_bar, union_label,
        )))

class AxiomChoiceIntro(Scene):
    def construct(self):

        title = TextMobject("Axioms").to_edge(UP)
        self.add(title)

        regularity_ax = TextMobject("Regularity")
        regularity_ax.to_edge(RIGHT, buff = 1).shift(1.5*UP)

        colors = [PURPLE, RED, ORANGE, YELLOW, GREEN, BLUE]
        omega_rects = VGroup(
            Square(
                side_length = 0.6 + 1.4*0.85**i,
                stroke_width = 4 * 0.95**i,
                color = colors[i % len(colors)],
            )
            for i in range(20)
        )
        for square in omega_rects:
            square.fade(1 - square.stroke_width/4)

        omega_rects.next_to(regularity_ax, DOWN, buff = 0.5)
        self.play(FadeIn(regularity_ax, submobject_mode = "lagged_start"))
        self.play(FadeIn(omega_rects, submobject_mode = "one_at_a_time"))

        cross = Cross(color = RED).replace(omega_rects).stretch_in_place(1.1, 0)
        self.play(omega_rects.fade, 0.5, ShowCreation(cross))

        colors = [ORANGE, PURPLE, RED, BLUE, GREEN, YELLOW_D, GRAY]
        subsets = []
        for color in colors:
            end_color = color_gradient((color, BLACK), 3)[1]
            dots = VGroup(Dot() for _ in range(6)).arrange_submobjects(buff = 0.3)
            dots.gradient_highlight(color, end_color)
            rect = SurroundingRectangle(dots, color = color, buff = 0.3)
            subsets.append((dots, rect))

        next_sets = VGroup(subsets[4:])
        subsets = VGroup(subsets[:4])

        subsets.arrange_submobjects(DOWN)
        subsets.shift(4*LEFT)

        next_sets.arrange_submobjects(DOWN)
        next_sets.next_to(subsets, DOWN)

        sets_rect = SurroundingRectangle(subsets, buff = 0.2, color = WHITE)
        
        choice_ax = TextMobject("Axiom of Choice").next_to(sets_rect, UP)
        chosen = VGroup(random.choice(dots) for (dots, rect) in subsets)

        chosen_circ = VGroup(
            Circle(color = GREEN, radius = 0.2).shift(dot.get_center())
            for dot in chosen
        )

        #self.wait_to(9.5)
        self.play(Write(choice_ax))
        self.play(ShowCreation(sets_rect))
        #self.wait_to(15)
        self.play(FadeIn(subsets, submobject_mode = "lagged_start"))
        #self.wait_to(21)
        self.play(ShowCreation(chosen_circ))

        #self.wait_to(25)

        chosen2 = chosen.copy()
        chosen2.save_state()
        chosen2.arrange_submobjects(DOWN, buff = 0.5)
        chosen2.next_to(sets_rect, buff = 0.8)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.3, color = YELLOW)

        self.play(MoveFromSaved(chosen2))
        self.play(ShowCreation(chosen_rect))

        #self.wait_to(28)
        self.play(FadeOut(VGroup(regularity_ax, omega_rects, cross)))

        AC_desc = TextMobject("We can make\\\\","infinite number of\\\\","incidental choices\\\\","at once.",
                              alignment = "\\hsize = 0.4\\hsize\\raggedright")
        AC_desc.next_to(ORIGIN).shift(0.5*UP)
        ##self.wait_to(37.5)
        self.play(Write(AC_desc))

        #self.wait_to(38)
        self.play(FocusOn2(AC_desc[1], scale = 1.1))
        #self.wait_to(39.5)
        self.play(FocusOn2(AC_desc[2], scale = 1.1))

        #self.wait_to(50.5)
        self.play(FadeOut(VGroup(chosen2, chosen_rect, chosen_circ)))
        #self.wait_to(54.5)

        chosen2_center = chosen2.get_center()
        chosen2 = VGroup(chosen[0].copy())
        chosen2.save_state()
        chosen2.move_to(chosen2_center, coor_mask = X_MASK)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.25, color = YELLOW)
        chosen_set = VGroup(chosen2, chosen_rect)

        self.play(MoveFromSaved(chosen2, path_arc = -0.3*np.pi))
        #self.wait_to(60 + 5.5)
        self.play(ShowCreation(chosen_rect))

        #self.wait_to(60 + 12)
        for i in range(1, len(chosen)):
            dot = chosen[i].copy()
            dot.save_state()
            dot.move_to(chosen2_center, coor_mask = X_MASK)
            dot_rect = SurroundingRectangle(dot, buff = 0.25, color = YELLOW)

            self.play(
                FadeIn(dot_rect),
                MoveFromSaved(dot, path_arc = -0.3*np.pi),
            )

            dot_set = VGroup(dot, dot_rect)
            sets_to_merge = VGroup(chosen_set, dot_set)
            sets_to_merge.save_state()

            dot_set.next_to(chosen_set, DOWN, buff = 0)
            sets_to_merge.move_to(VGroup(subsets[:i+1]), coor_mask = Y_MASK)

            self.play(MoveFromSaved(sets_to_merge), run_time = 0.5)

            self.remove(dot_set)
            chosen2.add(dot)
            self.add(dot)
            chosen_rect.replace(VGroup(chosen_rect.copy(), dot_rect), stretch = True)

        #self.wait_to(60 + 22)

        self.play(
            FadeIn(next_sets, submobject_mode = "lagged_start"),
            Transform(sets_rect,
                      SurroundingRectangle(VGroup(subsets, next_sets), color = WHITE), 
            ),
            FadeOut(VGroup(chosen2, chosen_rect)),
        )

        subsets.submobjects += next_sets.submobjects
        chosen = []
        for subset in subsets:
            chosen.append(subset[0][0])
        chosen = VGroup(chosen)

        chosen2 = chosen.copy()
        chosen2.save_state()
        chosen2.move_to(chosen2_center, coor_mask = X_MASK)
        chosen_circ = VGroup(
            Circle(color = GREEN, radius = 0.2).shift(dot.get_center())
            for dot in chosen
        )

        #self.wait_to(60 + 29.3)
        self.play(ShowCreation(chosen_circ, submobject_mode = "all_at_once"))
        #self.wait_to(60 + 31.5)
        self.play(MoveFromSaved(chosen2))
        #self.wait_to(60 + 34)

        AC_desc.save_state()
        self.play(AC_desc.to_edge, DOWN)

        replacement_ax = TextMobject("Axiom of Replacement").move_to(choice_ax)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.3, color = YELLOW)
        replacement_ax.next_to(chosen_rect, buff = 0.5, aligned_edge = UP)
        replacement_rule = TextMobject("Rule").next_to(replacement_ax, DOWN)
        replacement_rule.highlight(YELLOW)

        self.play(FadeIn(replacement_ax))
        #self.wait_to(60 + 37)
        self.play(Write(replacement_rule))
        #self.wait_to(60 + 47)

        self.play(ReplacementTransform(sets_rect.copy(), chosen_rect))

        #self.wait_to(2*60+6)

        chosen = []
        for subset in subsets:
            chosen.append(random.choice(subset[0]))

        chosen_circ.save_state()
        for circ, dot in zip(chosen_circ, chosen): circ.move_to(dot)
        chosen2.save_state()
        for dot2, dot in zip(chosen2, chosen): dot2.highlight(rgb_to_color(dot.fill_rgb))

        self.play(
            MoveFromSaved(chosen_circ),
            MoveFromSaved(chosen2),
        )
        #self.wait_to(2*60+8)
        self.play(
            FadeOut(VGroup(replacement_ax, replacement_rule)),
            AC_desc.restore,
        )

        #self.wait_to(2*60+11)
        conversation = Conversation(self)
        conversation.add_bubble("So the outcome of AC looks random?")
        self.dither(2)
        #self.wait_to(2*60+41)

class Prisoner(SVGMobject):
    CONFIG = {
        "initial_scale_factor" : 0.05,
        "file_name" : "prisoner",
        "hat_color" : None,
        "stroke_width" : DEFAULT_POINT_THICKNESS,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_stroke(width = self.stroke_width)
        self.eye.set_style_data(stroke_width = 0, stroke_color = WHITE,
                                fill_color = WHITE, fill_opacity = 1)
        if self.hat_color is None:
            self.hat_color = random.choice((BLUE, YELLOW))
        self.hat.set_fill(self.hat_color, 0.5)
        self.hide_bubble()

    def hide_bubble(self):
        self.bubble.scale_about_point(np.array([0.1,-0.1, 1]), self.bubble_tip)
        self.bubble.set_style_data(fill_opacity = 0, stroke_width = 0)

    def show_bubble(self, color):
        self.bubble.scale_about_point(np.array([10,-10, 1]), self.bubble_tip)
        self.bubble.set_style_data(
            fill_opacity = 0.5, fill_color = color,
            stroke_width = self.stroke_width,
        )

    def eye_cone(self, h = 0.6, w = 0.7):
        ratio = self[0].get_width()
        h *= ratio
        w *= ratio
        eye_center = self.eye.get_center()
        return VGroup(
            DashedLine(eye_center, eye_center + h*UP + w*RIGHT),
            DashedLine(eye_center, eye_center + h*DOWN + w*RIGHT),
        )

    @property
    def hat(self): return self.submobjects[-2]
    @property
    def bubble(self): return self.submobjects[-1]
    @property
    def bubble_tip(self): return np.array(self.bubble.points[0])
    @property
    def eye(self): return self.submobjects[2]


class ExamplesIntro(Scene):
    def construct(self):

        title = TextMobject("Examples").to_edge(UP)
        self.add(title)
        self.play(UnapplyMethod(title.behind_edge, UP))

        prisoners = VGroup(Prisoner() for _ in range(5)).arrange_submobjects()
        prisoners.shift(UP)
        hats_title = TextMobject("Hats").next_to(prisoners, UP, aligned_edge = LEFT)

        unm_line = DashedLine(LEFT, RIGHT, color = "#FF00FF")
        unm_brace = BraceText(unm_line, "?", UP)
        unm_title = TextMobject("Unmeasurable set")
        unmeasurable = VGroup((unm_line, unm_brace), unm_title)
        unmeasurable.arrange_submobjects(RIGHT, buff = 0.5).shift(DOWN)

        #self.wait_to(3)
        self.play(
            FadeIn(prisoners, submobject_mode = "lagged_start"),
        )
        #self.wait_to(5)

        self.play(
            ShowCreation(unm_line),
            unm_brace.creation_anim(),
        )
        #self.wait_to(7.3)

        self.play(
            FadeIn(hats_title, submobject_mode = "lagged_start"),
        )
        #self.wait_to(9.5)
        self.play(FadeIn(unm_title, submobject_mode = "lagged_start", run_time = 2))

        #self.wait_to(30.5)

        self.dither()
        self.play(FadeOut(VGroup(title, prisoners, hats_title, unmeasurable)))
        #self.wait_to(32.5)

def make_prisoners():
    corner = DOWN+RIGHT
    limit_point = corner * (SPACE_WIDTH, SPACE_HEIGHT, 0)
    limit_point -= corner * DEFAULT_MOBJECT_TO_EDGE_BUFFER
    ratio = 0.88

    prisoners = VGroup(
        (Prisoner(stroke_width = DEFAULT_POINT_THICKNESS * (ratio ** i))
         .to_corner(DOWN+LEFT).scale_about_point(ratio ** i, limit_point))
        for i in range(40)
    )
    prisoners.shift(0.5*UP)

    labels = VGroup(
        TexMobject(str(i)) for i in range(len(prisoners))
    )
    for label, p in zip(labels, prisoners):
        max_h = p.get_width() * 0.4
        if label.get_height() >= max_h: label.scale_to_fit_height(max_h)
        label.next_to(p, DOWN, buff = 0.7*label.get_height())

    return prisoners, labels

class PrisonersTale(Scene):
    def construct(self):

        king = SVGMobject(file_name = "evil_king", initial_scale_factor = 0.03, unpack_groups = False)
        king.to_corner(UP+LEFT)

        throne, arms, legs, head, crown = king
        throne.set_style_data(stroke_width = 0, fill_opacity = 1, fill_color = DARK_GREY)
        arms[0].set_style_data(fill_opacity = 1, fill_color = BLACK, stroke_width = 0)
        legs.set_fill(BLACK, 1)
        crown.set_style_data(fill_opacity = 1, fill_color = BLACK, stroke_color = YELLOW)

        head[0].set_fill(BLACK, 1)       # head outline
        head[1].mark_paths_closed = True # mouth
        VGroup(head[2:]).highlight(RED)  # eyes

        self.play(
            FadeIn(throne),
            Animation(arms[0]),
            ShowCreation(VGroup(arms[1:])),
            ShowCreation(legs),
            ShowCreation(head),
            ShowCreation(crown),
        )

        prisoner_cap = SVGMobject(file_name = "prisoner_cap", initial_scale_factor = 0.06, unpack_groups = False)
        stripes = prisoner_cap[0]
        stripes.set_style_data(stroke_width = 0, fill_opacity = 1, fill_color = WHITE)
        eye = prisoner_cap[-1]
        eye.set_style_data(stroke_width = 0, fill_opacity = 1, fill_color = WHITE)
        prisoners = VGroup(prisoner_cap.copy() for _ in range(8))
        prisoners.arrange_submobjects()
        prisoners.to_edge(DOWN, buff = 0)

        grid = VGroup(
            VGroup(Line(LEFT, RIGHT) for _ in range(3)).arrange_submobjects(DOWN, buff = 0.55),
            VGroup(Line(UP, DOWN) for _ in range(3)).arrange_submobjects(RIGHT, buff = 0.55),
        )
        grid.next_to(prisoners, UP)
        grid.to_edge(RIGHT)

        #self.wait_to(1.8)
        self.play(ShowCreation(grid))

        self.play(UnapplyMethod(prisoners.behind_edge, DOWN))

        #self.wait_to(16.5)
        self.dither(2)

        self.play(
            FadeOut(grid),
            prisoners.behind_edge, DOWN,
        )

        #self.wait_to(18.3)
        prisoners, labels = make_prisoners()
        self.play(UnapplyMethod(prisoners.behind_edge, DOWN))

        eye_cone = prisoners[2].eye_cone()
        hidden_hats = VGroup(p.hat for p in prisoners[:3])
        hidden_hats.save_state()
        #self.wait_to(23.5)
        self.play(
            ShowCreation(eye_cone[0]),
            ShowCreation(eye_cone[1]),
            hidden_hats.set_fill, BLACK,
        )

        #self.wait_to(32.5)
        self.play(ShowCreation(labels))
        
        #self.wait_to(36.5)

        self.dither(2)
        self.play(
            FadeOut(eye_cone),
            hidden_hats.restore,
        )
        #self.wait_to(38)

        bubbles = VGroup(p.bubble for p in prisoners)
        bubbles.save_state()

        for p in prisoners: p.show_bubble(random.choice((YELLOW, BLUE)))
        self.play(
            MoveFromSaved(bubbles)
        )

        rules = VGroup(
            TextMobject("Finite number of errors $\Rightarrow$ amnesty"),
            TextMobject("Infinite number of errors $\Rightarrow$\\\\mass execution"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        rules.next_to(king).to_edge(UP)

        #self.wait_to(41)
        self.play(FadeIn(rules[0], submobject_mode = "lagged_start", run_time = 2))
        #self.wait_to(46)
        self.play(FadeIn(rules[1], submobject_mode = "lagged_start", run_time = 2))

        #self.wait_to(52.5)

        def rate_func(x):
            x *= np.pi*5
            return np.abs(np.sin(x))

        self.play(ApplyMethod(VGroup(head, crown).shift, 0.2*DOWN, run_time = 1.5, rate_func = rate_func))

        #self.wait_to(60+3)

        #one_half = TexMobject("\\frac12")
        #self.play(Write(one_half))

        #self.wait_to(60+12)

        self.dither(2)
        self.play(
            king.behind_edge, LEFT,
            #VGroup(labels, prisoners).behind_edge, DOWN,
            FadeOut(VGroup(bubbles, rules, one_half)),
            #VGroup(p.hat for p in prisoners).set_fill, BLACK,
        )
        #self.wait_to(60+16)

class SimpleStrategy(Scene):
    def construct(self):

        prisoners, labels = make_prisoners()
        hats = VGroup((p.hat for p in prisoners), fill_opacity = 0.5)
        hats.save_state()
        hats.set_fill(BLACK)

        self.add(prisoners, labels)

        index = 2
        prisoner = prisoners[index]
        eye_cone = prisoner.eye_cone()
        #self.wait_to(5)
        self.play(
            ShowCreation(eye_cone[0]),
            ShowCreation(eye_cone[1]),
            VGroup(hats[index+1:], fill_opacity = 0.5).set_fill, BLUE,
        )
        #self.wait_to(7.5)

        prisoner.bubble.save_state()
        prisoner.show_bubble(BLUE)
        self.play(MoveFromSaved(prisoner.bubble))

        #self.wait_to(11.5)

        bubbles = VGroup(p.bubble for p in prisoners[index+1:])
        bubbles.save_state()
        for p in prisoners[index+1:]: p.show_bubble(BLUE)

        self.play(MoveFromSaved(bubbles, submobject_mode = "one_at_a_time"))

        #self.wait_to(23.5)
        self.dither()
        self.play(
            FadeOut(VGroup(prisoner.bubble, bubbles, eye_cone)),
            hats.restore,
        )

chapter9 = importlib.import_module('eost.09-axioms-cz')
dot_r_comp = chapter9.dot_r_comp

class HatsSet(Scene):
    def construct(self):
        prisoners, labels = make_prisoners()
        prisoners_g = VGroup(prisoners, labels)
        self.add(prisoners_g)

        seq = OrdinalOmega()
        next_bars = VGroup(seq[len(prisoners):])

        for bar, p in zip(seq, prisoners):
            bar.set_color(p.hat_color)
        for bar in next_bars:
            bar.set_color(random.choice((BLUE, YELLOW)))

        seq_ordinal = seq.copy()

        for bar, p in zip(seq, prisoners):
            bar.next_to(p.hat, UP, buff = p.hat.get_height() * 0.3)
        i = len(prisoners)-1
        next_bars.shift(seq[i].get_center() - seq_ordinal[i].get_center())
        for bar in next_bars:
            bar.next_to(prisoners[-1].hat, UP, coor_mask = Y_MASK, buff = 0)

        seq.save_state()
        for bar in seq: bar.scale_in_place(0)
        for bar, p in zip(seq, prisoners):
            bar.move_to(p.hat)
        for bar in next_bars:
            bar.move_to(prisoners[-1].hat, coor_mask = Y_MASK)

        #self.wait_to(2.2)
        self.play(seq.restore)
        #self.wait_to(6.5)
        self.play(Transform(seq, seq_ordinal))
        #self.wait_to(10)

        big_rect = Rectangle(width = 1.9*SPACE_WIDTH, height = 1.9*SPACE_HEIGHT)
        prisoners.save_state()
        self.play(
            ShowCreation(big_rect),
            prisoners_g.behind_edge, DOWN,
        )

        seq.save_state()
        seqs = VGroup(
            (OrdinalOmega(), OrdinalOmega()),
            (OrdinalOmega(), seq),
        )
        for bar in seqs[0][0]: bar.set_color(random.choice((YELLOW, BLUE)))
        for bar in seqs[0][1]: bar.set_color(BLUE)
        for i, bar in enumerate(seqs[1][0]): bar.set_color((BLUE, YELLOW)[i%2])
        seqs.scale(0.7)
        for row in seqs:row.arrange_submobjects()
        seqs.arrange_submobjects(DOWN)
        seqs.next_to(big_rect.get_corner(LEFT+UP), DOWN+RIGHT, buff = 0.5)

        self.play(
            MoveFromSaved(seq),
            FadeIn(seqs[0]),
            FadeIn(seqs[1][0]),
        )
        #self.wait_to(22.3)

        seqs = VGroup(seqs[0][0], seqs[1][0], seqs[0][1], seqs[1][1])
        classes = VGroup(SurroundingRectangle(seq, buff = 0, color = GREEN) for seq in seqs)
        seqs.save_state()
        for seq in seqs: seq.scale_in_place(np.array((0.9, 0.8, 1)))
        self.play(
            MoveFromSaved(seqs),
            FadeIn(classes),
        )
        #self.wait_to(24.2)

        seq = seqs[-1]
        rect = classes[-1]
        seq2 = seq.copy().next_to(rect, DOWN, coor_mask = Y_MASK)
        rect2 = rect.copy().shift(seq2[0].get_center() - seq[0].get_center())

        index = 4

        for bar in seq2[:index]: bar.set_color(random.choice((BLUE, YELLOW)))
        bar = seq2[index]
        if (color_to_rgb(bar.color) == color_to_rgb(YELLOW)).all(): bar.set_color(BLUE)
        elif (color_to_rgb(bar.color) == color_to_rgb(BLUE)).all(): bar.set_color(YELLOW)
        else: raise Exception("Unexpected color")

        self.play(
            FadeIn(seq2),
            Transform(rect, SurroundingRectangle(VGroup(rect, rect2), buff = 0, color = GREEN)),
        )

        edge = DashedLine(
            VGroup(seq[index:index+2]).get_center(),
            VGroup(seq2[index:index+2]).get_center(),
            color = GREEN,
        )
        arrow = Arrow(ORIGIN, RIGHT*2, color = GREEN).next_to(edge, buff = 0)
        #self.wait_to(27.5)
        self.play(ShowCreation(edge))
        self.play(ShowCreation(arrow))

        dots = VGroup(dot_r_comp(color = GREEN) for _ in seqs)
        dots.arrange_submobjects(buff = 1)
        dots.next_to(big_rect.get_edge_center(UP), DOWN, buff = 0.5)

        #self.wait_to(39)
        self.play(FadeOut(VGroup(edge, arrow)))

        seqs.save_state()
        seq2.save_state()
        for seq, dot in zip(seqs, dots):
            seq.scale(0)
            seq.move_to(dot.get_center())
        seq2.scale(0)
        seq2.move_to(dots[-1].get_center())
        self.play(
            MoveFromSaved(seqs),
            MoveFromSaved(seq2),
            ReplacementTransform(classes, dots),
        )

        self.seqs = seqs
        self.dots = dots

        #self.wait_to(47)
        self.expand_dot(2)
        #self.wait_to(56)
        self.dither()
        self.hide_dot()
        self.expand_dot(1)
        self.dither()
        #self.wait_to(60+12)
        self.hide_dot()
        #self.wait_to(60+14)

        prisoners.restore()
        prisoners.next_to(big_rect.get_edge_center(DOWN), UP)

        index = 3
        eye_cone = prisoners[index].eye_cone()
        hidden_hats = VGroup(p.hat for p in prisoners[:index+1])
        hidden_hats.save_state()
        hidden_hats.set_fill(BLACK)
        eye_cone.save_state()

        prisoners.save_state()
        VGroup(prisoners, eye_cone).behind_edge(DOWN)
        self.play(prisoners.restore, eye_cone.restore)
        self.dither(2)

        #self.wait_to(60+16.5)
        expand_anim = self.expand_dot_anim(3)
        arrows = VGroup(self.make_arrow(pr) for pr in prisoners)
        self.play(expand_anim, ShowCreation(arrows[index]))
        self.dither()

        #self.wait_to(60+25.5)
        self.play(
            hidden_hats.restore,
            FadeOut(eye_cone),
        )

        #self.wait_to(60+30)
        remaining_arrows = VGroup(arrows.submobjects)
        remaining_arrows.remove(arrows[index])
        self.play(ShowCreation(remaining_arrows))

        #self.wait_to(60+34.5)
        self.play(FadeOut(arrows))

        #self.wait_to(60+36)
        seq = self.interior[2]
        seq_ori = seq.copy()
        seq.save_state()
        for bar, p in zip(seq, prisoners):
            bar.next_to(p.hat, UP, buff = p.hat.get_height() * 0.3)
        i = len(prisoners)-1
        next_bars = VGroup(seq[len(prisoners):])
        next_bars.shift(seq[i].get_center() - seq.saved_state[i].get_center())
        for bar in next_bars:
            bar.next_to(prisoners[-1].hat, UP, coor_mask = Y_MASK, buff = 0)

        self.play(MoveFromSaved(seq))

        for i in reversed(range(20)):
            if (seq[i].stroke_rgb != prisoners[i].hat.fill_rgb).any(): break
        edge = DashedLine(ORIGIN, UP, color = GREEN)
        edge.next_to(VGroup(seq[i:i+2]).get_center(), UP, buff = 0)
        arrow = Arrow(LEFT, RIGHT, color = GREEN)
        arrow.next_to(edge, buff = 0)
        arrow.shift(0.2*UP)
        edge_g = VGroup(edge, arrow)
        #self.wait_to(60+38.5)
        self.play(ShowCreation(edge_g))

        #self.wait_to(60+54)

        self.play(FadeOut(edge_g))

        #self.wait_to(60+55.5)
        self.play(Transform(seq, seq_ori))
        corner = seq.get_corner(UP+LEFT)
        arrow = Arrow(corner+(UP+LEFT), corner, color = ORANGE)
        self.play(ShowCreation(arrow))

        #self.wait_to(2*60+4)

        self.interior.remove(self.interior[2])
        self.interior_collapsed.remove(self.interior_collapsed[2])

        arrow_dest = Arrow(ORIGIN, 1.5*DOWN, color = ORANGE)
        arrow_dest.next_to(self.rect.saved_state, DOWN)
        seq.save_state()
        seq.next_to(arrow_dest, DOWN)

        self.play(
            self.hide_dot_anim(),
            Transform(arrow, arrow_dest),
            MoveFromSaved(seq),
        )
        seq_ori = seq.copy()
        arrow_ori = arrow.copy()

        #self.wait_to(2*60+6)
        for i in reversed(range(3)):
            arrow.save_state()
            arrow.next_to(self.dots[i], DOWN)
            seq.save_state()
            seq.next_to(arrow, DOWN)
            for src, dest in zip(self.seqs[i], seq):
                dest.set_color(src.color)
            self.play(MoveFromSaved(arrow), MoveFromSaved(seq))

        AC_title = TextMobject("Axiom of Choice")
        AC_arrow = Arrow(ORIGIN, 1.5*DOWN, color = WHITE)
        repr_text = TextMobject("representatives").highlight(ORANGE)
        repr_rect = SurroundingRectangle(repr_text, color = WHITE)
        repr_g = VGroup(repr_text, repr_rect)
        AC_g = VGroup(AC_title, AC_arrow, repr_g).arrange_submobjects(DOWN)

        AC_g.move_to((seq.get_edge_center(RIGHT) + big_rect.get_edge_center(RIGHT))/2)
        AC_g.next_to(self.dots, DOWN, coor_mask = Y_MASK, buff = 1)

        #self.wait_to(2*60+24)
        self.play(FadeIn(AC_title, submobject_mode = "lagged_start"))
        #self.wait_to(2*60+28)
        self.play(ShowCreation(AC_arrow))
        self.play(FadeIn(repr_text, submobject_mode = "lagged_start"))
        #self.wait_to(2*60+31.5)
        self.play(ShowCreation(repr_rect))

        #self.wait_to(2*60+34)
        repr_g.save_state()
        repr_g.next_to(VGroup(prisoners[3:]), UP, buff = 0, coor_mask = Y_MASK)
        self.play(
            FadeOut(VGroup(AC_title, AC_arrow, arrow, seq)),
            MoveFromSaved(repr_g),
        )
        #self.wait_to(2*60+58.8)

        circ = Circle(radius = 0.2, color = WHITE)
        circ.rotate(np.pi/2)
        circ.stretch(-1, 0)
        circ.shift(self.dots[-1].get_center())
        self.play(ShowCreation(circ))
        #self.wait_to(3*60+5)
        arrow = arrow_ori
        seq = seq_ori
        self.play(ShowCreation(arrow), FadeIn(seq))

        #self.wait_to(3*60+14)
        self.play(FadeOut(big_rect))
        #self.wait_to(3*60+23.5)

        mathologer_pic = ImageMobject("mathologer-ac.jpg")
        mathologer_pic.scale(1./3)
        mathologer_label = TextMobject("Death by infinity puzzles\\\\(Mathologer)")
        mathologer_label.scale(0.7)
        mathologer_label.next_to(mathologer_pic, UP)
        mathologer = VGroup(mathologer_pic, mathologer_label)
        mathologer.to_edge(LEFT)
        self.play(UnapplyMethod(mathologer.behind_edge, RIGHT))
        self.dither(2)

        #self.wait_to(3*60+40)
        #self.play(FadeOut(VGroup(circ, seq, arrow, self.dots, repr_g, prisoners)))

    def make_arrow(self, pr):
        p0 = pr.hat.get_edge_center(UP) + 0.3*pr.hat.get_height()*UP
        x = p0[0]
        corner1 = self.rect_expanded.get_corner(DOWN+LEFT)
        corner2 = self.rect_expanded.get_corner(DOWN+RIGHT)
        no_tip = False
        if x < corner1[0]: x = corner1[0]
        elif x > corner2[0]:
            x = corner2[0]
            no_tip = True
        y = corner1[1]
        p1 = x*X_MASK + y*Y_MASK

        stroke_width = pr.stroke_width
        tip_length = min(0.25, pr.hat.get_height()*1)

        if no_tip: return Line(p0, p1, color = GREEN, stroke_width = stroke_width)
        return Arrow(p0, p1, color = GREEN, buff = 0, stroke_width = stroke_width, tip_length = tip_length)

    def expand_dot_anim(self, index):
        seq = OrdinalOmega()
        seq.stretch(0.6, 0)
        seq.stretch(0.6, 1)

        self.rect_expanded = self.dots[index]
        for src, dest in zip(self.seqs[index], seq):
            dest.set_color(src.color)

        self.interior = VGroup(seq.copy() for _ in range(4))
        table = VGroup(self.interior[:2], self.interior[2:])
        for row in table: row.arrange_submobjects()
        table.arrange_submobjects(DOWN)
        table.next_to(self.dots, DOWN, buff = 1)

        for i, seq in enumerate(self.interior):
            for bar in seq[:3+2*i]:
                bar.set_color(random.choice((BLUE, YELLOW)))

        self.interior_expanded = self.interior.copy()
        self.interior.scale(0).move_to(self.dots[index])
        self.interior_collapsed = self.interior.copy()

        self.rect_expanded = SurroundingRectangle(self.interior_expanded, color = GREEN, buff = 0.5)
        self.rect = self.dots[index]
        self.rect.save_state()
        return AnimationGroup(
            Transform(self.interior, self.interior_expanded),
            Transform(self.rect, self.rect_expanded),
        )

    def expand_dot(self, index):
        self.play(self.expand_dot_anim(index))

    def hide_dot_anim(self):

        return AnimationGroup(
            Transform(self.interior, self.interior_collapsed, remover = True),
            ApplyMethod(self.rect.restore),
        )

    def hide_dot(self):
        self.play(self.hide_dot_anim())

class MeasureIntro(Scene):
    def construct(self):

        title = TextMobject("Area").to_edge(UP)
        self.play(Write(title))

        triangle = Polygon(UP, DOWN+2*RIGHT, DOWN+LEFT)
        circ = Circle()
        areas_classical = VGroup(triangle, circ).arrange_submobjects().next_to(title, DOWN, buff = 0.5)
        areas_classical.set_fill(opacity = 0.3)
        areas_classical.set_color(RED)

        triangle_label = TexMobject("\\frac{av}2")
        triangle_label.move_to(triangle.points[0])
        triangle_label.next_to(triangle.get_anchors()[1], UP, coor_mask = Y_MASK)
        triangle_label.shift(0.15*RIGHT)

        circ_label = TexMobject("\\pi r^2")
        circ_label.shift(circ.get_center() - VGroup(circ_label[:2]).get_center())

        crazy_set = VGroup(
            Dot(np.random.random(size = 3)*2,
                radius = np.random.random()*0.05+0.01,
                color = random.choice((BLACK,RED))
            ).fade(0.3)
            for _ in range(800)
        )
        crazy_set.next_to(areas_classical, DOWN, buff = 0.5)

        #self.wait_to(5.5)
        self.play(ShowCreation(triangle))
        self.play(Write(triangle_label))
        #self.wait_to(10)

        self.play(ShowCreation(circ))
        self.play(Write(circ_label))

        #self.wait_to(16)
        self.play(ShowCreation(crazy_set))

        #self.wait_to(26)
        self.dither()
        self.play(FadeOut(VGroup(
            triangle, triangle_label,
            circ, circ_label,
            crazy_set,
        )))

set_shift = 0.2*UP

class MeasureProperties(Scene):
    def construct(self):

        title = TextMobject("Area").to_edge(UP)
        self.add(title)

        reals = NumberLine()
        self.play(ShowCreation(reals))
        #self.wait_to(4)

        subtitle = TextMobject("Measure").next_to(reals, UP).to_edge(LEFT)
        self.play(Write(subtitle))

        interval1 = Line(-3*X_MASK, -1*X_MASK).shift(set_shift).highlight(YELLOW)
        interval2 = Line(0*X_MASK, 3*X_MASK).shift(set_shift).highlight(YELLOW)

        interval1_label = TexMobject('2').next_to(interval1, UP).highlight(YELLOW)
        interval2_label = TexMobject('3').next_to(interval2, UP).highlight(YELLOW)

        #self.wait_to(13)
        self.play(ShowCreation(interval1))
        self.play(Write(interval1_label))

        #self.wait_to(17)
        self.play(ShowCreation(interval2), FadeIn(interval2_label))
        #self.wait_to(19)

        union_label = TexMobject('2+3').highlight(YELLOW)
        union_center = (interval1.get_corner(UP+RIGHT) + interval2.get_corner(LEFT))/2
        union_label.next_to(union_center, UP)
        self.play(
            ReplacementTransform(interval1_label[0], union_label[0]),
            FadeIn(union_label[1]),
            ReplacementTransform(interval2_label[0], union_label[2]),
        )
        ##self.wait_to(20)

        union_label2 = TexMobject('5').highlight(YELLOW).next_to(union_center, UP)
        self.play(ReplacementTransform(union_label, union_label2))

        added_points = VGroup(
            DashedLine(-4*X_MASK, -3*X_MASK),
            DashedLine(-1*X_MASK,  0*X_MASK),
            DashedLine( 3*X_MASK,  4*X_MASK),
        ).shift(set_shift).highlight(YELLOW)
        #self.wait_to(27)
        self.play(ShowCreation(added_points))

        union_label = TexMobject('\geq 5').next_to(union_center, UP)
        union_label[-1].highlight(YELLOW)

        #self.wait_to(29)
        self.play(
            FadeIn(union_label[0]),
            ReplacementTransform(union_label2[0], union_label[1]),
        )

        #self.wait_to(32.5)
        self.play(FadeOut(VGroup(added_points, union_label, interval1, interval2)))

        rec_set = []
        holes = [(0.,6.)]
        seg_len = 2.

        rec_set_layers = 7
        for _ in range(rec_set_layers):
            next_holes = []
            for a,b in holes:
                center = (a+b)/2
                c = center - seg_len/2
                d = center + seg_len/2
                next_holes += [(a,c), (d,b)]
                rec_set.append(Line(c*X_MASK, d*X_MASK))
            holes = next_holes
            seg_len /= 4

        rec_set = VGroup(rec_set)
        rec_set.shift(set_shift).highlight(YELLOW)

        rec_set.save_state()
        rec_set.shift(0.2*UP)
        rec_set.highlight(BLACK)

        #self.wait_to(34)
        self.play(rec_set.restore)

        rec_set_label = TexMobject("4").highlight(YELLOW).next_to(rec_set, UP)
        self.play(FadeIn(rec_set_label))

        ##self.wait_to(35)
        self.play(rec_set.shift, 3*LEFT)
        #self.wait_to(39)
        self.play(rec_set_label.shift, 3*LEFT)
        #self.wait_to(47)

        rec_set.save_state()
        rec_set.arrange_submobjects(DOWN, coor_mask = Y_MASK)
        rec_set.next_to(reals, DOWN, coor_mask = Y_MASK)

        self.play(MoveFromSaved(rec_set, run_time = 2))
        #self.wait_to(50)

        rec_set_folded = []
        for i in range(rec_set_layers):
            start = 2 - 2.0**(2-i)
            end = 2 - 2.0**(2-(i+1))
            points = np.linspace(start, end, 2**i + 1)
            for p0, p1 in zip(points, points[1:]):
                rec_set_folded.append(Line(p0*X_MASK, p1*X_MASK))

        rec_set_folded = VGroup(rec_set_folded)
        rec_set_folded.shift(set_shift).highlight(YELLOW)

        rec_set_folded_in_rows = rec_set_folded.copy()
        rec_set_folded_in_rows.arrange_submobjects(DOWN, coor_mask = Y_MASK)
        rec_set_folded_in_rows.next_to(reals, DOWN, coor_mask = Y_MASK)

        self.play(ReplacementTransform(rec_set, rec_set_folded_in_rows))

        #self.wait_to(54)
        self.play(ReplacementTransform(rec_set_folded_in_rows, rec_set_folded))

        #self.wait_to(60+9)
        self.dither(2)

        next_title = TextMobject("Unmeasurable set").to_edge(UP)
        next_title.save_state()
        next_title.shift(DOWN)
        next_title.set_fill(opacity = 0)
        title.save_state()
        title.shift(UP)
        title.set_fill(opacity = 0)
        self.play(
            FadeOut(VGroup(subtitle, rec_set_label, rec_set_folded)),
            MoveFromSaved(title),
            next_title.restore,
        )

class UnmeasurableOverview(Scene):
    def construct(self):

        title = TextMobject("Unmeasurable set").to_edge(UP)
        reals = NumberLine()
        self.add(title, reals)

        subinterval = GradientLine(ORIGIN, 2*X_MASK, YELLOW, YELLOW, segment_num = 50)
        subinterval.submobjects = subinterval.submobjects[::2]
        subinterval.shift(set_shift)

        AC_label = TextMobject("Axiom of Choice").next_to(subinterval, UP, buff = 0.5)
        self.play(FadeIn(AC_label, submobject_mode = "lagged_start"))

        numbers = reals.get_number_mobjects()
        zero_i = len(numbers)//2
        zero = numbers[zero_i]
        two = numbers[zero_i+2]
        #self.wait_to(4)
        self.play(
            ShowCreation(subinterval),
            FadeIn(VGroup(zero, two), submobject_mode = "one_at_a_time"),
        )

        shifts = []
        for i in range(5):
            shifts += [
                subinterval.copy().shift(i*(2*RIGHT)),
                subinterval.copy().shift((i+1)*(2*LEFT)),
                subinterval.copy().shift(RIGHT + (i+1)*(2*LEFT)),
                subinterval.copy().shift(RIGHT + i*(2*RIGHT)),
            ]
        shifts = VGroup(shifts)

        copies = VGroup(subinterval.copy() for _ in shifts)
        copies.arrange_submobjects(DOWN, coor_mask = Y_MASK)
        copies.next_to(reals, DOWN, coor_mask = Y_MASK)

        #self.wait_to(10)
        self.play(
            FadeOut(VGroup(zero, two)),
            ReplacementTransform(VGroup(subinterval), copies),
        )

        #self.wait_to(14)
        copies.save_state()
        for src, dest in zip(shifts, copies): dest.move_to(src, coor_mask = X_MASK)
        self.play(MoveFromSaved(copies, run_time = 2))

        #self.wait_to(17)
        self.play(ReplacementTransform(copies, shifts))

        #self.wait_to(22)
        self.dither()
        self.play(FadeOut(VGroup(AC_label, shifts)))

class UnmeasurableConstruction(Scene):
    def construct(self):

        title = TextMobject("Unmeasurable set").to_edge(UP)
        reals = NumberLine()
        self.add(title, reals)

        classes_desc = TextMobject("Groups modulo $\\mathbb Q$")
        classes_desc.next_to(title, DOWN, buff = 0.5)
        classes_desc.to_edge(LEFT)

        self.play(FadeIn(classes_desc))
        #self.wait_to(6.5)

        dot_pair = VGroup(
            Dot(np.sqrt(3) * X_MASK),
            Dot((np.sqrt(3)-3.5) * X_MASK),
        )
        dot_pair.set_fill(YELLOW, 0)

        dot_pair.save_state()
        dot_pair.shift(0.5*UP)
        dot_pair.set_fill(opacity = 1)

        self.play(MoveFromSaved(dot_pair))

        double_arrow = DoubleArrow(*dot_pair, color = WHITE)
        rat_desc = TextMobject("rational").next_to(double_arrow, UP)
        #self.wait_to(9)
        self.play(
            ShowCreation(double_arrow),
            FadeIn(rat_desc),
        )
        #self.wait_to(12.5)

        denom = 6
        nominators = range(-1-int((SPACE_WIDTH+2)*denom), int((SPACE_WIDTH+2)*denom)+2)
        zero_i = nominators.index(0)
        rat_dots_template = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05)
            for nom in nominators
        )

        rat_dots = rat_dots_template.copy()
        rat_dots_label = TexMobject("\\mathbb Q")
        rat_dots_label.next_to(rat_dots, DOWN).to_edge(RIGHT)
        rat_dots_g = VGroup(rat_dots, rat_dots_label)

        rat_dots_g.target = rat_dots_g.copy()
        rat_dots_g.target.to_edge(DOWN)
        rat_dots_g.set_fill(opacity = 0)

        self.play(MoveToTarget(rat_dots_g))

        real_sample = Dot(np.sqrt(2)*X_MASK, color = YELLOW)
        sample_label = TexMobject("\\sqrt2").next_to(real_sample, DOWN)
        sample_label.highlight(YELLOW)
        #self.wait_to(20)
        self.play(
            ApplyMethod(real_sample.shift, 0.2*DOWN, rate_func = there_and_back),
            FadeIn(sample_label)
        )
        #self.wait_to(24)

        shifted_label = TexMobject("\\sqrt 2"," + \\mathbb Q")
        shifted_label[0].highlight(YELLOW)
        shifted_label.next_to(rat_dots, UP, buff = 0.5)
        shifted_label.to_edge(RIGHT)

        shifted_dots = rat_dots_template.copy().shift(np.sqrt(2)*RIGHT)
        shifted_dots.target = shifted_dots.copy()
        shifted_dots.target.next_to(shifted_label, UP, coor_mask = Y_MASK)
        shifted_dots.target[zero_i].highlight(YELLOW)

        shifted_dots.set_fill(opacity = 0)
        shifted_dots.submobjects[zero_i] = real_sample

        self.play(
            MoveToTarget(shifted_dots),
            FadeIn(VGroup(shifted_label[1:])),
            ReplacementTransform(sample_label, shifted_label[0]),
        )
        #self.wait_to(27)

        self.play(FadeOut(VGroup(dot_pair, double_arrow, rat_desc)))

        rnd_dots = rat_dots_template.copy()
        rnd_dots.shift(np.random.random() * RIGHT)
        rnd_dots.target = rnd_dots.copy()
        rnd_dots.target.shift(set_shift)
        rnd_dots.set_fill(opacity = 0)
        self.play(
            MoveToTarget(rnd_dots),
        )

        brace = Brace(Line(ORIGIN, RIGHT), UP)
        brace.next_to(rnd_dots, UP, coor_mask = Y_MASK, buff = 0)

        all_dots = VGroup(rat_dots, shifted_dots, rnd_dots).family_members_with_points()
        self.play(GrowFromCenter(brace))
        for dot in all_dots:
            x = dot.get_center()[0]
            if x < 0 or x > 1:
                dot.set_fill(opacity = 0.3)

        #self.wait_to(34.5)

        def dots_choice(dots):
            result = random.choice([dot for dot in dots if dot.fill_opacity > 0.5])
            all_dots.remove(result)
            dots.remove(result)
            return result

        rnd_dots_c = dots_choice(rnd_dots)
        rat_dots_c = dots_choice(rat_dots)
        shifted_dots_c = dots_choice(shifted_dots)

        representants = VGroup(rnd_dots_c, shifted_dots_c, rat_dots_c)

        for dot in representants:
            dot.highlight(ORANGE)
            self.play(ApplyMethod(dot.shift, 0.3*UP), rate_func = there_and_back)

        #self.wait_to(34.5)
        self.dither()

        centers = [dot.get_center() for dot in representants]+[SPACE_HEIGHT*DOWN]
        for y in (interpolate(centers[0], centers[1], 0.5),
                  interpolate(centers[1], centers[2], 0.33),
                  interpolate(centers[1], centers[2], 0.66),
                  interpolate(centers[2], centers[3], 0.5)):
            representants.add(Dot(
                np.random.random()*RIGHT + y*Y_MASK,
                color = ORANGE, radius = 0.05,
                fill_opacity = 0,
            ))

        representants.save_state()

        for dot in representants:
            dot.set_fill(opacity = 1)
            dot.move_to(set_shift, coor_mask = Y_MASK)

        self.play(
            FadeOut(VGroup(brace, all_dots,
                           rat_dots_label, shifted_label)),
            MoveFromSaved(representants),
        )

        repr_label = TexMobject('R').highlight(ORANGE).next_to(representants, UP)
        self.play(Write(repr_label))

        #self.wait_to(42)
        self.play(FadeOut(classes_desc))

        #print([dot.get_center()[0] for dot in representants])

repr_x = [ # exported from previous scene
    0.87191077205623502,
    0.41421356237309515,
    0.33333333333333331,
    0.98231661040877083,
    0.013807249315600956,
    0.74240660026476424,
    0.038358018161719909
]

class TranslateDisjoint(Scene):
    def construct(self):

        title = TextMobject("Unmeasurable set").to_edge(UP)
        reals = NumberLine()

        denom = 6
        nominators = range(-1-int((SPACE_WIDTH+2)*denom), int((SPACE_WIDTH+2)*denom)+2)
        nominators.remove(0)
        dots_template = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05, color = DARK_GRAY)
            for nom in nominators
        )

        repr_dots = VGroup(
            Dot(x * X_MASK, radius = 0.05, color = ORANGE)
            for x in sorted(repr_x)
        ).shift(set_shift)
        repr_label = TexMobject("R").next_to(repr_dots, UP).highlight(ORANGE)

        self.add(title, reals, repr_dots, repr_label)

        sample1 = repr_dots[-2].copy()
        sample2 = repr_dots[-1].copy()

        self.play(
            sample1.shift, 1*DOWN,
            sample2.shift, 2*DOWN,
        )

        dots1 = dots_template.copy().shift(sample1.get_center())
        dots2 = dots_template.copy().shift(sample2.get_center())
        
        goal = 3
        approx = VGroup(
            min(dots, key = lambda dot: abs(goal - dot.get_center()[0]))
            for dots in (dots1, dots2)
        ).copy().highlight(ORANGE)

        #self.wait_to(3.5)
        self.play(
            FadeIn(dots1),
            ReplacementTransform(sample1.copy(), approx[0], path_arc = -np.pi/10),
        )
        self.play(
            FadeIn(dots2),
            ReplacementTransform(sample2.copy(), approx[1], path_arc = np.pi/10),
        )

        #self.wait_to(7)
        neq = TexMobject("\\neq").move_to(approx)
        self.play(Write(neq))

        #self.wait_to(17)

        copies = VGroup(repr_dots.copy() for _ in range(2))
        copies[0][-2].highlight(YELLOW)
        copies[1][-1].highlight(YELLOW)
        copies.save_state()

        copies[0].next_to(sample1, UP, buff = 0.2, coor_mask = Y_MASK)
        copies[1].next_to(sample2, DOWN, buff = 0.2, coor_mask = Y_MASK)

        self.play(MoveFromSaved(copies))

        copies2 = copies.copy()

        for dots, sample, apr in zip(copies2, (sample1, sample2), approx):
            dots.save_state()
            dots.shift(apr.get_center() - sample.get_center())

        #self.wait_to(20)
        self.play(MoveFromSaved(copies2[0]))
        self.play(MoveFromSaved(copies2[1]))

        def hl_set(dots):
            dots_hl = VGroup(
                dot.copy().scale_in_place(1.5)
                for dot in dots
            )
            dots_hl.highlight(YELLOW)
            dots_ori = dots.copy()
            self.play(Transform(
                dots, dots_hl,
                submobject_mode = "one_at_a_time",
            ))
            self.play(Transform(
                VGroup(dots), VGroup(dots_ori),
                submobject_mode = "one_at_a_time",
            ))

        #self.wait_to(28)
        hl_set(copies2[0])
        hl_set(copies2[1])

        #self.wait_to(33)
        self.play(FadeOut(VGroup(
            dots1, dots2, sample1, sample2,
            approx, neq,
            copies, copies2,
        )))

class MeasureContradiction(Scene):
    def construct(self):

        title = TextMobject("Unmeasurable set").to_edge(UP)
        reals = NumberLine()

        denom = 6
        nominators = range(-1-int((SPACE_WIDTH+2)*denom), int((SPACE_WIDTH+2)*denom)+1)
        zero_i = nominators.index(0)
        dots_template = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05, color = DARK_GRAY)
            for nom in nominators
        )

        repr_dots = VGroup(
            Dot(x * X_MASK, radius = 0.05, color = ORANGE)
            for x in sorted(repr_x)
        ).shift(set_shift)
        repr_label = TexMobject("R").next_to(repr_dots, UP).highlight(ORANGE)

        self.add(title, reals, repr_dots, repr_label)

        rat_dots = dots_template.copy().highlight(GREY)
        small_rats = VGroup(rat_dots[zero_i : zero_i+denom+1])
        small_rats.highlight(YELLOW)
        rat_dots_label = TexMobject("\\mathbb Q")
        rat_dots_label.next_to(rat_dots, DOWN).to_edge(RIGHT)
        rat_dots_g = VGroup(rat_dots, rat_dots_label)
        rat_dots_g.to_edge(DOWN)
        #self.wait_to(5.5)
        self.play(ShowCreation(rat_dots), FadeIn(rat_dots_label))

        brace = BraceDesc(small_rats, "\\aleph_0", UP, buff = 0.1)
        self.play(brace.creation_anim())
        #self.wait_to(10.5)
        self.play(brace.shift_brace, rat_dots)

        r_copies = VGroup(repr_dots.copy() for _ in small_rats)
        for dots, dot in zip(r_copies, small_rats):
            dots.x = dot.get_center()[0]
            dots.shift(dots.x * DOWN)

        r_copies.shift(DOWN)

        #self.wait_to(15)
        self.play(
            FadeOut(brace),
        )
        brace = BraceDesc(r_copies, "\\aleph_0", LEFT)
        self.play(
            brace.creation_anim(),
            FadeIn(r_copies),
        )
        #self.wait_to(24)

        r_copies.save_state()
        for dots in r_copies: dots.shift(dots.x * RIGHT)
        self.play(MoveFromSaved(r_copies))

        #self.wait_to(29)
        r_copies.save_state()
        center = r_copies.get_center()
        for dots in r_copies: dots.move_to(center, coor_mask = Y_MASK)
        self.play(MoveFromSaved(r_copies))

        #self.wait_to(32)
        lt_2_label = TexMobject("\leq 2").next_to(r_copies, UP)
        self.play(Write(lt_2_label))
        self.dither(2)

        #self.wait_to(41)
        r_copies_col = VGroup(repr_dots.copy() for _ in rat_dots)
        start_x = r_copies[0].x
        end_x = r_copies[-1].x
        ori_y = repr_dots.get_center()[1]
        start_y = reals.get_edge_center(DOWN)[1] - ori_y
        end_y = rat_dots.get_edge_center(DOWN)[1] + 0.2 - ori_y
        y_coor = np.linspace(start_y, end_y, len(r_copies_col))

        for dots, y in zip(r_copies_col, y_coor):
            dots.shift(y*Y_MASK)

        r_copies_dest = r_copies_col.copy()
        x_coor = np.linspace(start_x, end_x, len(r_copies_col))
        for dots, x in zip(r_copies_dest, x_coor):
            dots.shift(x*X_MASK)

        brace2 = BraceDesc(r_copies_dest, "\\aleph_0", LEFT)
        brace2.move_to(brace, coor_mask = X_MASK)
        self.play(
            FadeOut(lt_2_label),
            Transform(brace, brace2),
            ReplacementTransform(r_copies, r_copies_dest),
        )
        r_copies = r_copies_dest

        #self.wait_to(45.5)
        r_copies_dest = r_copies_col.copy()
        x_coor = [dot.get_center()[0] for dot in rat_dots]
        x_coor.sort(key = lambda x: (x % 2, x))
        for dots, x in zip(r_copies_dest, x_coor):
            dots.shift(x*X_MASK)

        self.play(
            ApplyMethod(VGroup(rat_dots[zero_i+denom+1:]).highlight, YELLOW, submobject_mode = "one_at_a_time"),
            ApplyMethod(VGroup(reversed(rat_dots[:zero_i])).highlight, YELLOW, submobject_mode = "one_at_a_time"),
        )

        #self.wait_to(47.5)
        self.play(
            FadeOut(brace),
            Transform(r_copies, r_copies_dest),
        )

        shift_approx = -4.5
        shift_index, shift_dot = min(
            enumerate(rat_dots),
            key = lambda (i,dot): abs(dot.get_center()[0] - shift_approx),
        )

        shift = X_MASK * shift_dot.get_center()
        copy_index = x_coor.index(shift_dot.get_center()[0])
        x_in_r = 4
        x = r_copies[copy_index][x_in_r].get_center()[0]
        x_repr = repr_dots[x_in_r].get_center()[0]
        x_dot = Dot(x * X_MASK, color = YELLOW)
        x_label = TexMobject('x').next_to(x_dot, UP)
        x_dot.save_state()
        x_dot.shift(LEFT)
        x_dot.set_fill(opacity = 0)

        #self.wait_to(60+10.5)
        self.play(x_dot.restore, FadeIn(x_label))

        #self.wait_to(60+15)

        x_class = dots_template.copy().shift(x_repr * X_MASK)
        x_class.next_to(repr_label, UP, coor_mask = Y_MASK)

        x_label.save_state()
        x_label.next_to(x_class[shift_index], UP)
        self.play(
            FadeIn(x_class),
            MoveFromSaved(x_label),
            Transform(x_dot, x_class[shift_index].copy().highlight(YELLOW)),
        )
        #self.wait_to(60+17.5)

        x_class[zero_i].highlight(YELLOW)
        self.play(x_class[zero_i].shift, 0.2*UP, rate_func = there_and_back)
        dot = x_class[zero_i].copy()
        dot_dest = repr_dots[x_in_r].copy().highlight(YELLOW)
        self.play(Transform(dot, dot_dest))
        self.remove(dot)
        repr_dots[x_in_r].highlight(YELLOW)

        #self.wait_to(60+24)

        repr_copy_x = repr_dots.copy()
        self.play(repr_copy_x.shift, shift)

        rect = SurroundingRectangle(r_copies[copy_index])
        #self.wait_to(60+30)
        self.play(
            ShowCreation(rect),
            r_copies[copy_index][x_in_r].highlight, YELLOW,
        )

        self.dither(2)
        #self.wait_to(60+37)

class FindingCause(Scene):
    def construct(self):

        title = TextMobject("What to blame?").to_edge(UP)
        self.play(FadeIn(title, submobject_mode = "lagged_start"))

        #self.wait_to(5)
        conversation = Conversation(self)
        conversation.add_bubble("The countable decomposition")
        self.dither(2)
        self.add_foreground_mobjects(conversation.dialog)

        rec_set = []
        holes = [(-3.,3.)]
        seg_len = 2.
        rec_set_layers = 6

        for _ in range(rec_set_layers):
            next_holes = []
            for a,b in holes:
                center = (a+b)/2
                c = center - seg_len/2
                d = center + seg_len/2
                next_holes += [(a,c), (d,b)]
                rec_set.append(Line(c*X_MASK, d*X_MASK))
            holes = next_holes
            seg_len /= 4

        rec_set = VGroup(rec_set)
        rec_set.shift(UP).highlight(YELLOW)

        self.play(FadeIn(rec_set))

        rec_set.save_state()
        rec_set.arrange_submobjects(DOWN, center = False, coor_mask = Y_MASK)

        self.play(MoveFromSaved(rec_set, run_time = 1))

        rec_set_folded = []
        for i in range(rec_set_layers):
            start = 2 - 2.0**(2-i)
            end = 2 - 2.0**(2-(i+1))
            points = np.linspace(start, end, 2**i + 1)
            for p0, p1 in zip(points, points[1:]):
                rec_set_folded.append(Line(p0*X_MASK, p1*X_MASK))

        rec_set_folded = VGroup(rec_set_folded)
        rec_set_folded.shift(UP).highlight(YELLOW)

        rec_set_folded_in_rows = rec_set_folded.copy()
        rec_set_folded_in_rows.arrange_submobjects(DOWN, center = False, coor_mask = Y_MASK)

        self.play(ReplacementTransform(rec_set, rec_set_folded_in_rows))
        self.play(ReplacementTransform(rec_set_folded_in_rows, rec_set_folded))

        denom = 6
        nominators = range(-1-int((SPACE_WIDTH+2)*denom), int((SPACE_WIDTH+2)*denom)+1)
        zero_i = nominators.index(0)
        dots = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05, color = DARK_GRAY)
            for nom in nominators
        )
        dots.highlight(GREY)
        VGroup(dots[zero_i : zero_i+denom+1]).highlight(YELLOW)

        self.play(ShowCreation(dots))

        #self.wait_to(19)
        self.play(FadeOut(rec_set_folded), FadeOut(dots))
        conversation.add_bubble("But there is the Banach-Tarski paradox.")

        banach_tarski_pic = ImageMobject("vsauce-banach-tarski.png")
        banach_tarski_pic.scale(1./3)
        banach_tarski_label = TextMobject("The Banach–Tarski Paradox\\\\(Vsauce)")
        banach_tarski_label.scale(0.7)
        banach_tarski_label.next_to(banach_tarski_pic, RIGHT)
        banach_tarski = VGroup(banach_tarski_pic, banach_tarski_label)
        banach_tarski.next_to(conversation.dialog, UP)
        #self.wait_to(21)
        self.play(UnapplyMethod(banach_tarski.behind_edge, RIGHT))

        #self.wait_to(42.5)
        self.dither(2)
        self.play(
            FadeOut(VGroup(banach_tarski_label, conversation.dialog)),
            FadeOut(banach_tarski_pic),
        )

        conversation = Conversation(self)
        conversation.add_bubble("So the Axiom of Choice?")
        self.dither(2)
        #self.wait_to(47)
        conversation2 = Conversation(self, start_answer = True)
        conversation2.add_bubble("Or just bad intuition.")
        self.dither(2)
        #self.wait_to(53)

class ChoiceStatus(Scene):
    def construct(self):

        title = TextMobject("Axiom of Choice").to_edge(UP)
        self.add(title)
        items = VGroup(
            TextMobject("$\\bullet$ used to be controversial,"),
            TextMobject("$\\bullet$ independent of other axioms"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT, buff = 0.4)
        items.next_to(title, DOWN, buff = 0.5).to_edge(LEFT)

        self.play(FadeIn(items[0], submobject_mode = "lagged_start"))
        #self.wait_to(12)

        stamp_text = TextMobject("Proven")
        stamp_rect = SurroundingRectangle(stamp_text, buff = 0.2)
        stamp_bg = BackgroundRectangle(stamp_rect)
        stamp = VGroup(stamp_bg, stamp_rect, stamp_text)
        stamp.set_color(RED)
        stamp.rotate(np.pi*0.1)
        stamp.next_to(items[1])
        stamp.shift(1.3*LEFT + 0.25*DOWN)

        self.play(
            FadeIn(items[1], submobject_mode = "lagged_start"),
        )
        self.play(
            FadeInZoomOut(stamp, about_point = stamp.get_center()),
        )
        #self.wait_to(34.5)

        chapter14 = importlib.import_module('eost.14-formal-recursion-cz')
        make_jumps = chapter14.make_jumps

        jumps = make_jumps(3, -4)
        line = Line(4.5*LEFT, 4.5*RIGHT, color = DARK_GREY)
        jumps_g = VGroup(line, jumps)
        jumps_g.shift(2*DOWN)

        self.play(ShowCreation(line))
        for i in range(14): self.play(ShowCreation(jumps[i], run_time = 0.5))
        self.play(ShowCreation(VGroup(jumps[i+1:])))

        self.dither(2)
        #self.wait_to(51.5)
