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
from topics.objects import VideoSeries, VideoIcon
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.chat_bubbles import Conversation, ChatBubble
from topics.numerals import DecimalNumber

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer, IconYes, IconNo
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic

import importlib

class Chapter10aOpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 10a\\\\ Cartesian Product -- Applications",
    }

class Chapter10aOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Mathematics is the art of giving","the same","name to","different","things."
        ],
        "highlighted_quote_terms" : {
            "different" : GREEN,
            "the same" : YELLOW,
        },
        "author" : "Henri Poincaré"
    }

class Chapter10bOpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 10b\\\\ Cartesian Product from Axioms",
    }

class Chapter10bOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Q:","Why do we accept Kuratowski's definition of ordered pairs?\\\\",
            "A:","We accept this definition because it works, and it works very well. On the other hand, nobody really cares about how you encode."
        ],
        "highlighted_quote_terms" : {
            "Q:" : BLUE,
            "A:" : YELLOW,
        },
        "author" : "shortened, from Math StackExchange"
    }

chapter4 = importlib.import_module('eost.04-well-ordering')
chapter9 = importlib.import_module('eost.09-axioms-cz')

class PreviousChapter(Scene):
    def construct(self):

        dots = chapter9.dot_triple(angle = "random", radius = 0.8)
        rect = SurroundingRectangle(dots, buff = 0.5)
        finite_label = TextMobject("Axioms of pair, union,")
        finite_label.next_to(rect, UP, aligned_edge = LEFT)
        finite_g = VGroup(dots, rect, finite_label)
        finite_g.to_corner(LEFT+UP)

        self.play(Write(finite_label))
        #self.wait_to(4)
        self.play(FadeIn(dots), ShowCreation(rect))

        omega = OrdinalOmega()
        p_powers = omega.add_descriptions(chapter4.make_p_power,
                                          direction = UP)
        p_powers[0].highlight(GREEN)
        omega[0].highlight(GREEN)
        limit_bar = omega[0].copy().next_to(omega).highlight(YELLOW)
        limit_label = TexMobject('U').next_to(limit_bar, UP).highlight(YELLOW)

        big_pic = VGroup(
            omega, p_powers, limit_bar, limit_label,
        )
        big_pic.move_to((rect.get_edge_center(RIGHT)+SPACE_WIDTH*RIGHT)/2)
        big_pic.next_to(finite_label, DOWN, coor_mask = Y_MASK)
        big_label = TextMobject("infinity,","powerset,","replacement,","union")
        big_label[0].highlight(GREEN)
        big_label[-1].highlight(YELLOW)
        big_label.next_to(big_pic, DOWN, aligned_edge = RIGHT)
        big_g = VGroup(big_pic, big_label)

        #self.wait_to(7)
        self.play(FadeIn(big_pic))
        self.play(FadeIn(big_label, submobject_mode = "lagged_start"))

        #self.wait_to(9.5)
        conversation = Conversation(self, start_answer = True)
        conversation.add_bubble("It is not just about sets")
        #self.wait_to(22)
        self.dither(2)
        self.play(FadeOut(VGroup(
            conversation.dialog,
            big_g, finite_g,
        )))

class Overview(Scene):
    def prepare(self):

        self.formal_world = TextMobject("Formal world")
        self.product = TextMobject("Cartesian product")
        self.applications = TextMobject(
            "Points in plane","matching","function","ordering",
            "directed graph",
        )
        VGroup(
            self.applications[0],
            VGroup(self.applications[1:-1]).arrange_submobjects(RIGHT, buff = 1, coor_mask = X_MASK),
            self.applications[-1],
        ).arrange_submobjects(DOWN, buff = 0.5)

        self.formal_world.to_edge(UP)
        self.applications.to_edge(DOWN)
        self.product.move_to((self.formal_world.get_center() + self.applications[0].get_center())/2)

        kwargs = {"color" : WHITE, "tip_length" : 0.25}
        self.arrow1 = Arrow(self.formal_world, self.product, **kwargs)
        self.arrow2 = Arrow(self.product, self.applications, **kwargs)

    def construct(self):

        self.prepare()
        self.play(Write(self.product))
        #self.wait_to(6)
        self.play(FadeIn(self.formal_world), ShowCreation(self.arrow1))
        #self.wait_to(8)
        self.play(FadeIn(self.applications), ShowCreation(self.arrow2))

        self.remove(self.arrow2)
        self.arrow2.highlight(YELLOW)
        self.play(
            ShowCreation(self.arrow2),
            VGroup(self.formal_world, self.arrow1).highlight, DARK_GREY, 
        )
        self.dither(2)
        return
        #self.wait_to(16)
        icon = VideoIcon()
        icon.highlight(BLUE)
        brace = Brace(VGroup(self.formal_world, self.applications), LEFT)
        brace.put_at_tip(icon)
        self.play(
            FadeIn(icon),
            GrowFromCenter(brace),
        )
        icons = VGroup(icon.copy() for _ in range(2))
        ab = TextMobject("ab")
        ab.scale_to_fit_height(icon.get_height() * 0.7)
        for picon, part in zip(icons, ab):
            picon.remove(picon[1])
            part.move_to(picon)
            picon.add(part)

        icons[0].next_to(self.arrow2, LEFT, buff = 0.5)
        icons[1].next_to(self.arrow1, LEFT, buff = 0.5)

        #self.wait_to(32)
        self.dither()
        self.play(FadeOut(brace))
        self.play(ReplacementTransform(VGroup(icon), icons))
        #self.wait_to(35)

        self.remove(self.arrow2)
        self.arrow2.highlight(YELLOW)
        self.play(
            ShowCreation(self.arrow2),
            VGroup(self.formal_world, self.arrow1).highlight, DARK_GREY, 
        )

        #self.wait_to(39)
        self.remove(self.arrow1)
        self.arrow1.highlight(YELLOW)
        self.play(
            ShowCreation(self.arrow1),
            VGroup(self.applications, self.arrow2).highlight, DARK_GREY,
            self.formal_world.highlight, WHITE,
        )
        #self.wait_to(60+8)

        self.play(
            self.arrow1.highlight, DARK_GREY,
            self.arrow2.highlight, YELLOW,
            self.applications.highlight, WHITE,
            self.formal_world.highlight, DARK_GREY,
        )
        #self.wait_to(60+40)

        product_dest = self.product.copy().to_edge(UP)
        to_black = VGroup(self.formal_world, self.applications, self.arrow1, self.arrow2, icons)
        everything = VGroup(self.product, to_black)
        everything.save_state()
        everything.shift(product_dest.get_center() - self.product.get_center())
        to_black.highlight(BLACK)
        self.play(MoveFromSaved(everything))

col_a = BLUE
col_b = RED

def make_pairs_table():
    prod_el = VGroup([
        [
            TexMobject('(',"a_{}".format(index1),',',"b_{}".format(index2),')')
            for index1 in range(3)
        ]
        for index2 in range(3)
    ])
    for row in prod_el:
        for pair in row:
            pair[1].highlight(col_a)
            pair[-2].highlight(col_b)

    for row in prod_el: row.arrange_submobjects(buff = 0.5)
    prod_el.arrange_submobjects(UP)

    return prod_el

class ProductDefinition(Scene):
    def construct(self):

        title = TextMobject("Cartesian product")
        title.to_edge(UP)
        self.add(title)

        elements = TexMobject(*[
            "{}_{}".format(let, str(index))
            for let in ('a','b')
            for index in range(3)
        ])
        elements_a = VGroup(elements[:3]).highlight(col_a)
        elements_b = VGroup(elements[3:]).highlight(col_b)
        rects_ab = []
        labels_ab = []
        buff = 0.2
        for el_part in (elements_a, elements_b):
            el_part.arrange_submobjects(buff = 0.5, center = False, coor_mask = X_MASK)
            el_part.move_to(ORIGIN, coor_mask = X_MASK)
            rects_ab.append(Rectangle(
                width = el_part.get_width()+2*buff,
                height = elements.get_height()+2*buff,
                color = WHITE,
            ))

        rect_a, rect_b = rects_ab
        label_a = TexMobject('A').next_to(rect_a, DOWN).highlight(col_a)
        label_b = TexMobject('B').next_to(rect_a, DOWN).highlight(col_b)
        set_a = VGroup(elements_a, rect_a, label_a)
        set_b = VGroup(elements_b, rect_b, label_b)

        VGroup(set_a, set_b).arrange_submobjects(
            buff = 1, coor_mask = X_MASK,
        )

        prod_el = make_pairs_table()
        prod_el.save_state()

        prod_pile = VGroup(
            prod_el[0],
            prod_el[1].submobjects + [prod_el[2][-1]],
            prod_el[2][:-1],
        )
        for row in prod_pile: row.arrange_submobjects(buff = 0.5)
        prod_pile.arrange_submobjects(UP)
        prod_rect = SurroundingRectangle(prod_pile)
        prod_label = TexMobject("A\\times B").next_to(prod_rect, UP)
        prod_label[0].highlight(col_a)
        prod_label[-1].highlight(col_b)

        prod_g = VGroup(prod_el, prod_rect, prod_label)
        prod_g.next_to(title, DOWN, buff = 0.5)
        VGroup(set_a, set_b).next_to(prod_g, DOWN, buff = 0.5)

        self.play(
            ShowCreation(rect_a),
            FadeIn(elements_a),
            FadeIn(label_a),
        )
        self.play(
            ShowCreation(rect_b),
            FadeIn(elements_b),
            FadeIn(label_b),
        )

        #self.wait_to(3)
        self.play(Write(prod_label))
        #self.wait_to(5.5)
        self.play(
            ShowCreation(prod_rect),
            FadeIn(prod_el),
        )

        #self.wait_to(25)

        self.play(Swap(set_a, set_b))

        sets_ab_prod = VGroup(set_a, set_b, prod_g)
        sets_ab_prod.save_state()

        prod_el.restore()
        prod_rect.replace(SurroundingRectangle(prod_el), stretch = True)
        prod_label.next_to(prod_rect, UP)

        for el_a, el_row in zip(elements_a, prod_el[0]):
            el_a.move_to(el_row, coor_mask = X_MASK)
        rect_a.stretch_to_fit_width(prod_rect.get_width())
        rect_a.move_to(prod_rect, coor_mask = X_MASK)
        label_a.next_to(rect_a, DOWN)
        set_a.next_to(prod_rect, DOWN)

        for el_b, row in zip(elements_b, prod_el):
            el_b.move_to(row[0][-2])
        rect_b.stretch_to_fit_width(elements_b.get_width()+0.5)
        rect_b.stretch_to_fit_height(prod_rect.get_height())
        rect_b.move_to(prod_rect)
        rect_b.move_to(elements_b, coor_mask = X_MASK)
        label_b.next_to(rect_b, LEFT)
        set_b.next_to(prod_rect, LEFT)

        self.play(MoveFromSaved(sets_ab_prod))
        #self.wait_to(34)

        sel_a = 1
        sel_b = 2

        prod_el.save_state()
        elements_a.save_state()
        opacity = 0.3
        elements_a.set_fill(opacity = opacity)
        elements_a[sel_a].set_fill(opacity = 1)

        for row in prod_el:
            for i,pair in enumerate(row):
                pair[-2].set_fill(opacity = opacity)
                if i != sel_a: pair[1].set_fill(opacity = opacity)

        self.play(
            MoveFromSaved(elements_a),
            MoveFromSaved(prod_el),
            elements_b.set_fill, None, opacity,
        )

        #self.wait_to(37.5)
        to_highlight = VGroup(pair[-2] for pair in prod_el[sel_b])
        to_highlight.add(elements_b[sel_b])
        self.play(
            to_highlight.set_fill, None, 1,
        )
        #self.wait_to(60+17)

class CartesianCoordinates(Scene):
    def construct(self):

        axes = Axes()
        numbers_x = axes[0].get_number_mobjects().highlight(BLUE)
        numbers_y = axes[1].get_number_mobjects(direction = LEFT).highlight(RED)
        numbers_y.remove(numbers_y[len(numbers_y)//2])

        axes[0].highlight(col_a)
        axes[1].highlight(col_b)

        self.play(ShowCreation(VGroup(axes[0], numbers_x)))
        #self.wait_to(3.5)

        zero = numbers_x[len(numbers_x)//2]
        zero.save_state()
        zero.next_to(axes[1].main_line, coor_mask = X_MASK, buff = 0.2)
        tick_marks = axes[1].tick_marks
        tick_marks.remove(*[
            tick
            for tick in tick_marks
            if tick.get_center()[1] == 0
        ])
        self.play(
            ShowCreation(VGroup(axes[1], numbers_y)),
            MoveFromSaved(zero, run_time = 0.5),
        )
        #self.wait_to(6)

        plane = NumberPlane(color = DARK_GREY, secondary_color = PURPLE)
        black_axes = plane.axes.highlight(BLACK)
        black_axes.set_stroke(width = 20)

        lines = plane.main_lines.submobjects + plane.secondary_lines.submobjects
        hlines = VGroup(filter(lambda mob: mob.get_width() > mob.get_height(), lines))
        vlines = VGroup(filter(lambda mob: mob.get_width() < mob.get_height(), lines))
        htick = axes[1].tick_marks[0].scale(-1)
        vtick = axes[0].tick_marks[1]

        for line in plane.main_lines: line.tick_scale = 1
        for line in plane.secondary_lines: line.tick_scale = 0
        hlines_src = VGroup(htick.copy().scale(hline.tick_scale).move_to(hline) for hline in hlines)
        vlines_src = VGroup(vtick.copy().scale(vline.tick_scale).move_to(vline) for vline in vlines)

        for axis in axes:
            self.remove(axis.tick_marks)
            axis.remove(axis.tick_marks)
        axes[0].remove(*numbers_x)

        self.play(
            ReplacementTransform(hlines_src, hlines, submobject_mode = "lagged_start"),
            ReplacementTransform(vlines_src, vlines, submobject_mode = "lagged_start"),
            FadeIn(black_axes),
            Animation(axes),
            Animation(numbers_x),
            Animation(numbers_y),
            run_time = 2,
        )
        #self.wait_to(9.5)

        coor = [3,2]
        point = np.array(coor+[0])
        dot = Dot(point)

        dot.save_state()
        dot.scale(1.3)
        dot.set_fill(opacity = 0)
        self.play(dot.restore)

        pair = TexMobject('(',str(coor[0]),',',str(coor[1]),')')
        pair[1].highlight(col_a)
        pair[-2].highlight(col_b)
        pair.next_to(dot, UP)
        #self.wait_to(11.5)
        self.play(ReplacementTransform(dot.copy(), pair))
        #self.wait_to(16.5)

        connection_x = Line(point, point*X_MASK, color = col_a, buff = 0.2)
        connection_y = Line(point, point*Y_MASK, color = col_b, buff = 0.2)

        self.play(ShowCreation(connection_x))
        self.play(ShowCreation(connection_y))
        #self.wait_to(43)
        self.dither(2)

        self.play(
            FadeOut(VGroup(
                plane,
                axes,
                numbers_x, numbers_y,
                dot, pair,
                connection_x, connection_y,
            ),
        ))

class MatchingScene(Scene):
    def construct(self):

        v_spacing = 1
        elements = VGroup(TexMobject("a_{}".format(i), "b_{}".format(i), "\\cdot") for i in range(3))
        for i,el in enumerate(elements): el.move_to(i*v_spacing*DOWN)

        center_points = VGroup(el[-1] for el in elements)
        elements_a = VGroup(el[0] for el in elements)
        elements_a.highlight(col_a)
        elements_b = VGroup(el[1] for el in elements)
        elements_b.highlight(col_b)

        rect_b = SurroundingRectangle(elements_b, color = YELLOW)
        rect_a = rect_b.copy().move_to(elements_a, coor_mask = X_MASK)
        label_a = TexMobject('A').next_to(rect_a, DOWN).highlight(col_a)
        label_b = TexMobject('B').next_to(rect_b, DOWN).highlight(col_b)

        set_a = VGroup(elements_a, rect_a, label_a)
        set_b = VGroup(elements_b, rect_b, label_b)

        sets = VGroup(set_a, set_b)
        sets.arrange_submobjects(coor_mask = X_MASK, buff = 1.5, center = False)
        VGroup(sets, center_points).center()
        sets.to_edge(LEFT, buff = 1)

        points_a = [
            a.get_edge_center(RIGHT)*X_MASK + dot.get_center()*Y_MASK + 0.1*RIGHT
            for a, dot in zip(elements_a, center_points)
        ]
        points_b = [
            b.get_edge_center(LEFT)*X_MASK + dot.get_center()*Y_MASK + 0.1*LEFT
            for b, dot in zip(elements_b, center_points)
        ]
        straight_matching = VGroup(
            Line(a, b)
            for a, b in zip(points_a, points_b)
        )
        permutation = (1,2,0)
        points_b_permuted = [points_b[i] for i in permutation]
        matching = VGroup(
            Line(a, b)
            for a, b in zip(points_a, points_b_permuted)
        )
        matching_label = TextMobject("matching").next_to(sets, UP, buff = 1)

        self.play(
            ShowCreation(rect_a),
            FadeIn(elements_a),
            FadeIn(label_a),
        )
        self.play(
            ShowCreation(rect_b),
            FadeIn(elements_b),
            FadeIn(label_b),
        )
        #self.wait_to(8.5)
        self.play(ShowCreation(matching))
        #self.wait_to(20.5)
        self.play(FadeIn(matching_label, submobject_mode = "lagged_start"))
        #self.wait_to(30)

        matching_label.save_state()

        definition_items = VGroup(
            TextMobject("$\\bullet$ subset of", "$A\\times B$"),
            TextMobject("$\\bullet$ everything from", "$A$", "once on left"),
            TextMobject("$\\bullet$ everything from", "$B$", "once of right"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        definition_items[0][1][0].highlight(col_a)
        definition_items[0][1][-1].highlight(col_b)
        definition_items[1][1].highlight(col_a)
        definition_items[2][1].highlight(col_b)

        definition_rect = SurroundingRectangle(definition_items, buff = 0.2, color = GREEN)
        definition_frame = VGroup(definition_rect, definition_items)
        definition_label = TextMobject("(formal definition)")
        definition = VGroup(matching_label, definition_label, definition_frame)
        definition.arrange_submobjects(DOWN, center = False)
        definition.to_edge(RIGHT)

        self.play(
            MoveFromSaved(matching_label),
            FadeIn(definition_label),
        )
        #self.play(Write(definition_label))

        #self.wait_to(36.5)
        #self.dither()
        matching_rect = SurroundingRectangle(VGroup(elements_a, elements_b), buff = 0.5)
        label_a.save_state()
        label_a.next_to(matching_rect, DOWN, coor_mask = Y_MASK)
        label_b.save_state()
        label_b.next_to(matching_rect, DOWN, coor_mask = Y_MASK)
        self.play(
            FadeOut(VGroup(rect_a, rect_b)),
            MoveFromSaved(label_a),
            MoveFromSaved(label_b),
        )
        self.play(ShowCreation(matching_rect))
        #self.dither()

        elements_b.save_state()
        for a,b in enumerate(permutation):
            elements_b[b].shift(DOWN*v_spacing*(a-b))

        self.play(
            MoveFromSaved(elements_b, path_arc = np.pi/2),
            Transform(matching, straight_matching, path_arc = np.pi/2),
        )

        #self.wait_to(42)
        pairs = VGroup(
            TexMobject("(","a_{}".format(a),",","b_{}".format(b),")")
            for a,b in enumerate(permutation)
        )
        for i,pair in enumerate(pairs):
            pair[1].highlight(col_a)
            pair[3].highlight(col_b)
            pair.shift(elements_a[i].get_center() - pair[1].get_center())
            pair.move_to(matching_rect, coor_mask = X_MASK)

        open_brace = pairs[0][0].copy().set_fill(opacity = 0)
        close_brace = pairs[0][-1].copy().set_fill(opacity = 0)

        pairs_src = VGroup(
            [
                open_brace.copy().next_to(elements_a[a], LEFT),
                elements_a[a], matching[a], elements_b[b],
                close_brace.copy().next_to(elements_b[b], RIGHT),
            ]
            for a,b in enumerate(permutation)
        )
        self.play(ReplacementTransform(pairs_src, pairs))
        #self.wait_to(44)

        self.play(ShowCreation(definition_rect), Write(definition_items[0], run_time = 2))
        #self.wait_to(54)
        self.play(Write(definition_items[1], run_time = 2))
        pairs.save_state()
        for pair in pairs:
            pair.set_fill(opacity = 0.3)
            pair[1].set_fill(opacity = 1)
        self.play(
            MoveFromSaved(pairs),
            label_b.set_fill, None, 0.3,
        )
        #self.wait_to(60+5.5)

        self.play(
            pairs.set_fill, None, 1,
            label_b.set_fill, None, 1,
        )
        self.play(FadeIn(definition_items[2], submobject_mode = "lagged_start", run_time = 1.5))
        #self.wait_to(60+8.5)

        pairs.save_state()
        for pair in pairs:
            pair.set_fill(opacity = 0.3)
            pair[3].set_fill(opacity = 1)
        self.play(
            MoveFromSaved(pairs),
            label_a.set_fill, None, 0.3,
        )

        #self.wait_to(60+31)
        self.dither(2)
        everything = VGroup(
            pairs,
            matching_rect,
            label_a, label_b,
            definition,
        )
        self.play(FadeOut(everything))

col_f = GREEN

class FunctionsIntro(Scene):
    def construct(self):

        title = TextMobject("Function").scale(1.3).to_edge(UP)
        self.play(FadeIn(title))

        f_desc = TexMobject("2-x^2/2")
        x_in_f = f_desc[2]
        x_in_f.highlight(col_a)

        f_rect = SurroundingRectangle(f_desc, buff = 0.3, color = col_f)
        f_label = TexMobject("f").next_to(f_rect)
        f_box = VGroup(f_desc, f_rect, f_label)

        x = TexMobject("x","=","3")
        fx = TexMobject("f(x)","=","-2.5")
        x[0].highlight(col_a)
        x[-1].highlight(col_a)
        fx[0].highlight(col_b)
        fx[-1].highlight(col_b)

        x.shift(f_desc.get_center() - x[0].get_center())
        fx.shift(f_desc.get_center() - fx[0].get_center())
        x.shift(2*UP)
        fx.shift(2*DOWN)

        arrow1 = Arrow(x[0], f_desc, color = col_f)
        arrow2 = Arrow(f_desc, fx[0], color = col_f)

        #self.wait_to(1.5)
        self.play(FadeIn(x[0]), ShowCreation(arrow1))
        #self.wait_to(4.5)
        self.play(FadeIn(f_box))
        #self.wait_to(9.5)
        self.play(FadeIn(fx[0]), ShowCreation(arrow2))

        #self.wait_to(13)
        self.play(FadeIn(x[1]), Write(x[2]))
        #self.wait_to(16.5)
        plugged = x[2].copy()
        plugged.save_state()
        plugged.shift(x_in_f.get_edge_center(DOWN) - plugged.get_edge_center(DOWN))

        self.play(
            x_in_f.highlight, DARK_GREY,
            MoveFromSaved(plugged),
        )
        #self.wait_to(22)

        result_src = VGroup(f_desc.submobjects)
        result_src.submobjects[2] = plugged
        self.play(
            FadeIn(fx[1]),
            ReplacementTransform(result_src.copy(), fx[2]),
        )

        #self.wait_to(25)
        self.dither()

        f_desc.save_state()
        f_desc.to_corner(UP+RIGHT)
        x_in_f.highlight(col_a)

        title.add_background_rectangle()
        self.add_foreground_mobjects(title)

        axes = Axes()

        self.play(
            FadeOut(VGroup(
                arrow1, arrow2,
                x,fx,
                plugged,
                f_rect,f_label,
            )),
            MoveFromSaved(f_desc),
        )
        self.play(ShowCreation(axes))
        #self.wait_to(28)

        function = lambda x: 2-x**2/2
        x_val = 3
        y_val = function(float(x_val))
        dot_x = Dot(x_val*RIGHT, color = col_a)
        dot_y = Dot(x_val*RIGHT + y_val*UP, color = col_b)
        x_label = TexMobject('x','=',str(x_val)).next_to(dot_x, UP).highlight(col_a)
        y_label = TexMobject('f(x)','=',str(y_val)).next_to(dot_y, RIGHT).highlight(col_b)
        x_label[1].highlight(WHITE)
        y_label[1].highlight(WHITE)
        x_g = VGroup(dot_x, x_label)
        y_g = VGroup(dot_y, y_label)

        self.play(UnapplyMethod(x_g.behind_edge, RIGHT))
        y_g.save_state()
        y_g.shift(y_val*DOWN)
        y_label.set_fill(opacity = 0)
        dot_y.highlight(col_a)

        #self.wait_to(33)
        self.play(y_g.restore)

        #self.wait_to(37)
        self.play(FadeOut(VGroup(x_g, y_label)))

        graph = FunctionGraph(function, color = col_b)

        dot_y_copy = dot_y.copy()
        self.add(dot_y_copy)
        dots = VGroup(dot_x, dot_y)
        def update_dots(dots):

            if len(graph.points) == 0:
                x = -SPACE_WIDTH
                y = f(x)
            else:
                x,y,_ = graph.points[-1]

            dot_x.move_to(x*RIGHT)
            dot_y.move_to(x*RIGHT + y*UP)

            #label_x = TexMobject("{:.2f}".format(x))
            label_x = DecimalNumber(x, color = col_a)
            label_x.next_to(dot_x, LEFT+UP)
            label_x_bg = BackgroundRectangle(label_x)

            label_y = DecimalNumber(y, color = col_b)
            label_y.next_to(dot_y, RIGHT)
            label_y_bg = BackgroundRectangle(label_y)

            self.extra_mobjects_for_animation = label_x_bg, label_y_bg, label_x, label_y

        self.play(
            ShowCreation(graph, run_time = 7, rate_func = None),
            UpdateFromFunc(dots, update_dots),
        )
        self.remove(dots)
        #self.wait_to(56)
        self.dither(2)

        everything = VGroup(
            axes, graph, dot_y_copy, f_desc,
        )
        self.play(FadeOut(everything))

class FunctionsAtoB(Scene):
    def construct(self):

        title = TextMobject("Function").scale(1.3).to_edge(UP)
        self.add(title)

        a_rect = Rectangle(width = 3, height = 1, color = col_a)
        b_rect = a_rect.copy().highlight(col_b)
        f_rect = a_rect.copy().highlight(col_f)
        VGroup(a_rect, f_rect, b_rect).arrange_submobjects(DOWN, buff = 0.5)

        a_label = TexMobject('A').highlight(col_a).next_to(a_rect, LEFT)
        b_label = TexMobject('B').highlight(col_b).next_to(b_rect, LEFT)
        f_label = TexMobject('f\\colon A\\to B').scale(0.7).next_to(f_rect, LEFT)
        f_label[2].highlight(col_a)
        f_label[4].highlight(col_b)
        arrow1 = Arrow(a_rect.get_center(), f_rect.get_center(), buff = 0.4, color = GREEN)
        arrow2 = Arrow(f_rect.get_center(), b_rect.get_center(), buff = 0.4, color = GREEN)

        spacing = 0.7
        elements_a = VGroup(
            TexMobject("a_{}".format(i)).shift(i*spacing*RIGHT)
            for i in range(3)
        )
        elements_b = VGroup(
            TexMobject("b_{}".format(i)).shift(i*spacing*RIGHT)
            for i in range(3)
        )
        elements_a.highlight(GREY).move_to(a_rect)
        elements_b.highlight(GREY).move_to(b_rect)

        general_f_pic = VGroup(
            elements_a, elements_b,
            a_rect, b_rect, f_rect,
            arrow1, arrow2,
            a_label, b_label, f_label,
        )
        general_f_pic.to_edge(LEFT)

        self.play(
            FadeIn(f_rect),
            FadeIn(f_label[0]),
        )
        
        #self.wait_to(2.2)

        self.play(*map(FadeIn, [
            a_rect, a_label, elements_a,
        ]))

        self.play(
            FadeIn(b_rect),
            FadeIn(b_label),
            FadeIn(elements_b),
            ShowCreation(VGroup(arrow1, arrow2)),
        )

        #self.wait_to(5)
        self.play(Write(VGroup(f_label[1:])))
        #self.wait_to(12)

        function = (0,2,0)
        for x in range(3):
            y = function[x]
            sample = elements_a[x].copy()
            sample.save_state()
            sample.scale_in_place(1.2)
            sample.highlight(col_a)
            elements_a[x].highlight(col_a)
            self.remove(elements_a[x])
            self.play(MoveFromSaved(sample, run_time = 0.5, rate_func = rush_into))
            self.play(Transform(sample, elements_a[x], run_time = 0.5, rate_func = rush_from))
            self.add(elements_a[x])
            self.play(sample.move_to, f_rect)
            dest = elements_b[y].copy().highlight(col_b)
            self.play(Transform(sample, dest))
            self.remove(sample)
            elements_b[y].highlight(col_b)
            #self.dither()
            self.play(
                elements_a[x].highlight, GREY,
                elements_b[y].highlight, GREY,
            )

        graph_table = VGroup(
            VGroup(Dot() for _ in range(3)).arrange_submobjects(UP, buff = 0.8)
            for _ in range(3)
        ).arrange_submobjects(RIGHT, buff = 0.8)
        x_labels = elements_a.copy()
        x_labels.highlight(col_a).next_to(graph_table, DOWN, buff = 0.5)
        y_labels = elements_b.copy()
        y_labels.highlight(col_b)

        for label, column in zip(x_labels, graph_table):
            label.move_to(column, coor_mask = X_MASK)
        for label, dot in zip(y_labels, graph_table[0]):
            label.next_to(graph_table, RIGHT, buff = 0.5)
            label.move_to(dot, coor_mask = Y_MASK)

        graph_label = TextMobject("graph of function").next_to(graph_table, UP, buff = 0.5)
        graph = VGroup(graph_table, graph_label, x_labels, y_labels)
        graph.move_to(RIGHT*SPACE_WIDTH/2)

        #self.wait_to(27)
        self.play(FadeIn(graph_label, submobject_mode = "lagged_start"))
        self.play(
            ShowCreation(x_labels),
            ShowCreation(y_labels),
            FadeIn(graph_table, submobject_mode = "lagged_start"),
        )
        #self.wait_to(31)

        circles = []
        for x in range(3):
            y = function[x]
            sample = x_labels[x].copy()
            sample.save_state()
            self.play(sample.move_to, graph_table[x][y])
            self.play(Transform(sample, y_labels[y]))
            self.remove(sample)
            circ = Circle(radius = 0.3, color = GREEN).shift(graph_table[x][y].get_center())
            self.play(ShowCreation(circ))
            circles.append(circ)

        #self.wait_to(49)
        #self.play(FocusOn2(VGroup(graph_table, circles), scale = 1.1))
        #self.wait_to(53.5)
        #self.play(FocusOn2(f_rect, scale = 1.1))

        #self.wait_to(60)
        eq = TexMobject('=').next_to(title)
        self.play(
            FadeIn(eq),
            graph_label.next_to, eq,
        )
        #self.wait_to(60+16)

        graph.remove(x_labels, graph_label)
        circles = VGroup(circles)
        graph.add(circles)

        general_f_pic.save_state()
        graph.save_state()
        graph.scale(0.7)
        ori_height = f_rect.get_height()
        new_height = graph.get_height()+0.5
        f_rect.stretch_in_place(new_height / ori_height, 1)
        shift = (new_height-ori_height)/2
        VGroup(arrow1, a_label, a_rect, elements_a).shift(shift*UP)
        VGroup(arrow2, b_label, b_rect, elements_b).shift(shift*DOWN)

        graph.shift(f_rect.get_center() - graph_table.get_center())
        self.play(
            FadeOut(x_labels),
            MoveFromSaved(graph),
            MoveFromSaved(general_f_pic),
        )
        #self.wait_to(60+22.5)

        x = 1
        y = function[x]
        tmp = elements_a[x].copy()
        self.play(
            elements_a[x].highlight, col_a,
            Transform(tmp, graph_table[x].copy().highlight(col_a), path_arc = -np.pi/3),
        )
        self.remove(tmp)
        graph_table[x].highlight(col_a)
        tmp = circles[x].copy()
        #self.wait_to(60+27)
        self.play(Transform(tmp, y_labels[y]))
        self.play(Transform(tmp, elements_b[y].copy().highlight(col_b), path_arc = -np.pi/2))
        self.remove(tmp)
        elements_b[y].highlight(col_b)
        #self.wait_to(60+31)

        definition_items = VGroup(
            TextMobject("$\\bullet$ subset of", "$A\\times B$"),
            TextMobject("$\\bullet$ everything from", "$A$\\\\", "once on left"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        definition_rect = SurroundingRectangle(definition_items, buff = 0.2, color = GREEN)
        definition_label = TextMobject("formal definition").next_to(definition_rect, UP)
        definition = VGroup(definition_rect, definition_items, definition_label)
        definition.to_edge(RIGHT)
        definition_items[0][1][0].highlight(col_a)
        definition_items[0][1][-1].highlight(col_b)
        definition_items[1][1].highlight(col_a)

        self.play(
            FadeIn(definition_label, submobject_mode = "lagged_start"),
            ShowCreation(definition_rect),
        )
        #self.wait_to(60+34)
        self.play(
            FadeIn(definition_items[0],  submobject_mode = "lagged_start"),
        )
        #self.wait_to(60+36.5)
        self.play(
            FadeIn(definition_items[1],  submobject_mode = "lagged_start"),
        )
        #self.wait_to(60+49)

        matching_note = TextMobject("matching","$=$\\\\","bijective function")
        matching_note.move_to(definition).to_edge(DOWN)
        self.play(FadeIn(matching_note[0]))

        #self.wait_to(2*60+12.2)
        self.play(circles[2].move_to, graph_table[2][1])
        #self.wait_to(2*60+17)
        self.play(Write(VGroup(matching_note[1:])))
        #self.wait_to(2*60+30.5)
        self.dither(2)

        matching_vs_graph = TextMobject("matching","$\\times$","graph of","a bijective function")
        matching_vs_graph[1].highlight(RED)
        matching_vs_graph.to_edge(DOWN)
        matching_vs_graph[2].save_state()
        matching_vs_graph[2].highlight(BLACK)
        matching_vs_graph[2].next_to(matching_note[-1], LEFT, coor_mask = X_MASK)

        self.play(
            FadeOut(VGroup(
                general_f_pic, graph,
                definition,
                title, eq, graph_label,
            )),
            matching_vs_graph[2].restore,
            Transform(
                VGroup(matching_note[:2]), VGroup(matching_vs_graph[:2]),
                path_arc = np.pi/3,
            ),
            Transform(matching_note[2], matching_vs_graph[3]),
        )

class GraphMatching(Scene):
    def construct(self):

        matching_vs_graph = TextMobject("matching","$\\times$","graph of","a bijective function")
        matching_vs_graph[1].highlight(RED)
        matching_vs_graph.to_edge(DOWN)
        self.add(matching_vs_graph)

        graph_theory = TextMobject("Graph theory")
        graph_theory.next_to(matching_vs_graph[0], UP, buff = 2)
        arrow = Arrow(graph_theory, matching_vs_graph[0])

        #self.wait_to(5.5)
        self.play(
            ShowCreation(arrow),
            FadeIn(graph_theory),
        )
        #self.wait_to(10)

        spacing = 1
        elements_a = VGroup(
            TexMobject("a_{}".format(i)).shift(i*spacing*RIGHT)
            for i in range(3)
        )
        elements_b = VGroup(
            TexMobject("b_{}".format(i)).shift(i*spacing*RIGHT)
            for i in range(3)
        )
        
        elements_a.highlight(col_a)
        elements_b.highlight(col_b)
        elements_b.shift(2*DOWN)
        elements = VGroup(elements_a, elements_b)
        elements.move_to((graph_theory.get_corner(UP+RIGHT)[0]+SPACE_WIDTH)/2*RIGHT)
        compl_label = TextMobject("Complete","bipartite","graph").next_to(elements_a, UP, buff = 0.5)
        VGroup(elements, compl_label).to_edge(UP)

        points_a = [mob.get_edge_center(DOWN) for mob in elements_a]
        points_b = [mob.get_edge_center(UP) for mob in elements_b]
        compl_graph = VGroup(
            [
                Line(a,b, buff = 0.1, color = GREY)
                for b in points_b
            ]
            for a in points_a
        )

        self.play(
            FadeIn(elements),
            FadeIn(compl_label),
            ShowCreation(compl_graph),
        )
        #self.wait_to(13.5)
        #self.play(FocusOn2(compl_label[0], scale = 1.1))

        bundle1, bundle2, bundle3 = compl_graph
        self.play(bundle1.highlight, YELLOW, run_time = 0.5)
        self.play(
            bundle1.highlight, GREY,
            bundle2.highlight, YELLOW, run_time = 0.5,
        )
        self.play(
            bundle2.highlight, GREY,
            bundle3.highlight, YELLOW, run_time = 0.5,
        )
        self.play(bundle3.highlight, GREY, run_time = 0.5)

        #self.wait_to(17)
        #self.play(FocusOn2(compl_label[1], scale = 1.1))
        rectangles = VGroup(
            SurroundingRectangle(elements_a, color = col_a),
            SurroundingRectangle(elements_b, color = col_b),
        )
        self.play(ShowCreation(rectangles))
        #self.wait_to(22)
        self.dither()
        self.play(FadeOut(rectangles))

        matching_data = (0,2,1)
        matching = VGroup(
            compl_graph[a][b]
            for a,b in enumerate(matching_data)
        )
        self.play(matching.highlight, YELLOW)
        #self.wait_to(28.5)

        matching_label = TextMobject("perfect","matching").next_to(elements_b, DOWN, buff = 0.5)
        self.play(FadeIn(matching_label), submobject_mode = "lagged_start")

        partial_label = TextMobject("$\\times$ partial matching")
        partial_label[0].highlight(RED)
        partial_label.next_to(matching_label, DOWN)

        #self.wait_to(33.5)
        self.play(FadeIn(partial_label, submobject_mode = "lagged_start"))
        self.play(
            matching_label.highlight, GREY,
            matching[0].highlight, GREY,
        )
        #self.wait_to(40)
        #self.play(FocusOn2(matching_label, scale = 1.1))
        #self.wait_to(41.5)
        matching[0].highlight(YELLOW)
        self.play(ShowCreation(matching[0]))
        #self.wait_to(44)
        self.dither(2)

        graph_theory.save_state()
        graph_theory.scale(1.2).center().to_edge(UP)

        self.play(
            FadeOut(VGroup(
                matching_vs_graph, arrow,
                elements, compl_graph, compl_label,
                matching_label, partial_label,
            )),
            MoveFromSaved(graph_theory),
        )

class DirectedGraphs(Scene):
    def construct(self):

        title = TextMobject("Graph theory").scale(1.2).to_edge(UP)
        subtitle = TextMobject("Directed graph").next_to(title, DOWN)

        self.add(title)
        self.play(Write(subtitle))

        points = compass_directions(5, 1.7*UP)
        points[:,0] *= -1
        points += DOWN

        vertices = VGroup(
            TexMobject("v_{}".format(i)).move_to(points[i])
            for i in range(5)
        ).highlight(GREEN)

        vertices_rect = SurroundingRectangle(vertices, buff = 0.5, color = WHITE)
        vertices_label = TexMobject('V').highlight(GREEN).next_to(vertices_rect, LEFT, aligned_edge = UP)

        #self.wait_to(8)
        self.play(
            FadeIn(vertices_label),
            ShowCreation(vertices_rect),
            FadeIn(vertices),
        )
        #self.wait_to(16)
        
        radius = 0.4
        loop_arrow = Arc(
            angle = np.pi*3/2,
            radius = radius,
            color = YELLOW,
        )
        loop_arrow.add_tip()
        loop_arrow.shift(radius*(LEFT+UP))
        loop_arrow.rotate(-np.pi/4)
        loop_arrow.stretch(-1,0)

        def make_edge(i,j):
            if i == j:
                edge = loop_arrow.copy()
                edge.rotate(-i*2*np.pi/5)
                edge.shift(points[i])
                return edge
            else:
                return Arrow(points[i], points[j], buff = 0.4)

        compl_graph = VGroup(
            [
                make_edge(i,j)
                for j in range(5)
            ]
            for i in range(5)
        )

        example_pair_data = (3,1)
        example_pair = TexMobject(
            "(",
            "v_{}".format(example_pair_data[0]),
            ",",
            "v_{}".format(example_pair_data[1]),
            ")",
        )
        example_pair.next_to(vertices_rect, buff = 1)
        example_pair[1].highlight(GREEN)
        example_pair[3].highlight(GREEN)

        #self.play(Write(example_pair))
        self.play(FadeIn(example_pair))
        #self.wait_to(21.5)
        nodes = VGroup(example_pair[1::2]).copy()
        arrow = Arrow(
            *nodes,
            tip_length = 0.1,
            stroke_width = 0,
            fill_opacity = 0
        )
        nodes_dest = VGroup(vertices[i] for i in example_pair_data)
        self.play(
            Transform(nodes, nodes_dest, remover = True),
            Transform(arrow, compl_graph[example_pair_data[0]][example_pair_data[1]]),
        )
        #self.wait_to(28)
        self.dither()

        product_label = TexMobject("V\\times V")
        VGroup(product_label[::2]).highlight(GREEN)
        product_label.next_to(compl_graph[1][1], aligned_edge = UP)
        subset_label = TextMobject("subset").next_to(product_label, UP)

        self.play(FadeOut(VGroup(vertices_rect, vertices_label, example_pair)))
        self.play(ShowCreation(compl_graph), FadeIn(product_label))
        self.remove(arrow)
        #self.wait_to(32.5)
        self.dither()

        edges_removed = []
        edges_preserved = []
        for bundle in compl_graph:
            for edge in bundle:
                if random.random() < 0.4: edges_preserved.append(edge)
                else: edges_removed.append(edge)

        edges_removed = VGroup(edges_removed)
        edges_preserved = VGroup(edges_preserved)
        self.play(
            FadeIn(subset_label),
            FadeOut(edges_removed),
            Animation(edges_preserved),
        )
        self.dither(3)
        #self.wait_to(51.5)

class OrderingScene(Scene):
    def construct(self):

        title = TextMobject("Ordering").scale(1.2).to_edge(UP)
        self.add(title)

        colors = [BLUE, ORANGE, PURPLE, GREEN, RED]
        bars = VGroup(
            Line(ORIGIN, DOWN, color = color)
            for color in colors
        )
        bars.arrange_submobjects(RIGHT, buff = 1)

        self.play(ShowCreation(bars))
        #self.wait_to(6.5)

        for _ in range(3):
            bars.save_state()
            reorder = VGroup(bars.submobjects)
            random.shuffle(reorder.submobjects)
            reorder.arrange_submobjects(RIGHT, buff = 1)

            self.play(MoveFromSaved(bars, path_arc = np.pi/2))

        bars = reorder

        arrows = VGroup(
            Arrow(a,b, tip_length = 0.15, buff = 0.1)
            for a,b in zip(bars, bars[1:])
        )
        #self.wait_to(21.5)
        self.play(ShowCreation(arrows))
        #self.wait_to(32.5)

        bars_faded = bars.copy()
        bars_faded.highlight(BLACK).shift(UP)
        bars_ori = bars.copy()
        arrows.save_state()
        arrows.shift(UP).highlight(BLACK)

        reals_line = GradientLine(2.5*LEFT, 2.5*RIGHT, WHITE, DARK_BLUE)
        zero = TexMobject('0').next_to(reals_line.get_start(), DOWN)
        one = TexMobject('1').next_to(reals_line.get_end(), DOWN)
        reals = VGroup(
            reals_line, zero, one
        )
        reals.save_state()
        reals.shift(DOWN)
        reals.highlight(BLACK)

        self.play(
            Transform(bars, bars_faded, remover = True),
            MoveFromSaved(arrows, remover = True),
            reals.restore,
        )

        #self.wait_to(40.5)
        reals = reals_line
        reals_dest = reals.copy()
        reals_ori = reals.copy()
        random.shuffle(reals_dest.submobjects)
        for src, dest in zip(reals, reals_dest):
            dest.set_color(rgb_to_color(src.stroke_rgb))

        self.play(
            FadeOut(VGroup(zero, one)),
            ReplacementTransform(reals, reals_dest, path_arc = np.pi/2)
        )
        reals = reals_dest

        #self.wait_to(43.5)
        self.dither()
        self.play(
            ReplacementTransform(reals_dest, reals_ori, path_arc = -np.pi/2)
        )
        reals = reals_ori

        single_real_col = rgb_to_color(reals[len(reals)//2].stroke_rgb)
        single_real = Dot(color = single_real_col, stroke_width = 2)
        self.play(UnapplyMethod(single_real.scale, 0))

        empty_dot = single_real.copy().set_fill(BLACK)
        single_real.set_stroke(width = 0)
        self.add(empty_dot)
        self.play(single_real.shift, 0.5*UP)

        #self.wait_to(51)

        center = 0.5*RIGHT+0.8*DOWN
        start_angle = angle_of_vector(ORIGIN-center)
        angle = np.pi - 2*start_angle
        radius = np.linalg.norm(ORIGIN - center)
        arc_template = Arc(
            angle, start_angle = start_angle,
            radius = radius,
            color = YELLOW,
        ).shift(center)
        thin_template = arc_template.copy().set_stroke(width = 1)
        thin_template.fade()

        def make_arrow_to(x, thin = False, add_tip = True, tip_length = 0.1):
            if thin: arrow = thin_template.copy()
            else: arrow = arc_template.copy()
            arrow.scale(x)
            if add_tip: arrow.add_tip(tip_length)
            arrow.shift(single_real.get_center())
            return arrow

        def make_arc_to(x):
            return make_arrow_to(x, thin = True, add_tip = False)

        x = 1.7
        pointer = TrianglePointer(color = YELLOW)
        pointer.scale(-1).next_to(x*RIGHT, DOWN, buff = 0)
        pointer.save_state()
        pointer.move_to(ORIGIN, coor_mask = X_MASK)
        pointer.set_fill(opacity = 0)
        arrow = make_arrow_to(x)
        self.play(
            pointer.restore,
            ShowCreation(arrow),
        )

        for _ in range(3):
            x *= 0.5
            self.play(
                pointer.next_to, x*RIGHT, DOWN, 0,
                Transform(arrow, make_arrow_to(x)),
                run_time = 0.5,
            )
            self.dither(0.5)

        self.play(FadeOut(VGroup(pointer, arrow)))

        arrow_ends = np.linspace(0, reals.get_edge_center(RIGHT)[0], 8)[1:]
        arc_ends = np.linspace(0, reals.get_edge_center(RIGHT)[0], 80)[1:]
        arrows_to = VGroup(make_arrow_to(x) for x in arrow_ends)
        arcs_to = VGroup(make_arc_to(x) for x in arc_ends)

        #self.wait_to(60+5.5)
        self.play(
            ShowCreation(arcs_to, submobject_mode = "all_at_once"),
            *[
                ShowCreation(arrow) for arrow in arrows_to
            ]
        )
        #self.wait_to(60+10.5)

        def make_arrow_from(x, **kwargs):
            return make_arrow_to(-x, **kwargs).shift(x*RIGHT)
        def make_arc_from(x):
            return make_arc_to(-x).shift(x*RIGHT)

        arrow_starts = np.linspace(reals.get_edge_center(LEFT)[0], 0, 8)[:-1]
        arc_starts = np.linspace(reals.get_edge_center(LEFT)[0], 0, 80)[:-1]
        arrows_from = VGroup(make_arrow_from(x) for x in arrow_starts)
        arcs_from = VGroup(make_arc_from(x) for x in arc_starts)

        self.play(
            ShowCreation(arcs_from, submobject_mode = "all_at_once"),
            *[
                ShowCreation(arrow) for arrow in arrows_from
            ]
        )

        #self.wait_to(60+30)
        reals_g = VGroup(reals, empty_dot, single_real, arcs_to, arcs_from, arrows_to, arrows_from)
        bars.shift(UP)

        bar_arrows = []
        layers = []
        for i,bar1 in enumerate(bars_ori[:-1]):
            for j,bar2 in enumerate(bars_ori[i+1:]):

                bar_arrow = Arrow(
                    bar1.get_start(), bar2.get_start(),
                    tip_length = 0.15, buff = 0.1,
                )
                l = 0
                while l < len(layers) and layers[l] > i: l += 1
                if l == len(layers): layers.append(i+j+1)
                else: layers[l] = i+j+1

                bar_arrow.shift(0.2*l*UP)
                bar_arrows.append(bar_arrow)

        bar_arrows = VGroup(bar_arrows)
        bar_arrows.save_state()
        bar_arrows.shift(bars.get_center() - bars_ori.get_center())
        bar_arrows.set_style_data(
            stroke_color = BLACK, stroke_width = 0,
            fill_color = BLACK, fill_opacity = 0,
        )

        self.play(
            bar_arrows.restore,
            Transform(bars, bars_ori),
            reals_g.shift, 2*DOWN,
        )
        #self.wait_to(60+35.5)

        examples = VGroup(bars, bar_arrows, reals_g)
        self.play(examples.to_edge, LEFT)

        definition_items = VGroup(
            TextMobject("$\\bullet$ edge between every pair"),
            TextMobject("$\\bullet$ no cycles"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        definition_items.to_edge(RIGHT)

        #self.wait_to(60+38.5)
        self.play(FadeIn(definition_items[0]))
        #self.wait_to(60+44.3)
        self.play(FadeIn(definition_items[1]))

        x1, x2 = 2.7, 1.4
        cycle = VGroup(
            make_arrow_to(x1, tip_length = 0.25),
            make_arrow_to(x2, tip_length = 0.25).shift(x1*RIGHT),
            make_arrow_from(x1+x2, tip_length = 0.25),
        )
        cycle.next_to(definition_items, DOWN, buff = 0.5)
        #self.wait_to(60+47)
        self.play(ShowCreation(cycle))

        #self.wait_to(60+51)
        self.play(FadeOut(cycle))

        definition_rect = SurroundingRectangle(definition_items, color = GREEN)
        definition_label = TextMobject("formal definition").next_to(definition_rect, UP)

        self.dither()
        self.play(
            ShowCreation(definition_rect),
            FadeIn(definition_label),
        )
        self.dither(2)
        #self.wait_to(2*60+7.5)

class ExampleSummary(Scene):
    def construct(self):

        title = TextMobject("Subsets of cartesian product").to_edge(UP)
        self.add(title)

        matching_dots = VGroup(Dot() for _ in range(6)).highlight(col_a)
        matching_dots.arrange_submobjects(buff = 0.4)
        matching_dots2 = matching_dots.copy().highlight(col_b)
        matching_dots2.shift(1.5*DOWN)
        random.shuffle(matching_dots2.submobjects)
        matching_lines = VGroup(
            Line(dot1.get_center(), dot2.get_center(), buff = 0.2)
            for dot1, dot2 in zip(matching_dots, matching_dots2)
        )
        matching = VGroup(matching_dots, matching_dots2, matching_lines)

        function = VGroup(
            Axes(x_min = -2, x_max = 2),
            FunctionGraph(lambda x: np.sin(x), x_min = -2, x_max = 2),
        )
        function.scale(0.8)

        point_data = [
            (-0.74, -0.68),
            (-0.61, 0.71),
            (0.3, 0.06),
            (0.68, 0.67),
            (0.5, -0.5),
            (-0.32, 0.03),
        ]
        edge_data = [
            (2,3), (2,4), (2,5), (1,5), (5,0), (0,2), (2,1), (1,0),
        ]
        point_data = np.array([
            point+(0,)
            for point in point_data
        ])*1.5
        dots = VGroup(Dot(point) for point in point_data)
        arrows = VGroup(
            Arrow(point_data[i], point_data[j], tip_length = 0.15)
            for i,j in edge_data
        )
        oriented = VGroup(dots, arrows)

        ordinal = OrdinalSum(OrdinalOmega, 0.5, OrdinalOmega, x0 = -2, x1 = 2)
        ordinal[0][0].highlight(GREEN)
        ordinal[1][0].highlight(YELLOW)

        examples = VGroup(
            [matching, function],
            [oriented, ordinal],
        )
        for column, buff in zip(examples, (0.3, 1)):
            column.arrange_submobjects(DOWN, buff = buff)
        examples.arrange_submobjects(buff = 1)
        examples.shift((SPACE_HEIGHT-title.get_edge_center(DOWN)[1])/2*DOWN)

        #self.wait_to(6.5)
        self.play(FadeIn(examples[0][0]))
        #self.wait_to(8.5)
        self.play(FadeIn(examples[0][1]))
        #self.wait_to(10.5)
        self.play(FadeIn(examples[1][0]))
        #self.wait_to(13)
        self.play(FadeIn(examples[1][1]))
        #self.wait_to(25)
        self.dither(2)

class NextPart(Overview):
    def construct(self):

        self.prepare()
        self.add(
            self.product, self.applications, self.formal_world,
            self.arrow1, self.arrow2,
        )
        self.arrow1.highlight(DARK_GREY)
        self.formal_world.highlight(DARK_GREY)
        self.arrow2.highlight(YELLOW)

        #self.wait_to(5)
        self.play(
            self.arrow1.highlight, YELLOW,
            self.formal_world.highlight, WHITE,
            self.arrow2.highlight, DARK_GREY,
            self.applications.highlight, DARK_GREY,
        )
        #self.wait_to(19.5)

class PartBIntro(Scene):
    def construct(self):

        elements = TexMobject(*[
            "{}_{}".format(let, str(index))
            for let in ('a','b')
            for index in range(3)
        ]).arrange_submobjects(coor_mask = X_MASK)
        elements_a = VGroup(elements[:3]).highlight(col_a)
        elements_b = VGroup(elements[3:]).highlight(col_b)
        elements_a.shift(0.3*LEFT)
        elements_b.shift(0.3*RIGHT)
        rect_b = SurroundingRectangle(elements_b, color = WHITE, buff = 0.2)
        rect_a = rect_b.copy().move_to(elements_a, coor_mask = X_MASK)
        set_a_label = TexMobject('A').highlight(col_a).next_to(rect_a, LEFT)
        set_b_label = TexMobject('B').highlight(col_b).next_to(rect_b, RIGHT)
        sets = VGroup(
            set_a_label, rect_a, elements_a,
            set_b_label, rect_b, elements_b,
        )
        sets.to_edge(UP)
        table = make_pairs_table()
        table = VGroup(reversed(table.submobjects))
        table_rect = SurroundingRectangle(table)
        product_label = TexMobject('A\\times B').next_to(table_rect, UP).highlight(YELLOW)

        self.play(FadeIn(sets))
        #self.wait_to(4.5)
        self.play(
            ShowCreation(table_rect),
            FadeIn(product_label),
            FadeIn(table, submobject_mode = "lagged_start", run_time = 3),
        )
        questions = [
            ("What is ordered pair?",),
            ("Why is there","$A\\times B$","for any","$A$, $B$?",),
        ]
        questions = VGroup(TextMobject(*text) for text in questions)
        questions.arrange_submobjects(DOWN, aligned_edge = LEFT).next_to(table_rect, DOWN, buff = 0.5)
        questions[1][3][0].highlight(col_a)
        questions[1][3][2].highlight(col_b)
        questions[1][1].highlight(YELLOW)

        #self.wait_to(21)
        self.play(FadeIn(questions[0], submobject_mode = "lagged_start", run_time = 2))
        #self.wait_to(24.5)
        self.play(FadeIn(questions[1], submobject_mode = "lagged_start", run_time = 2))
        self.dither(2)
        #self.wait_to(32)

class FormalPairIssues(Scene):
    def construct(self):

        title = TextMobject("Ordered pair").to_edge(UP)
        self.add(title)

        pair = TexMobject("(a,b)").shift(UP)
        pair[1].highlight(col_a)
        pair[3].highlight(col_b)
        box = Rectangle(width = 2, height = 1).shift(DOWN)
        box_label = TextMobject('??').next_to(box, DOWN)
        arrow = Arrow(pair.get_corner(UP+LEFT), pair.get_corner(UP+RIGHT))
        arrow.next_to(pair, UP)

        self.play(FadeIn(pair))
        #self.wait_to(2.5)
        self.play(ShowCreation(box), FadeIn(box_label))
        #self.wait_to(9.7)
        self.play(
            pair[1].shift, 0.3*UP,
            rate_func = there_and_back,
            run_time = 0.5,
        )
        self.play(
            pair[3].shift, 0.3*UP,
            rate_func = there_and_back,
            run_time = 0.5,
        )
        self.play(ShowCreation(arrow))
        #self.wait_to(14.5)

        ordering_text = TextMobject("Ordering").to_edge(RIGHT).shift(DOWN)
        product_text = TextMobject("Cartesian product").to_edge(RIGHT).shift(UP)
        ordering_arrow = Arrow(ordering_text, product_text)
        product_arrow = Arrow(product_text.get_edge_center(UP), title)

        self.play(FadeIn(ordering_text, submobject_mode = "lagged_start"))
        #self.wait_to(20)
        self.play(ShowCreation(ordering_arrow), FadeIn(product_text))
        #self.wait_to(22.3)
        self.play(ShowCreation(product_arrow))
        #self.wait_to(29)

        self.dither()
        self.play(FadeOut(VGroup(
            ordering_text, product_text,
            ordering_arrow, product_arrow,
        )))
        #self.wait_to(32)

        box_points = [
            box.get_edge_center(direction)-direction*box.get_height()/2
            for direction in (LEFT, RIGHT)
        ]
        elements_in_pair = VGroup(pair[1::2])
        elements = elements_in_pair.copy()
        elements.save_state()
        elements.move_to(box)
        for el, point in zip(elements, box_points): el.move_to(point, coor_mask = X_MASK)

        self.play(MoveFromSaved(elements))
        #self.wait_to(41.5)

        elements.save_state()
        elements_in_pair.save_state()
        elements_in_pair_dest = elements_in_pair.copy()
        elements_in_pair_dest[0].move_to(elements_in_pair[1], coor_mask = X_MASK)
        elements_in_pair_dest[1].move_to(elements_in_pair[0], coor_mask = X_MASK)
        elements_in_pair_dest[0].highlight(col_b)
        elements_in_pair_dest[1].highlight(col_a)

        self.play(
            elements[0].highlight, col_b,
            elements[1].highlight, col_a,
            Transform(elements_in_pair, elements_in_pair_dest, path_arc = np.pi/2)
        )
        #self.wait_to(49.7)

        self.play(
            elements.restore,
            ApplyMethod(elements_in_pair.restore, path_arc = -np.pi/2),
        )

        a_rect = Square(side_length = box.get_height()-0.3)
        a_rect.move_to(box_points[0])
        #self.wait_to(57)
        self.play(ShowCreation(a_rect))
        #self.wait_to(60+7)
        self.dither()

        elements.save_state()
        elements_in_pair.save_state()
        a_rect.save_state()
        self.play(
            elements[0].highlight, col_b,
            elements[1].highlight, col_a,
            a_rect.move_to, box_points[1],
            Transform(elements_in_pair, elements_in_pair_dest, path_arc = np.pi/2)
        )
        #self.wait_to(60+12)

        self.play(
            elements.restore,
            a_rect.restore,
            ApplyMethod(elements_in_pair.restore, path_arc = -np.pi/2),
        )
        self.dither()

        #self.wait_to(60+27)
        #counter = Counter()
        #counter.count_from(5, self)

        cd_pair = TexMobject("(c,d)")
        d_space = 0.15
        cd_pair[3].shift(d_space*RIGHT)
        cd_pair[4].shift(2*d_space*RIGHT)
        cd_pair.move_to(pair)

        cd_in_pair = VGroup(cd_pair[1::2])
        cd_in_box = cd_in_pair.copy()
        cd_in_pair[0].set_color(col_a)
        cd_in_pair[1].set_color(col_b)
        cd_in_box.move_to(box)
        for element, point in zip(cd_in_box, box_points):
            element.move_to(point, coor_mask = X_MASK)

        b_rect = a_rect.copy().move_to(box_points[1])

        #self.wait_to(60+35.5)
        self.play(
            FadeIn(b_rect),
            ReplacementTransform(elements, cd_in_box),
        )
        #self.wait_to(60+42.5)

        right_box = SurroundingRectangle(cd_in_pair[1], color = WHITE)
        right_box.highlight(col_b)
        self.play(
            b_rect.highlight, col_b,
            cd_in_box[0].highlight, col_a,
            cd_in_box[1].highlight, col_b,
            ReplacementTransform(pair, cd_pair),
            FadeIn(right_box)
        )
        #self.wait_to(60+49.5)

        cd_in_pair_dest = cd_in_pair.copy()
        for src, dest in zip(cd_in_pair, reversed(cd_in_pair_dest)):
            dest.move_to(src, coor_mask = X_MASK)
            dest.highlight(src.color)

        self.play(
            Transform(cd_in_pair, cd_in_pair_dest, path_arc = np.pi/2),
            b_rect.highlight, WHITE,
            a_rect.highlight, col_b,
            cd_in_box[0].highlight, col_b,
            cd_in_box[1].highlight, col_a,
        )
        #self.wait_to(2*60+5)
        self.dither(2)

        subtitle = TextMobject("Kuratovski definition").next_to(title, DOWN)
        self.play(
            FadeOut(VGroup(
                cd_pair, right_box,
                a_rect, b_rect,
                box, box_label, cd_in_box,
                arrow,
            )),
            Write(subtitle),
        )

class FormalPairKuratowski(Scene):
    def construct(self):

        title = TextMobject("Ordered pair").to_edge(UP)
        subtitle = TextMobject("Kuratovski definition").next_to(title, DOWN)
        self.add(title, subtitle)

        pair = TexMobject("(a,b)")

        ab_in_pair = VGroup(pair[1::2])
        ab_in_pair[0].highlight(col_a)
        ab_in_pair[1].highlight(col_b)
        self.play(FadeIn(pair))

        ab = ab_in_pair.copy()

        buff = 0.2
        ab_rect = SurroundingRectangle(ab, buff = buff, color = col_b)
        ab_g = VGroup(ab, ab_rect)
        a = ab[0].copy()
        a_rect = ab_rect.copy().stretch_to_fit_width(a.get_width()+2*buff)
        a_rect.move_to(a, coor_mask = X_MASK)
        a_rect.highlight(col_a)
        a_g = VGroup(a, a_rect)
        middle_el = VGroup(a_g, ab_g).arrange_submobjects()
        outer_rect = SurroundingRectangle(middle_el, buff = buff, color = WHITE)
        outer_g = VGroup(middle_el, outer_rect)
        outer_g.shift(2*DOWN)

        #self.wait_to(5)
        self.play(ReplacementTransform(ab_in_pair[0].copy(), a))
        self.play(ShowCreation(a_rect))
        #self.wait_to(8.5)
        self.play(ReplacementTransform(ab_in_pair.copy(), ab))
        self.play(ShowCreation(ab_rect))
        #self.wait_to(12)
        self.play(ShowCreation(outer_rect))

        b_in_pair_dest = ab_in_pair[0].copy().move_to(ab_in_pair[1], coor_mask = X_MASK)
        b_in_pair_dest.highlight(col_b)
        ab_in_pair[1].save_state()

        outer_g.save_state()
        b_dest = ab[0].copy().move_to(ab[1], coor_mask = X_MASK).highlight(col_b)

        #self.wait_to(31.8)
        self.play(
            Transform(ab_in_pair[1], b_in_pair_dest),
            Transform(ab[1], b_dest),
        )

        a_dest = a.copy().move_to(ab).fade_to(col_b, 0.5)
        #self.wait_to(41.3)
        self.play(Transform(ab, VGroup(a_dest)))
        self.remove(ab[1])

        square = Square(side_length = ab_rect.get_height())
        square.highlight(col_a)
        square.fade_to(col_b, 0.5)
        square.move_to(ab_rect)
        a_dest = ab[0].copy()
        src = VGroup([[a, a_rect], [ab[0], ab_rect]], outer_rect)
        dest = VGroup(
            [[a_dest, square]],
            SurroundingRectangle(square, color = WHITE, buff = buff),
        )
        dest.move_to(outer_rect)

        #self.wait_to(47.2)
        self.play(Transform(src, dest))
        self.remove(ab, ab_rect)
        #self.wait_to(58.5)
        self.dither(2)
        ab[1].move_to(ab[0])

        self.play(
            ab_in_pair[1].restore,
            outer_g.restore,
        )
        one = TexMobject('1').next_to(a_rect, DOWN, buff = buff*2)
        two = TexMobject('2').next_to(ab_rect, DOWN, buff = buff*2)
        #self.wait_to(60+6.5)
        self.play(FadeIn(one))
        #self.wait_to(60+8)
        self.play(FadeIn(two))

        #self.wait_to(60+10.5)
        self.play(FadeOut(ab_in_pair))
        #self.wait_to(60+13.5)
        self.play(ReplacementTransform(a.copy(), ab_in_pair[0]))
        #self.wait_to(60+17.5)
        self.play(ab[0].highlight, DARK_GREY)
        self.play(ReplacementTransform(ab[1].copy(), ab_in_pair[1]))
        #self.wait_to(60+42.5)
        self.dither(2)

class ConstructionOverview(Scene):
    def construct(self):

        title = TextMobject("Construction of cartesian product")
        title.to_edge(UP)
        self.add(title)

        variants_data = [
            [
                "union of pair,\\\\",
                "powerset,\\\\",
                "selection"
            ],
            [
                "replacement,\\\\",
                "union"
            ],
        ]

        variants = VGroup(
            TextMobject(
                *variant,
                alignment = "\\raggedright"
            )
            for variant in variants_data
        )
        variants.arrange_submobjects(buff = 2, aligned_edge = UP)
        variants.next_to(title, DOWN, buff = 2)
        connections = []
        for variant, direction in zip(variants, (RIGHT, LEFT)):
            end = variant.get_edge_center(UP)
            start = end*X_MASK + title.get_edge_center(DOWN)*Y_MASK + 0.9*direction
            connections.append(Line(start, end, color = YELLOW, buff = 0.2))
        connections = VGroup(connections)

        #self.wait_to(3)
        self.play(ShowCreation(connections[0]))
        axioms = variants[0]
        self.play(FadeIn(axioms, submobject_mode = "lagged_start", run_time = 2))
        #self.wait_to(7)
        #self.play(FocusOn2(axioms[1], scale = 1.1))
        #self.play(FocusOn2(axioms[2], scale = 1.1))
        self.dither(2)

        #self.wait_to(11.5)
        self.play(ShowCreation(connections[1]))
        axioms = variants[1]
        self.play(FadeIn(axioms, submobject_mode = "lagged_start", run_time = 2))
        #self.wait_to(17)
        #self.play(FocusOn2(axioms[0], scale = 1.1))
        self.dither(2)

        #self.wait_to(19)
        self.play(
            VGroup(connections, title, variants[1]).behind_edge, UP,
            variants[0].to_corner, UP+LEFT,
        )
        #self.wait_to(20.5)

class BruteForceConstruction(Scene):
    def construct(self):

        axioms = TextMobject(
            "union of pair,\\\\",
            "powerset,\\\\",
            "selection",
            alignment = "\\raggedright",
        ).to_corner(UP+LEFT)

        self.add(axioms)

        elements = TexMobject("a_0", "a_1", "a_2", "b_0", "b_1", "b_2")
        elements.arrange_submobjects(buff = 0.2, coor_mask = X_MASK)
        elements_a = VGroup(elements[:3])
        elements_b = VGroup(elements[3:])

        elements_a.highlight(col_a)
        elements_b.highlight(col_b)
        rect_b = SurroundingRectangle(elements_b, color = col_b, buff = 0.2)
        rect_a = rect_b.copy().move_to(elements_a, coor_mask = X_MASK)
        rect_a.highlight(col_a)
        VGroup(
            [elements_a, rect_a],
            [elements_b, rect_b],
        ).arrange_submobjects().to_edge(UP).shift(RIGHT)

        self.play(FadeIn(elements_a), FadeIn(rect_a))
        self.play(FadeIn(elements_b), FadeIn(rect_b))

        elements_rect = SurroundingRectangle(VGroup(rect_a, rect_b), color = WHITE)
        #self.wait_to(4)
        self.play(ShowCreation(elements_rect))
        self.play(Uncreate(rect_a), Uncreate(rect_b))
        #self.wait_to(7)
        self.play(FocusOn2(axioms[0], scale = 1.1))

        buff = 0.2
        ab_template = VGroup(elements_a[0], elements_b[0]).copy()
        ab_template.arrange_submobjects(buff = buff, coor_mask = X_MASK)
        rect_ab = SurroundingRectangle(ab_template, buff = buff, color = WHITE)
        rect_a = rect_ab.copy()
        rect_a.stretch_to_fit_width(ab_template[0].get_width()+2*buff)
        rect_a.move_to(ab_template[0], coor_mask = X_MASK)

        def make_ab(a, b):
            a_mob = elements_a[a].copy()
            a_mob.shift(ab_template[0][0].get_center() - a_mob[0].get_center())
            b_mob = elements_b[b].copy()
            b_mob.shift(ab_template[1][0].get_center() - b_mob[0].get_center())
            return VGroup(a_mob, b_mob, rect_ab.copy())

        def make_a(a):
            a_mob = elements_a[a].copy()
            a_mob.shift(ab_template[0][0].get_center() - a_mob[0].get_center())
            return VGroup(a_mob, rect_a.copy())

        table = [[make_a(a) for a in range(3)]]
        for b in range(3):
            table.append([make_ab(a,b) for a in range(3)])
        table = VGroup(table)
        for column in table: column.arrange_submobjects(DOWN)
        table.arrange_submobjects()

        dots = TexMobject("\\cdots")
        dots.add(SurroundingRectangle(dots, stroke_width = 0, buff = 0.3))
        dots.next_to(table, DOWN)
        table_g = VGroup(table, dots)

        table_rect = SurroundingRectangle(table_g, color = GREY)
        table_g.add(table_rect)

        table_g.next_to(elements_rect, DOWN, buff = 1.5, aligned_edge = LEFT)
        arrow = Arrow(elements_rect.get_corner(DOWN+LEFT), table_rect.get_corner(UP+LEFT))
        arrow.shift(elements_rect.get_width()/2 * RIGHT)
        arrow_label = TexMobject("\\mathcal P").next_to(arrow)
        arrow_g = VGroup(arrow, arrow_label)

        #self.wait_to(11.5)
        self.play(FocusOn2(axioms[1], scale = 1.1))
        
        #self.wait_to(13.5)
        self.play(
            ShowCreation(arrow),
            FadeIn(arrow_label),
            ShowCreation(table_rect),
        )
        #self.wait_to(16.5)
        self.play(
            FadeIn(table[0], submobject_mode = "lagged_start", run_time = 2)
        )
        #self.wait_to(22)
        self.play(
            FadeIn(VGroup(table[1:]), submobject_mode = "lagged_start", run_time = 2)
        )
        #self.wait_to(27.5)
        self.play(ShowCreation(dots))

        #self.wait_to(31)
        dots2 = dots.copy()
        table_g.save_state()
        table_g.scale(0.7, about_point = table_g.get_edge_center(LEFT))
        table_g.to_edge(UP)
        self.play(
            MoveFromSaved(table_g),
            ApplyMethod(VGroup(
                elements, elements_rect, arrow_g
            ).behind_edge, UP, remover = True),
        )

        pairs = [
            TexMobject("(a_{},b_{})".format(a,b))
            for a in range(3)
            for b in range(3)
        ]
        for pair in pairs:
            VGroup(pair[1:3]).highlight(col_a)
            VGroup(pair[4:6]).highlight(col_b)

        pairs_r1 = VGroup(pairs[:5]).arrange_submobjects()
        pairs_r2 = VGroup(pairs[5:]).arrange_submobjects()
        pairs = VGroup(pairs_r1, pairs_r2, dots2).arrange_submobjects(DOWN)
        pairs_rect = SurroundingRectangle(pairs, color = GREY)
        pairs.add(pairs_rect)
        pairs.to_edge(DOWN)

        start = table_rect.get_edge_center(DOWN)
        end = pairs_rect.get_edge_center(UP)
        x = (start[0]+end[0])/2
        start[0] = x
        end[0] = x
        arrow = Arrow(start, end)
        arrow_label.next_to(arrow)

        self.play(
            ShowCreation(arrow),
            FadeIn(arrow_label),
            ShowCreation(pairs_rect),
        )

        expanded_a = make_a(0)
        expanded_ab = make_ab(0,0)
        expanded_aab = VGroup(expanded_a, expanded_ab).arrange_submobjects()
        expanded_rect = SurroundingRectangle(expanded_aab, buff = 0.15, color = YELLOW)
        expanded = VGroup(expanded_aab, expanded_rect)

        expanded.shift(
            pairs_rect.get_corner(UP+LEFT)
            - expanded.get_corner(UP+LEFT)
            + 0.1*(RIGHT+DOWN)
        )

        #self.wait_to(39.8)
        self.play(
            ShowCreation(expanded_rect),
            ReplacementTransform(table[0][0].copy(), expanded_a),
            ReplacementTransform(table[1][0].copy(), expanded_ab),
        )

        cur_pair = pairs_r1[0]
        cur_pair.save_state()
        eq = TexMobject('=').next_to(expanded)
        cur_pair.next_to(eq)

        #self.wait_to(43)
        self.play(FadeIn(eq), FadeIn(cur_pair))
        #self.wait_to(47)
        self.play(
            FadeOut(VGroup(eq, expanded)),
            cur_pair.restore,
        )
        #self.wait_to(50)
        self.play(
            FadeIn(
                VGroup(pairs_r1[1:], pairs_r2),
                submobject_mode = "lagged_start",
                run_time = 2,
            ),
        )
        #self.wait_to(55.5)
        self.play(ShowCreation(dots2))

        #self.wait_to(60+2.8)
        self.play(FocusOn2(axioms[2], scale = 1.1))

        #self.wait_to(60+16)
        self.dither()

        pairs.remove(dots2)
        pairs_rect.save_state()
        self.play(
            FadeOut(dots2),
            Transform(
                pairs_rect,
                SurroundingRectangle(
                    VGroup(pairs_r1, pairs_r2),
                    color = GREY,
                ),
            ),
        )

        product_label = TexMobject("A\\times B")
        product_label[0].highlight(col_a)
        product_label[2].highlight(col_b)
        product_label.next_to(pairs_rect, UP, aligned_edge = RIGHT)
        #self.wait_to(60+18)
        self.play(Write(product_label))

        #self.wait_to(60+26.5)
        expanded.next_to(pairs_rect, UP, aligned_edge = LEFT).shift(LEFT)
        self.play(
            ReplacementTransform(VGroup(pairs_r1[0][1:3]).copy(), expanded_a[0]),
            ReplacementTransform(VGroup(pairs_r1[0][1:3]).copy(), expanded_ab[0]),
            ReplacementTransform(VGroup(pairs_r1[0][4:6]).copy(), expanded_ab[1]),
            FadeIn(expanded_a[-1]),
            FadeIn(expanded_ab[-1]),
            FadeIn(expanded_rect),
        )
        #self.wait_to(2*60+1)
        self.dither(2)

        everything = VGroup(
            expanded,
            table_g,
            arrow, arrow_label,
            pairs, product_label,
            axioms,
        )

        axioms2 = TextMobject(
            "replacement,\\\\",
            "union",
            alignment = "\\raggedright",
        ).to_corner(UP+RIGHT)

        self.play(
            everything.behind_edge, LEFT,
            UnapplyMethod(axioms2.behind_edge, RIGHT),
        )

class ReplacementConstruction(Scene):
    def construct(self):

        axioms = TextMobject(
            "replacement,\\\\",
            "union",
            alignment = "\\raggedright",
        ).to_corner(UP+RIGHT)
        self.add(axioms)

        table = make_pairs_table()
        elements_a = VGroup(
            pair[1].copy().next_to(pair, UP, buff = 1.5)
            for pair in table[-1]
        )
        elements_b = VGroup(
            row[0][3].copy().next_to(row, LEFT, buff = 1.5)
            for row in table
        )
        arrows_a = VGroup(
            Arrow(a, pair)
            for a, pair in zip(elements_a, table[-1])
        )
        arrows_b = VGroup(
            Arrow(b, row)
            for b,row in zip(elements_b, table)
        )

        el_a = elements_a[0].copy()
        self.play(Write(el_a))
        self.play(FocusOn2(el_a))
        #self.wait_to(6.5)
        el_b = elements_b[0].copy()
        self.play(FadeIn(el_b))
        #self.wait_to(10.5)
        self.play(ShowCreation(arrows_b[0]), FadeIn(table[0][0]))

        for i in range(1,3):
            self.play(Transform(el_b, elements_b[i]))
            self.play(
                ShowCreation(arrows_b[i]),
                FadeIn(table[i][0]),
            )
        #self.wait_to(21)

        rect_b = SurroundingRectangle(elements_b, buff = 0.3, color = col_b)
        set_b_label = TexMobject('B').highlight(col_b).next_to(rect_b, UP)
        self.play(
            FadeIn(elements_b),
            FadeIn(set_b_label),
            ShowCreation(rect_b),
            axioms[0].highlight, YELLOW,
        )
        self.remove(el_b)

        column_rects = VGroup(
            SurroundingRectangle(VGroup(column), color = col_b)
            for column in zip(*table)
        )
        #self.wait_to(22.5)
        self.play(ReplacementTransform(rect_b, column_rects[0]))
        #self.wait_to(31)

        self.dither()
        self.play(FadeOut(VGroup(arrows_b, elements_b, set_b_label)))
        #self.wait_to(34)
        self.play(ShowCreation(arrows_a[0]))
        #self.wait_to(36.5)
        for i in range(1,3):
            self.play(Transform(el_a, elements_a[i]))
            self.play(
                ShowCreation(arrows_a[i]),
                FadeIn(column_rects[i]),
                FadeIn(VGroup(row[i] for row in table))
            )

        #self.wait_to(43)
        rect_a = SurroundingRectangle(elements_a, buff = 0.3, color = col_a)
        set_a_label = TexMobject('A').highlight(col_a).next_to(rect_a, LEFT)
        self.play(
            FadeIn(elements_a),
            FadeIn(set_a_label),
            ShowCreation(rect_a),
        )
        self.remove(el_a)

        product_rect = SurroundingRectangle(column_rects, buff = 0.2, color = WHITE)
        #self.wait_to(54.5)
        self.play(ReplacementTransform(rect_a, product_rect))

        #self.wait_to(60+2)
        self.play(
            FadeOut(VGroup(elements_a, set_a_label, arrows_a)),
            axioms[0].highlight, WHITE,
            Animation(product_rect),
        )
        #self.wait_to(60+8.5)
        self.play(axioms[1].highlight, YELLOW)
        #self.wait_to(60+11)
        self.play(Uncreate(column_rects, submobject_mode = "all_at_once"))

        product_label = TexMobject("A\\times B")
        product_label[0].highlight(col_a)
        product_label[2].highlight(col_b)
        product_label.next_to(product_rect, DOWN, aligned_edge = RIGHT)

        #self.wait_to(60+15.5)
        self.play(FadeIn(product_label))
        #self.wait_to(60+33)
        self.dither(2)

class NextChapter(Scene):
    def construct(self):

        naturals = VGroup(
            TexMobject(str(i)) for i in range(20)
        ).arrange_submobjects(buff = 0.5).to_corner(UP+LEFT)

        self.play(ShowCreation(naturals))

        nine_in_row = naturals[9]
        nine = nine_in_row.copy()
        #self.wait_to(13.7)
        self.play(
            nine_in_row.highlight, YELLOW,
            nine.center,
        )

        nine_set = VGroup(naturals[:9]).copy().center()
        nine_set.highlight(GREY)
        nine_set[7].highlight(WHITE)
        nine_rect = SurroundingRectangle(nine_set, buff = 0.5, color = WHITE)
        self.play(
            GrowFromCenter(nine_set),
            ReplacementTransform(nine, nine_rect),
        )
        #self.wait_to(23)
