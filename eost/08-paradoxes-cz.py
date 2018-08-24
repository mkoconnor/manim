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
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.chat_bubbles import Conversation, ChatBubble

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic

import importlib

class Chapter8OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 8\\\\ Paradoxy a formální teorie",
    }

class Chapter8OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Není náhoda, že se","všichni slavní logici","zbláznili."
        ],
        "highlighted_quote_terms" : {
            "všichni slavní logici" : GREEN,
        },
        "author" : "Pavel Paták"
    }

class LargeOrdinalsScene(Scene):
    def construct(self):

        num = 5
        ordinals_cnt_base = OrdinalFiniteProd(OrdinalOmega, num, x1 = -4+num*2.5)

        ordinals_cnt = VGroup([
            VGroup(ordinals_cnt_base[:i]).copy()
            for i in range(1,num+1)
        ])
        ordinals_cnt.save_state()
        ordinals_cnt.arrange_submobjects(DOWN, center = False, coor_mask = Y_MASK)
        ordinals_cnt.to_edge(UP)

        self.play(ShowCreation(ordinals_cnt))

        self.dither()
        self.play(ordinals_cnt.restore)

        self.remove(ordinals_cnt)
        self.add(ordinals_cnt_base)

        omega1 = Omega1()
        brace = BraceDesc(omega1, "\\omega_1", DOWN)

        omega1.line.save_state()
        omega1.line.behind_edge(RIGHT)

        omega1_bars_src = make_ordinal_power(2)
        omega1_bars_src.next_to(ordinals_cnt_base)
        omega1_bars_src.add_to_back(*ordinals_cnt_base)

        brace.desc.highlight(BLUE)
        brace.save_state()
        brace.shift_brace(omega1_bars_src)
        brace.highlight(BLACK)

        self.play(
            brace.restore,
            omega1.line.restore,
            ReplacementTransform(omega1_bars_src, omega1.bars),
        )

        self.dither()

        aleph1 = TexMobject("\\aleph_1","=|","\omega_1","|")
        aleph1[2].highlight(BLUE)
        aleph1[0].highlight(RED)
        aleph1.shift(brace.desc.get_center() - aleph1[2].get_center())
        aleph1.remove(aleph1[2])

        self.play(Write(aleph1))

        ordinals_a1 = VGroup([omega1.copy() for _ in range(num)])
        
        aleph1[0].save_state()
        aleph1[0].next_to(omega1, LEFT, coor_mask = X_MASK)
        self.play(
            omega1.to_edge, UP,
            FadeOut(VGroup(brace, aleph1[1:])),
            MoveFromSaved(aleph1[0]),
        )
        aleph1 = aleph1[0]

        scale_center = np.array(ordinals_a1[0].line.get_start())
        for i,o in enumerate(ordinals_a1):
            o.line.scale(1+i*0.2, about_point = scale_center)

        ordinals_a1_lines_dest = VGroup([o.line for o in ordinals_a1]).copy()
        ordinals_a1_bars_dest = VGroup([o.bars for o in ordinals_a1]).copy()
        ordinals_a1.arrange_submobjects(DOWN, False, coor_mask = Y_MASK)
        ordinals_a1.to_edge(UP)
        ordinals_a1_lines = VGroup([o.line for o in ordinals_a1])
        ordinals_a1_bars = VGroup([o.bars for o in ordinals_a1])

        self.remove(omega1)
        self.add(ordinals_a1[0])
        self.play(FadeIn(VGroup(ordinals_a1[1:])))
        self.play(
            Transform(ordinals_a1_lines, ordinals_a1_lines_dest),
            Transform(ordinals_a1_bars, ordinals_a1_bars_dest),
        )
        self.remove(*ordinals_a1[:-1])
        omega2_src = ordinals_a1[-1]
        omega2 = LongOrdinal(ordinal_end = 0.3, line_start = 0.2)

        brace = BraceDesc(omega2, "\\omega_2", DOWN)
        brace.desc.highlight(BLUE)
        brace.save_state()
        brace.shift_brace(omega2_src)
        brace.highlight(BLACK)

        self.play(
            brace.restore,
            ReplacementTransform(omega2_src, omega2),
        )

        self.dither()

        aleph2 = TexMobject("\\aleph_2","=|","\omega_2","|")
        aleph2[2].highlight(BLUE)
        aleph2[0].highlight(RED)
        aleph2.shift(brace.desc.get_center() - aleph2[2].get_center())
        aleph2.remove(aleph2[2])

        self.play(Write(aleph2))
        self.dither()

        ordinal_fin = OrdinalFinite(7, x1 = SPACE_WIDTH+1).highlight(BLUE)
        ord_labels = VGroup([
            TexMobject("\\omega_{}".format(i+1)).highlight(BLUE).next_to(bar, UP)
            for i,bar in enumerate(ordinal_fin[:4])
        ])
        card_labels = VGroup([
            TexMobject("\\aleph_{}".format(i+1)).highlight(RED).next_to(bar, DOWN)
            for i,bar in enumerate(ordinal_fin[:4])
        ])

        self.play(
            FadeOut(VGroup(aleph2[1:], brace, omega2)),
            ReplacementTransform(aleph1, card_labels[0]),
            ReplacementTransform(aleph2[0], card_labels[1]),
        )

        for i in range(4):
            self.play(FadeIn(ord_labels[i]), ShowCreation(ordinal_fin[i]))
            if i >= 2: self.play(FadeIn(card_labels[i]))

        self.play(ShowCreation(VGroup(ordinal_fin[4:], rate_func = rush_into)))

        omega = OrdinalOmega().highlight(BLUE)
        omega_src = omega.copy()
        omega_src.next_to(ordinal_fin, buff = 1)
        omega_src.add_to_back(*ordinal_fin)

        label1 = VGroup(ord_labels[0], card_labels[0])
        labels_to_fade = VGroup(list(zip(ord_labels[1:], card_labels[1:])))
        labels_to_fade.save_state()
        for l, bar in zip(labels_to_fade, omega[1:4]):
            l.move_to(bar, coor_mask = X_MASK)
            l.highlight(BLACK)

        limit_bar = omega[0].copy().next_to(omega)
        limit_lord = TexMobject("\\omega_\\omega").highlight(BLUE).next_to(limit_bar, UP)
        limit_lcard = TexMobject("\\aleph_\\omega").highlight(RED).next_to(limit_bar, DOWN)
        limit_g = VGroup(limit_bar, limit_lord, limit_lcard)

        limit_g.next_to(omega, coor_mask = X_MASK)
        limit_g.save_state()
        limit_g.next_to(omega_src, coor_mask = X_MASK)

        self.play(
            MoveFromSaved(labels_to_fade),
            ReplacementTransform(omega_src, omega),
            Animation(label1),
            limit_g.restore,
        )
        self.remove(labels_to_fade)

        plus1_bar = limit_bar.copy()
        plus1_label = TexMobject("\\omega_{\\omega+1}").highlight(BLUE).next_to(plus1_bar, UP)
        plus1_g = VGroup(plus1_bar, plus1_label)
        plus1_g.next_to(limit_g, coor_mask = X_MASK, buff = 0.5)

        self.play(FadeIn(plus1_label), ShowCreation(plus1_bar))
        self.dither()

        omega_pow = make_ordinal_power(2, q=(0.8, 0.9, 0.9)).highlight(BLUE)
        omega_pow_src = omega_pow.copy()
        omega_pow_src.behind_edge(RIGHT)
        omega_pow_src[0].add_to_back(limit_bar, plus1_bar)
        omega_pow_src.add_to_back(omega)

        limit_g.remove(limit_bar)
        limit_g.save_state()
        plus1_label.save_state()

        limit_g.move_to(omega_pow[1][0], coor_mask = X_MASK)
        plus1_label.move_to(omega_pow[1][1], coor_mask = X_MASK).highlight(BLACK)

        pow_bar = limit_bar.copy()
        pow_label = TexMobject("\\omega_{\\omega\\cdot\\omega}").highlight(BLUE).next_to(pow_bar, UP)
        pow_g = VGroup(pow_bar, pow_label)
        pow_g.next_to(omega_pow, coor_mask = X_MASK, buff = -.2)
        pow_g.save_state()
        pow_g.next_to(omega_pow_src, coor_mask = X_MASK)

        self.play(
            MoveFromSaved(plus1_label),
            ReplacementTransform(omega_pow_src, omega_pow),
            MoveFromSaved(limit_g),
            pow_g.restore,
        )
        self.remove(plus1_label)

        self.dither()

        labels_to_fade = VGroup(label1, limit_g, pow_label)
        labels_to_fade.save_state()
        labels_to_fade.highlight(BLACK)

        omega1 = Omega1(color = BLUE)
        omega1_bar = pow_bar.copy()
        omega1_label = TexMobject("\\omega_{\\omega_1}").highlight(BLUE).next_to(omega1_bar, UP)
        omega1_g = VGroup(omega1_bar, omega1_label)
        omega1_g.shift(omega1.line.get_end() - omega1_bar.get_center())
        omega1_g.add(omega1.line)
        omega1_g.save_state()
        omega1_g.behind_edge(RIGHT)

        limit_g.move_to(omega1.bars[1][0], coor_mask = X_MASK)
        pow_label.move_to(omega1.bars[-1], coor_mask = X_MASK)
        pow_bar.save_state()
        pow_bar.scale(0)
        pow_bar.set_stroke(width = 0)
        pow_bar.move_to(omega1.bars[-1])

        self.play(
            MoveFromSaved(labels_to_fade, remover = True),
            omega1_g.restore,
            MoveFromSaved(pow_bar, remover = True),
            ReplacementTransform(omega_pow, omega1.bars),
        )
        self.dither()

        ordinal_fin = OrdinalFinite(6, x1 = SPACE_WIDTH+1).highlight(BLUE)
        omega1.save_state()
        omega1.stretch_about_point(0, 0, ordinal_fin[0].get_center())

        labels = VGroup([
            TexMobject((i+1)*"\\omega_{"+"\\omega_1"+(i+1)*"}").next_to(bar, UP)
            for i, bar in enumerate(ordinal_fin[:3])
        ])
        labels.highlight(BLUE)

        next_bar = VGroup(labels[1], ordinal_fin[1])
        next_bar.save_state()
        next_bar.shift(8*RIGHT)

        self.play(
            MoveFromSaved(omega1, remover = True),
            next_bar.restore,
            ReplacementTransform(omega1_label, labels[0]),
            ReplacementTransform(omega1_bar, ordinal_fin[0]),
        )
        self.play(FadeIn(labels[2]), ShowCreation(ordinal_fin[2]))
        self.play(ShowCreation(VGroup(ordinal_fin[3:]), rate_func = rush_into))
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("A co sjednotit všechny ordinály?")
        self.dither()

        self.play(
            FadeOut(VGroup(labels, ordinal_fin)),
            Animation(conversation.dialog)
        )

class CesareBuraltiParadox(Scene):
    def construct(self):

        self.force_skipping()
        conversation = Conversation(self)
        conversation.add_bubble("A co sjednotit všechny ordinály?")
        self.revert_to_original_skipping_status()

        forti_pic = ImageMobject("BuraliForti1.jpg", use_cache = False)
        forti_pic.scale(0.43)
        forti_pic.to_corner(UP+LEFT)

        ordinal_class = OrdinalClass(color = BLUE).shift(UP)
        ordinal_class.next_to(forti_pic, coor_mask = X_MASK)
        num = 7
        subordinals = VGroup([ordinal_class.copy() for _ in range(num)])
        for subord, x in zip(subordinals, np.linspace(0.3, 1, num)):
            i = int(x*len(subord.line))
            subord.line.remove(*subord.line[i:])

        lines_dest = VGroup([subord.line for subord in subordinals]).copy()
        bars_dest = VGroup([subord.bars for subord in subordinals]).copy()
        subordinals.arrange_submobjects(UP, False, coor_mask = Y_MASK)
        subordinals.next_to(conversation.dialog, UP, coor_mask = Y_MASK)
        lines = VGroup([subord.line for subord in subordinals])
        bars = VGroup([subord.bars for subord in subordinals])

        self.play(FadeIn(subordinals))
        self.play(
            Transform(lines, lines_dest),
            Transform(bars, bars_dest),
        )
        self.remove(subordinals)
        self.add(ordinal_class)
        self.dither()
        conversation.add_bubble("Cesare Burali-Forti paradox")

        next_bar = ordinal_class.bars[0][0].copy().next_to(ordinal_class)
        next_bar.highlight(YELLOW)
        self.play(ShowCreation(next_bar))

        brace = BraceText(VGroup(ordinal_class, next_bar), "Nový ordinál", UP)
        self.play(brace.creation_anim())
        self.dither()

        picture = VGroup(ordinal_class, brace, next_bar)
        picture.save_state()
        picture.next_to(forti_pic, coor_mask = X_MASK)

        self.play(FadeIn(forti_pic))

        self.dither()
        self.play(*map(FadeOut, [
            picture,
            conversation.dialog,
            forti_pic,
        ]))

chapter4 = importlib.import_module('eost.04-well-ordering')

class OrdinalsMotivation(Scene):
    def construct(self):

        omega = OrdinalOmega(q=(0.8, 0.9, 0.9))
        omega[0].highlight(GREEN)

        for i in range(4):
            self.play(ShowCreation(omega[i]))

        self.play(ShowCreation(VGroup(omega[i+1:])))

        p_powers = omega.add_descriptions(chapter4.make_p_power,
                                          direction = UP)
        for i,label in enumerate(p_powers):
            label[-i-1].highlight(GREEN)

        self.play(Write(p_powers[0]))
        self.dither()
        self.play(ReplacementTransform(p_powers[0][0].copy(), p_powers[1][-2]))
        self.play(Write(VGroup(p_powers[1][:-2], p_powers[1][-1])))
        self.dither()
        self.play(ShowCreation(VGroup(p_powers[2:])))

        union_bar = omega[0].copy().highlight(YELLOW).next_to(omega)
        union_label = TextMobject("Sjednocení").highlight(YELLOW).next_to(union_bar, UP)

        self.play(ShowCreation(union_bar))
        self.play(ReplacementTransform(
            p_powers.copy(), VGroup(union_label),
        ))
        self.dither()
        self.play(FadeOut(VGroup(
            omega, p_powers, union_bar, union_label
        )))

class AllSetsPicture(SVGMobject):
    CONFIG = {
        "file_name" : "all_sets",
        "unpack_groups" : False,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        rectangles, dots = self
        rectangles.set_style_data(
            stroke_width = DEFAULT_POINT_THICKNESS,
            fill_opacity = 0,
        )
        dots.set_style_data(
            stroke_width = 0,
            fill_opacity = 1,
        )
        dots.submobjects.sort(key = lambda mob: mob.points[0][0]-mob.points[0][1])
        dots.gradient_highlight(RED, BLUE)
        self.scale_to_fit_width(1.8*SPACE_WIDTH)    

        rectangles.submobjects.sort(
            key = lambda mob: mob.get_height() * mob.get_width(),
            reverse = True,
        )

class CantorParadox(Scene):
    def construct(self):

        all_sets = AllSetsPicture()
        rectangles, dots = all_sets
        all_sets_label = TextMobject("Všech","ny"," množin","y", arg_separator = '')
        all_sets_g = VGroup(all_sets_label, all_sets).arrange_submobjects(DOWN)

        self.play(
            FadeIn(rectangles, submobject_mode = "all_at_once"),
            FadeIn(dots, submobject_mode = "lagged_start"),
            run_time = 2,
        )
        self.play(FadeIn(all_sets_label, submobject_mode = "lagged_start"))
        self.add(all_sets_g)
        self.dither()

        union_rect = SurroundingRectangle(rectangles, buff = 0)
        union_label = TextMobject("Sjednocení","všech","množin")
        union_label[0].highlight(YELLOW)
        union_label.next_to(union_rect, UP)

        rectangles.save_state()
        self.play(
            FadeOut(VGroup(rectangles[4:])),
            Transform(VGroup(rectangles[:4]), union_rect),
        )
        self.remove(rectangles)
        rectangles.restore()
        self.add(union_rect)

        to_fade = VGroup(all_sets_label[1], all_sets_label[3])
        to_fade.save_state()
        to_fade.highlight(BLACK)
        for m1, m2 in zip(to_fade, union_label[1:]):
            m1.next_to(m2, buff = 0.05, coor_mask = X_MASK)

        union_label[0].save_state()
        union_label[0].highlight(BLACK)
        union_label[0].next_to(all_sets_label[0], LEFT, coor_mask = X_MASK)
        self.play(
            MoveFromSaved(to_fade, remover = True),
            ReplacementTransform(
                VGroup(all_sets_label[0::2]), VGroup(union_label[1:])
            ),
            union_label[0].restore,
        )
        self.dither()

        union = VGroup(dots, union_rect)
        union_label2 = TexMobject('A').highlight(YELLOW)
        union.save_state()
        VGroup(rectangles, union).scale(0.5)
        union_label2.next_to(union, UP)
        union_g = VGroup(union_label2, union, rectangles)
        union_g.to_corner(UP+RIGHT)
        union_g.remove(rectangles)

        self.play(
            ReplacementTransform(union_label, VGroup(union_label2)),
            MoveFromSaved(union),
        )
        self.dither()

        pws_col = BLUE
        powerset_rect = union_rect.copy().highlight(pws_col)
        powerset_rect.stretch(1.3, 0)
        powerset_rect.next_to(union_rect, DOWN, aligned_edge = RIGHT)

        powerset_label = TexMobject("|A|<|","\\mathcal P(A)","|")
        powerset_label[0][1].highlight(YELLOW)
        powerset_label[1].highlight(pws_col)

        powerset_label.shift(
            powerset_rect.get_corner(UP+LEFT)
            - powerset_label[1].get_corner(DOWN+LEFT)
            + DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*UP
        )
        self.play(
            FadeIn(powerset_label[1]),
            ShowCreation(powerset_rect),
        )
        self.play(Write(VGroup(powerset_label[::2])))

        rectangles.save_state()
        rectangles[1].highlight(pws_col)
        self.play(ReplacementTransform(powerset_rect.copy(), rectangles[1]))

        self.dither()
        self.play(FadeOut(rectangles[1]))
        rectangles.restore()

        only_sets_text = TextMobject("Pouze\\\\množiny")
        only_sets_arrow = Arrow(ORIGIN, 2*RIGHT)
        only_sets_g = VGroup(only_sets_text, only_sets_arrow).arrange_submobjects()
        only_sets_g.shift(powerset_rect.get_edge_center(LEFT) - only_sets_arrow.get_center())

        self.play(
            FadeIn(only_sets_text),
            ShowCreation(only_sets_arrow),
        )

        self.play(
            FadeOut(union_label2),
            ReplacementTransform(union_rect, VGroup(rectangles[:4])),
            FadeIn(VGroup(rectangles[4:])),
        )
        all_sets_rect = SurroundingRectangle(rectangles)
        all_sets_label = TexMobject('A').next_to(all_sets_rect, UP).highlight(YELLOW)
        self.play(ShowCreation(all_sets_rect))

        self.play(Write(all_sets_label))
        self.play(FadeOut(VGroup(
            all_sets,
            only_sets_g,
            powerset_label[::2],
        )))
        
        h = 1.4*SPACE_HEIGHT
        w1 = 1
        w2 = 1.6*SPACE_WIDTH
        all_sets_dest = Rectangle(width = w1, height = h).to_edge(LEFT).highlight(YELLOW)
        powerset_dest = Rectangle(width = w2, height = h).to_edge(RIGHT).highlight(pws_col)

        powerset_label = powerset_label[1]
        self.play(
            all_sets_label.to_corner, UP+LEFT,
            powerset_label.to_corner, UP+RIGHT,
            Transform(all_sets_rect, all_sets_dest),
            Transform(powerset_rect, powerset_dest),
        )

class DiagonalPrincipleRecall(Scene):
    def construct(self):

        pws_col = BLUE
        
        h = 1.4*SPACE_HEIGHT
        w1 = 1
        w2 = 1.6*SPACE_WIDTH
        set_A = Rectangle(width = w1, height = h).to_edge(LEFT).highlight(YELLOW)
        set_PA = Rectangle(width = w2, height = h).to_edge(RIGHT).highlight(pws_col)
        set_A_label = TexMobject('A').highlight(YELLOW).to_corner(UP+LEFT)
        set_PA_label = TexMobject('\\mathcal P(A)').highlight(pws_col).to_corner(UP+RIGHT)

        dots_num = 10
        p0 = set_A.get_edge_center(UP) + set_A.get_width()/2*DOWN
        p1 = set_A.get_edge_center(DOWN) + set_A.get_width()/2*UP
        vdots = VGroup([
            Dot(interpolate(p0,p1,alpha))
            for alpha in np.linspace(0,1,dots_num)
        ])

        subset = Rectangle(width = w2-1, height = 0.7).move_to(set_PA)
        subset.save_state()
        p0 = subset.get_edge_center(LEFT) + RIGHT
        p1 = subset.get_edge_center(RIGHT) + LEFT
        hdots = VGroup([
            Dot(interpolate(p0,p1,alpha))
            for alpha in np.linspace(0,1,dots_num)
        ])

        for i,dot in enumerate(vdots):
            dot.index = i
            dot.set_color(random.choice([RED, GREEN]))

        green_dots = filter(lambda dot: dot.color == Color(GREEN), vdots)
        red_dots = filter(lambda dot: dot.color == Color(RED), vdots)

        self.add(set_A, set_PA, set_A_label, set_PA_label)

        dots_to_show = VGroup(vdots.submobjects)

        cur_dot = green_dots[2]
        dots_to_show.remove(cur_dot)
        subset.move_to(cur_dot, coor_mask = Y_MASK)
        x_var = TexMobject('x').move_to(cur_dot)
        line = Line(x_var, subset, buff = 0.2)

        self.play(GrowFromCenter(x_var))
        self.play(ShowCreation(line), FadeIn(subset))

        x_inside = x_var.copy().move_to(hdots[cur_dot.index])
        x_inside.move_to(subset, coor_mask = Y_MASK)
        x_inside.save_state()
        x_inside.shift(UP)
        x_inside.set_fill(opacity = 0)
        self.play(x_inside.restore)
        self.dither()
        self.play(FadeOut(VGroup(line, subset, x_inside)))
        self.play(ReplacementTransform(x_var, cur_dot))

        cur_dot = red_dots[2]
        dots_to_show.remove(cur_dot)
        subset.move_to(cur_dot, coor_mask = Y_MASK)
        x_var = TexMobject('x').move_to(cur_dot)
        line = Line(x_var, subset, buff = 0.2)

        self.play(GrowFromCenter(x_var))
        self.play(ShowCreation(line), FadeIn(subset))
        self.dither()

        x_inside = x_var.copy().move_to(hdots[cur_dot.index])
        x_inside.move_to(subset, coor_mask = Y_MASK)
        x_inside.shift(UP)
        x_inside.save_state()
        x_inside.shift(DOWN)
        x_inside.set_fill(opacity = 0)
        self.play(x_inside.restore)
        self.dither()
        self.play(FadeOut(VGroup(line, subset, x_inside)))
        self.play(ReplacementTransform(x_var, cur_dot))

        self.dither()

        self.play(ShowCreation(dots_to_show))

        subset.restore()

        red_hdots = VGroup([hdots[dot.index] for dot in red_dots]).highlight(RED)
        self.play(
            ReplacementTransform(VGroup(list(red_dots)).copy(), red_hdots),
        )
        self.play(ShowCreation(subset))
        self.dither()

        subset_g = VGroup(subset, hdots)
        visible_g = VGroup(subset, red_hdots)

        cur_dot = green_dots[2]
        visible_g.save_state()
        subset_g.move_to(cur_dot, coor_mask = Y_MASK)
        line = Line(cur_dot, subset, buff = 0.2)
        self.play(
            MoveFromSaved(visible_g),
            ShowCreation(line),
        )
        cur_hdot = hdots[cur_dot.index]
        cur_hdot.highlight(GREEN)
        self.dither()
        self.add(cur_hdot)
        self.dither(0.3)
        self.remove(cur_hdot)
        self.dither(0.2)
        self.add(cur_hdot)
        self.dither()
        self.remove(cur_hdot)

        ori_line = line
        cur_dot = red_dots[2]
        visible_g.save_state()
        subset_g.move_to(cur_dot, coor_mask = Y_MASK)
        line = Line(cur_dot, subset, buff = 0.2)
        self.play(
            FadeOut(ori_line),
            MoveFromSaved(visible_g),
            ShowCreation(line),
        )

        cur_hdot = hdots[cur_dot.index]
        cur_hdot.highlight(YELLOW)
        self.dither(0.3)
        cur_hdot.highlight(RED)
        self.dither(0.2)
        cur_hdot.highlight(YELLOW)
        self.dither()

        cur_hdot.highlight(RED)
        visible_g.save_state()
        subset_g.move_to(ORIGIN, coor_mask = Y_MASK)

        self.play(FadeOut(line), MoveFromSaved(visible_g))
        self.dither()

        cur_dot = vdots[-3]
        subset2 = subset.copy().move_to(cur_dot, coor_mask = Y_MASK)
        line = Line(cur_dot, subset2, buff = 0.2)

        self.play(ShowCreation(line))
        self.dither()
        self.play(Uncreate(line))
        self.play(ReplacementTransform(cur_dot.copy(), subset2))

        self.dither()
        title = TextMobject("Russellův paradox").next_to(subset, UP)
        self.play(FadeIn(title, submobject_mode = "lagged_start"))
        self.dither()

        title.save_state()
        title.center()
        title.to_edge(UP)
        self.play(
            FadeOut(VGroup(
                set_A, set_A_label, set_PA, set_PA_label,
                vdots, visible_g, subset2,
            )),
            MoveFromSaved(title),
        )

class RussellParadox(Scene):
    def construct(self):

        title = TextMobject("Russellův paradox").to_edge(UP)
        self.add(title)

        set_inside = TextMobject("Množiny, které neobsahují samu sebe")
        set_rect = SurroundingRectangle(set_inside, buff = 0.8, color = RED)
        self.play(FadeIn(set_inside), ShowCreation(set_rect))

        X_label = TexMobject('X').next_to(set_rect, UP, aligned_edge = LEFT)
        self.play(Write(X_label))

        bubble_q = ChatBubble("Obsahuje $X$ samu sebe?", True)
        bubble_q.save_state()
        bubble_q.stretch_about_point(0,1,SPACE_HEIGHT*DOWN)
        bubble_q.highlight(BLACK)
        self.play(ApplyMethod(bubble_q.restore, rate_func = rush_from))

        self.dither()

        bubble_a = ChatBubble("Že by neobsahuje?", False)
        bubble_a.save_state()
        bubble_a.stretch_about_point(0,1,SPACE_HEIGHT*DOWN)
        bubble_a.highlight(BLACK)
        self.play(ApplyMethod(bubble_a.restore, rate_func = rush_from))
        self.dither()

        X_label2 = X_label.copy()
        X_label2.shift(
            set_rect.get_corner(UP+RIGHT)
            - X_label2.get_corner(UP+RIGHT)
        )
        X_label2.shift(0.2*(DOWN+LEFT))

        X_label2.save_state()
        X_label2.shift(UP)
        X_label2.set_fill(opacity = 0)
        self.play(X_label2.restore)
        self.dither()

        self.play(FadeOut(bubble_a))

        bubble_a = ChatBubble("Tak obsahuje?", False)
        bubble_a.save_state()
        bubble_a.stretch_about_point(0,1,SPACE_HEIGHT*DOWN)
        bubble_a.highlight(BLACK)
        self.play(ApplyMethod(bubble_a.restore, rate_func = rush_from))
        self.dither()

        X_label2.save_state()
        X_label2.shift(UP)
        X_label2.set_fill(opacity = 0)
        self.play(MoveFromSaved(X_label2, remover = True))
        self.dither()

        self.play(FadeOut(VGroup(
            bubble_q, bubble_a, title, X_label,
            set_rect, set_inside,
        )))

class ParadoxesGeneral(Scene):

    def construct(self):

        steps_str = [
            "Všechny množiny určité vlastnosti",
            "Hromadná operace",
            "Nový prvek dané vlastnosti",
        ]
        steps = VGroup([TextMobject(step_str) for step_str in steps_str])
        steps.arrange_submobjects(DOWN, buff = 1.5)
        #steps.to_edge(UP)
        arrow1 = Arrow(steps[0], steps[1])
        arrow2 = Arrow(steps[1], steps[2])

        self.play(FadeIn(steps[0], submobject_mode = "lagged_start"))

        ordinals = OrdinalClass().to_edge(DOWN)
        self.play(FadeIn(ordinals))
        brace = BraceText(ordinals, ["Typy dobře uspořádaných","množin"], UP)
        brace.desc[-1].highlight(YELLOW)
        self.play(brace.creation_anim())

        self.dither()

        self.play(FadeOut(VGroup(ordinals, brace)))
        self.play(
            ShowCreation(arrow1),
            FadeIn(steps[1], submobject_mode = "lagged_start"),
        )
        self.dither()

        all_sets1 = AllSetsPicture().scale(0.45)
        all_sets2 = all_sets1.copy()
        all_sets1.to_corner(DOWN+LEFT)
        all_sets2.to_corner(DOWN+RIGHT)

        rect1 = SurroundingRectangle(all_sets1, buff = 0)
        rect2 = SurroundingRectangle(all_sets2)

        self.play(FadeIn(all_sets1))
        rectangles = all_sets1[0]
        self.play(
            FadeOut(VGroup(rectangles[4:])),
            ReplacementTransform(VGroup(rectangles[:4]), VGroup(rect1)),
        )
        self.remove(rectangles)

        self.dither()
        self.play(FadeIn(all_sets2))
        self.play(ShowCreation(rect2))
        self.dither()
        self.play(FadeOut(VGroup(all_sets1[1], all_sets2, rect1, rect2)))

        self.play(
            ShowCreation(arrow2),
            FadeIn(steps[2], submobject_mode = "lagged_start"),
        )

        p0 = steps[2].get_corner(UP+RIGHT) + 0.1*UP
        p1 = steps[0].get_corner(DOWN+RIGHT) + 0.1*DOWN
        p1 = p1*Y_MASK + p0*X_MASK
        center = (p0+p1)/2 + 7*LEFT
        radius = np.linalg.norm(p0-center)
        a0 = angle_of_vector(p0-center)
        a1 = angle_of_vector(p1-center)
        angle = (a1-a0)

        arrow3 = Arc(angle, radius = radius, start_angle = a0).shift(center)
        arrow3.add_tip()
        arrow3.highlight(RED)
        contr_label = TextMobject("Spor!").next_to(arrow3)

        self.play(ShowCreation(arrow3), FadeIn(contr_label))
        self.dither()

        self.play(FadeOut(VGroup(
            arrow1, arrow2, arrow3, contr_label,
            steps,
        )))

class ObjectsVsSets(Scene):
    def construct(self):

        axes = Axes(x_min = -2.2, x_max = 2.5)
        plane_rect = SurroundingRectangle(axes, color = WHITE)
        labels = TextMobject("Body v rovině", "Formální svět množin")
        labels.next_to(plane_rect, UP)
        plane_label, st_label = labels
        plane_label.move_to(plane_rect, coor_mask = X_MASK)
        plane_set = SVGMobject(file_name = "blob").scale_to_fit_width(2)
        plane_set.set_color(YELLOW)
        plane_set.set_fill(opacity = 0.3)
        plane_set.shift(0.7*LEFT+DOWN)
        objects_l = TextMobject("objekty")
        objects_l.shift(
            plane_rect.get_corner(UP+RIGHT)
            - objects_l.get_corner(UP+RIGHT)
            + 0.2*(DOWN+LEFT)
        )
        points = [(-0.7, 1.9), (-1.8, 1.1), (1.2, 1), (1.5, -1.3)]
        points = VGroup([
            Dot(np.array(coor+(0,)), color = YELLOW)
            for coor in points
        ])
        plane_g = VGroup(
            axes, plane_rect, plane_label, plane_set, objects_l, points
        )

        st_rect = plane_rect.copy()
        st_points = points.copy().highlight(WHITE)
        st_class = Circle(color = WHITE, fill_opacity = 0.1)
        st_class.stretch(-1,1).rotate(np.pi/2)
        st_class.replace(plane_set, stretch = True)
        st_class.center().scale(1.8).shift(0.2*DOWN + 0.2*LEFT)

        st_class_points = []
        buff_border = 0.2
        buff_inside = 0.3
        circle_to_ellipse = np.array([
            st_class.get_width()/2 - buff_border,
            st_class.get_height()/2 - buff_border,
        ])
        for _ in range(500):
            point = np.random.random([2])*2-1
            if np.linalg.norm(point) >= 1: continue
            point *= circle_to_ellipse
            for prev_point in st_class_points:
                if np.linalg.norm(point - prev_point) < buff_inside: break
            else: st_class_points.append(point)

        st_class_points = np.concatenate(
            [st_class_points, np.zeros([len(st_class_points),1])],
            axis = 1,
        )
        st_class_points += st_class.get_center()
        st_class_points = VGroup([
            Dot(point) for point in st_class_points
        ])
        st_class_g = VGroup(st_class, st_class_points)

        st_g = VGroup(st_rect, st_points, st_class_g)
        st_g.next_to(plane_rect, buff = 1)

        st_label.move_to(st_rect, coor_mask = X_MASK)
        st_objects_l = TextMobject("\\uv{množiny}")
        st_objects_l.shift(
            st_rect.get_corner(UP+RIGHT)
            - st_objects_l.get_corner(UP+RIGHT)
            + 0.2*(DOWN+LEFT)
        )
        st_g.add(st_objects_l, st_label)

        VGroup(plane_g, st_g).center().to_edge(UP)

        self.play(
            ShowCreation(VGroup(axes, plane_rect)),
            FadeIn(points, submobject_mode = "lagged_start"),
        )
        self.play(FadeIn(plane_label, submobject_mode = "lagged_start"))
        self.dither()

        plane_set_fill = plane_set.copy().set_stroke(width = 0)
        plane_set_stroke = plane_set.copy().set_fill(opacity = 0)
        self.play(FadeIn(plane_set_fill), ShowCreation(plane_set_stroke))
        self.remove(plane_set_fill, plane_set_stroke)
        self.add(plane_set)
        self.dither()
        plane_set.save_state()
        plane_set.next_to(plane_rect, DOWN, aligned_edge = LEFT)
        self.play(MoveFromSaved(plane_set))
        self.dither()

        self.play(ShowCreation(st_rect), FadeIn(st_points))
        self.play(FadeIn(st_label, submobject_mode = "lagged_start"))
        self.dither()

        plane_sets_l = TextMobject("množiny").next_to(plane_set)

        self.play(FadeIn(objects_l, submobject_mode = "lagged_start"))
        self.play(FadeIn(plane_sets_l, submobject_mode = "lagged_start"))

        self.dither()

        self.play(Write(st_objects_l))

        st_class_fill = st_class.copy().set_stroke(width = 0)
        st_class_stroke = st_class.copy().set_fill(opacity = 0)
        self.play(
            FadeIn(st_class_fill),
            FadeIn(st_class_points),
            ShowCreation(st_class_stroke),
        )
        self.remove(st_class_fill, st_class_stroke)
        self.add(st_class_g)

        st_class_g.save_state()

        st_class_g.replace(plane_set)
        st_class_g.next_to(st_rect, DOWN, aligned_edge = LEFT)
        st_class_l = TextMobject("třídy").next_to(st_class)
        self.play(MoveFromSaved(st_class_g))
        self.play(Write(st_class_l))

        st_points.save_state()
        st_objects_l.save_state()
        for point in st_points:
            coor = point.get_center() - st_rect.get_center()
            coor[0] *= 2*SPACE_WIDTH / st_rect.get_width()
            coor[1] *= 2*SPACE_HEIGHT / st_rect.get_height()
            point.move_to(coor)
            point.highlight(BLACK)

        title_point = st_points[0]
        title_point.highlight(WHITE)
        VGroup(title_point, st_objects_l).arrange_submobjects().to_corner(UP+RIGHT)

        self.play(
            VGroup(plane_g, plane_sets_l).behind_edge, LEFT,
            VGroup(st_class_g, st_class_l).behind_edge, DOWN,
            st_label.behind_edge, UP,
            Transform(st_rect,
                      Rectangle(width = 2.1*SPACE_WIDTH,
                                height = 2.1*SPACE_HEIGHT)
            ),
            MoveFromSaved(st_points),
            MoveFromSaved(st_objects_l),
        )
        self.dither()

class SetTheoryGraph(Scene):
    def construct(self):

        title1 = VGroup(Dot(), TextMobject("\\uv{množiny}")).arrange_submobjects()
        title1.to_corner(UP+RIGHT)
        self.add(title1)

        A_dot = Dot(LEFT)
        B_dot = Dot(RIGHT)
        A_label = TexMobject('A').next_to(A_dot, UP)
        B_label = TexMobject('B').next_to(B_dot, UP)

        self.play(ShowCreation(A_dot), FadeIn(A_label))
        self.play(ShowCreation(B_dot), FadeIn(B_label))

        A_g = VGroup(A_dot, A_label)
        A_dest = A_g.copy().shift(B_dot.get_center() - A_dot.get_center())
        B_rect = SurroundingRectangle(A_dest, color = WHITE, buff = 0.5)
        B_g = VGroup(B_dot, B_label)
        AB = VGroup(A_g, B_g)
        AB.save_state()

        self.play(
            B_label.next_to, B_rect, UP,
            Transform(B_dot, B_rect),
        )
        self.dither()
        self.play(
            Transform(A_g, A_dest)
        )
        self.dither()

        self.play(AB.restore)
        arrow = Arrow(A_dot, B_dot, color = BLUE)
        self.play(ShowCreation(arrow))

        title2 = VGroup(arrow.copy(), TextMobject("\\uv{je prvkem}"))
        title2.arrange_submobjects()
        title2.next_to(title1, DOWN, aligned_edge = RIGHT)

        self.dither()

        graph_points = [
            (11.52, -6.1 ),
            (13.92, -2.8),
            ( 9.92,  1.12),
            ( 8.32, -2.44),
            ( 5.28,  0.48),
            ( 1.32, -2.52),
            (11.08, -1   ),
            (17.34, -2.9 ),
            ( 6.69, -1.64),
            ( 7.82, -3.46),
            (10.8,  -3.51),
            (11.34, -4.29),
            ( 8.18, -1.02),
            ( 3.72, -2.44),
            ( 9.66, -1.18),
        ]


        graph_points = np.array([point+(0,) for point in graph_points])
        graph_points *= 1.2
        graph_points = VGroup([Dot(point, radius=  0.12) for point in graph_points])

        graph_arrows = []
        for i,dot in enumerate(graph_points):
            for j in range(4):
                if (i//(2**j))%2 == 1:
                    graph_arrows.append(Arrow(
                        graph_points[j].get_center(), dot.get_center(),
                        buff = 0.3, color = BLUE,
                    ))

        graph_arrows = VGroup(graph_arrows)

        graph = VGroup(graph_arrows, graph_points)
        graph.scale(0.5)
        graph.center().to_edge(DOWN)

        self.play(
            VGroup(AB, arrow).shift, 1.5*UP,
            FadeIn(graph_points)
        )
        self.play(
            ShowCreation(title2[0]),
            FadeIn(title2[1], submobject_mode = "lagged_start"),
            FadeIn(graph_arrows)
        )
        self.dither()

        A_col = YELLOW
        B_col = RED
        self.play(
            FadeOut(graph),
            FadeOut(arrow),
            A_g.highlight, A_col,
            B_g.highlight, B_col,
        )

        elements = VGroup([
            Dot(interpolate(3*LEFT, 3*RIGHT, alpha))
            for alpha in np.linspace(0,1,4)
        ]).shift(DOWN)
        num = 3
        buff = 0.5
        A_arrows = [Arrow(el, A_dot) for el in elements[:num]]
        B_arrows = [Arrow(el, B_dot) for el in elements]
        VGroup(A_arrows, B_arrows).highlight(BLUE)
        #self.add(elements, VGroup(A_arrows, B_arrows))

        A_rect = SurroundingRectangle(VGroup(elements[:num]), color = A_col, buff = buff)
        B_rect = SurroundingRectangle(VGroup(elements), color = B_col, buff = buff)
        A_rect.shift(0.1*(UP+LEFT))
        B_rect.shift(0.1*(DOWN+RIGHT))

        self.dither()
        A_rect.save_state()
        A_rect.scale(0)
        A_rect.set_stroke(width = 0)
        A_rect.move_to(A_dot)
        self.show_rev_arrows(
            A_arrows,
            FadeIn(VGroup(elements[:num])),
            ApplyMethod(A_rect.restore),
            fg = [A_rect],
        )
        self.dither()
        B_rect.save_state()
        B_rect.scale(0)
        B_rect.set_stroke(width = 0)
        B_rect.move_to(B_dot)
        self.show_rev_arrows(
            B_arrows[:num],
            ApplyMethod(B_rect.restore),
            Animation(A_rect),
            fg = [A_rect, B_rect],
        )
        self.dither()
        self.show_rev_arrows(
            B_arrows[num:],
            FadeIn(VGroup(elements[num:])),
            Animation(A_rect),
            Animation(B_rect),
            fg = [A_rect, B_rect],
        )
        self.dither()
        self.play(ShowCreation(arrow))
        self.dither()
        self.play(FadeOut(arrow))
        self.dither()
        
        class_set = TextMobject("Třídy i množiny").next_to(VGroup(A_rect, B_rect), DOWN)
        self.play(FadeIn(class_set, submobject_mode = "lagged_start"))
        self.dither()
        self.play(FadeOut(VGroup(
            title1, title2, A_arrows, B_arrows,
            A_dot, B_dot, A_rect, B_rect, A_label, B_label,
            elements, class_set,
        )))

    def show_rev_arrows(self, arrows, *animation, **kwargs):
        if 'fg' in kwargs: fg = kwargs['fg']
        else: fg = []

        rev_lines = VGroup([
            Line(arrow.get_end(), arrow.get_start(), color = BLUE)
            for arrow in arrows
        ])
        tips = VGroup([arrow.tip for arrow in arrows])

        
        self.play(
            FadeIn(tips, run_time = 0.4),
            ShowCreation(rev_lines, submobject_mode = "all_at_once"),
            *animation
        )
        self.remove(rev_lines, tips)
        self.add(*arrows)
        self.add(*fg)

class ProperClasses(Scene):
    def construct(self):
        all_sets = TextMobject("Všechny množiny")
        ordinals = OrdinalClass()
        VGroup(all_sets, ordinals).arrange_submobjects(DOWN, buff = 1)
        ordinals_rect = SurroundingRectangle(ordinals, color = YELLOW, buff = 0.3)
        all_sets_rect = SurroundingRectangle(VGroup(ordinals, all_sets), color = RED, buff = 0.3)
        all_sets_rect.shift(0.05*(UP+LEFT))
        ordinals_rect.shift(0.05*(DOWN+RIGHT))
        proper_classes = TextMobject("Vlastní třídy")
        proper_classes.next_to(VGroup(all_sets_rect, ordinals_rect), DOWN)
        all_sets_rect_src = Rectangle(
            width = 2.1*SPACE_WIDTH,
            height = 2.1*SPACE_HEIGHT,
            color = all_sets_rect.color,
        )

        self.play(
            FadeIn(all_sets, submobject_mode = "lagged_start"),
            ReplacementTransform(all_sets_rect_src, all_sets_rect),
        )
        self.dither()
        self.play(
            FadeIn(ordinals),
            FadeIn(ordinals_rect),
        )
        self.dither()
        self.play(Write(proper_classes))
        self.dither()

        self.play(FadeOut(VGroup(
            all_sets, all_sets_rect,
            ordinals, ordinals_rect,
            proper_classes,
        )))

class WhatAreSets(Scene):
    def construct(self):

        series = VideoSeries(num_videos = 16).to_edge(UP)
        brace = Brace(VGroup(series[8:]), DOWN)
        series.save_state()
        series.behind_edge(UP)
        question = TextMobject("Co všechno jsou množiny?")
        self.play(series.restore, GrowFromCenter(brace))
        self.play(Write(question))

        self.play(
            FadeOut(brace),
            question.shift, 2*DOWN
        )
        series_active = series.copy()
        series_active.highlight(YELLOW).shift(0.5*DOWN)

        for i,icon in enumerate(series_active):
            chap_num = TexMobject(str(i+1)).replace(icon, 1)
            chap_num.scale_in_place(0.7)
            icon.remove(icon[1])
            icon.add(chap_num)

        axiom_chap = series[8]
        axiom_chap.target = series_active[8]
        axiom_chap.save_state()

        self.play(MoveToTarget(axiom_chap))
        axiom_text = [
            "Axiomy teorie množin",
            "$\\bullet$ Pravidla",
            "$\\bullet$ Povolené konstrukce",
        ]
        axiom_text = VGroup([TextMobject(text) for text in axiom_text])
        axiom_text.arrange_submobjects(DOWN, aligned_edge = LEFT)
        tmp = axiom_text[0].copy().next_to(axiom_chap, DOWN)
        axiom_text.shift(tmp.get_center() - axiom_text[0].get_center())

        for ax in axiom_text:
            self.play(FadeIn(ax), submobject_mode = "lagged_start")
            self.dither()

        self.play(
            FadeOut(axiom_text),
            axiom_chap.restore,
        )
        objects = [
            "Párování",
            "Uspořádání",
            "Ordinální čísla",
            "Reálná čísla",
            "Kardinální čísla",
        ]
        objects = VGroup([TextMobject(text) for text in objects])
        objects.arrange_submobjects(DOWN)
        objects.next_to(series, DOWN)

        objects[2].next_to(series[10], DOWN, coor_mask = X_MASK, aligned_edge = RIGHT)
        objects[4].to_edge(RIGHT)
        print([
            (obj, coef)
            for obj, coef in zip(objects[2:], (0.5, -1.0, 0.5))
        ])
        objects[3].shift(X_MASK*sum([
            obj.get_edge_center(RIGHT)*coef
            for obj, coef in zip(objects[2:], (0.5, -1.0, 0.5))
        ]))
        objects[0].shift(2*LEFT)
        objects[1].shift(1*LEFT)

        lines = [
            Line(objects[0], series_active[9], buff = 0.2),
            Line(objects[1], series_active[9].get_edge_center(DOWN)+0.2*LEFT, buff = 0.2),
        ]
        for obj, i in zip(objects[2:], (10,11,15)):
            p1 = series_active[i].get_edge_center(DOWN)
            p0 = obj.get_corner(UP+RIGHT)
            p0 = p0*Y_MASK + p1*X_MASK
            lines.append(Line(p0, p1, buff = 0.2))

        self.play(FadeIn(objects[2], submobject_mode = "lagged_start"))
        self.play(
            ShowCreation(lines[2]),
            Transform(series[10], series_active[10]),
        )

        self.dither()
        self.play(
            FadeIn(objects[4]),
            ShowCreation(lines[4]),
            Transform(series[15], series_active[15])
        )
        self.play(
            FadeIn(objects[0]),
            ShowCreation(lines[0]),
            Transform(series[9], series_active[9])
        )
        self.play(
            FadeIn(objects[3]),
            ShowCreation(lines[3]),
            Transform(series[11], series_active[11])
        )
        self.play(
            FadeIn(objects[1]),
            ShowCreation(lines[1]),
        )

        self.dither()

class AxiomList(Scene):
    def construct(self):

        axiom_list = TextMobject(
            """Axiomy
~
            0) Existence
            1) Extensionalita
            2) Dvojice
            3) Sjednocení
            4) Vydělení
            5) Nekonečno
            6) Potenční množina
            7) Nahrazení
            8) Výběr
            9) Fundovanost""",
            alignment="\\raggedright"
        )

        axiom_list.to_edge(DOWN)
        axiom_list.save_state()
        axiom_list.behind_edge(DOWN)
        self.play(
            axiom_list.restore,
            run_time = 10,
            rate_func = None,
        )
        self.dither()
