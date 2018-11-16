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
        self.dither()

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
        self.play(ShowCreation(grid))

        self.play(UnapplyMethod(prisoners.behind_edge, DOWN))

        self.dither(2)

        self.play(
            FadeOut(grid),
            prisoners.behind_edge, DOWN,
        )

        prisoners, labels = make_prisoners()
        self.play(UnapplyMethod(prisoners.behind_edge, DOWN))

        eye_cone = prisoners[2].eye_cone()
        hidden_hats = VGroup(p.hat for p in prisoners[:3])
        hidden_hats.save_state()
        self.play(
            ShowCreation(eye_cone[0]),
            ShowCreation(eye_cone[1]),
            hidden_hats.set_fill, BLACK,
        )

        self.play(ShowCreation(labels))
        
        self.dither()

        self.play(
            FadeOut(eye_cone),
            hidden_hats.restore,
        )

        bubbles = VGroup(p.bubble for p in prisoners)
        bubbles.save_state()

        for p in prisoners: p.show_bubble(random.choice((YELLOW, BLUE)))
        self.play(
            MoveFromSaved(bubbles)
        )

        self.dither(2)

        rules = VGroup(
            TextMobject("Konečně chyb $\Rightarrow$ všichni volní"),
            TextMobject("Nekonečně chyb $\Rightarrow$ všichni mrtví"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        rules.next_to(king).to_edge(UP)

        self.play(FadeIn(rules[0], submobject_mode = "lagged_start", run_time = 2))
        self.play(FadeIn(rules[1], submobject_mode = "lagged_start", run_time = 2))

        self.dither()

        def rate_func(x):
            x *= np.pi*5
            return np.abs(np.sin(x))

        self.play(ApplyMethod(VGroup(head, crown).shift, 0.2*DOWN, run_time = 3, rate_func = rate_func))

        self.dither()

        one_half = TexMobject("\\frac12")
        self.play(Write(one_half))

        self.dither(2)

        self.play(
            king.behind_edge, LEFT,
            #VGroup(labels, prisoners).behind_edge, DOWN,
            FadeOut(VGroup(bubbles, rules, one_half)),
            VGroup(p.hat for p in prisoners).set_fill, BLACK,
        )

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
        self.play(
            ShowCreation(eye_cone[0]),
            ShowCreation(eye_cone[1]),
            VGroup(hats[index+1:], fill_opacity = 0.5).set_fill, BLUE,
        )

        prisoner.bubble.save_state()
        prisoner.show_bubble(BLUE)
        self.play(MoveFromSaved(prisoner.bubble))
        
        bubbles = VGroup(p.bubble for p in prisoners[index+1:])
        bubbles.save_state()
        for p in prisoners[index+1:]: p.show_bubble(BLUE)

        self.play(MoveFromSaved(bubbles, submobject_mode = "one_at_a_time"))

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
        self.add(prisoners, labels)

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

        self.play(seq.restore)
        self.dither()
        self.play(Transform(seq, seq_ordinal))
        self.dither()

        big_rect = Rectangle(width = 1.9*SPACE_WIDTH, height = 1.9*SPACE_HEIGHT)
        self.play(
            ShowCreation(big_rect),
            VGroup(prisoners, labels).behind_edge, DOWN,
        )
        self.dither()

        seq.save_state()
        seqs = VGroup(
            (OrdinalOmega(), OrdinalOmega()),
            (OrdinalOmega(), seq),
        )
        for bar in seqs[0][0]: bar.highlight(random.choice((YELLOW, BLUE)))
        seqs[0][1].highlight(BLUE)
        for i, bar in enumerate(seqs[1][0]): bar.highlight((BLUE, YELLOW)[i%2])
        seqs.scale(0.7)
        for row in seqs:row.arrange_submobjects()
        seqs.arrange_submobjects(DOWN)
        seqs.next_to(big_rect.get_corner(LEFT+UP), DOWN+RIGHT, buff = 0.5)

        self.play(
            MoveFromSaved(seq),
            FadeIn(seqs[0]),
            FadeIn(seqs[1][0]),
        )
        self.dither()

        seqs = VGroup(seqs[0][0], seqs[1][0], seqs[0][1], seqs[1][1])
        classes = VGroup(SurroundingRectangle(seq, buff = 0, color = GREEN) for seq in seqs)
        seqs.save_state()
        for seq in seqs: seq.scale_in_place(np.array((0.9, 0.8, 1)))
        self.play(
            MoveFromSaved(seqs),
            FadeIn(classes),
        )

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
        self.play(ShowCreation(edge))
        self.play(ShowCreation(arrow))

        dots = VGroup(dot_r_comp(color = GREEN) for _ in seqs)
        dots.arrange_submobjects(buff = 1)
        dots.next_to(big_rect.get_edge_center(UP), DOWN, buff = 1)

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

        self.dither()

        self.seqs = seqs
        self.dots = dots

        #self.expand_dot(3)
        #self.hide_dot()
