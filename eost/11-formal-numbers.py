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

class Chapter11OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 11\\\\Formal Numbers",
    }

class Chapter11OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Everything is nothing, with a twist.",
        ],
        "highlighted_quote_terms" : {
            "twist." : GREEN,
        },
        "author" : "Kurt Vonnegut"
    }

colors = [GREY, GREEN, YELLOW, ORANGE, RED, PURPLE, BLUE]
def rect_color(n):
    if n == 0: return colors[0]
    n = (n-1) % (len(colors)-1)
    return colors[n+1]

class FirstAttempt(Scene):
    def construct(self):

        title = TextMobject("Sets").scale(1.2).to_edge(UP)
        self.play(Write(title))

        rect = Square(side_length = 0.5, color = rect_color(0))
        rects = [rect]
        for c in range(1, 10):
            rect = SurroundingRectangle(rect, color = rect_color(c))
            rects.append(rect)

        #self.wait_to(4.5)
        self.play(GrowFromCenter(rects[0]))
        #self.wait_to(6.5)
        self.play(ShowCreation(rects[1]))

        naturals = VGroup(TexMobject(str(n)) for n in range(9))
        naturals.arrange_submobjects(buff = 1.2)
        naturals.to_corner(LEFT+DOWN).shift(RIGHT)

        #self.wait_to(11)
        self.play(ShowCreation(naturals))

        nat_rects = VGroup(
            VGroup(rects[:i+1]).copy().move_to(nat)
            for i,nat in enumerate(naturals)
        )
        max_len = 1.2
        for rect in nat_rects:
            if rect.get_width() > max_len:
                rect.scale_to_fit_width(max_len)
        nat_rects.next_to(naturals, UP, coor_mask = Y_MASK)

        #self.wait_to(26)
        self.play(
            FadeOut(rects[1]),
            ReplacementTransform(rects[0], nat_rects[0][0]),
        )

        for i,t in zip(range(1,3), (32, 36)):
            #self.wait_to(t)
            self.play(
                ReplacementTransform(
                    nat_rects[i-1].copy(),
                    VGroup(nat_rects[i][:i])
                )
            )
            self.play(ShowCreation(nat_rects[i][i]))

        #self.wait_to(39)
        self.play(FadeIn(VGroup(nat_rects[i+1:])))


        omega_rects = VGroup(
            Square(
                side_length = 0.6 + 1.4*0.85**i,
                stroke_width = 4 * 0.95**i,
                color = rect_color(-1-i),
            )
            for i in range(20)
        )
        for square in omega_rects:
            square.fade(1 - square.stroke_width/4)

        omega_p1_rects = omega_rects.copy()
        omega_p1_rects.add(Square(side_length = 0.5))
        ordinal_rects = VGroup(omega_rects, omega_p1_rects).arrange_submobjects(buff = 0.5)

        omega_label = TexMobject("\\omega").next_to(omega_rects, UP)
        omega_p1_label = TexMobject("\\omega+1").next_to(omega_p1_rects, UP)

        #self.wait_to(54)
        self.play(FadeIn(omega_label))
        #self.wait_to(59.5)
        self.play(FadeIn(omega_rects))
        #self.wait_to(60.5)
        self.play(FadeIn(VGroup(omega_p1_label, omega_p1_rects)))

        cross = Cross(color = RED).replace(ordinal_rects, stretch = True)
        #self.wait_to(60+22)
        self.play(
            ordinal_rects.fade, 0.7,
            ShowCreation(cross),
        )

        #self.wait_to(60+24.5)
        self.dither()

        n = 4
        number_label = naturals[n]
        number_rects = nat_rects[n]
        naturals.remove(number_label)
        nat_rects.remove(number_rects)
        self.play(FadeOut(VGroup(
            ordinal_rects, cross,
            omega_label, omega_p1_label,
            naturals, nat_rects,
        )))

        apples = VGroup(Apple(i) for i in range(n))
        apples.arrange_submobjects(buff = 0.4)

        #self.wait_to(60+32.5)
        if self.skip_animations: self.add(apples)
        else:
            for apple in apples:
                apple.save_state()
                apple.scale_in_place(0)
            self.play(
                Succession(
                    *[ApplyMethod(apple.restore) for apple in apples],
                    rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME
                )
            )

        starts = [
            apple.get_edge_center(DOWN)
            for apple in apples
        ]
        ends = [
            interpolate(
                number_rects.get_corner(UP+LEFT),
                number_rects.get_corner(UP+RIGHT),
                alpha
            )
            for alpha in np.linspace(0,1, n)
        ]
        matching = VGroup(
            Line(start, end, buff = 0.2)
            for start, end in zip(starts, ends)
        )
        #self.wait_to(60+37.5)
        self.play(ShowCreation(matching))
        #self.wait_to(60+46)

        end = number_rects.get_edge_center(UP)
        ends = [
            start*X_MASK + end*Y_MASK
            for start in starts
        ]
        matching_dest = VGroup(
            Line(start, end, buff = 0.2)
            for start, end in zip(starts, ends)
        )
        number_rects.save_state()

        rect = number_rects[-1]
        rect.stretch_to_fit_width(apples.get_width()+0.5)
        rect.move_to(apples, coor_mask = X_MASK)

        rect = VGroup(number_rects[:-1])
        rect[-1].set_fill(opacity = 0.5)
        rect.scale_in_place(0.7)
        rect.move_to(ends[2], coor_mask = X_MASK)

        self.play(
            Transform(matching, matching_dest),
            MoveFromSaved(number_rects),
        )
        #self.wait_to(2*60+6)
        self.play(
            title.behind_edge, UP,
            VGroup(apples, matching, number_rects, number_label).behind_edge, DOWN,
        )

class NaturalsDefinition(Scene):
    def construct(self):

        naturals = VGroup(TexMobject(str(n)) for n in range(7))
        naturals.arrange_submobjects(DOWN, buff = 0.7)
        naturals.to_corner(UP+LEFT)

        sets = []
        max_h = 1.0
        for i,nat in enumerate(naturals):
            if len(sets) == 0:
                cur_set = Square(side_length = 0.5, color = rect_color(i))
            else:
                elements = VGroup(sets).copy().arrange_submobjects()
                rect = SurroundingRectangle(elements, color = rect_color(i))
                cur_set = VGroup(elements, rect)

            if cur_set.get_height() > max_h: cur_set.scale_to_fit_height(max_h)
            cur_set.next_to(nat)
            sets.append(cur_set)

        sets = VGroup(sets)

        self.play(
            FadeIn(naturals[0]), GrowFromCenter(sets[0]),
        )
        #self.wait_to(3.3)
        self.play(
            Transform(sets[0].copy(), sets[1][0][0]),
            FadeIn(naturals[1]),
        )
        #self.wait_to(4.7)
        self.play(ShowCreation(sets[1][1]))

        #self.wait_to(9.5)
        self.play(
            FadeIn(naturals[2]),
            ShowCreation(sets[2][1]),
        )
        #self.wait_to(17.7)
        self.play(FocusOn2(naturals[0]), run_time = 0.5)
        self.play(FocusOn2(naturals[1]), run_time = 0.5)
        #self.wait_to(20)
        self.play(Transform(VGroup(sets[:2]).copy(), sets[2][0]))

        #self.wait_to(24.5)
        self.play(
            FadeIn(naturals[3]),
            Transform(VGroup(sets[:3]).copy(), sets[3][0]),
        )
        self.play(ShowCreation(sets[3][1]))

        #self.wait_to(29)
        for i in range(4, len(sets)):
            self.play(
                FadeIn(naturals[i]),
                FadeIn(sets[i][1]),
                Transform(VGroup(sets[:i]).copy(), sets[i][0]),
            )

        conversation = Conversation(self)
        conversation.add_bubble("Agrh, I cannot imagine that!")
        self.dither(2)
        #self.wait_to(38)
        conversation.add_bubble("You don't have to draw it this way.")
        self.dither(2)

        #self.wait_to(49.5)

        n = 5
        number_text = TexMobject(str(n)).scale(1.5)
        number_elements = VGroup(TexMobject(str(i)) for i in range(n))
        number_elements.arrange_submobjects()
        number_elements.scale(1.3)
        VGroup(number_elements, number_text).shift(2*UP+2*RIGHT)
        number_rect = SurroundingRectangle(number_elements, stroke_color = GREY, buff = 0.2)
        number_rect.save_state()
        number_rect.scale_in_place(0)
        number_rect.set_fill(opacity = 1)

        self.play(FadeIn(number_text))
        #self.wait_to(52.3)
        self.play(
            GrowFromCenter(number_elements),
            number_rect.restore,
            Transform(number_text, number_rect.saved_state.copy(), remover = True),
        )
        self.dither(2)
        #self.wait_to(59.5)

class Code(VMobject):
    def __init__(self, code, base_line = 0.5):
        VMobject.__init__(self)
        for i, line in enumerate(code.split('\n')):
            if line.strip() == '': continue
            line_obj = TexMobject(":"+line,
                                  template_tex_file = TEMPLATE_VERBATIM_FILE,
                                  should_center = False)
            line_obj.shift(i*base_line * DOWN - line_obj[0].get_center())
            line_obj.remove(line_obj[0])
            line_obj.code = line
            self.add(line_obj)

        self.center()
        self.scale(0.65)

class ProgrammingExcursion(Scene):
    def construct(self):

        python_code_data = """
Python 2.7.12
Type "help", "copyright", "credits" or "license" for more information.
>>> range(5)
[0, 1, 2, 3, 4]
>>> for i in range(5): print "|" + "-"*i + "|"
||
|-|
|--|
|---|
|----|
"""        
        st_code_data = """
Set Theory ZFC
>>> 5
5 = {0, 1, 2, 3, 4}
"""

        python_code = Code(python_code_data)
        st_code = Code(st_code_data)

        python_title = TextMobject("Python").next_to(python_code, UP, buff = 0.5)
        st_title = TextMobject("Set theory").next_to(st_code, UP, buff = 0.5)
        python = VGroup(python_code, python_title).to_edge(UP)
        st = VGroup(st_code, st_title).next_to(python, DOWN, buff = -0.5)

        self.play(FadeIn(python_title, submobject_mode = "lagged_start"))
        self.cursor = SurroundingRectangle(
            python_code[0][0],
            buff = 0, color = WHITE, fill_opacity = 1, stroke_width = 0,
        )
        self.cursor.scale(np.array([0.9, 1.2, 1]))

        self.add(python_code[0])
        self.dither(0.1)
        self.add(python_code[1])
        self.dither(0.1)
        self.row = python_code[2]
        self.prepare_row()

        self.dither()
        #self.wait_to(5.5)

        self.write_row()

        self.dither()
        #self.wait_to(14)

        self.remove(self.cursor)
        self.dither(0.1)
        self.add(python_code[3])

        self.dither()
        #self.wait_to(17)
        self.row = python_code[4]
        self.prepare_row()
        self.dither()

        self.write_row()
        self.dither()

        self.remove(self.cursor)
        self.dither(0.1)
        for row in python_code[5:]:
            self.add(row)
            self.dither(0.1)

        self.dither()
        #self.wait_to(28.5)

        self.play(FadeIn(st_title, submobject_mode = "lagged_start"))
        self.add(st_code[0])
        self.dither(0.1)
        self.row = st_code[1]
        self.prepare_row()

        self.dither()
        #self.wait_to(35.5)
        self.write_row()

        self.dither()
        #self.wait_to(37.3)
        self.remove(self.cursor)
        self.dither(0.1)
        self.add(st_code[2])

        self.dither()
        #self.wait_to(52)

    def prepare_row(self):
        self.add(*self.row[:3])
        self.dither(0.1)
        self.move_cursor(4)
        self.add(self.cursor)

    def move_cursor(self, i):
        point = self.row[0].get_center()
        point += i*(self.row[1].get_center() - point)
        self.cursor.move_to(point)

    def write_row(self):

        i = 4
        j = 3

        while i < len(self.row.code):

            if self.row.code[i].isalpha():
                self.dither(0.05*random.randint(1,3))
            else:
                self.dither(0.05*random.randint(3,5))

            if self.row.code[i] != ' ':
                self.add(self.row[j])
                j += 1

            i += 1
            self.move_cursor(i)

class ExtensionToOrdinals(Scene):
    def construct(self):

        bars = OrdinalOmega()
        naturals = bars.add_descriptions(lambda n: TexMobject(str(n)),
                                         direction = UP, size = 0.5)
        omega_inside = VGroup(bars, naturals)

        omega_rect = SurroundingRectangle(omega_inside, color = GREEN, buff = 0.5)
        omega_label = TexMobject("\\omega").highlight(GREEN)
        omega_label.next_to(omega_rect, UP+RIGHT).shift(DOWN)

        self.play(ShowCreation(omega_rect), FadeIn(omega_label))
        #self.wait_to(3)
        self.play(ShowCreation(bars))
        #self.wait_to(6)
        self.play(FadeIn(naturals))
        #self.wait_to(22)
        
        omega_bar = bars[0].copy().next_to(bars)
        omega_src = VGroup(omega_rect, bars.copy(), naturals.copy())
        omega_src.save_state()
        omega_src.replace(omega_bar, stretch = True)
        omega_src.highlight(WHITE)
        omega_rect.set_fill(opacity = 0.3)
        omega_label.save_state()
        omega_label.next_to(omega_bar, UP)
        omega_label.highlight(WHITE)

        self.play(
            MoveFromSaved(omega_label),
            MoveFromSaved(omega_src, remover = True),
        )
        self.add(omega_bar)
        self.dither()

        omega_p1_inside = VGroup(bars, naturals, omega_bar, omega_label)
        omega_p1_rect = SurroundingRectangle(omega_p1_inside, color = GREEN, buff = 0.5)
        omega_p1_label = TexMobject("\\omega+1").highlight(GREEN)
        omega_p1_label.next_to(omega_p1_rect.get_corner(UP+RIGHT), UP)
        self.play(
            ShowCreation(omega_p1_rect),
            FadeIn(omega_p1_label),
        )
        #self.wait_to(28.9)

        omega_p1_label.save_state()
        omega_p1_src = VGroup(omega_p1_rect, omega_p1_inside.copy())
        omega_p1_src.save_state()

        omega_p1_bar = omega_bar.copy()
        omega_p1_label.next_to(omega_p1_bar, UP)
        VGroup(omega_p1_bar, omega_p1_label).next_to(omega_label, buff = 0.5, coor_mask = X_MASK)
        omega_p1_label.highlight(WHITE)

        omega_p1_src.replace(omega_p1_bar, stretch = True)
        omega_p1_src.highlight(WHITE)
        omega_p1_rect.set_fill(opacity = 0.3)

        self.play(
            MoveFromSaved(omega_p1_label),
            MoveFromSaved(omega_p1_src, remover = True),
        )
        self.add(omega_p1_bar)
        self.dither()

        #self.wait_to(33)
        self.play(FadeOut(VGroup(
            naturals, omega_label, omega_p1_label,
        )))

        supremum_title = TextMobject("Supremum $=$ Union").to_edge(UP)
        #self.wait_to(37.5)
        self.play(FadeIn(supremum_title))

        supremum = OrdinalFiniteProd(OrdinalOmega, 2, q = (0.8, 0.9, 0.9))
        ordinals = []
        for num, bars_x1 in zip(range(2,10), np.linspace(bars.x1, 0, 6)):
            x1 = omega_p1_bar.get_center()[0] - omega_bar.get_center()[0] + bars.x1
            x1 += (x1-bars_x1)/(num-1)
            ratio = (bars_x1-bars.x0) / (x1-bars.x0)
            ordinal = OrdinalSum(
                OrdinalOmega, ratio, lambda **kwargs: OrdinalFinite(num, **kwargs),
                x0 = bars.x0,
                x1 = x1,
            )
            ordinal[1].shift(RIGHT*(omega_bar.get_center()[0] - bars.x1))
            ordinals.append(ordinal)

        ordinals.append(supremum.copy())
        ordinals = VGroup(ordinals)

        self.add(ordinals[0])
        self.remove(bars, omega_bar, omega_p1_bar)

        for i,ordinal in enumerate(ordinals[1:]):
            ordinal.stretch(0.5 * 0.7**i, 1)
        ordinals.arrange_submobjects(DOWN, center = False, coor_mask = Y_MASK, buff = 0.1)

        #self.wait_to(40)
        self.play(FadeIn(VGroup(
            ordinals[1:-1],
            submobject_mode = "lagged_start",
            run_time = 1.5,
        )))

        #self.wait_to(46.2)
        ordinals.save_state()

        supremum[0].align_submobjects(ordinals[0][0])
        ordinals.save_state()

        for ordinal in ordinals:
            for part, spart in zip(ordinal, supremum):
                for bar, dest in zip(part, spart):
                    bar.move_to(dest, coor_mask = X_MASK)

        self.play(MoveFromSaved(ordinals))
        #self.wait_to(48.2)
        self.play(
            Transform(
                ordinals,
                VGroup(
                    [
                        supremum[0].copy(),
                        VGroup(supremum[1][:len(ordinal[1])]).copy(),
                    ]
                    for ordinal in ordinals
                ),
                remover = True,
            )
        )
        self.add(supremum)
        #self.wait_to(53)

        self.play(FadeOut(supremum_title))

class Chapter5Reminder(Scene):
    def construct(self):

        ordinal = OrdinalFiniteProd(OrdinalOmega, 2, q = (0.8, 0.9, 0.9))
        self.add(ordinal)

        series = VideoSeries(num_videos = 16).to_edge(UP)
        cur_chap = series[4]
        cur_chap.remove(cur_chap[1])
        cur_chap_num = TexMobject('5').replace(cur_chap, dim_to_match = 1)
        cur_chap_num.scale_in_place(0.7)
        cur_chap.add(cur_chap_num)
        cur_chap.highlight(YELLOW)

        #self.play(UnapplyMethod(series.behind_edge, UP))

        subord = VGroup(ordinal[0], ordinal[1][:3])
        brace = BraceDesc(subord, "\\omega+3", DOWN)
        #self.wait_to(5.5)
        self.play(brace.creation_anim())
        ordinal.highlight(DARK_GREY)
        subord.highlight(WHITE)
        #self.wait_to(9.5)

        bar = ordinal[1][3].copy().highlight(YELLOW)
        pointer = TrianglePointer().next_to(bar, UP)
        bar_label = TexMobject("\\omega+3").next_to(pointer, UP)
        pointer_g = VGroup(pointer, bar_label).highlight(YELLOW)
        pointer_g.save_state()
        pointer_g.shift(LEFT)
        pointer_g.set_fill(opacity = 0)
        self.play(
            pointer_g.restore,
            ShowCreation(bar),
        )
        self.remove(bar)
        ordinal[1][3].highlight(YELLOW)

        #self.wait_to(16)
        subord_dest = VGroup(
            subord[0].copy(),
            [subord[1][0].copy() for _ in subord[1]],
        )
        subord_dest[1].arrange_submobjects(
            buff = (subord[1][-1].get_center()[0] - subord[1][0].get_center()[0])/(len(subord[1])-1),
            center = False,
        )
        brace2 = Brace(subord_dest, UP)
        VGroup(subord_dest, brace2).shift(
            bar.get_edge_center(DOWN)
            - brace2.get_tip()
            + 0.005*RIGHT
        )

        subord = subord.copy()
        subord.save_state()
        brace.save_state()
        VGroup(
            subord, brace,
        ).shift(
            Y_MASK*(subord_dest.get_center() - subord.get_center())
        )
        brace.highlight(BLACK)
        self.play(
            MoveFromSaved(subord),
            MoveFromSaved(brace, remover = True),
        )

        #self.wait_to(17.5)
        self.play(
            Transform(subord, subord_dest),
            GrowFromCenter(brace2),
        )

        #self.wait_to(22)

        subord.save_state()
        path_start = subord.get_center()
        subord.replace(bar, stretch = True)
        subord.highlight(YELLOW)
        self.play(
            MoveFromSaved(subord, rate_func = smooth),
            MoveAlongPath(subord, Line(path_start, bar.get_center()), rate_func = rush_into),
            brace2.scale_about_point, 0, np.array(brace2.get_tip()),
        )
        self.remove(brace2, subord)

        #self.wait_to(24)
        self.play(
            #series.behind_edge, UP,
            ordinal.highlight, DARK_GREY,
            FadeOut(pointer_g),
        )

class GraphView(Scene):
    def construct(self):

        ordinal = OrdinalFiniteProd(OrdinalOmega, 2, q = (0.8, 0.9, 0.9))
        self.add(ordinal)

        ineq = TexMobject("\\alpha < \\beta")
        ineq.next_to(ordinal, DOWN)
        a_bar = ordinal[0][8]
        a_bar_copy = a_bar.copy()
        b_bar = ordinal[1][1]
        b_bar_copy = b_bar.copy()
        ineq[0].move_to(a_bar, coor_mask = X_MASK)
        ineq[2].move_to(b_bar, coor_mask = X_MASK)
        ineq[1].move_to(VGroup(ineq[0], ineq[2]), coor_mask = X_MASK)

        #self.wait_to(5)
        ordinal.highlight(DARK_GREY)
        self.play(FadeIn(ineq[0]), ShowCreation(a_bar_copy))
        self.play(FadeIn(ineq[2]), ShowCreation(b_bar_copy))
        self.remove(a_bar_copy, b_bar_copy)
        VGroup(a_bar, b_bar).highlight(WHITE)

        #self.wait_to(10)
        self.play(Write(ineq[1]))
        #self.wait_to(13.5)

        alpha = ineq[0].copy()
        beta = ineq[2].copy()
        alpha.save_state()
        beta.save_state()
        buff = 0.2
        left = ordinal.get_edge_center(LEFT)+buff*LEFT
        right = beta.get_edge_center(LEFT)+buff*LEFT
        b_rect = Rectangle(height = alpha.get_height()+2*buff, width = right - left)
        b_rect.shift(X_MASK * (left+right)/2)
        b_rect.move_to(beta, coor_mask = Y_MASK)
        alpha.move_to(b_rect, coor_mask = Y_MASK)

        VGroup(alpha, beta, b_rect).next_to(ineq, DOWN, coor_mask = Y_MASK)

        self.play(
            MoveFromSaved(beta),
            ShowCreation(b_rect),
        )
        #self.wait_to(16.5)
        self.play(MoveFromSaved(alpha))
        #self.wait_to(24.5)

        ab_arrow = Arrow(alpha, beta, color = BLUE)
        b_rect.save_state()
        b_rect.scale(0, about_point = b_rect.get_edge_center(RIGHT))
        b_rect.highlight(BLACK)
        self.play(
            MoveFromSaved(b_rect, remover = True),
            ShowCreation(ab_arrow),
            Animation(alpha),
        )

        angle = np.pi*0.3
        arc_template = Arc(
            -angle,
            start_angle = np.pi/2 + angle/2,
            color = BLUE,
            stroke_width = 1,
        )
        arc_template.scale_to_fit_width(1)
        arc_template.shift(-arc_template.points[0])
        def make_arc(x0, x1):
            arc = arc_template.copy()
            arc.scale(x1-x0)
            arc.shift(x0*RIGHT)
            return arc

        all_bars = ordinal[0].submobjects + ordinal[1].submobjects
        points = [
            bar.x0
            for bar in all_bars
        ]
        ordering = VGroup(
            [
                make_arc(x0, x1)
                for x1 in points[i+1:]
            ]
            for i, x0 in enumerate(points)
        )
        ordering.fade()
        ordering.shift(UP)

        def nearest_arrow(x0, x1):

            i0 = min(range(len(points)), key = lambda i: abs(points[i]-x0))
            i1 = min(range(len(points)), key = lambda i: abs(points[i]-x1))
            if i0 == i1: return
            if i0 > i1: i0,i1 = i1,i0

            arrow = ordering[i0][i1-i0-1].copy()

            arrow.set_stroke(BLUE, width = DEFAULT_POINT_THICKNESS)
            arrow.add_tip(0.1)
            return arrow, i0, i1

        arrows = [nearest_arrow(alpha.get_center()[0], beta.get_center()[0])]
        for _ in range(10):
            x0, x1 = np.random.random([2])*(ordinal.x1-ordinal.x0) + ordinal.x0

            arrow = nearest_arrow(x0, x1)
            if arrow is None: continue

            arrows.append(arrow)

        #self.wait_to(28)
        arrows_mob = VGroup(arrow for arrow,i0,i1 in arrows)
        for i, (arrow, i0, i1) in enumerate(arrows):
            ordinal.highlight(DARK_GREY)
            VGroup(all_bars[i0], all_bars[i1]).highlight(WHITE)
            if i == 0: run_time = 1
            else: run_time = 0.5
            self.play(ShowCreation(arrow), run_time = run_time)

        #self.wait_to(37.5)
        self.play(
            ordinal.highlight, WHITE,
            ShowCreation(ordering, submobject_mode = "all_at_once"),
            Animation(arrows_mob),
        )

        #self.wait_to(58.5)
        self.dither()
        self.play(FadeOut(VGroup(
            alpha, beta, ab_arrow, ineq,
        )))

        title = TextMobject("Definition").to_edge(UP)
        rect = SurroundingRectangle(VGroup(ordinal, ordering), buff = 0.2, color = WHITE)
        ordinal_label = TextMobject("ordinal number").next_to(rect, UP)

        #self.wait_to(61)
        self.play(FadeIn(title, submobject_mode = "lagged_start"))
        self.play(FadeIn(ordinal_label, submobject_mode = "lagged_start"))
        #self.wait_to(60+4.5)
        self.play(
            ShowCreation(rect),
        )

        bar = ordinal[0][2]
        dot_outside = Dot(bar.get_center())
        dot_outside.next_to(rect, DOWN, coor_mask = Y_MASK, buff = 1)
        arrow_outside = Arrow(dot_outside, bar, color = BLUE, buff = 0.1)
        cross = Cross(color = RED).scale(0.5).shift(dot_outside.get_center() + 0.5*UP)

        #self.wait_to(60+13.5)
        self.play(FadeIn(dot_outside), ShowCreation(arrow_outside))
        #self.wait_to(60+16.2)
        self.play(arrow_outside.highlight, DARK_GREY, ShowCreation(cross))

        transitive_set = TextMobject("Transitive set")
        transitive_set.next_to(rect, DOWN)
        transitive_set.next_to(cross, coor_mask = X_MASK)
        #self.wait_to(60+27.5)
        self.play(FadeIn(transitive_set, submobject_mode = "lagged_start"))

        self.dither(3)
        #self.wait_to(60+38)

class ConstructionsIntro(Scene):
    def prepare(self):
        title = TextMobject("Construction from axioms").to_edge(UP)
        omegas = TexMobject("\\omega", "\\omega_1").scale(1.5)
        omegas[0].shift(LEFT)
        omegas[1].shift(RIGHT)
        self.add(title, omegas)

        underlines = VGroup(
            Line(ORIGIN, RIGHT, color = BLUE).next_to(omega, DOWN)
            for omega in omegas
        )
        return omegas, underlines
        
    def construct(self):

        omegas, underlines = self.prepare()

        #self.wait_to(7.5)
        self.play(ShowCreation(underlines[0]))
        #self.wait_to(9.5)
        self.play(ShowCreation(underlines[1]))
        #self.wait_to(11.5)

        self.dither(2)
        self.play(FadeOut(underlines[1]), omegas[1].highlight, DARK_GREY)
        #self.wait_to(13.5)

class ConstructionOmega(Scene):
    def construct(self):

        axiom_name = TextMobject("Axiom of infinity:")
        axiom_name.to_corner(UP+LEFT)
        axiom_name.highlight(GREEN)
        axiom_desc = TextMobject("There is a set of natural numbers.")
        axiom_desc.next_to(axiom_name, DOWN, aligned_edge = LEFT)

        self.play(FadeIn(axiom_name, submobject_mode = "lagged_start"), Write(axiom_desc))
        #self.wait_to(11.5)

        naturals = VGroup(TexMobject(str(i)) for i in range(20))
        naturals.arrange_submobjects(buff = 0.5).to_edge(LEFT)
        rect = SurroundingRectangle(naturals, color = GREEN)
        omega_label = TexMobject("\\omega").highlight(GREEN).scale(1.5)
        omega_label.next_to(rect, UP, coor_mask = Y_MASK)
        omega_g = VGroup(naturals, rect, omega_label)

        self.play(FadeIn(naturals), FadeIn(rect))
        self.play(Write(omega_label))
        #self.wait_to(22)

        cancel_line = Line(
            axiom_desc.get_edge_center(LEFT), axiom_desc.get_edge_center(RIGHT),
            color = RED,
        )
        self.dither(2)
        self.play(
            axiom_desc.highlight, DARK_GREY,
            ShowCreation(cancel_line),
        )
        self.dither(2)
        #self.wait_to(33.5)

        self.play(FadeOut(VGroup(
            axiom_desc, cancel_line, omega_g,
        )))

        empty_set = Square(side_length = 0.5, color = GREY)
        m_rect = Rectangle(width = 7, height = 4)
        m_label = TexMobject("M").next_to(m_rect, UP)
        VGroup(m_rect, m_label).highlight(GREEN)

        #self.wait_to(37)
        self.play(
            ShowCreation(m_rect),
            FadeIn(m_label),
        )
        
        empty_set.shift(
            m_rect.get_corner(UP+LEFT)
            - empty_set.get_corner(UP+LEFT)
            + 0.2*(DOWN+RIGHT)
        )
        empty_set.save_state()
        empty_set.shift(1.5*LEFT)
        empty_set.highlight(BLACK)
        #self.wait_to(39.8)
        self.play(empty_set.restore)

        dots = VGroup(Dot() for _ in range(3)).arrange_submobjects(buff = 0.5)
        x_rect = SurroundingRectangle(dots, buff = 0.5, color = YELLOW)
        x_label = TexMobject('x').highlight(YELLOW).next_to(x_rect)
        x_g = VGroup(dots, x_label, x_rect)
        x2_g = x_g.copy()
        x2_rect = Rectangle(color = ORANGE, height = x_rect.get_height(), width = x_g.get_width() + 0.2)
        x2_rect.shift(x_rect.get_edge_center(LEFT) - x2_rect.get_edge_center(LEFT))

        VGroup(x2_g, x2_rect).next_to(x_g, DOWN, aligned_edge = LEFT)
        x_gg = VGroup(x_g, x2_g, x2_rect)
        x_gg.shift(m_rect.get_corner(UP+RIGHT) - x_gg.get_corner(UP+RIGHT) + 0.1*(LEFT+DOWN))

        #self.wait_to(42)
        self.play(FadeIn(dots), FadeIn(x_label), ShowCreation(x_rect))
        #self.wait_to(47.5)
        self.play(
            ReplacementTransform(x_g.copy(), x2_g)
        )
        #self.wait_to(49.3)
        self.play(Transform(x2_g[-1], x2_rect))
        x2_rect = x2_g[-1]

        nat_points = [
            empty_set.get_center() + i*0.75*DOWN
            for i in range(9)
        ]
        naturals = VGroup(
            TexMobject(str(i)).move_to(point)
            for i,point in enumerate(nat_points)
        )

        #self.add(naturals)

        es_copy = empty_set.copy().move_to(nat_points[1])
        set_1 = SurroundingRectangle(es_copy, color = WHITE)

        #self.wait_to(56.8)
        self.play(FocusOn2(empty_set))
        #self.wait_to(58)
        self.play(FadeIn(set_1))
        #self.wait_to(60.5)
        self.play(ReplacementTransform(empty_set.copy(), es_copy))

        #self.wait_to(60+7)
        self.play(ReplacementTransform(VGroup(es_copy, set_1), naturals[1]))
        #self.wait_to(60+9.2)
        self.play(ReplacementTransform(empty_set, naturals[0]))

        naturals_row = VGroup(naturals[0].copy())
        naturals_row.move_to(nat_points[2])

        nr_rect = SurroundingRectangle(naturals_row, color = WHITE)
        naturals_row.highlight(GREY)
        nr_g = VGroup(naturals_row, nr_rect)
        #self.wait_to(60+14.5)
        self.play(FadeIn(nr_rect), FadeIn(naturals_row[0]))

        def update_m_height(point):
            point += 0.2*DOWN
            top_point = m_rect.get_corner(UP+LEFT)
            new_height = top_point[1] - point[1]
            ori_height = m_rect.get_height()
            if new_height > ori_height:
                m_rect.stretch_about_point(new_height / ori_height, 1, top_point)

        for i in range(3):

            cur_nat = naturals[i+1]
            cur_nat_dest = cur_nat.copy().next_to(naturals_row[-1])
            naturals_row.add(cur_nat_dest)
            #if i == 0: self.wait_to(60+17)
            #elif i == 1: self.wait_to(60+26)
            self.play(
                ReplacementTransform(cur_nat.copy(), cur_nat_dest, path_arc = -np.pi/2),
                Transform(nr_rect, SurroundingRectangle(naturals_row, color = WHITE)),
            )
            nr_copy = nr_g.copy()

            #if i == 0: self.wait_to(60+23.5)
            #elif i == 1: self.wait_to(60+28)
            nr_g.save_state()
            nr_g.move_to(nat_points[i+3], coor_mask = Y_MASK)
            naturals_row.highlight(GREY)
            m_rect.save_state()
            update_m_height(nr_g.get_corner(LEFT+DOWN))
            self.play(
                MoveFromSaved(nr_g),
                MoveFromSaved(m_rect),
                ReplacementTransform(nr_copy, naturals[i+2]),
            )

        m_rect.save_state()
        update_m_height((SPACE_HEIGHT+1)*DOWN)
        self.play(
            MoveFromSaved(m_rect),
            FadeIn(VGroup(naturals[i+3:])),
            ApplyMethod(nr_g.behind_edge, DOWN, remover = True),
        )
        #self.wait_to(60+36.2)

        self.play(FadeOut(VGroup(
            axiom_name[-1], x_gg,
        )))
        ordinals = [
            "\\omega + {}".format(i)
            for i in range(8)
        ]
        ordinals[0] = "\\omega"
        ordinals = VGroup(TexMobject(ordinal) for ordinal in ordinals)
        for ordinal, point in zip(ordinals, nat_points):
            ordinal.shift(-ordinal[0].get_center())
            ordinal.move_to(point, coor_mask = Y_MASK)

        ordinals.next_to(naturals, buff = 1.5, coor_mask = X_MASK)
        #self.wait_to(60+45.5)
        self.play(FadeIn(ordinals), submobject_mode = "lagged_start")

        apple = Apple().scale(0.8)
        apple_set = VGroup(apple, SurroundingRectangle(apple, color = RED, buff = 0.2))
        apple_set2 = VGroup(apple.copy(), apple_set.copy()).arrange_submobjects()
        apple_set2.add(SurroundingRectangle(apple_set2, color = PURPLE, buff = 0.2))
        apple_set2.next_to(apple_set, DOWN, aligned_edge = LEFT)
        dots = TexMobject("\\vdots").next_to(apple_set2, DOWN)
        apple_g = VGroup(apple_set, apple_set2, dots)

        apple_g.next_to(m_rect.get_corner(UP+RIGHT), LEFT+DOWN)

        #self.wait_to(60+48.5)
        self.play(FadeIn(apple_g))

        axiom_sel = TextMobject("Axiom of selection").to_corner(UP+RIGHT)
        #self.wait_to(60+52.5)
        self.play(FadeIn(axiom_sel, submobject_mode = "lagged_start"))
        #self.wait_to(60+57)
        self.dither()

        m_rect.save_state()
        left_point = m_rect.get_edge_center(LEFT)
        new_width = 2*(naturals.get_center()[0] - left_point[0])
        m_rect.stretch_about_point(new_width / m_rect.get_width(), 0, left_point)

        omega_label = TexMobject("\\omega").scale(1.5).highlight(GREEN)
        omega_label.next_to(m_rect, coor_mask = X_MASK)

        self.play(
            FadeOut(VGroup(
                apple_g, ordinals,
                m_label,
            )),
            MoveFromSaved(m_rect),
        )

        #self.wait_to(2*60)
        self.play(Write(omega_label))
        self.dither(2)
        #self.wait_to(2*60+13.5)

class ConstructionsOverview2(ConstructionsIntro):
    def construct(self):

        omegas, underlines = self.prepare()
        omegas[1].highlight(DARK_GREY)
        line = underlines[0]
        self.add(line)

        self.dither()
        self.play(
            Transform(line, underlines[1]),
            omegas[0].highlight, DARK_GREY,
            omegas[1].highlight, WHITE,
        )
        self.dither()
        #self.wait_to(11)

class ProductPowerset(Scene):
    def construct(self):
        
        omega = OrdinalOmega()
        nat_labels = omega.add_descriptions(lambda n: TexMobject(str(n)),
                                            direction = DOWN, size = 0.5)
        make_half_ordinal(omega, False)
        omega_label = TexMobject("\\omega").highlight(GREEN).next_to(omega, LEFT)
        omega_g = VGroup(
            omega, omega_label, nat_labels,
        )
        omega_shift = 2.5*UP
        omega_g.shift(omega_shift)

        self.play(FadeIn(omega_g))

        big_set_label = TexMobject("\\mathcal P(\\omega\\times\\omega)")
        big_set_label.next_to(omega_g, DOWN, coor_mask = Y_MASK)
        #self.wait_to(6.5)
        self.play(Write(VGroup(big_set_label[2:-1])))

        angle = np.pi*0.3
        arc_template = Arc(
            -angle,
            start_angle = np.pi/2 + angle/2,
            color = YELLOW,
            stroke_width = 1,
        )
        arc_template.scale_to_fit_width(1)
        arc_template.shift(-arc_template.points[0])
        def make_arc(x0, x1):
            arc = arc_template.copy()
            arc.scale(x1[0]-x0[0])
            if x1[0] < x0[0]: arc.stretch(-1,1)
            arc.shift(x0)
            return arc

        omega_points = [
            bar.get_edge_center(UP)
            for bar in omega
        ]
        arcs = VGroup(
            [
                make_arc(x0, x1)
                for x1 in omega_points[i+1:]
            ]
            for i, x0 in enumerate(omega_points)
        )
        arcs.fade()

        arc_template_bak = arc_template.copy()
        arc_template.highlight(YELLOW)
        arc_template.set_stroke(width = DEFAULT_POINT_THICKNESS)
        arc_template.add_tip(0.04)
        arc_template.points = arc_template.points[::-1]
        arc_template.add_tip(0.07)

        double_arrows = VGroup(
            make_arc(point1, point2)
            for point1, point2 in zip(omega_points, omega_points[4:])
        )
        for arrow in double_arrows[20:]:
            arrow.submobjects = []

        #self.wait_to(10.5)
        self.play(FadeIn(arcs), FadeIn(double_arrows))

        big_rect = Rectangle(width = 2*SPACE_WIDTH, height = 2*SPACE_HEIGHT, color = GREEN)
        big_rect.next_to(big_set_label, DOWN)
        big_rect.to_edge(LEFT)
        big_rect.save_state()
        big_rect.scale(0)
        big_rect.highlight(BLACK)
        big_rect.next_to(big_set_label, DOWN)

        #self.wait_to(25.5)
        self.play(
            Write(VGroup(big_set_label[:2], big_set_label[-1])),
            big_rect.restore,
        )
        #self.wait_to(32)

        graph = VGroup(
            bundle[:10-i]
            for i,bundle in enumerate(arcs[:10])
        ).copy()
        graph = VGroup(graph.family_members_with_points())
        random.shuffle(graph.submobjects)
        graph.submobjects = graph.submobjects[:15]
        graph.highlight(YELLOW)
        graph.set_stroke(width = DEFAULT_POINT_THICKNESS)

        def add_proportional_tip(edge):
            x = edge.points[-1][0]
            size = (4-x)*0.025
            if size < 0.01: size = 0
            edge.add_tip(size)

        def add_back_tip(edge):
            points = edge.points
            edge.points = points[::-1]
            add_proportional_tip(edge)
            edge.points = points

        for edge in graph:
            fwd_tip = True
            back_tip = True
            rnd = random.random()
            if rnd < 0.4: fwd_tip = False
            if rnd > 0.4: back_tip = False

            if fwd_tip: add_proportional_tip(edge)
            if back_tip: add_back_tip(edge)

        self.dither()
        self.play(
            FadeOut(arcs),
            FadeOut(double_arrows),
            FadeIn(graph),
        )
        #self.wait_to(39.5)

        graph.save_state()
        graph.scale(0.8)
        graph.next_to(big_set_label, DOWN, buff = 0.5)
        graph.shift(0.5*LEFT)

        self.play(MoveFromSaved(graph))
        self.dither(2)

        arc_template = arc_template_bak
        indices = range(len(omega_points))
        indices = list(reversed(indices[1::2])) + indices[0::2]
        seq = VGroup(
            make_arc(omega_points[i0], omega_points[i1])
            for i0, i1 in zip(indices, indices[1:])
        )
        seq.set_stroke(YELLOW, width = DEFAULT_POINT_THICKNESS)
        for edge in seq: add_proportional_tip(edge)
        self.play(FadeIn(arcs), FadeIn(seq))

        Z_fwd = OrdinalOmega(x0 = 0).shift(omega_shift)
        Z_back = Z_fwd.copy().stretch(-1,0)
        Z_back.remove(Z_back[0])
        Z_fwd_labels = Z_fwd.add_descriptions(lambda n: TexMobject(str(2*n)),
                                              direction = DOWN, size = 0.5)
        Z_back_labels = Z_back.add_descriptions(lambda n: TexMobject(str(2*n+1)),
                                                direction = DOWN, size = 0.4)
        make_half_ordinal(Z_fwd, False)
        make_half_ordinal(Z_back, False)
        Z_bars = list(itertools.chain(*zip(Z_fwd, Z_back)))
        Z_bars = Z_bars[:len(omega)]
        Z_points = [bar.get_edge_center(UP) for bar in Z_bars]
        Z_arcs = VGroup(
            [
                make_arc(x0, x1)
                for x1 in Z_points[i+1:]
            ]
            for i, x0 in enumerate(Z_points)
        )
        Z_arcs.fade()

        Z_seq = VGroup(
            make_arc(Z_points[i0], Z_points[i1])
            for i0, i1 in zip(indices, indices[1:])
        )
        Z_seq.set_stroke(YELLOW, width = DEFAULT_POINT_THICKNESS)
        Z_seq_from = VGroup(Z_seq[:len(Z_seq)//2])
        Z_seq_from.scale(-1)
        for edge in Z_seq: add_proportional_tip(edge)
        Z_seq_from.scale(-1)

        fwd_labels_src = VGroup(nat_labels[0::2])
        back_labels_src = VGroup(nat_labels[1::2])
        Z_fwd_labels_trunc = VGroup(Z_fwd_labels[:len(fwd_labels_src)])
        Z_back_labels_trunc = VGroup(Z_back_labels[:len(back_labels_src)])

        #self.wait_to(52)
        self.dither(2)
        self.play(
            FadeOut(omega_label, run_time = 1),
            Transform(arcs, Z_arcs),
            Transform(seq, Z_seq),
            ReplacementTransform(LimitSubOrdinal(omega[::2]), Z_fwd),
            ReplacementTransform(LimitSubOrdinal(omega[1::2]), Z_back),
            ReplacementTransform(fwd_labels_src, Z_fwd_labels_trunc),
            ReplacementTransform(back_labels_src, Z_back_labels_trunc),
            run_time = 2,
        )
        self.add(Z_fwd_labels, Z_back_labels)

        #self.wait_to(59.8)
        self.play(FadeOut(VGroup(seq, arcs)))

        #self.wait_to(60+6)

        Z_sample = VGroup(Z_fwd, Z_back, Z_fwd_labels, Z_back_labels).copy()
        Z_sample.save_state()
        Z_sample.scale(0.7)

        ordering_rect = big_rect.copy().highlight(GREY)
        ordering_label = TextMobject("Ordering").next_to(big_rect.get_edge_center(LEFT), RIGHT)
        ordering_label.next_to(graph, DOWN, coor_mask = Y_MASK, buff = -0.1)
        ordering_rect.shift(0.2*RIGHT)
        ordering_rect.next_to(ordering_label, DOWN, coor_mask = Y_MASK, buff = 0.1)
        Z_sample.next_to(ordering_rect.get_corner(UP+LEFT), DOWN+RIGHT)

        self.play(
            FadeIn(ordering_label),
            FadeIn(ordering_rect),
            MoveFromSaved(Z_sample),
        )
        self.dither(2)

        rev_back = Z_fwd.copy().shift(4*LEFT)
        rev_back_labels = rev_back.add_descriptions(lambda n: TexMobject(str(2*n+1)),
                                                    direction = DOWN, size = 0.5)
        rev_back_labels_trunc = VGroup(rev_back_labels[:len(Z_back_labels)])
        #self.wait_to(60+17)
        self.play(
            ReplacementTransform(Z_back, rev_back),
            ReplacementTransform(Z_back_labels, rev_back_labels_trunc),
        )
        self.add(rev_back_labels)
        #self.wait_to(60+26)

        wo_sample = VGroup(Z_fwd, rev_back, Z_fwd_labels, rev_back_labels).copy()
        wo_sample.save_state()
        wo_sample.scale(0.7)
        wo_label = TextMobject("Well ordered").next_to(ordering_rect, UP, buff = 0.1)
        wo_label.to_edge(RIGHT)
        wo_rect = ordering_rect.copy().highlight(WHITE)
        wo_rect.shift(-wo_rect.get_edge_center(LEFT) * X_MASK + 0.1*DOWN)
        wo_sample.next_to(wo_rect.get_corner(UP+LEFT), DOWN+RIGHT)
        self.play(
            FadeIn(wo_label),
            FadeIn(wo_rect),
            MoveFromSaved(wo_sample),
        )

        #self.wait_to(60+36)
        self.dither(2)

        to_up = VGroup(
            big_set_label, graph, ordering_label, wo_label,
            Z_fwd, Z_fwd_labels, rev_back, rev_back_labels,
        )
        to_up.save_state()
        to_up.behind_edge(UP)
        Z_sample.save_state()
        Z_sample.move_to(ORIGIN)
        Z_sample.behind_edge(LEFT, buff = 1)
        rects = VGroup(big_rect, ordering_rect, wo_rect)
        rects.save_state()
        for rect in rects:
            rect.scale_about_point(2, rect.get_corner(UP+LEFT))
        rects.shift(to_up.get_center() - to_up.saved_state.get_center())
        rects.shift(X_MASK*(Z_sample.get_center() - Z_sample.saved_state.get_center()))

        omega2 = OrdinalFiniteProd(OrdinalOmega, 2).stretch(-1,1)
        omega2_labels = VGroup(
            omega2[0].add_descriptions(lambda n: TexMobject(str(2*n+1)),
                                       direction = DOWN, size = 0.5),
            omega2[1].add_descriptions(lambda n: TexMobject(str(2*n)),
                                       direction = DOWN, size = 0.5),
        )
        omega2_g = VGroup(omega2, omega2_labels)
        omega2_src = VGroup(
            [wo_sample[1], wo_sample[0]],
            [wo_sample[3], wo_sample[2]],
        )

        self.play(
            MoveFromSaved(to_up, remover = True),
            MoveFromSaved(Z_sample, remover = True),
            MoveFromSaved(rects, remover = True),
            Transform(omega2_src, omega2_g),
        )

        #self.wait_to(60+39.5)

class OrderingToOrdinal(Scene):
    def construct(self):

        omega2 = OrdinalFiniteProd(OrdinalOmega, 2).stretch(-1,1)
        self.add(omega2)
        nat_labels = VGroup(
            omega2[0].add_descriptions(lambda n: TexMobject(str(2*n+1)),
                                       direction = DOWN, size = 0.5),
            omega2[1].add_descriptions(lambda n: TexMobject(str(2*n)),
                                       direction = DOWN, size = 0.5),
        )
        def omega_plus(n):
            if n == 0: return "\\omega"
            else: return "\\omega+{}".format(n)
        ord_labels = VGroup(
            omega2[0].add_descriptions(lambda n: TexMobject(str(n)),
                                       direction = UP, size = 0.5),
            omega2[1].add_descriptions(lambda n: TexMobject(omega_plus(n)),
                                       direction = UP, size = 0.8),
        )
        ord_labels.highlight(BLUE)
        ord_labels[0][1].scale_about_point(0.8, omega2[0][1].get_edge_center(UP))

        self.add(omega2, nat_labels)

        #self.wait_to(13.2)

        #rect = SurroundingRectangle(VGroup(nat_labels[0][:4]))
        #self.play(FadeIn(rect))
        #self.wait_to(18)
        #self.play(
        #    Transform(rect, SurroundingRectangle(VGroup(ord_labels[0][:4])))
        #)
        #self.play(FadeOut(rect))

        #self.wait_to(22.5)
        rect = Square(side_length = 0.5).next_to(nat_labels[0][0], LEFT)
        self.play(GrowFromCenter(rect))
        #self.wait_to(25)
        self.play(rect.next_to, ord_labels[0][0], LEFT)
        #self.wait_to(27)
        self.play(ReplacementTransform(rect, ord_labels[0][0]))

        for i in range(1,5):
            rect = SurroundingRectangle(VGroup(nat_labels[0][:i]))
            #if i == 1: self.wait_to(29)
            #elif i == 2: self.wait_to(35)
            if i == 1: self.play(FadeIn(rect))
            else: self.add(rect)

            #if i == 1: self.wait_to(31.5)
            self.play(Transform(rect, SurroundingRectangle(VGroup(ord_labels[0][:i]))))
            #if i == 1: self.wait_to(33.5)
            self.play(ReplacementTransform(rect, ord_labels[0][i]))

        self.play(ShowCreation(VGroup(ord_labels[0][i+1:])))

        #self.wait_to(43)
        poly_points = [
            nat_labels[0].get_edge_center(LEFT) * X_MASK + 0.2*LEFT,
            nat_labels[0].get_corner(LEFT+DOWN) + 0.2*LEFT + 0.3*DOWN,
            omega2[1][0].get_center() + 0.7*DOWN,
            omega2[1][0].get_center(),
        ]
        poly = Polygon(*poly_points, color = YELLOW)
        poly_dest_points = np.array([
            poly_points[i] for i in [1,0,3,2]
        ])
        poly_dest_points[:,1] *= -1
        poly_dest = Polygon(*poly_dest_points, color = YELLOW)

        self.play(FadeIn(poly))
        #self.wait_to(46.5)
        self.play(Transform(poly, poly_dest))
        #self.wait_to(49.5)
        self.play(ReplacementTransform(poly, ord_labels[1][0]))
        #self.wait_to(51)
        self.play(ShowCreation(VGroup(ord_labels[1][1:])))
        #self.wait_to(54)

        end_point = Dot(omega2.get_edge_center(RIGHT), radius = 0)
        rect = SurroundingRectangle(VGroup(nat_labels, end_point))
        rect_dest = SurroundingRectangle(VGroup(ord_labels, end_point))
        self.play(FadeIn(rect))
        self.play(Transform(rect, rect_dest))
        label = TexMobject("\\omega\\cdot 2").highlight(YELLOW).next_to(rect, UP)

        self.play(FadeIn(label))

        omega1 = Omega1(color = GREY)
        omega1.scale(0.7)
        omega1.to_corner(UP+RIGHT)
        #self.wait_to(59)
        self.play(
            FadeOut(VGroup(ord_labels, rect)),
            FadeIn(omega1),
        )

        bar = omega1.bars[2][0]
        bar_copy = bar.copy().highlight(YELLOW)
        bar_copy.save_state()
        bar_copy.scale(0).move_to(label[1])
        label.save_state()
        label.replace(bar, stretch = True)

        self.play(
            MoveFromSaved(label, remover = True),
            ApplyMethod(bar_copy.restore, remover = True),
        )
        bar.highlight(YELLOW)
        self.add(bar)

        #self.wait_to(60+3)

        omega2_g = VGroup(omega2, nat_labels)
        omega2_g.save_state()
        omega2_g.scale(0.7).to_corner(UP+LEFT)
        arrow = Arrow(omega2, omega1)
        self.play(MoveFromSaved(omega2_g))
        #self.wait_to(60+6.5)
        self.play(ShowCreation(arrow))

        omega_p1 = OrdinalOmega()
        labels2 = omega_p1.add_descriptions(lambda n: TexMobject(str(n+1)),
                                            direction = DOWN, size = 0.5),
        next_bar = omega_p1[0].copy().next_to(omega_p1)
        next_bar_l = TexMobject('0').scale_to_fit_height(labels2[0][0].get_height())
        next_bar_l.next_to(next_bar, DOWN)
        omega_p1 = VGroup(omega_p1, next_bar)
        omega_p1_g = VGroup(omega_p1, labels2, next_bar_l)

        omega_p1_g.scale(0.7).to_edge(LEFT)
        omega_p1_g.next_to(omega2_g, DOWN, coor_mask = Y_MASK)
        omega1_2 = omega1.copy().move_to(omega_p1, coor_mask = Y_MASK)
        omega1_2.bars.highlight(GREY)
        omega1_2.bars[1][1].highlight(YELLOW)
        arrow2 = Arrow(omega_p1, omega1_2)

        assignment2 = VGroup(omega_p1_g, omega1_2, arrow2)
        #self.wait_to(60+10)
        self.play(FadeIn(assignment2))

        ldots = TexMobject("\\vdots").next_to(omega_p1_g, DOWN)
        rdots = ldots.copy().move_to(omega1, coor_mask = X_MASK)

        self.play(ShowCreation(ldots), ShowCreation(rdots))

        rect = SurroundingRectangle(VGroup(omega2_g, omega_p1_g), color = WHITE, buff = 0.2)
        rect.stretch_about_point(2*SPACE_HEIGHT / rect.get_height(), 1, rect.get_edge_center(UP))
        #self.wait_to(60+25.5)
        self.play(ReplacementTransform(Rectangle(width = 2*SPACE_WIDTH+1, height = 2*SPACE_HEIGHT+1), rect))

        #self.wait_to(60+33.5)
        rect_dest = SurroundingRectangle(omega1, color = WHITE, buff = 0.2)
        rect_dest.stretch_about_point(2*SPACE_HEIGHT / rect_dest.get_height(), 1,
                                      rect_dest.get_edge_center(UP))
        self.play(Transform(rect, rect_dest))

        self.dither(2)
        #self.wait_to(60+47.5)

class Omega1Finish(Scene):
    def construct(self):

        omega1 = Omega1(color = GREY)
        omega1_label = TexMobject("\\omega_1").next_to(omega1, LEFT)
        self.add(omega1, omega1_label)

        finite_brace = BraceText(omega1.bars[0], "finite", UP)
        aleph0_brace = BraceText(VGroup(omega1.bars[1:], omega1.line), "cardinality $\\aleph_0$", DOWN)

        #self.wait_to(5.5)
        self.play(finite_brace.creation_anim())
        #self.wait_to(8)
        self.play(aleph0_brace.creation_anim())
        self.remove(omega1)
        omega1 = Omega1(color = YELLOW)
        self.add(omega1)
        omega1.bars[0].highlight(GREY)

        #self.wait_to(16.5)

        omega = OrdinalOmega(height = 0.5, x1 = 0)
        omega.next_to(finite_brace.brace, UP)
        omega_label = TexMobject("\\omega").next_to(omega, UP)

        self.dither()
        self.play(
            FadeOut(finite_brace.desc),
            FadeIn(omega),
            FadeIn(omega_label),
        )

        #self.wait_to(21)
        omega_dest = omega1.bars[0].copy().highlight(WHITE)
        self.play(Transform(omega.copy(), omega_dest, remover = True))
        omega1.bars[0].highlight(WHITE)

        #self.wait_to(48)
        self.dither(3)

class NextChapter(Scene):
    def construct(self):

        #title = TextMobject("Problem of the uncountable chain")
        #title.to_edge(UP)
        #self.add(title)

        base_elements = VGroup(TexMobject(str(i)) for i in range(3))
        base_elements.arrange_submobjects()
        base_rect = SurroundingRectangle(base_elements, color = GREEN)
        base_set = VGroup(base_rect, base_elements)

        poset_dict = dict()

        def make_subset(elements):
            subset = base_set.copy()
            subset[1].submobjects = [
                submob
                for i,submob in enumerate(subset[1].submobjects)
                if i in elements
            ]
            if len(subset[1].submobjects) == 0:
                subset.remove(subset[1])
            subset.data = elements
            poset_dict[elements] = subset
            return subset

        poset_data = [
            ((0,1,2,),),
            ((0,1,), (0,2,), (1,2,),),
            ((0,), (1,), (2,),),
            ((),),
        ]

        poset_elements = VGroup(
            VGroup(
                make_subset(elements)
                for elements in row
            ).arrange_submobjects(buff = 0.4)
            for row in poset_data
        ).arrange_submobjects(DOWN, buff = 0.7)

        def make_edge(r1, r2):
            if r1.get_center()[0] > r2.get_center()[0]+0.1:
                direction = LEFT
            elif r2.get_center()[0] > r1.get_center()[0]+0.1:
                direction = RIGHT
            else: direction = ORIGIN

            return Line(
                r1.get_critical_point(DOWN+direction),
                r2.get_critical_point(UP-direction),
            )

        poset_edges = []
        edge_dict = dict()
        for row1, row2 in zip(poset_elements, poset_elements[1:]):
            for el1 in row1:
                for el2 in row2:
                    if set(el2.data).issubset(el1.data):
                        edge = make_edge(el1, el2)
                        poset_edges.append(edge)
                        edge.data = (el1.data, el2.data)
                        edge_dict[edge.data] = edge

        poset_edges = VGroup(poset_edges)

        poset_rect = SurroundingRectangle(poset_elements, color = YELLOW)
        poset_label = TexMobject("\\mathcal P(3)").next_to(poset_rect, DOWN)
        self.play(
            FadeIn(poset_label),
            FadeIn(poset_elements),
            ShowCreation(poset_rect),            
        )

        self.play(
            ShowCreation(poset_edges),
        )
        poset_edges.highlight(DARK_GREY)
        poset_elements.highlight(DARK_GREY)

        middle_edges = filter(lambda e: len(e.data[0]) == 2, poset_edges)

        def get_chain(edge):

            seq = ((0,1,2),) + edge.data + ((),)

            chain_elements = VGroup(
                poset_dict[data]
                for data in seq
            )
            chain_edges = VGroup(
                edge_dict[el1, el2]
                for el1, el2 in zip(seq, seq[1:])
            )

            return chain_edges, chain_elements

        for edge in middle_edges:

            poset_elements.highlight(GREY)
            poset_edges.highlight(GREY)
            VGroup(get_chain(edge)).highlight(YELLOW)

            self.dither(0.5)

        self.play(FadeOut(VGroup(
            poset_edges, poset_elements,
        )))

        self.dither()

        label_dest = TexMobject("\\mathcal P(\\omega)").move_to(poset_label)
        poset_rect.save_state()
        poset_rect.stretch_in_place(1.5, 0)
        poset_rect.set_fill(None, 0.1)
        self.play(
            Transform(poset_label, label_dest),
            MoveFromSaved(poset_rect),
        )

        continuum = TexMobject("\\mathfrak c").scale(2).next_to(poset_rect.get_corner(UP+LEFT), DOWN+RIGHT, buff = 1)

        length = 5
        midpoints = 2
        osc1, osc2 = 0.5, 0.5
        points = []
        y_seq = np.linspace(length, 0, 3*(midpoints+2))
        for i in range(0,len(y_seq),3):
            y1,y2,y3 = y_seq[i:i+3]
            x = interpolate(-osc1, osc1, np.random.random())
            x2 = interpolate(-osc2, osc2, np.random.random())
            points += [[x-x2,y1,0],[x,y2,0],[x+x2,y3,0]]

        points = np.array(points[1:-1])
        chain = Line(UP, DOWN, color = YELLOW)
        chain.points = points

        chain.center()
        self.play(
            FadeIn(continuum),
            ShowCreation(chain),
        )

        self.dither()
        self.play(FadeOut(chain))

        bound = 3.5
        reals = NumberLine(x_min = -bound, x_max = bound).shift(0.5*DOWN)
        reals_label = TexMobject("\\mathbb R").next_to(reals, DOWN, aligned_edge = RIGHT)
        self.play(ShowCreation(reals), FadeIn(reals_label))
        self.dither()

        #self.wait_to(19.5)
