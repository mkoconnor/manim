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
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 13\\\\Axiom výběru",
    }

class Chapter13OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Axiom výběru potřebujeme k tomu, abychom si z~nekonečně mnoho párů ponožek mohli vzít nekonečně mnoho ponožek, ale ne nekonečně mnoho párů.",
        ],
        "author" : "Bertrand Russell"
    }

class AxiomRecallSelExt(Scene):
    def construct(self):

        title = TextMobject("Axiomy").to_edge(UP)
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

        selection_title = TextMobject("Vydělení").next_to(rect, UP)

        self.play(
            Write(selection_title),
            ShowCreation(rect),
            FadeIn(dots),
        )
        self.play(ShowCreation(icons))
        self.dither()

        subset_dots.save_state()
        subset_dots.shift(1.5*DOWN)
        subset_rect = SurroundingRectangle(subset_dots, buff = 0.3)

        self.play(MoveFromSaved(subset_dots))
        self.play(ShowCreation(subset_rect))

        self.dither()

        subset = VGroup(subset_dots, subset_rect)
        subset2 = subset.copy()
        subset2_dots, subset2_rect = subset2
        subset2_dots.save_state()
        subset2.shift(1.5*DOWN)

        subsets = VGroup(subset, subset2)
        eq = TexMobject('=').move_to(subsets)
        ext_title = TextMobject("Extensionalita").next_to(subsets)
        
        self.play(FadeIn(ext_title, submobject_mode = "lagged_start"))
        self.play(MoveFromSaved(subset2_dots))
        self.play(ShowCreation(subset2_rect))
        self.play(Write(eq))

        self.dither(2)
        
        self.play(FadeOut(VGroup(
            subsets, eq,
            dots, rect, icons,
            ext_title, selection_title,
        )))

chapter4 = importlib.import_module('eost.04-well-ordering')

class AxiomRecallBigSet(Scene):
    def construct(self):

        title = TextMobject("Axiomy").to_edge(UP)
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
        inf_ax = TextMobject("Nekonečno").next_to(nat_rect, DOWN, aligned_edge = LEFT)
        VGroup(naturals, nat_rect, inf_ax).to_corner(DOWN+LEFT)

        self.play(
            FadeIn(inf_ax),
            FadeIn(naturals, submobject_mode = "lagged_start"),
            ShowCreation(nat_rect),
        )

        self.dither()

        self.play(ReplacementTransform(nat_rect.copy(), p_powers[0]))
        self.play(ShowCreation(omega[0]))
        #self.add(omega, p_powers)

        powerset_ax = TextMobject("Potenční množina").next_to(p_powers[0], UP, buff = 0.5)
        powerset_ax.to_edge(LEFT)

        self.play(FadeIn(powerset_ax))

        self.play(ReplacementTransform(p_powers[0][0].copy(), p_powers[1][-2]))
        self.play(
            Write(VGroup(p_powers[1][:-2], p_powers[1][-1])),
            ShowCreation(omega[1]),
        )
        for i in range(2,4):
            self.play(
                ShowCreation(omega[i]),
                FadeIn(VGroup(p_powers[i][:2], p_powers[i][-1])),
                ReplacementTransform(p_powers[i-1].copy(), VGroup(p_powers[i][2:-1])),
            )
        self.play(
            ShowCreation(VGroup(omega[i+1:])),
            ShowCreation(VGroup(p_powers[i+1:])),
        )
        self.dither()

        replacement_ax = TextMobject("Nahrazení")
        replacement_ax.next_to(powerset_ax.get_corner(DOWN+LEFT), UP+RIGHT)
        replacement_ax.save_state()
        powerset_ax.save_state()
        powerset_ax.shift(UP)
        powerset_ax.set_fill(opacity = 0)
        replacement_ax.shift(DOWN)
        replacement_ax.set_fill(opacity = 0)

        self.play(replacement_ax.restore, MoveFromSaved(powerset_ax))

        self.dither()
        rect = SurroundingRectangle(VGroup(p_powers, omega[-1].copy().scale_in_place(0)), color = GREEN)
        
        self.play(ReplacementTransform(nat_rect, rect))

        union_bar = omega[0].copy().highlight(YELLOW)
        union_label = TextMobject("Sjednocení").highlight(YELLOW).next_to(union_bar, UP)
        VGroup(union_bar, union_label).next_to(rect, coor_mask = X_MASK)

        union_src = []
        for p_power in p_powers: union_src += p_power.submobjects
        union_src = VGroup(union_src).copy()
        self.play(ReplacementTransform(union_src, union_label))

        self.play(ShowCreation(union_bar))

        self.dither(2)
        self.play(FadeOut(VGroup(
            naturals, inf_ax,
            omega, p_powers, rect,
            replacement_ax, union_bar, union_label,
        )))

class AxiomChoiceIntro(Scene):
    def construct(self):

        self.force_skipping()
        title = TextMobject("Axiomy").to_edge(UP)
        self.add(title)

        regularity_ax = TextMobject("Fundovanost")
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
        
        choice_ax = TextMobject("Axiom výběru").next_to(sets_rect, UP)
        chosen = VGroup(random.choice(dots) for (dots, rect) in subsets)

        chosen_circ = VGroup(
            Circle(color = GREEN, radius = 0.2).shift(dot.get_center())
            for dot in chosen
        )

        self.play(Write(choice_ax))
        self.play(ShowCreation(sets_rect))
        self.play(FadeIn(subsets, submobject_mode = "lagged_start"))
        self.dither()
        self.play(ShowCreation(chosen_circ))

        self.dither()

        chosen2 = chosen.copy()
        chosen2.save_state()
        chosen2.arrange_submobjects(DOWN, buff = 0.5)
        chosen2.next_to(sets_rect, buff = 0.8)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.3, color = YELLOW)

        self.play(MoveFromSaved(chosen2))
        self.play(ShowCreation(chosen_rect))

        self.dither()
        self.play(FadeOut(VGroup(regularity_ax, omega_rects, cross)))

        AC_desc = TextMobject("Lze provést\\\\","nekonečně mnoho\\\\","nahodilých výběrů\\\\","najednou.",
                              alignment = "\\hsize = 0.4\\hsize\\raggedright")
        AC_desc.next_to(ORIGIN).shift(0.5*UP)
        self.play(Write(AC_desc))
        self.dither()
        self.play(FocusOn2(AC_desc[1]))
        self.play(FocusOn2(AC_desc[2]))

        self.dither()
        self.play(FadeOut(VGroup(chosen2, chosen_rect, chosen_circ)))

        chosen2_center = chosen2.get_center()
        chosen2 = VGroup(chosen[0].copy())
        chosen2.save_state()
        chosen2.move_to(chosen2_center, coor_mask = X_MASK)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.25, color = YELLOW)
        chosen_set = VGroup(chosen2, chosen_rect)

        self.play(MoveFromSaved(chosen2, path_arc = -0.3*np.pi))
        self.play(ShowCreation(chosen_rect))

        self.revert_to_original_skipping_status()

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

        self.dither()

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

        self.play(ShowCreation(chosen_circ, submobject_mode = "all_at_once"))
        self.play(MoveFromSaved(chosen2))
        self.dither()

        AC_desc.save_state()
        self.play(AC_desc.to_edge, DOWN)

        replacement_ax = TextMobject("Axiom nahrazení").move_to(choice_ax)
        chosen_rect = SurroundingRectangle(chosen2, buff = 0.3, color = YELLOW)
        replacement_ax.next_to(chosen_rect, buff = 0.5, aligned_edge = UP)
        replacement_rule = TextMobject("Pravidlo").next_to(replacement_ax, DOWN)
        replacement_rule.highlight(YELLOW)

        self.play(FadeIn(replacement_ax))
        self.play(Write(replacement_rule))
        self.dither()

        self.play(ReplacementTransform(sets_rect.copy(), chosen_rect))

        self.dither(2)

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
            FadeOut(VGroup(replacement_ax, replacement_rule)),
            AC_desc.restore,
        )

        conversation = Conversation(self)
        conversation.add_bubble("Takže výsledek axiomu výběru vypadá náhodně?")

class Prisoner(SVGMobject):
    CONFIG = {
        "initial_scale_factor" : 0.05,
        "file_name" : "prisoner",
        "hat_color" : None,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.eye.set_style_data(stroke_width = 0, stroke_color = WHITE,
                                fill_color = WHITE, fill_opacity = 1)
        if self.hat_color is None:
            self.hat_color = random.choice((BLUE, YELLOW))
        self.hat.set_style_data(
            stroke_width = DEFAULT_POINT_THICKNESS,
            fill_opacity = 0.5,
            fill_color = self.hat_color,
        )
        self.hide_bubble()

    def hide_bubble(self):
        self.bubble.scale_about_point(np.array([0.1,-0.1, 1]), self.bubble_tip)
        self.bubble.set_style_data(fill_opacity = 0, stroke_width = 0)

    def show_bubble(self, color):
        self.bubble.scale_about_point(np.array([10,-10, 1]), self.bubble_tip)
        self.bubble.set_style_data(
            fill_opacity = 0.5, fill_color = color,
            stroke_width = DEFAULT_POINT_THICKNESS,
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

        title = TextMobject("Příklady").to_edge(UP)
        self.add(title)

        prisoners = VGroup(Prisoner() for _ in range(5)).arrange_submobjects()
        prisoners.shift(UP)
        hats_title = TextMobject("Klobouky").next_to(prisoners, UP, aligned_edge = LEFT)

        unm_line = DashedLine(LEFT, RIGHT, color = "#FF00FF")
        unm_brace = BraceText(unm_line, "?", UP)
        unm_title = TextMobject("Neměřitelná množina")
        unmeasurable = VGroup((unm_line, unm_brace), unm_title)
        unmeasurable.arrange_submobjects(RIGHT, buff = 0.5).shift(DOWN)

        self.play(
            FadeIn(prisoners, submobject_mode = "lagged_start"),
        )
        self.dither()

        self.play(
            ShowCreation(unm_line),
            unm_brace.creation_anim(),
        )
        self.dither()

        self.play(
            FadeIn(hats_title, submobject_mode = "lagged_start"),
        )
        self.play(FadeIn(unm_title, submobject_mode = "lagged_start", run_time = 2))

        self.dither(2)

        self.play(FadeOut(VGroup(title, prisoners, hats_title, unmeasurable)))

class PrisonersTale(Scene):
    def construct(self):

        
