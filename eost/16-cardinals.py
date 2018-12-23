#!/usr/bin/env python
# coding: utf-8

from helpers import *
import itertools
import new

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject, MobjectFromPixelArray
from mobject.vectorized_mobject import *
from topics.icons import IconYes

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

class Chapter16OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 16\\\\ Recursion on Cardinal",
    }

class Chapter16OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Infinity","turns out to be the opposite of what people say it is."
        ],
        "highlighted_quote_terms" : {
            "Infinity" : GREEN,
        },
        "author" : "Aristotle"
    }

card_color = RED
ord_color = BLUE

class SeriesIntro(Scene):
    def construct(self):

        series = VideoSeries(num_videos = 16).to_edge(UP)
        cardinals_title = TextMobject("Cardinal numbers")
        ordinals_title = TextMobject("Ordinal numbers")
        formal_card_title = TextMobject("Formal meaning")
        formal_ord_title = formal_card_title.copy()

        cardinals_title.next_to(series[1], DOWN, aligned_edge = LEFT)
        ordinals_title.next_to(series[3], DOWN, aligned_edge = LEFT)

        formal_ord_title.next_to(series[-2], DOWN, aligned_edge = RIGHT)
        formal_card_title.next_to(series[-1], DOWN, aligned_edge = RIGHT)

        cardinals_meaning = TexMobject(
            "|\\omega|=\\aleph_0",
            ",|\\mathbb R|=\\mathfrak c",
            ",\ldots",
        ).next_to(cardinals_title, DOWN)

        ordinals_meaning = OrdinalFiniteProd(
            OrdinalOmega, 2,
            x0 = -2, x1 = 2, height = 0.7,
        ).next_to(ordinals_title, DOWN)


        card_g = VGroup(cardinals_title, formal_card_title, cardinals_meaning)
        ord_g = VGroup(ordinals_title, formal_ord_title, ordinals_meaning)
        card_g.shift(4*DOWN)
        ord_g.shift(DOWN)

        def make_vert_line(obj1, obj2, buff = 0.1):
            p0 = obj1.get_edge_center(DOWN)
            p1 = obj2.get_edge_center(UP) + UP*buff
            p1 = p0*X_MASK + p1*Y_MASK
            return Line(p0, p1)

        cardinals_line = make_vert_line(VGroup(series[1:3]), cardinals_title)
        ordinals_line = make_vert_line(VGroup(series[5]), ordinals_title)
        formal_ord_line = make_vert_line(VGroup(series[10]), formal_ord_title)
        formal_card_line = make_vert_line(VGroup(series[15]), formal_card_title)

        card_g.add(cardinals_line, formal_card_line)
        ord_g.add(ordinals_line, formal_ord_line)

        card_g.highlight(card_color)
        ord_g.highlight(ord_color)

        card_arrow = Arrow(formal_card_title, cardinals_title)
        ord_arrow = Arrow(formal_ord_title, ordinals_title)

        numbered_series = series.copy()
        for i,icon in enumerate(numbered_series):
            chap_num = TexMobject(str(i+1)).replace(icon, 1)
            chap_num.scale_in_place(0.6)
            icon.remove(icon[1])
            icon.add(chap_num)

        numbered_series.highlight(card_color)
        VGroup(numbered_series[4:-1]).highlight(ord_color)

        series.highlight(DARK_GREY)
        series.submobjects[1] = numbered_series[1]
        series.submobjects[2] = numbered_series[2]

        series.save_state()
        series.behind_edge(UP)
        self.play(series.restore)
        #self.wait_to(2.5)
        self.play(
            ShowCreation(cardinals_line),
            FadeIn(cardinals_title, submobject_mode = "lagged_start"),
        )
        #self.wait_to(4.5)
        self.play(FadeIn(cardinals_meaning[0]))
        #self.wait_to(8)
        self.play(FadeIn(cardinals_meaning[1]))
        #self.wait_to(10)
        self.play(FadeIn(cardinals_meaning[2]))

        #self.wait_to(11.5)
        self.play(Transform(VGroup(series[4:7]), VGroup(numbered_series[4:7])))
        self.play(
            ShowCreation(ordinals_line),
            FadeIn(ordinals_title, submobject_mode = "lagged_start"),
        )
        self.play(FadeIn(ordinals_meaning))

        #self.wait_to(18)
        self.play(
            Transform(series[10], numbered_series[10]),
            ShowCreation(formal_ord_line),
            FadeIn(formal_ord_title),
        )
        self.play(ShowCreation(ord_arrow))

        #self.wait_to(24)
        self.play(
            Transform(series[15], numbered_series[15]),
            ShowCreation(formal_card_line),
            FadeIn(formal_card_title),
        )
        #self.wait_to(26.5)
        self.play(ShowCreation(card_arrow))

        question = TexMobject("\\mathfrak c = \\mathord{?}")
        question[0].highlight(card_color)
        question.shift(cardinals_meaning[1][-1].get_center() - question[0].get_center())
        question.to_edge(RIGHT)

        reals = VGroup(cardinals_meaning[1][1:]).copy()
        reals.save_state()
        reals.shift(question[0].get_center() - reals[-1].get_center())

        #self.wait_to(35)
        self.play(
            MoveFromSaved(reals, path_arc = 1.0)
        )
        self.play(Write(VGroup(question[1:])))
        #self.wait_to(40.5)
        self.dither(2)

        self.remove(reals[-1])
        reals.remove(reals[-1])

        card_g.remove(formal_card_title)
        picture = VGroup(
            series, card_g, ord_g, ord_arrow, reals,
        )
        formal_card_title_dest = formal_card_title.copy()
        formal_card_title_dest.to_corner(UP+RIGHT)

        picture.save_state()
        picture.shift(
            Y_MASK*(
                formal_card_title_dest.get_center()
                - formal_card_title.get_center()
            )
        )
        card_arrow_dest = Arrow(formal_card_title_dest, cardinals_title)
        picture.highlight(BLACK)
        card_arrow_dest.highlight(BLACK)

        self.play(
            MoveFromSaved(picture),
            Transform(formal_card_title, formal_card_title_dest),
            Transform(card_arrow, card_arrow_dest),
            question.to_corner, DOWN+RIGHT,
        )

class ContinuumQuestion(Scene):
    def construct(self):

        title = TextMobject("Formal meaning")
        title.highlight(card_color)
        title.to_corner(UP+RIGHT)

        question = TexMobject("\\mathfrak c = \\mathord{?}")
        question[0].highlight(card_color)
        question.to_corner(DOWN+RIGHT)

        self.add(title, question)

        reals = NumberLine(x_min = -3.9, x_max = 3.9)
        reals.next_to(title, DOWN, buff = 1, coor_mask = Y_MASK)
        reals_l = TexMobject("\\mathbb R")
        reals_l.next_to(reals, LEFT)

        subset_seq = VGroup([
            TexMobject(str(i)) for i in range(20)
        ]).arrange_submobjects()
        subsets_int = VGroup([
            subset_seq.copy() for _ in range(3)
        ])
        for seq in subsets_int:
            for num in seq:
                num.highlight(random.choice((WHITE, DARK_GREY)))
        subsets_int[1].shift(RIGHT+0.8*UP)
        subsets_int[2].scale(0.9)
        subsets_int[2].shift(2*RIGHT+0.7*DOWN)
        subsets_rect = SurroundingRectangle(subsets_int, buff = 0.5)
        subsets = VGroup(subsets_int, subsets_rect)
        subsets.next_to(reals, DOWN, buff = 1, aligned_edge = LEFT)

        subsets_l = TexMobject("\\mathcal P(\\omega)")
        subsets_l.next_to(subsets, LEFT)

        #self.wait_to(3.5)
        self.play(FadeIn(reals_l), ShowCreation(reals))

        #self.wait_to(5)
        self.play(ShowCreation(subsets_int), run_time = 1.5)
        self.play(FadeIn(subsets_l), ShowCreation(subsets_rect))

        corner = VGroup(subsets_l, reals_l, reals).get_corner(UP+LEFT)
        corner += 0.4*(UP+LEFT)
        start = corner*Y_MASK + SPACE_WIDTH*RIGHT
        end = corner*X_MASK + SPACE_HEIGHT*DOWN

        proper_class = VGroup(
            DashedLine(start, corner),
            DashedLine(corner, end),
        )
        #self.wait_to(10)
        self.play(ShowCreation(proper_class))

        paradox = TextMobject("Russel's paradox")
        paradox.highlight(YELLOW)
        paradox.next_to(proper_class, UP, aligned_edge = LEFT)
        paradox.shift(0.5*LEFT)

        #self.wait_to(14.5)
        self.add(paradox)
        self.dither(0.3)
        self.remove(paradox)
        self.dither(0.2)
        self.add(paradox)
        self.dither()

        #self.wait_to(23)
        self.play(FadeOut(VGroup(paradox, proper_class)))

        q_mark = question[-1].copy()
        q_mark.move_to(reals_l)
        q_mark.shift(1.5*(UP+LEFT))
        arrow = Arrow(q_mark, reals_l.get_corner(LEFT+UP))

        #self.wait_to(28.5)
        self.play(FadeIn(q_mark), ShowCreation(arrow))
        #self.wait_to(33.5)

        q_mark.save_state()
        q_mark.shift(subsets_l.get_center() - reals_l.get_center())
        arrow_dest = Arrow(q_mark, subsets_l)
        self.play(
            MoveFromSaved(q_mark),
            Transform(arrow, arrow_dest),
        )

        #self.wait_to(37.5)
        self.dither()
        self.play(FadeOut(VGroup(q_mark, arrow)))
        #self.wait_to(60+5)

        ordinal = LongOrdinal(
            color = reals.color,
            x0 = reals.x_min,
            x1 = reals.x_max,
            height = 0.7,
        ).move_to(reals)

        bars = ordinal[1].family_members_with_points()
        segments = ordinal[0].family_members_with_points()
        for bar in bars:
            bar.priority = 100
        for segment in segments:
            segment.priority = np.sum(segment.stroke_rgb)

        dest_mobjects = bars + segments
        reals_line = reals.main_line
        self.remove(reals_line)
        reals.remove(reals_line)

        src_mobjects = reals.family_members_with_points()
        choped_line = GradientLine(
            reals_line.get_start(), reals_line.get_end(),
            reals.color, reals.color,
            segment_num = len(dest_mobjects) - len(src_mobjects)
        )
        src_mobjects += choped_line.submobjects

        random.shuffle(src_mobjects)
        for src, dest in zip(src_mobjects, dest_mobjects):
            src.priority = dest.priority

        def order_f(mob):
            if hasattr(mob, "priority"):
                return mob.priority
            return -1

        src_mobjects = VGroup(src_mobjects)
        dest_mobjects = VGroup(dest_mobjects)
        self.play(
            Transform(
                src_mobjects, dest_mobjects,
                path_arc = np.pi/2,
                submobject_mode = "lagged_start",
            ),
            FadeOut(reals_l),
            run_time = 2,
            order_f = order_f,
        )

        conversation = Conversation(self)

        #self.wait_to(60+14)
        conversation.add_bubble("Is this the cardinality?")
        self.dither(2)
        #self.wait_to(60+21.5)
        conversation.add_bubble("Almost, we just have to pick one.")

        self.dither(2)
        #self.wait_to(60+28.5)
        self.remove(src_mobjects)
        picture = VGroup(
            subsets,
            subsets_l,
            ordinal,
            question,
            conversation.dialog,
        )
        self.play(FadeOut(picture))


class CardinalDefinition(Scene):
    def construct(self):

        title = TextMobject("Formal meaning")
        title.highlight(card_color)
        title.to_corner(UP+RIGHT)
        self.add(title)

        aleph0 = TexMobject("\\aleph_0").scale(1.2).to_edge(UP)
        aleph0.highlight(card_color)
        omega = OrdinalOmega().highlight(YELLOW).next_to(aleph0, DOWN)
        #aleph0.next_to(omega, UP)
        self.play(Write(aleph0))

        ordinals = make_ordinal_power(2, q=(0.8, 0.9, 0.9), x0 = -5, x1 = SPACE_WIDTH+1)
        labeled_bars = [ordinals[1][0], ordinals[3][0]]
        labels = VGroup([
            TexMobject(text).scale(scale).next_to(bar, DOWN)
            for text, scale, bar in zip(("\\omega", "\\omega\cdot3"), (1,0.8), labeled_bars)
        ])
        labels.highlight(ord_color)
        VGroup(ordinals, labels).to_edge(DOWN)

        omega_l = labels[0].copy().next_to(omega, DOWN)
        #self.wait_to(2)
        self.play(
            FadeIn(omega),
            FadeIn(omega_l),
        )
        #self.wait_to(3.5)

        bar = labeled_bars[0].copy().highlight(YELLOW)
        self.play(
            FadeIn(ordinals),
            Transform(omega, bar),
            ReplacementTransform(omega_l, labels[0]),
        )
        self.remove(omega)
        labeled_bars[0].highlight(YELLOW)

        omega3 = OrdinalFiniteProd(OrdinalOmega, 3).highlight(YELLOW)
        omega3.next_to(aleph0, DOWN)
        omega3_l = labels[1].copy().next_to(omega3, DOWN)

        self.play(
            FadeIn(omega3),
            FadeIn(omega3_l),
        )
        #self.wait_to(8.5)

        bar = labeled_bars[1].copy().highlight(YELLOW)
        self.play(
            Transform(omega3, bar),
            ReplacementTransform(omega3_l, labels[1]),
        )
        self.remove(omega3)
        labeled_bars[1].highlight(YELLOW)

        #self.wait_to(11)

        omega1 = Omega1(x0 = -5, x1 = -3, ordinal_end = 0.7, height = 0.5, color = YELLOW)
        omega1[1][0].highlight(WHITE)
        omega1.shift(ordinals.get_edge_center(LEFT) - omega1.get_edge_center(LEFT))
        omega1_end = omega1[0].get_end()
        omega1_bar = Line(ORIGIN, 0.8*UP)
        omega1_bar.move_to(omega1_end)
        omega1_l = TexMobject("\\omega_1")
        omega1_l.next_to(omega1_bar, DOWN)
        omega1_l.highlight(ord_color)

        labels[0].save_state()
        labels[0].scale(0.8)
        labels[0].next_to(omega1[1][1][0], DOWN)
        labels[0].shift(0.15*UP+0.1*RIGHT)

        labels[1].save_state()
        labels[1].shift(
            omega1[1][3][0].get_edge_center(DOWN) - labels[1][0].get_corner(UP+LEFT)
        )
        labels[1].shift(
            labels[0].get_corner(UP+LEFT) - omega1[1][1][0].get_edge_center(DOWN)
        )
        labels[1].highlight(BLACK)

        aleph0_dest = TexMobject("\\aleph_0")
        aleph0_dest.highlight(card_color)
        aleph0_dest.next_to(omega1, UP, buff = 0.5)
        aleph0_dest.shift(omega1[1][0].get_width()/2)

        bigger_ordinals = GradientLine(
            omega1_end, omega1_end*Y_MASK + 5*RIGHT,
            GRAY, GRAY, BLACK,
        )
        gradient_line = VGroup(omega1[0], bigger_ordinals, omega1_bar, omega1_l)
        gradient_line.save_state()
        gradient_line.behind_edge(RIGHT)

        self.play(
            MoveFromSaved(labels[1]),
            gradient_line.restore,
            ReplacementTransform(ordinals, omega1[1]),
            MoveFromSaved(labels[0]),
            Transform(aleph0, aleph0_dest),
        )
        self.remove(labels[1])

        self.remove(ordinals)
        self.add(omega1, bigger_ordinals, omega1_bar, omega1_l)

        points_aleph0 = [
            omega1[1][1][0].get_edge_center(UP),
            omega1.get_center(),
            omega1[0].get_edge_center(RIGHT)+0.2*LEFT,
        ]
        arrows_aleph0 = VGroup([
            Arrow(aleph0, p) for p in points_aleph0
        ])
        for arrow in arrows_aleph0:
            self.play(ShowCreation(arrow), run_time = 0.7)

        cont_segment = Line(ORIGIN, omega1.get_width()*RIGHT)
        cont_segment.highlight(YELLOW)
        cont_segment.move_to(bigger_ordinals)
        continuum = TexMobject("\\mathfrak c").highlight(card_color)
        continuum.move_to(aleph0)
        continuum.move_to(cont_segment, coor_mask = X_MASK)
        cont_points = [0.2, 0.5, 0.8]
        cont_points = [
            interpolate(cont_segment.get_start(), cont_segment.get_end(), alpha)
            for alpha in cont_points
        ]
        cont_dots = VGroup([
            Dot(point).highlight(YELLOW)
            for point in cont_points
        ])
        cont_arrows = VGroup([
            Arrow(continuum, point)
            for point in cont_points
        ])

        #self.wait_to(21)
        self.play(FadeIn(continuum))
        for arrow, dot in zip(cont_arrows, cont_dots):
            self.play(
                ShowCreation(arrow),
                FadeIn(dot),
                run_time=  0.7,
            ) 
        #self.wait_to(25)

        cont_dots.save_state()
        for dot in cont_dots:
            ratio = cont_segment.get_width() / dot.get_width()
            dot.scale(np.array([ratio,0,1]))
            dot.move_to(cont_segment)
        cont_segment.save_state()
        cont_segment.scale_in_place(0)

        self.play(MoveFromSaved(cont_dots), cont_segment.restore)
        self.remove(cont_dots)
        #cont_segment.highlight(RED)

        cont_bar = omega1[1].family_members_with_points()[0].copy()
        cont_bar.highlight(YELLOW)
        cont_bar.move_to(cont_segment.get_start())
        cont_bar.save_state()
        cont_bar.scale_in_place(0)
        cont_bar.set_stroke(width = 0)
        #self.wait_to(39)
        self.play(cont_bar.restore)
        #self.wait_to(42.5)
        self.play(
            FadeOut(cont_arrows),
            continuum.next_to, cont_bar, UP,
        )

        #self.wait_to(52)
        self.dither()

        bar = omega1[1][1][0]
        bar.save_state()
        bar.scale_in_place(2)
        omega_l = TexMobject("\\omega").highlight(ord_color)
        omega_l.next_to(bar, DOWN)
        aleph0.save_state()
        aleph0.next_to(bar, UP)

        self.play(
            FadeOut(arrows_aleph0),
            MoveFromSaved(bar),
            ReplacementTransform(labels[0], omega_l),
            MoveFromSaved(aleph0),
        )
        #self.wait_to(57.5)

        aleph1 = TexMobject("\\aleph_1").highlight(card_color)
        aleph1.next_to(omega1_bar, UP)
        self.play(FadeIn(aleph1))

        aleph_omega = TexMobject("\\aleph_\\alpha","=","\\omega_\\alpha")
        aleph_omega[0].highlight(card_color)
        aleph_omega[2].highlight(ord_color)
        aleph_omega.shift(UP)
        #self.wait_to(60.5)
        self.play(Write(aleph_omega))
        self.dither(2)

        #self.wait_to(60+26)
        picture = VGroup(
            omega_l, aleph0,
            omega1,
            omega1_bar, omega1_l, aleph1,
            bigger_ordinals,
            cont_bar, cont_segment,
            continuum,
            title,
            aleph_omega,
        )
        self.play(FadeOut(picture))


import importlib
chapter1 = importlib.import_module('eost.01-intro')

TurnSquares = chapter1.TurnSquares
make_inf_grid_lines = chapter1.make_inf_grid_lines

class GridScene(Scene):
    CONFIG = {
        "sq_size": 0.8,
        "color_row": BLUE,
        "color_col": YELLOW,
        "bg_buff": 0.2,
    }
    def make_grid(self):

        self.grid_lines = make_inf_grid_lines(self.sq_size)
        self.grid_lines.highlight(GREY)

        self.grid_height = int(np.ceil(SPACE_HEIGHT / self.sq_size))
        self.grid_width = int(np.ceil(SPACE_WIDTH / self.sq_size))

        self.grid = VGroup([
            VGroup([
                Square(
                    side_length = self.sq_size,
                    stroke_width = 0,
                    fill_opacity = 0.5,
                    color = BLACK,
                )
                for _ in range(self.grid_width*2+1)
            ]).arrange_submobjects(buff = 0)
            for _ in range(self.grid_height*2+1)
        ]).arrange_submobjects(DOWN, buff = 0)

        self.add(self.grid, self.grid_lines)

    def make_rc_line(self, position):
        rc, index = position
        if rc == 'r':
            result = Line(
                SPACE_WIDTH*LEFT,
                SPACE_WIDTH*RIGHT,
                color = self.color_row,
                #dashed_segment_length = dash_len,
            )
            result.shift(index*self.sq_size*DOWN)
        else:
            result = Line(
                SPACE_HEIGHT*UP,
                SPACE_HEIGHT*DOWN,
                color = self.color_col,
                #dashed_segment_length = dash_len,
            )
            result.shift(index*self.sq_size*RIGHT)

        result.rc = rc
        result.index = index
        result.position = position

        return result

    def make_bg(self, *fg):
        return BackgroundRectangle(VGroup(*fg), buff = self.bg_buff)

    def get_squares(self, position):
        rc, index = position
        if rc == 'r':
            if abs(index) > self.grid_height: return None
            return self.grid[self.grid_height+index]
        else:
            if abs(index) > self.grid_width: return None
            return [
                row[self.grid_width+index]
                for row in self.grid
            ]

    def get_colors(self, squares, position):
        rc, index = position
        if rc == 'r': color = self.color_row
        else: color = self.color_col
        colors = [square.color for square in squares]
        for i,c in enumerate(colors):
            if (color_to_rgb(c) == color_to_rgb(BLACK)).all():
                colors[i] = color
        return colors

    def colorify_rc(self, position):
        squares = self.get_squares(position)
        if squares is None: return
        colors = self.get_colors(squares, position)
        for sq, color in zip(squares, colors):
            sq.set_color(color)
    
    def play_bar(self, omega, bg=[], fast = True):
        bg = VGroup(bg)

        bar = omega[0]
        line = self.make_rc_line(bar.position)
        if fast: run_time = 0.3
        else: run_time = 1
        self.play(ReplacementTransform(bar, line, run_time = run_time))
        omega.remove(bar)

        if fast:
            self.colorify_rc(line.position)
            self.remove(line)

        else:
            squares = self.get_squares(line.position)
            if squares is None: self.remove(line)
            else:
                colors = self.get_colors(squares, line.position)
                if len(self.bar_waits) > 0:
                    t = self.bar_waits.pop(0)
                    #if t is not None: self.wait_to(t)
                self.play(
                    TurnSquares(squares, colors),
                    Animation(VGroup(self.grid_lines, bg, omega)),
                    FadeOut(line),
                )

        return line.rc, line.index

    def play_bars(self, omega, bg, fast_pos, last_pos, bg_fadeout):

        fast = False

        for bar in omega:
            if bar.position == fast_pos: fast = True
            position = self.play_bar(omega, bg, fast)
            if len(self.bar_waits) > 0:
                t = self.bar_waits.pop(0)
                #if t is not None: self.wait_to(t)
            if position == last_pos: break

        lines = VGroup([
            self.make_rc_line(bar.position)
            for bar in omega
        ])

        for bar in omega: bar.applied = False

        def hide_finished(omega):
            for bar, line in zip(omega, lines):
                if (bar[0].points == line.points).all():
                    if not bar.applied:
                        self.colorify_rc(bar.position)
                        bar.applied = True

                    bar.set_stroke(width = 0)

        animations = [Animation(VGroup(self.grid, self.grid_lines, bg))]
        if bg_fadeout: animations.append(FadeOut(VGroup(bg)))
        else: animations.append(Animation(VGroup(bg)))
        animations += [
            Transform(
                omega, lines,
                submobject_mode = "lagged_start",
            ),
            UpdateFromFunc(omega, hide_finished),
        ]
        self.play(*animations, run_time = 1.5)
        self.remove(omega)

class GridIntro(GridScene):
    def construct(self):

        self.make_grid()
        
        random.shuffle(self.grid_lines.submobjects)
        for line in self.grid_lines[1::2]:
            line.scale_in_place(-1)

        self.play(
            ShowCreation(
                self.grid_lines,
                submobject_mode = "lagged_start",
            )
        )
        self.add_foreground_mobjects(self.grid_lines)

        #self.wait_to(5.5)

        row = self.grid[self.grid_height]
        colors = [self.color_row for _ in row]
        for i in range(3):
            colors[self.grid_width-1+i] = self.color_col

        self.play(TurnSquares(row, colors))

        #self.wait_to(8.5)
        self.dither()
        self.play(row.highlight, BLACK)
        for sq in row: sq.color = BLACK

        column = VGroup([row[self.grid_width+2] for row in self.grid])
        colors = [self.color_col for _ in column]
        for i in range(2):
            colors[self.grid_height+i] = self.color_row
        self.play(TurnSquares(column, colors))

        #self.wait_to(12.5)
        self.dither()
        self.play(column.highlight, BLACK)
        for sq in column: sq.color = BLACK

        #self.wait_to(21)

class GridCollect(GridScene):
    def construct(self):

        self.make_grid()

        columns_Z = self.make_Z(4, 'c', self.color_col)
        rows_Z = self.make_Z(2, 'r', self.color_row)
        rows_Z.rotate(-np.pi/2)
        rows_Z.stretch(-1,0)
        VGroup(columns_Z,rows_Z).arrange_submobjects(buff = 0.5)

        rows_bg, rows_Z = rows_Z
        columns_bg, columns_Z = columns_Z

        rows_Z_fam = VGroup(rows_Z.family_members_with_points())
        columns_Z_fam = VGroup(columns_Z.family_members_with_points())

        rows = VGroup([self.make_rc_line(row.position) for row in rows_Z_fam])
        columns = VGroup([self.make_rc_line(col.position) for col in columns_Z_fam])

        self.play(ShowCreation(columns, submobject_mode = "all_at_once"))
        #self.wait_to(3)
        self.play(ShowCreation(rows, submobject_mode = "all_at_once"))

        #self.wait_to(6)
        self.play(
            FadeIn(columns_bg),
            ReplacementTransform(columns, columns_Z_fam),
        )
        self.play(
            FadeIn(rows_bg),
            ReplacementTransform(rows, rows_Z_fam),
        )

        #self.wait_to(10)

        # Transform compact rows and columns -> ordinal omega*4

        omega4 = OrdinalFiniteProd(OrdinalOmega, 4)
        omega4.highlight(self.color_row)
        VGroup(omega4[:2]).highlight(self.color_col)

        columns_Z[1].stretch_in_place(-1,1)
        rows_Z[0].stretch_in_place(-1,0)
        bg = columns_bg
        
        self.play(
            Transform(bg, self.make_bg(omega4[0], columns_Z[0])),
            ReplacementTransform(
                columns_Z[1], omega4[0],
                path_arc = np.pi,
            ),
            Animation(columns_Z[0]),
        )
        self.play(
            ReplacementTransform(
                columns_Z[0], omega4[1],
            ),
        )
        self.play(
            Transform(bg, self.make_bg(omega4[:3])),
            rows_bg.replace, self.make_bg(rows_Z[0]), 0, True,
            ReplacementTransform(
                rows_Z[1], omega4[2],
            ),
            Animation(VGroup(omega4[:2], rows_Z[0])),
        )
        self.play(
            FadeOut(rows_bg),
            Transform(bg, self.make_bg(omega4)),
            ReplacementTransform(
                rows_Z[0], omega4[3],
                path_arc = np.pi/2,
            ),
            Animation(VGroup(omega4[:3])),
        )

        # omega*4 -> omega

        #self.wait_to(16.5)

        part_order = 0,2,1,3
        omega = OrdinalOmega().to_edge(DOWN)

        omega4_mid = omega4.copy()
        omega_mid = VGroup([
            LimitSubOrdinal(omega[i::4]) for i in part_order
        ])
        for i,omega_part in enumerate(omega_mid):
            if i<2: omega_part.highlight(self.color_col)
            else: omega_part.highlight(self.color_row)
        omega_mid = omega_mid.copy()

        omega_mid.save_state()

        for mid in (omega_mid, omega4_mid):
            mid.stretch(0.5, 1)
            mid.arrange_submobjects(DOWN, buff = 0, coor_mask = Y_MASK)
            mid.move_to(VGroup(omega4, omega))

        self.play(
            Transform(bg, self.make_bg(omega4_mid)),
            ReplacementTransform(omega4, omega4_mid),
        )
        self.play(ReplacementTransform(omega4_mid, omega_mid))
        self.play(
            Transform(bg, self.make_bg(omega)),
            omega_mid.restore,
        )
        self.remove(omega_mid)
        self.add(omega)

        self.dither()
        #self.wait_to(23)

    def make_Z(self, size, symbol, color):
        
        omega = OrdinalOmega(x0=0, x1 = size)
        rev_omega = omega.copy().stretch(-1,0)

        for i,bar in enumerate(omega):
            bar.position = symbol,i
            bar[0].position = bar.position
        for i,bar in enumerate(rev_omega):
            bar.position = symbol,-i
            bar[0].position = bar.position
        omega.remove(omega[0])

        Z = VGroup(omega, rev_omega)
        Z.highlight(color)
        bg = self.make_bg(Z)
        return VGroup(bg, Z)

class OmegaGridColoring(GridScene):
    def construct(self):

        self.make_grid()

        omega = OrdinalOmega().to_edge(DOWN)
        omega_bg = self.make_bg(omega)

        i = 0
        rc = 'c'
        for bar in omega:
            if rc == 'c': bar.highlight(self.color_col)
            else: bar.highlight(self.color_row)
            bar.position = rc,i

            if rc == 'c': rc = 'r'
            else:
                rc = 'c'
                if i>0: i = -i
                else: i = -i+1

        self.add(omega_bg, omega)

        #self.wait_to(3.5)
        self.bar_waits = [5, 7.5, 11, 15.5, None, 19, None]
        self.play_bars(
            omega, omega_bg,
            ('c', -1), ('r', self.grid_height),
            bg_fadeout = True,
        )
        #self.wait_to(30.5)
        self.dither(2)

        self.play(
            self.grid.highlight, BLACK,
            Animation(self.grid_lines),
        )

class Omega4GridColoring(GridScene):
    def construct(self):

        self.make_grid()
        
        omega4 = OrdinalFiniteProd(OrdinalOmega,4).to_edge(DOWN)
        omega4_bg = self.make_bg(omega4)

        VGroup(omega4[0::2]).highlight(self.color_col)
        VGroup(omega4[1::2]).highlight(self.color_row)

        for i,bar in enumerate(omega4[0]):
            bar.position = 'c',i

        self.play(FadeIn(omega4_bg), FadeIn(omega4))

        omega_backup = omega4[0].copy()
        self.bar_waits = []
        self.play_bars(
            omega4[0], (omega4_bg, omega4[1:]),
            ('c', 1), ('c', 6),
            bg_fadeout = False,
        )
        #self.wait_to(9)

        omega4[1][0].position = 'r',0

        self.play_bar(omega4[1], (omega4_bg, omega4[2:]), fast = False)
        #self.wait_to(16)

        grid_problem = Line(
            ORIGIN, RIGHT*SPACE_WIDTH,
            color = YELLOW,
        )
        self.play(ShowCreation(grid_problem))
        ordinal_problem = Line(
            omega_backup.get_edge_center(LEFT)+0.1*LEFT,
            omega_backup.get_edge_center(RIGHT),
            color = YELLOW,
        )
        omega = omega_backup.copy()
        omega.highlight(DARK_GREY)
        #self.wait_to(20)
        self.play(
            FadeIn(omega),
            ShowCreation(ordinal_problem),
        )

        #self.wait_to(25)
        self.dither()
        self.play(
            FadeOut(grid_problem),
            VGroup(self.grid[self.grid_height][:self.grid_width]).highlight, BLACK,
            Animation(VGroup([
                self.grid_lines, omega4_bg, omega, omega4[1:], ordinal_problem,
            ]))
        )

        cut = 5
        #self.wait_to(29)
        self.dither()
        omega.save_state()
        VGroup(omega[cut:]).set_stroke(width = 0)
        self.play(
            VGroup([
                row[self.grid_width+cut:] for row in self.grid
            ]).highlight, BLACK,
            Animation(VGroup(self.grid_lines, omega4_bg)),
            MoveFromSaved(omega),
            Animation(VGroup(omega4[1:], ordinal_problem)),
        )

        for row in self.grid:
            for sq in row: sq.set_color(BLACK)
            for sq in row[self.grid_width : self.grid_width+cut]: sq.set_color(self.color_col)

        omega4[1][0].position = 'r',0
        #self.wait_to(33)
        self.play_bar(
            omega4[1],
            (omega4_bg, omega, ordinal_problem, omega4[2:]),
            fast = False
        )

        #self.wait_to(40.5)
        self.dither(2)
        self.play(
            FadeOut(VGroup(self.grid, self.grid_lines)),
            Animation(omega4_bg),
            FadeOut(VGroup(omega, omega4, ordinal_problem)),
        )

class CardinalFeature(Scene):
    def construct(self):

        omega = OrdinalOmega()
        omega.highlight(ord_color)
        omega_l = TexMobject("\\omega","=","\\aleph_0").next_to(omega, LEFT)
        omega_l[0].highlight(ord_color)
        omega_l[2].highlight(card_color)
        omega_g = VGroup(omega, omega_l)
        self.play(FadeIn(omega_g))

        pointer = TrianglePointer(color = YELLOW)
        pointer.next_to(omega[0], UP)
        pointer.set_fill(opacity = 0)

        for i in (1,2,3,4,5):
            pointer.save_state()
            pointer.set_fill(opacity = 1)
            pointer.next_to(omega[i], UP)
            self.play(MoveFromSaved(pointer, path_arc = -np.pi/3), run_time = 0.7)

        brace = BraceDesc(omega[:i+1], "<\\aleph_0")
        brace.desc.highlight(card_color)
        self.play(brace.creation_anim())

        #self.wait_to(9.5)

        continuum = LongOrdinal(color = ord_color)
        continuum_l = TexMobject("\\mathfrak c")
        continuum_l.highlight(card_color)
        continuum_l.next_to(continuum, LEFT, buff = 0.5)
        continuum_g = VGroup(continuum, continuum_l)

        shift = 2.2*UP
        continuum_g.save_state()
        continuum_g.shift(-shift)
        continuum_g.fade(1)

        omega_g.add(pointer, brace)
        omega_g.save_state()
        omega_g.shift(shift)
        omega_g.fade(1)
        self.play(
            MoveFromSaved(omega_g),
            continuum_g.restore,
        )

        pointer = TrianglePointer(color = YELLOW)
        pointer.next_to(continuum[1][0][0], UP)
        pointer.set_fill(opacity = 0)

        for i in (2,6):
            pointer.save_state()
            pointer.set_fill(opacity = 1)
            pointer.next_to(continuum[1][i][0], UP)
            self.play(MoveFromSaved(pointer, path_arc = -np.pi/3), run_time = 0.7)

        bars = []
        for x in (0, 2):
            bar = Line(ORIGIN, DOWN).highlight(ord_color).move_to(x*RIGHT)
            bar.save_state()
            pointer.save_state()
            pointer.next_to(bar, UP)
            bar.scale_in_place(0)
            bar.set_stroke(width=0)
            self.play(
                bar.restore,
                MoveFromSaved(pointer, path_arc = -np.pi/3),
                run_time = 0.7,
            )
            bars.append(bar)

        brace = BraceDesc([continuum[1][0][0], bar], "<\\mathfrak c")
        brace.desc.highlight(card_color)

        self.play(brace.creation_anim())
        self.dither(2)
        #self.wait_to(23)

class MagicSetScene(Scene):

    # pixels, intensity map

    def pixel_coord_to_point(self, pixel_coord):
        x,y = pixel_coord
        x = float(x)
        y = float(y)
        x += 1
        y += 1
        ph, pw = self.camera.pixel_shape
        sh, sw = self.camera.space_shape
        x -= pw/2
        y -= ph/2
        x *= 2*sw / pw
        y *= -2*sh / ph
        return np.array([x,y,0])

    def point_to_pixel_coord(self, point):
        return self.camera.points_to_pixel_coords(np.expand_dims(point,0))[0]

    def make_bg(self):
        bg = np.random.random(self.camera.pixel_shape)
        bg = 1-20*bg

        bg = np.maximum(bg, 0)
        bg = np.minimum(bg, 1)

        self.bg_intensity = np.stack([
            bg*1000,
            np.tile(
                np.arange(self.camera.pixel_shape[1]),
                (self.camera.pixel_shape[0], 1),
            ),
            np.tile(
                np.arange(self.camera.pixel_shape[0]),
                (self.camera.pixel_shape[1], 1),
            ).T,
        ], axis = -1).astype(np.int)

        bg = (255*bg).astype(np.uint8)
        bg = np.tile(np.expand_dims(bg,2),(1,1,3))

        return bg

    def find_bright_index(self, center, radius):
        x,y = self.point_to_pixel_coord(center)

        radius *= self.camera.pixel_shape[1] / SPACE_WIDTH
        radius = int(radius)
        y1, y2, x1, x2 = y-radius, y+radius, x-radius, x+radius
        y1 = max(y1,0)
        y2 = min(y2,self.camera.pixel_shape[0])
        x1 = max(x1,0)
        x2 = min(x2,self.camera.pixel_shape[1])

        bg_part = self.bg_intensity[y1:y2, x1:x2]
        bg_part = bg_part.reshape(-1, 3)
        max_index = np.argmax(bg_part[:,0])

        return bg_part[max_index,1:]

    def find_bright(self, center, radius = 0.1):
        return self.pixel_coord_to_point(self.find_bright_index(center, radius))
    
    def find_bright_points(self, points, radius = 0.1):
        result = []
        intensity_backup = []
        for point in points:
            index = self.find_bright_index(point, radius)
            result.append(self.pixel_coord_to_point(index))

            x,y = index
            intensity_backup.append((x,y,self.bg_intensity[y][x][0]))
            self.bg_intensity[y][x][0] = 0

        for x,y,intensity in intensity_backup:
            self.bg_intensity[y][x][0] = intensity

        return np.array(result)

    # circle manipulation

    def make_circum_circle(self, input_points):
        points = np.array(input_points)[:,:2]
        matrix = np.concatenate(
            (2*points, np.full([3,1], 1.0)),
            axis = 1,
        )
        b = points.T[0]**2 + points.T[1]**2

        try:
            (x,y,r) = np.linalg.solve(matrix, b)
            #print("circle")
            r += x**2 + y**2
            r = np.sqrt(r)
            center = np.array([x,y,0])
            result = Circle(radius = r).shift(center)
            result.center = center

        except np.linalg.LinAlgError:
            #print("line")
            result = Line(input_points[0], input_points[1])
            result.radius = 10**10
            result.scale_in_place(
                (SPACE_HEIGHT+SPACE_WIDTH)*2 / np.linalg.norm(points[0]-points[1])
            )
            print(result.points)

        return result.set_color(BLUE)

    def intersection_cc(self, circle1, circle2):
        center_diff = circle2.center - circle1.center
        center_dist_squared = np.dot(center_diff, center_diff)
        center_dist = np.sqrt(center_dist_squared)
        relative_center = (circle1.radius**2 - circle2.radius**2) / center_dist_squared
        center = (circle1.center + circle2.center)/2 + relative_center*center_diff/2

        rad_sum  = circle1.radius + circle2.radius
        rad_diff = circle1.radius - circle2.radius
        det = (rad_sum**2 - center_dist_squared) * (center_dist_squared - rad_diff**2)
        if np.isclose(det, 0): return [center]
        if det < 0: return []
        center_deviation = np.sqrt(det)
        center_deviation = np.array(((center_deviation,),(-center_deviation,)))
        center_deviation = center_deviation * 0.5*rotate_vector(center_diff, np.pi/2) / center_dist_squared

        return list(center + center_deviation)

    def show_circle_with_dots(self, circle, dots, base_time = 1, time1 = 0.1, time2 = 0.2, mid_layer = None):

        center = circle.get_center()
        vectors = np.array([dot.get_center() for dot in dots])
        vectors -= center
        cstart = circle.points[0]-center
        cend = circle.points[-1]-center
        angles = np.angle(-(vectors[:,0] + 1j*vectors[:,1])*(cstart[0]-1j*cstart[1]))

        if np.isclose(cstart, cend).all(): max_angle = np.pi
        else: max_angle = np.angle(-(cend[0] + 1j*cend[1])*(cstart[0]-1j*cstart[1]))

        angles += np.pi
        max_angle += np.pi
        angles /= max_angle

        def smooth_inverse(t):
            a = 0.0 # smooth(a) < t
            b = 1.0 # smooth(a) > t
            for _ in range(20):
                m = (a+b)/2
                if smooth(m) < t: a = m
                elif smooth(m) > t: b = m
                else: break

            return m

        dot_starts = np.array([smooth_inverse(angle) for angle in angles])

        for dot in dots:
            dot.save_state()
            dot.scale_in_place(0)

        run_time = base_time + time1 + time2
        time1 /= run_time
        time2 /= run_time
        dot_starts *= base_time / run_time
        dot_time = time1+time2

        animations = [
            ShowCreation(circle,
                         rate_func = squish_rate_func(smooth, time1, 1-time2))
        ]
        if mid_layer is not None: animations.append(Animation(mid_layer))

        for dot,start in zip(dots,dot_starts):
            animations.append(
                ApplyMethod(dot.restore,
                            rate_func = squish_rate_func(smooth, start, start+dot_time))
            )

        self.play(
            *animations,
            run_time = run_time
        )

class MagicSetIntro(MagicSetScene):

    def prepare_effect(self, dots_in_row = 50):

        bg = self.make_bg()

        bg_black = Rectangle(
            width = 2*SPACE_WIDTH+0.1,
            height = 2*SPACE_HEIGHT+0.1,
            fill_opacity = 1,
            stroke_width = 0,
            color = BLACK,
        )
        dots_in_column = int(dots_in_row * SPACE_HEIGHT/SPACE_WIDTH)
        points = np.stack([
            np.tile(np.linspace(-SPACE_WIDTH, SPACE_WIDTH, dots_in_row+2)[1:-1], (dots_in_column,1)),
            np.tile(np.linspace(-SPACE_HEIGHT, SPACE_HEIGHT, dots_in_column+2)[1:-1], (dots_in_row,1)).T,
            np.zeros([dots_in_column, dots_in_row]),
        ], axis = -1).reshape([-1,3])
        points = list(self.find_bright_points(points, radius = SPACE_WIDTH / dots_in_row))
        random.shuffle(points)
        dots = VGroup([
            Dot(point)
            for point in points
        ])
        dots_dest = dots.copy()
        for dot in dots_dest: dot.scale_in_place(0)
        dots.set_fill(opacity = 0)
        dots.scale(1.1)

        self.set_camera_background(bg)

        return bg_black, dots, dots_dest

    def construct(self):

        #bg_mob = MobjectFromPixelArray(bg)
        #pixel_size = 2*SPACE_WIDTH / self.camera.pixel_shape[1]
        #bg_mob.shift(UP*pixel_size)
        #bg_mob.save_state()
        #bg_mob.scale(1.2)
        #bg_mob.fade(1)

        bg_black, dots, dots_dest = self.prepare_effect()

        self.play(
            #bg_mob.restore,
            FadeOut(bg_black),
            Transform(dots, dots_dest, submobject_mode = "lagged_start", rate_func = None),
            run_time = 3,
        )
        #self.remove(bg_mob)
        #self.wait_to(3.5)

        points = [
            [0.12, 0.77],
            [-1.77, 2.82],
            [-2.43, 0.19],
            [-3.19, -1.75],
            [0.38, -0.43],
            [2.28, -1.01],
            [-6.04, -0.69],
            [5.23, 2.52],
        ]
        points = np.array([point+[0] for point in points])
        points = self.find_bright_points(points)
        point_i_triples = [
            (0,1,2),
            (2,3,4),
            (0,4,5),
        ]
        dots = VGroup()
        circles = VGroup()
        used_indices = set()

        def show_triple(point_i_triple, to_arc = None):
            point_triple = [points[i] for i in point_i_triple]
            circle = self.make_circum_circle(point_triple)
            new_points = [points[i] for i in point_i_triple if i not in used_indices]
            new_dots = VGroup([Dot(point) for point in new_points])

            if to_arc is not None:
                start, end = to_arc
                arc = Arc(end-start, start_angle = start, radius = circle.radius)
                arc.shift(circle.center)
                circle = arc

            circle.highlight(BLUE)
            new_dots.highlight(YELLOW)

            self.show_circle_with_dots(circle, new_dots)
            self.add_foreground_mobjects(*new_dots)

            dots.add(*new_dots)
            circles.add(circle)
            used_indices.add(point_i_triple)

        for point_i_triple in point_i_triples: show_triple(point_i_triple)

        #self.wait_to(8)
        self.play(circles.highlight, GREY)
        #self.wait_to(9.5)

        mini_places = [
            [-5.08, 2.59],
            [-5.17, 1.],
            [-5.06, -2.73],
            [-1.1, -1.96],
            [-1.42, 1.42],
            [1.17, 2.72],
            [1.55, -2.71],
            [4.86, -2.05],
            [5.46, 0.06],
        ]
        random.shuffle(mini_places)
        mini_places = np.array([point+[0] for point in mini_places])
        radius = 0.5
        sample_size = 6

        mini_circles = []
        for center in mini_places:
            sample = self.find_bright_points(np.tile(center, (sample_size,1)), radius = radius)
            circle_candidates = [
                (self.make_circum_circle((A,B,C)), (A,B,C))
                for i,A in enumerate(sample)
                for j,B in enumerate(sample[:i])
                for C in sample[:j]
            ]
            mini_circles.append(min(circle_candidates, key = lambda (circle,abc): circle.radius))

        mini_circles.sort(key = lambda (circle, abc): circle.radius, reverse = True)
            
        for circle, abc in mini_circles:
            new_dots = [Dot(point).highlight(YELLOW) for point in abc]

            self.show_circle_with_dots(circle, new_dots, base_time = 0.5)

            dots.add(*new_dots)
            self.add_foreground_mobjects(*new_dots)
            circles.add(circle)

        #self.wait_to(18.5)
        self.play(circles.highlight, GREY)
        show_triple((4,6,7), to_arc = (4.3, 5.8))

        #self.wait_to(29.5)
        self.dither(2)
        self.play(
            FadeIn(bg_black),
            FadeOut(circles),
            FadeOut(dots),
        )

class ContinuumSquare(Scene):
    def construct(self):

        colors = (BLUE, YELLOW)
        series = VideoSeries(num_videos = 16).to_edge(UP)
        series[1].highlight(YELLOW)

        aleph0_eq = self.make_card_eq("\\aleph_0")
        aleph0_pair = TexMobject("r,c")
        aleph0_pair[0].highlight(colors[0])
        aleph0_pair[-1].highlight(colors[1])
        aleph0_line = Line(ORIGIN, 1.5*DOWN)
        aleph0_enc = TexMobject("2^r","\\cdot","(2c+1)","-1")
        aleph0_enc[0].highlight(colors[0])
        aleph0_enc[2].highlight(colors[1])
        aleph0_g = VGroup(aleph0_eq, aleph0_pair, aleph0_line, aleph0_enc)
        aleph0_g.arrange_submobjects(DOWN).to_edge(LEFT)
        aleph0_eq.next_to(series, DOWN, coor_mask = 0.7*Y_MASK)

        series.save_state()
        series.behind_edge(UP)
        self.play(series.restore)
        #self.wait_to(2.5)
        self.play(Write(aleph0_eq))
        #self.wait_to(6)
        self.play(FadeIn(aleph0_pair))
        #self.wait_to(10.5)
        self.play(
            FadeIn(aleph0_enc),
            ShowCreation(aleph0_line),
        )

        #self.wait_to(18)
        self.play(series.behind_edge, UP)

        cont_eq = self.make_card_eq("\\mathfrak{c}")
        cont_eq.move_to(aleph0_eq)
        cont_eq.to_edge(RIGHT, buff = 2)

        finite_neq = TexMobject("2\\cdot2\\neq4")
        VGroup([finite_neq[i] for i in (0,2,-1)]).highlight(card_color)
        finite_neq.move_to(cont_eq)
        #self.wait_to(24)
        self.play(FadeIn(finite_neq))

        #self.wait_to(30.5)
        self.play(FadeOut(finite_neq))
        self.play(FadeIn(cont_eq))

        self.digit_spacing = 0.5
        sequences = VGroup([self.make_rand_seq() for _ in range(2)])
        sequences.arrange_submobjects(DOWN, coor_mask = Y_MASK)
        sequences[1].shift(RIGHT*self.digit_spacing/2)
        for seq, col in zip(sequences, colors): seq.highlight(col)
        sequences.move_to(aleph0_pair)
        sequences.shift(RIGHT*(SPACE_WIDTH - sequences[1][-1].get_center()))

        merged = VGroup(list(itertools.chain(*zip(*sequences)))).copy()

        merged.save_state()
        merged.move_to(aleph0_enc, coor_mask = Y_MASK)

        cont_line = Line(
            sequences.get_corner(LEFT+DOWN),
            merged.get_corner(LEFT+UP),
            buff = 0.1
        )
        cont_line.move_to(cont_eq, coor_mask = X_MASK)

        for seq,t in zip(sequences, (33.5, 37)):
            #self.wait_to(t)
            self.play(ShowCreation(seq))

        #self.wait_to(40)
        self.play(
            MoveFromSaved(merged),
            ShowCreation(cont_line),
        )

        #self.wait_to(45)
        merged.save_state()
        self.arrange_seq(merged)
        merged.next_to(sequences, DOWN, aligned_edge = LEFT)
        merged.move_to(aleph0_enc, coor_mask = Y_MASK)

        cont_line_dest = Line(
            sequences.get_corner(LEFT+DOWN),
            merged.get_corner(LEFT+UP),
            buff = 0.1
        )
        cont_line_dest.move_to(cont_line, coor_mask = X_MASK)
        self.play(
            MoveFromSaved(merged),
            Transform(cont_line, cont_line_dest),
        )

        #self.wait_to(48.5)

        general = VGroup(
            TexMobject("|A|","\\geq","\\aleph_0","\\Rightarrow"),
            TexMobject("|A\\times A|","=","|A|"),
        ).arrange_submobjects(DOWN)
        for eq in general:
            VGroup(eq[0], eq[2]).highlight(card_color)

        general.to_edge(UP)
        gen_rect = SurroundingRectangle(general)

        self.play(
            ShowCreation(gen_rect),
            FadeIn(general[1]),
        )
        #self.wait_to(54)
        self.play(FadeIn(general[0]))        

        #self.wait_to(57)
        cont_g = VGroup(cont_eq, sequences, merged, cont_line)

        cont_assumption = TexMobject("|A|","<","\\mathfrak c")
        cont_impl = TexMobject("|A\\times A|","<","\\mathfrak c")
        cont_usage = VGroup(cont_assumption, cont_impl).arrange_submobjects(DOWN)

        for eq in cont_usage:
            VGroup(eq[0], eq[2]).highlight(card_color)

        self.play(
            aleph0_g.behind_edge, LEFT,
            cont_g.behind_edge, RIGHT,
            FadeIn(cont_assumption, submobject_mode = "lagged_start"),
        )
        #self.wait_to(60+2)
        self.play(FadeIn(cont_impl, submobject_mode = "lagged_start"))
        #self.wait_to(60+7)

        third_A = VGroup(cont_impl[0][1:3]).copy()
        shift = cont_impl[0][1].get_center() - cont_impl[0][3].get_center()
        self.play(
            third_A.shift, shift,
            cont_impl[0][0].shift, shift,
        )
        #self.wait_to(60+20.5)
        self.dither()
        self.play(FadeOut(VGroup(general, gen_rect, cont_usage, third_A)))

    def make_card_eq(self, cardinal):
        card_eq = TexMobject(cardinal,"\\cdot",cardinal,"=",cardinal)
        VGroup(card_eq[::2]).highlight(card_color)
        return card_eq

    def arrange_seq(self, seq):
        for i,digit in enumerate(seq):
            digit.move_to(i*self.digit_spacing*RIGHT)
        return seq

    def make_rand_seq(self, seq_len = 10):
        digits = [TexMobject(str(i)) for i in range(2)]
        return self.arrange_seq(VGroup([
            random.choice(digits).copy()
            for _ in range(seq_len)
        ]))

def make_circles_cardinal():
    ordinal = LongOrdinal(color = BLUE, height = 0.5)
    ordinal_l = TexMobject("\\mathfrak c").next_to(ordinal, LEFT).highlight(card_color)
    circles_label = TextMobject("Circles").next_to(ordinal, DOWN)
    ordinal_g = VGroup(ordinal, ordinal_l, circles_label)
    ordinal_g.to_edge(DOWN)
    ordinal_bg = BackgroundRectangle(ordinal_g, buff = 0.2)
    ordinal_g.add_to_back(ordinal_bg)
    return ordinal_g

class CirclesCardinality(Scene):
    def construct(self):

        ordinal_g = make_circles_cardinal()
        ordinal_bg, ordinal, ordinal_l, circles_label = ordinal_g
        ordinal_g.remove(ordinal_l)

        self.add(ordinal_bg)
        self.play(ordinal.creation_anim())
        #self.wait_to(2.5)
        self.play(FadeIn(circles_label, submobject_mode = "lagged_start"))
        #self.wait_to(7.5)

        axes = Axes()
        self.play(ShowCreation(axes), Animation(ordinal_g))

        center_p = np.array([-2.6, 1.9, 0])
        radius = 1.5
        circle = Circle(color = BLUE, radius = radius).shift(center_p)
        center = Dot(center_p)
        self.play(
            GrowFromCenter(circle),
            GrowFromCenter(center),
        )

        rad_line = Line(center_p, center_p+radius*RIGHT, color = GREEN)
        rad_label = TexMobject(str(radius))
        rad_label.highlight(GREEN)
        rad_label.scale(0.8)
        rad_label.next_to(rad_line, UP)
        self.play(
            ShowCreation(rad_line),
            Animation(center),
            Animation(circle),
            FadeIn(rad_label),
        )
        center_l = TexMobject('[',str(center_p[0]),',',str(center_p[1]),']')
        center_l.scale(0.8)
        center_l.next_to(center, DOWN)

        #self.wait_to(12.5)
        self.play(
            FadeIn(center_l),
            FocusOn2(center),
        )
        triple_num = TexMobject(str(center_p[0]),',',str(center_p[1]),',', str(radius))
        triple_num.next_to(ORIGIN, LEFT+DOWN, buff = 0.3)
        triple_num[-1].highlight(GREEN)

        #self.wait_to(16.5)
        self.play(
            FadeIn(triple_num[3]),
            ReplacementTransform(VGroup(center_l[1:-1]).copy(), VGroup(triple_num[:3])),
            ReplacementTransform(rad_label.copy(), triple_num[4], path_arc = -np.pi/3),
        )

        cont_dot = TexMobject("\\mathfrak c\cdot")
        cont_dot.next_to(ordinal, UP)
        triple_cont = VGroup([
            cont_dot[0].copy().move_to(VGroup(num[-3:]), coor_mask = X_MASK)
            for num in triple_num[::2]
        ])
        triple_cont.highlight(card_color)
        double_dot = VGroup([
            cont_dot[1].copy().move_to(VGroup(triple_cont[i:i+2]))
            for i in range(2)
        ])
        #self.wait_to(22)
        self.play(Write(triple_cont[0]), run_time = 0.8)
        for cont, dot in zip(triple_cont[1:], double_dot):
            self.play(
                FadeIn(dot),
                Write(cont),
                run_time = 0.8,
            )

        #self.wait_to(25.3)
        self.dither(2)
        double_dot.save_state()
        triple_cont.save_state()
        for cont in triple_cont[::2]:
            cont.move_to(triple_cont[1])
        for dot in double_dot:
            dot.move_to(triple_cont[1], coor_mask = X_MASK)
            dot.set_fill(opacity = 0)

        self.play(
            FadeOut(VGroup(
                triple_num,
                rad_line,
                rad_label,
                axes,
                circle,
                center,
                center_l,
            )),
            MoveFromSaved(double_dot),
            MoveFromSaved(triple_cont),
            Animation(ordinal_g),
        )
        self.remove(double_dot, triple_cont)
        cont_label = triple_cont[1]
        self.add(cont_label)

        #self.wait_to(28.5)
        self.play(
            ReplacementTransform(cont_label, ordinal_l, path_arc = np.pi)
        )
        #self.wait_to(38.5)

class MagicSetConstruction(MagicSetScene):

    def intersection_set(self, circle, circle_set):
        intersections = []
        for circle2 in circle_set:
            intersection += self.other_intersections(circle, circle2)
        return intersections

    def other_intersections(self, circ1, circ2):
        intersections = []
        for intersection in self.intersection_cc(circ1, circ2):
            for point in self.points:
                if np.isclose(intersection, point).all():
                    break
            else:
                intersections.append(intersection)

        return intersections

    def put_dot_anim(self, dot, circle, scale = 1.5):
        dot_src = dot.copy()
        dot_src.save_state()
        dot_src.scale(1.5, about_point = circle.center)
        dot_src.set_fill(opacity = 0)
        return ReplacementTransform(dot_src, dot)

    def put_dot(self, dot, circle, **kwargs):
        self.play(self.put_dot_anim(dot, circle, **kwargs))
        self.dots_y.add(dot)

    def bar_to_circle(self, bar, circle, animations = ()):
        bar_c = bar[0].copy()
        self.play(
            bar.highlight, YELLOW,
            bar_c.shift, 1.5*UP,
            *animations
        )
        bar_c.align_data(circle)
        bar_c.points = np.array([
            interpolate(bar_c.get_start(), bar_c.get_end(), alpha)
            for alpha in np.linspace(0,1,len(circle.points))
        ])
        self.play(ReplacementTransform(bar_c, circle))

    def construct(self):

        ordinal_g = make_circles_cardinal()
        ordinal_bg, ordinal, ordinal_l, circles_label = ordinal_g
        self.add(ordinal_g)

        points = [
            [-1.01,  2.56],
            [-3.89,  1.48],
            [-1.82, -0.17],
            [ 0.65,  2.38],
            [ 2.21,  0.71],
            [ 1.44, -0.6],
            [-2.5,   0.89],
            [-2.44, -0.71],
            [ 0.53,  0.33],
        ]
        points = np.array([point+[0] for point in points])
        circ3_points = points[6:]
        points = points[:6]
        self.points = points
        dots = VGroup([
            Dot(point, color = YELLOW)
            for point in points
        ])

        triple_indices = list(itertools.combinations(range(6), 3))
        circles = VGroup([
            self.make_circum_circle([points[i] for i in triple])
            for triple in triple_indices
        ])
        circles_d = dict(zip(triple_indices, circles))

        circles.highlight(DARK_GREY)
        #circles_d[0,1,2].highlight(GREY)
        #circles_d[3,4,5].highlight(BLUE)

        circle1 = circles_d[0,1,2]
        circle1.highlight(BLUE)
        self.bar_to_circle(ordinal[1][0][0], circle1)
        self.dots_y = VGroup()
        self.dots_n = VGroup()

        self.add_foreground_mobjects(self.dots_y, self.dots_n)

        for dot in dots[:3]:
            self.put_dot(dot, circle1)

        circle2 = circles_d[3,4,5]
        circle2.highlight(BLUE)
        self.bar_to_circle(ordinal[1][0][1], circle2,
                           animations = (ApplyMethod(circle1.highlight, GREY),))

        intersections = self.intersection_cc(circle1, circle2)
        inter_dots = VGroup([Dot(inter, color = RED) for inter in intersections])
        dot = inter_dots[0].highlight(YELLOW)

        self.foreground_mobjects = [self.dots_n, self.dots_y]
        #self.wait_to(8)
        self.play(self.put_dot_anim(dot, circle2))
        self.dots_n.add(dot)
        
        #self.wait_to(11.5)
        self.add(circle1, self.dots_n, self.dots_y)
        circle1.highlight(RED)
        self.dither(0.3)
        circle1.highlight(GREY)
        self.dither(0.2)
        circle1.highlight(RED)
        self.dither(2)

        #self.wait_to(19)
        self.play(circle1.highlight, GREY)
        inter_dots[0].highlight(RED)
        self.dots_n.add(inter_dots[1])
        self.add(circle2, inter_dots)

        #self.wait_to(23.5)
        self.put_dot(dots[3], circle2)

        #self.wait_to(31.5)
        index = 0
        for triple in triple_indices:
            if 3 not in triple: continue
            if triple[-1] > 3: continue

            dots.highlight(GREY)
            for i in triple: dots[i].highlight(YELLOW)
            intersections = self.other_intersections(circles_d[triple], circle2)
            inter_dots = VGroup([
                Dot(point).highlight(RED) for point in intersections
            ])
            #if index == 0: self.wait_to(34.5)
            self.show_circle_with_dots(
                circles_d[triple],
                inter_dots,
                mid_layer = VGroup(circle1, circle2)
            )
            self.dots_n.add(*inter_dots)
            #if index == 0: self.wait_to(43)

            index += 1

        dots.highlight(YELLOW)
        #self.wait_to(53)

        self.foreground_mobjects = [circle1, circle2, self.dots_n, self.dots_y, ordinal_g]
        self.put_dot(dots[4], circle2)
        #self.wait_to(57.5)
        for triple in triple_indices:
            if 4 not in triple: continue
            if triple[-1] > 4: continue

            dots.highlight(GREY)
            for i in triple: dots[i].highlight(YELLOW)
            circ = circles_d[triple]
            intersections = self.other_intersections(circ, circle2)
            inter_dots = VGroup([
                Dot(point).highlight(RED) for point in intersections
            ])
            self.dots_n.add(*inter_dots)
            self.add(circ, *self.foreground_mobjects)
            self.dither(0.4)

        dots.highlight(YELLOW)

        #self.wait_to(60+5)
        self.foreground_mobjects = [self.dots_n, self.dots_y]
        self.put_dot(dots[5], circle2)

        self.foreground_mobjects = [circle1, circle2, self.dots_n, self.dots_y, ordinal_g]
        remaining_circles = filter(lambda circ: circ not in self.mobjects, circles)

        #self.wait_to(60+7)
        self.play(*map(FadeIn, remaining_circles))

        #self.wait_to(60+10)

        self.foreground_mobjects = [self.dots_y]
        self.play(
            circle2.highlight, GREY,
            FadeOut(self.dots_n),
        )

        circle3 = self.make_circum_circle(circ3_points)
        circle3.save_state()
        #self.wait_to(60+11.5)
        self.bar_to_circle(ordinal[1][0][2], circle3)

        #self.wait_to(60+17)
        self.play(Transform(circle3, self.make_circum_circle([
            points[1], circ3_points[0], circ3_points[1],
        ])))
        self.dither()
        self.play(Transform(circle3, self.make_circum_circle([
            points[1], points[2], circ3_points[1],
        ])))

        #self.wait_to(60+23)
        self.play(Transform(circle3, circles_d[1,2,3].copy().highlight(BLUE)))

        #self.wait_to(60+36)
        self.play(circle3.restore)

        intersections = itertools.chain(*[
            self.intersection_cc(circle3, circ)
            for circ in circles
        ])
        intersections = VGroup([
            Dot(point, color = RED)
            for point in intersections
        ])
        intersections.save_state()
        for dot in intersections: dot.scale_in_place(0)
        #self.wait_to(60+45.5)
        self.play(intersections.restore)

        pointer = TrianglePointer(color = YELLOW).next_to(ordinal, UP)
        pointer.move_to(ordinal[1][0][2], coor_mask = X_MASK)
        pointer.save_state()
        pointer.shift(LEFT)
        pointer.set_fill(opacity = 0)

        #self.wait_to(60+48)
        self.play(pointer.restore)

        #self.wait_to(60+51)
        shift = ordinal.get_edge_center(UP) - pointer.get_edge_center(UP)
        arc_path = -2*angle_of_vector(shift)
        self.play(ApplyMethod(pointer.shift, shift, path_arc = arc_path))

        #self.wait_to(60+55.5)
        self.dither(2)
        self.foreground_mobjects = [ordinal_g, pointer]

        self.play(FadeOut(VGroup(
            list_update(circles, [circle1, circle2]), circle3,
            intersections, self.dots_y,
        )))

class MagicSetEffect(MagicSetIntro):

    def construct(self):

        ordinal_g = make_circles_cardinal()
        ordinal_bg, ordinal, ordinal_l, circles_label = ordinal_g
        for bar in ordinal[1][0][:3]: bar.highlight(YELLOW)
        self.add(ordinal_g)

        ordinal_dest = LongOrdinal(height = ordinal.height, color = YELLOW).move_to(ordinal)

        bg_black, dots, dots_dest = self.prepare_effect()
        circle = Circle(color = BLUE)
        def update_circle(circle, alpha):
            random_circle = Circle(radius = 0.1+np.random.random()*SPACE_HEIGHT)
            random_circle.shift(np.array([
                SPACE_WIDTH*(2*np.random.random()-1),
                SPACE_HEIGHT*(2*np.random.random()-1),
                0,
            ]))
            circle.points = random_circle.points
            circle.set_stroke(width = 4*(1-alpha))

        self.play(
            UpdateFromAlphaFunc(circle, update_circle),
            FadeOut(bg_black),
            Transform(dots, dots_dest),
            Animation(ordinal_bg),
            Transform(
                ordinal[0], ordinal_dest[0],
                rate_func = squish_rate_func(smooth, 0, 1),
                submobject_mode = "lagged_start",
            ),
            Transform(
                ordinal[1], ordinal_dest[1],
                rate_func = squish_rate_func(rush_from, 0, 0.85),
                submobject_mode = "one_at_a_time",
            ),
            Animation(ordinal_l), Animation(circles_label),
            run_time = 5,
        )
        self.remove(dots, circle)
        #self.wait_to(19.5)
        self.dither(2)
        self.play(FadeIn(bg_black))

class MagicSetCardinality(MagicSetConstruction):

    def construct(self):

        ordinal_g = make_circles_cardinal()
        ordinal_bg, ordinal, ordinal_l, circles_label = ordinal_g
        for bar in ordinal[1][0][:3]: bar.highlight(YELLOW)

        pointer = TrianglePointer().highlight(YELLOW)
        pointer.shift(ordinal.get_edge_center(UP) - pointer.get_edge_center(UP))

        self.add(ordinal_g, pointer)

        less_c_str = "<\\mathfrak c"
        brace_steps = BraceDesc(
            Line(
                ordinal.get_corner(UP+LEFT),
                pointer.get_corner(UP+LEFT),
            ),
            less_c_str,
            UP,
        )
        brace_steps.desc.highlight(RED)
        #self.wait_to(3)
        self.play(brace_steps.creation_anim())

        #self.wait_to(11)

        buff = 0.5
        min_x = -SPACE_WIDTH+buff
        max_x = 4
        min_y = brace_steps.get_edge_center(UP)[1]+buff
        max_y = SPACE_HEIGHT-buff

        points = np.random.random(size = [300,3])
        points *= np.array([max_x - min_x, max_y - min_y, 0])
        points += np.array([min_x, min_y, 0])

        dot = Dot().highlight(YELLOW)
        dots = []
        for point in points:
            dot.move_to(point)
            dots.append(dot)
            dot = dot.copy()
            dot.scale(0.99)

        dots = VGroup(dots)

        brace_plane = BraceDesc(dots, less_c_str, RIGHT)
        brace_plane.desc.highlight(RED)
        max_x = brace_plane.brace.get_edge_center(LEFT)[0]

        self.play(FadeIn(dots), brace_plane.creation_anim())

        #self.wait_to(15)

        circles = []
        used = set()
        while len(circles) < 160:
            triple = tuple(sorted(np.random.randint(100, size = 3)))
            if len(set(triple)) < 3: continue
            if triple in used: continue
            used.add(triple)
            circle = self.make_circum_circle([points[i] for i in triple])
            circle.stroke_width *= 0.995 ** triple[-1]
            circle.triple = triple
            corner = circle.get_corner(DOWN+RIGHT)
            if corner[0] > max_x: continue
            if corner[1] < min_y: continue
            circles.append(circle)

        circles.sort(
            key = lambda circ: max(
                circ.get_edge_center(UP)[0] - min_y,
                max_y-min_y,
            ) / circ.stroke_width,
        )
        circles = VGroup(circles)
        circles.highlight(DARK_GREY)

        #self.add(circles, dots)
        # 1, 4, 5
        circle1 = circles[1]
        circle1.highlight(BLUE)

        dots.save_state()
        dots.highlight(GREY)
        hl_dots1 = VGroup([dots[i] for i in circle1.triple])
        hl_dots1.highlight(YELLOW)

        self.play(MoveFromSaved(dots))
        self.play(ShowCreation(circle1), Animation(hl_dots1))

        circle2 = circles[4]
        circle2.highlight(DARK_GREY)
        hl_dots2 = VGroup([dots[i] for i in circle2.triple])

        #self.wait_to(19.5)
        self.play(ShowCreation(circle2), hl_dots2.highlight, YELLOW)

        #self.wait_to(36)
        missing_circles = list_difference_update(circles.submobjects, [circle1, circle2])
        self.play(
            FadeIn(VGroup(missing_circles)),
            circle1.highlight, DARK_GREY,
            circle2.highlight, DARK_GREY,
            dots.highlight, YELLOW,
        )

        p0 = dots.get_corner(DOWN+RIGHT)+0.2*RIGHT
        p1 = np.array(p0)
        p1[1] = SPACE_HEIGHT+1
        #self.wait_to(40)
        self.play(brace_plane.shift_brace, Line(p0, p1))

        bar = Line(ORIGIN, 0.6*DOWN, color = BLUE)
        bar.next_to(circles, DOWN, coor_mask = Y_MASK)
        bar.save_state()
        bar.scale(0)
        bar.move_to(ordinal)

        #self.wait_to(43.5)
        self.play(
            FadeOut(dots),
            bar.restore,
        )

        circle = Circle(color = BLUE, radius = 1.3)
        circle.center = 1.7*UP + 0.8*LEFT
        circle.shift(circle.center)
        bar.points = np.array([
            interpolate(bar.get_start(), bar.get_end(), alpha)
            for alpha in np.linspace(0,1,len(circle.points))
        ])

        self.play(ReplacementTransform(bar, circle))

        #self.wait_to(47.5)

        circles_inter = list(filter(lambda c: len(self.intersection_cc(c, circle)) > 1, circles))

        red_circ = circles_inter[1]
        self.play(red_circ.highlight, RED)

        intersections = self.intersection_cc(red_circ, circle)
        inter_hl = VGroup([
            Circle(color = YELLOW, radius = 0.1).shift(point)
            for point in intersections
        ])
        #self.wait_to(49)
        self.play(ShowCreation(inter_hl))

        red_dots = VGroup([
            Dot(color = RED).shift(point)
            for point in intersections
        ])
        self.play(
            red_circ.highlight, DARK_GREY,
            ReplacementTransform(inter_hl, red_dots),
        )

        dashed_circ = DashedMobject(circle, dashes_num = 30, spacing = 0.5, color = RED)
        angle_src = angle_of_vector(dashed_circ[0].points[-1]-circle.center) / 2
        angle_dest = angle_of_vector(red_dots[0].get_center()-circle.center)
        dashed_circ.rotate(angle_dest-angle_src, about_point = circle.center)

        #self.wait_to(54.5)
        red_dots.save_state()
        for dot in red_dots: dot.scale_in_place(0)
        self.play(
            circle.fade, 0.8,
            ShowCreation(dashed_circ),
            FadeOut(brace_plane.brace),
            MoveFromSaved(red_dots),
        )
        self.remove(red_dots)

        red_points_label = TexMobject(less_c_str).highlight(RED)
        red_points_label.next_to(circle, UP)
        red_points_label.shift(RIGHT+0.3*DOWN)

        #self.wait_to(56)
        self.play(
            FadeOut(circles),
            Animation(circle), 
            Animation(dashed_circ),
            ReplacementTransform(brace_plane.desc, red_points_label),
        )

        i = 8
        angle1 = angle_of_vector(dashed_circ[i].points[-1] - circle.center)
        angle2 = angle_of_vector(dashed_circ[i+1].points[0] - circle.center)
        angle = (angle1+angle2)/2
        point = circle.center + circle.radius * rotate_vector(RIGHT, angle)
        dot = Dot(point, color = YELLOW)
        self.dots_y = VGroup()
        #self.wait_to(60+1.5)
        self.put_dot(dot, circle)

        #self.wait_to(60+14)
        self.play(FocusOn2(ordinal_l))
        #self.wait_to(60+16)
        self.play(FocusOn2(brace_steps.desc))
        #self.wait_to(60+20)
        self.dither()
        self.play(FadeOut(VGroup(
            circle, dashed_circ, red_points_label, brace_steps, pointer, dot
        )))

class Aleph0Square(Scene):
    def construct(self):

        goal = TexMobject("\\kappa\\times\\kappa = \\kappa").scale(1.2)
        subgoal = TexMobject("\\aleph_0","\\times","\\aleph_0","=","\\aleph_0")
        subgoal2 = TexMobject("\\aleph_1","\\times","\\aleph_1","=","\\aleph_1")
        subgoal.next_to(goal, UP)
        subgoal2.to_corner(UP+RIGHT)
        for g in (goal, subgoal, subgoal2): VGroup(g[::2]).highlight(card_color)
        self.play(Write(goal))
        #self.wait_to(16.5)
        self.play(FadeIn(subgoal, submobject_mode = "lagged_start"))
        #self.wait_to(24.5)
        self.play(
            FadeOut(goal),
            subgoal.to_corner, UP+LEFT,
        )

        sq_size = np.array([0.8, 0.8, 1])
        side_len = 11
        dots = VGroup([
            [
                Dot(i*sq_size*DOWN + j*sq_size*RIGHT, color = YELLOW)
                for j in range(side_len)
            ]
            for i in range(side_len)
        ])
        subsquares = VGroup([
            Square(
                side_length = i+1, color = GREEN
            ).scale(sq_size).shift(i*sq_size*0.5*(DOWN+RIGHT))
            for i in range(side_len)
        ])
        surr_square = SurroundingRectangle(subsquares, color = WHITE)
        #r1 = subsquares[0]
        #r2 = subsquares[1]
        #print()
        L_shapes = VGroup([
            Polygon(
                *np.concatenate((r1.get_anchors()[::-1], r2.get_anchors()), 0),
                color = GREEN,
                stroke_width = 0,
                fill_opacity = 0.2
            )
            for r1, r2 in zip(subsquares, subsquares[1:])
        ])
        square_g = VGroup(surr_square, subsquares, dots, L_shapes)
        square_g.to_corner(DOWN+RIGHT, buff = -0.2)
        square_g.to_edge(UP, buff = 1.5)

        rows_l = VGroup([TexMobject(str(i)) for i in range(side_len)])
        cols_l = rows_l.copy()
        for label, row in zip(rows_l, dots):
            label.move_to(row)
            label.next_to(surr_square, LEFT, coor_mask = X_MASK)
        for label, col in zip(cols_l, dots[0]):
            label.move_to(col)
            label.next_to(surr_square, UP, coor_mask = Y_MASK)

        self.dither()
        self.play(
            FadeIn(
                cols_l,
                submobject_mode = "lagged_start",
                rate_func = squish_rate_func(smooth, 0, 0.5),
            ),
            FadeIn(
                rows_l,
                submobject_mode = "lagged_start",
                rate_func = squish_rate_func(smooth, 0.5, 1),
            ),
            ShowCreation(surr_square),
            FadeIn(dots, submobject_mode = "one_at_a_time")
        )

        #self.wait_to(36.5)
        self.play(ShowCreation(subsquares[0]), run_time = 0.5)
        self.play(ShowCreation(subsquares[1]))
        self.play(ShowCreation(subsquares[2]))
        self.play(
            FadeIn(VGroup(subsquares[3:]), submobject_mode = "lagged_start"),
            Animation(VGroup(subsquares[:3])),
        )

        dark_green = rgb_to_color(interpolate(
            color_to_rgb(BLACK),
            color_to_rgb(GREEN),
            0.2,
        ))

        zero = rows_l[0].copy().highlight(BLUE)
        zero.add_background_rectangle(dark_green)
        zero.move_to(dots[0][0])
        #self.wait_to(49.5)
        self.play(subsquares[0].set_fill, None, 0.2)
        self.play(FadeIn(zero[0]), Write(zero[1]))

        #self.wait_to(53)

        fg_digits = VGroup()
        self.add_foreground_mobjects(fg_digits)
        fg_digits.add(zero)

        lines = []
        dots_transposed = VGroup(list(zip(*dots)))
        for i in range(side_len-1):
            if i % 2 == 0: curd = dots
            else: curd = dots_transposed

            points = [curd[i][0]]
            points += curd[i+1][:i+2]
            for row in reversed(curd[:i+1]):
                points.append(row[i+1])
            points = [mob.get_center() for mob in points]
            line = PolyLine(
                *points,
                color = YELLOW
            )
            lines.append(line)

            digits = []
            max_w = 0.7*sq_size[0]
            for j, point in enumerate(points[1:]):
                digit = TexMobject(str((i+1)**2+j))
                digit.highlight(BLUE)
                digit.add_background_rectangle(dark_green)
                digit[0].get_fill_color = new.instancemethod(
                    VMobject.get_fill_color, digit[0], BackgroundRectangle
                )
                if digit.get_width() > max_w: digit.scale_to_fit_width(max_w)
                digit.move_to(point)
                digits.append(digit)

            digits = VGroup(digits)

            self.play(
                ShowCreation(line),
                FadeIn(L_shapes[i]),
                FadeIn(VGroup([digit[0] for digit in digits]), submobject_mode = "one_at_a_time"),
                FadeIn(VGroup([digit[1] for digit in digits]), submobject_mode = "one_at_a_time"),
            )
            fg_digits.add(digits)

        #self.wait_to(60+5)
        self.dither()

        subsquare_i = 5
        subsquares[0].set_fill(opacity = 0)
        self.remove(*L_shapes[:subsquare_i])
        subsquares[subsquare_i].set_fill(opacity = 0.2)
        other_subsquares = VGroup(subsquares[:subsquare_i]+subsquares[subsquare_i+1:])
        brace = BraceText(rows_l[:subsquare_i+1], "finite", LEFT)
        brace.desc.highlight(GREEN)

        to_fade = VGroup(fg_digits[subsquare_i+1:])
        self.play(
            brace.creation_anim(),
            FadeOut(other_subsquares),
            FadeOut(VGroup(L_shapes[subsquare_i:])),
            VGroup([num[0] for sample in to_fade for num in sample]).highlight, BLACK,
        )

        #self.wait_to(60+11)
        fg_digits.remove(*to_fade)
        self.play(FadeOut(to_fade))

        self.foreground_mobjects = []
        lines = VGroup(lines)
        #self.wait_to(60+27)
        self.dither()
        self.play(
            FadeOut(VGroup(
                rows_l, cols_l,
                lines, dots,
                brace,
                fg_digits,
            )),
            FadeIn(subgoal2),
        )

class Aleph1Square(Scene):
    def construct(self):

        prev_title = TexMobject("\\aleph_0","\\times","\\aleph_0","=","\\aleph_0")
        title = TexMobject("\\aleph_1","\\times","\\aleph_1","=","\\aleph_1")
        for t in (title, prev_title): VGroup(t[::2]).highlight(card_color)
        title.to_corner(UP+RIGHT)
        prev_title.to_corner(UP+LEFT)
        prev_square = Square(side_length = 0.8*11 + 2*SMALL_BUFF, color = WHITE)
        prev_subsquare = Square(side_length = 0.8*6, color = GREEN, fill_opacity = 0.2)
        prev_square.to_corner(UP+LEFT, buff = 0)
        prev_subsquare.to_corner(UP+LEFT, buff = 0.1)
        prev_g = VGroup(prev_square, prev_subsquare)
        prev_g.to_corner(DOWN+RIGHT, buff = -0.2)
        prev_g.to_edge(UP, buff = 1.5)
        self.add(prev_g, prev_title, title)

        omega = OrdinalOmega(height = 0.5, x0 = 0, x1 = 3)
        cols_l = make_half_ordinal(omega.copy())
        cols_l = VGroup(
            cols_l,
            cols_l[0].copy(),
            cols_l.copy(),
            cols_l.copy(),
            cols_l.copy(),
        ).arrange_submobjects(RIGHT, buff = 0.6, coor_mask = X_MASK)

        rows_l = cols_l.copy().stretch(-1,1).rotate(-np.pi/2)
        square = Square(side_length = 10)
        square.to_corner(DOWN+RIGHT, buff = -0.5)
        square.to_edge(UP, buff = 2)

        buff = 0.1
        cols_l.next_to(square, UP, buff = 0, aligned_edge = LEFT).shift(3*buff*RIGHT)
        rows_l.next_to(square, LEFT, buff = 0, aligned_edge = UP).shift(3*buff*DOWN)
        subsquare = Square(side_length = cols_l[0].get_width() + 3*buff, color = GREEN)
        subsquare.shift(square.get_corner(UP+LEFT) - subsquare.get_corner(UP+LEFT))
        subsquare.shift(buff*(RIGHT+DOWN))

        rows_cols_l = VGroup(rows_l, cols_l)
        rows_cols_l.save_state()
        rows_cols_l.highlight(BLACK)
        rows_cols_l.shift(
            prev_square.get_corner(LEFT+UP)
            - square.get_corner(LEFT+UP)
        )
        self.play(
            FadeOut(prev_title),
            rows_cols_l.restore,
            ReplacementTransform(prev_square, square),
            ReplacementTransform(prev_subsquare, subsquare),
            Animation(title),
        )

        ordinal_idx = OrdinalFiniteProd(OrdinalOmega, 5, height = 0.5)
        ordinal_idx.highlight(YELLOW)
        ordinal_idx.to_corner(UP+LEFT).shift(0.2*UP + 0.5*RIGHT)
        omega1_l = TexMobject("\\omega_1")
        omega1_l.next_to(ordinal_idx, DOWN, aligned_edge = LEFT)
        #self.wait_to(7)
        self.play(FadeIn(omega1_l))

        corners = [
            vbar.get_center()*X_MASK + hbar.get_center()*Y_MASK
            for vbar, hbar in zip(cols_l[0], rows_l[0])
        ]
        points = []
        for i, corner in enumerate(corners):
            new_points = [
                corners[0]*X_MASK + corner*Y_MASK,
                corner,
                corners[0]*Y_MASK + corner*X_MASK,
            ]
            if i%2 == 0: new_points.reverse()
            points += new_points

        omega_line = []
        for i, bar in enumerate(cols_l[0][:-1]):
            cur_points = list(points[3*i+2:i+3*i+6])
            if i == 0: cur_points.append(cur_points[-1]+0.1*RIGHT)
            omega_line.append(PolyLine(
                *cur_points,
                stroke_width = bar.thickness
            ))

        omega_line = VGroup(omega_line)
        omega_line.gradient_highlight(YELLOW, BLACK)

        filled_square = subsquare.copy()
        filled_square.set_fill(opacity = 0.2)
        filled_square.save_state()
        filled_square.scale(0, about_point = subsquare.get_corner(UP+LEFT))
        #self.wait_to(12)
        self.play(
            ShowCreation(omega_line),
            ApplyMethod(filled_square.restore, rate_func = rush_from),
        )
        #self.wait_to(14)

        self.play(ShowCreation(ordinal_idx[0]))

        omega.stretch(0.6, 1)
        omega.move_to(cols_l[0])
        omega.move_to(rows_l[1], coor_mask = Y_MASK)
        omega_c = omega.copy().rotate(-np.pi/2)
        omega_c.move_to(rows_l[0])
        omega_c.move_to(cols_l[1], coor_mask = X_MASK)
        dot = Dot(rows_l[1].get_center())
        dot.move_to(cols_l[1], coor_mask = X_MASK)

        next_layer = VGroup(omega, omega_c, dot)
        
        width = cols_l[2].get_edge_center(LEFT)[0] - subsquare.get_edge_center(LEFT)[0] - buff

        #self.wait_to(15.5)
        subsquare.save_state()
        subsquare.scale_to_fit_width(width)
        subsquare.shift(filled_square.get_corner(UP+LEFT) - subsquare.get_corner(UP+LEFT))

        self.play(
            FadeIn(next_layer),
            MoveFromSaved(subsquare),
        )
        start = filled_square.get_corner(UP+RIGHT)+buff*DOWN
        end = dot.get_center()
        mid = start*Y_MASK + end*X_MASK
        points = [start] + [
            interpolate(mid, end, alpha)
            for alpha in np.linspace(0,1,6)
        ] + [end+0.3*LEFT]
        next_line = PolyLine(
            *points,
            color = YELLOW
        )
        self.play(ShowCreation(next_line))

        #self.wait_to(18)
        self.play(ShowCreation(VGroup(ordinal_idx[1], ordinal_idx[2][0])))
        self.dither()
        start = next_line.get_anchors()[-1]
        bad_line = Line(start, start+0.4*LEFT, color = YELLOW)
        def rate_func(alpha):
            alpha *= 2
            if alpha > 1: alpha -= 1
            return there_and_back(alpha)

        #self.wait_to(21.2)
        self.play(ShowCreation(bad_line, rate_func = rate_func))
        self.remove(bad_line)
        self.dither()
        good_line = Line(
            start, omega.get_corner(UP+LEFT)+buff*(UP+LEFT),
            color = YELLOW,
        )
        y = good_line.points[-1][1]
        for point in good_line.points[1:3]: point[1] = y
        good_line.points[1] += 0.8*RIGHT
        good_line.points[2] += 0.5*LEFT
        good_line.points = np.concatenate([
            good_line.points,
            PolyLine(
                good_line.points[-1],
                omega.get_edge_center(LEFT)+buff*LEFT,
                omega.get_edge_center(RIGHT)+buff*RIGHT,
            ).points[1:],
        ], 0)

        #self.wait_to(34)
        self.play(ShowCreation(good_line))
        self.play(ShowCreation(VGroup(ordinal_idx[2][1:])))
        self.play(filled_square.replace, subsquare)

        #self.wait_to(39)

        subsquare.save_state()
        subsquare.scale_to_fit_width(
            VGroup(cols_l[2][:2]).get_center()[0] - subsquare.get_edge_center(LEFT)[0]
        )
        subsquare.shift(
            filled_square.get_corner(LEFT+UP) - subsquare.get_corner(LEFT+UP)
        )
        self.play(MoveFromSaved(subsquare))

        prev_line1 = next_line
        prev_line2 = good_line
        next_line1 = next_line.copy()
        next_line2 = good_line.copy()
        next_line1.stretch_to_fit_width((subsquare.get_width() - filled_square.get_width())/2)
        start = next_line1.get_edge_center(UP)
        next_line1.stretch_about_point(
            factor = (start[1] - rows_l[2][0].get_center()[1]) / next_line1.get_height(),
            dim = 1,
            point = start,
        )
        next_line1.next_to(filled_square, RIGHT, buff = 0, coor_mask = X_MASK)
        start = next_line1.points[-1]
        mid = prev_line2.get_edge_center(LEFT)
        next_line2.stretch_to_fit_width(start[0] - mid[0])
        next_line2.stretch(0.5, 1)
        next_line2.shift(start - next_line2.points[0])

        self.play(
            ShowCreation(VGroup(next_line1, next_line2)),
            ShowCreation(VGroup(ordinal_idx[3:])),
        )
        self.play(filled_square.replace, subsquare)

        #self.wait_to(45)

        omega1 = Omega1(height = ordinal_idx.height)
        omega1.shift(ordinal_idx.get_edge_center(LEFT) - omega1.get_edge_center(LEFT))
        omega1_src = omega1.copy()
        omega1_src[1].remove(*omega1[1][:len(ordinal_idx)])
        omega1_src.highlight(BLACK)
        omega1_src[1].shift(
            ordinal_idx.get_edge_center(RIGHT)
            - omega1[1].get_edge_center(LEFT)
        )
        omega1_src[1].add_to_back(*ordinal_idx)
        corner = subsquare.get_corner(UP+LEFT)
        self.remove(subsquare)
        to_scale = VGroup(
            omega_line,
            omega, omega_c, dot,
            prev_line1, prev_line2,
            next_line1, next_line2,
        )
        to_scale.save_state()
        to_scale.scale(0.5, about_point = corner)
        cols_l.save_state()
        cols_l.stretch_about_point(0.5, 0, corner)
        rows_l.save_state()
        rows_l.stretch_about_point(0.5, 1, corner)
        VGroup(cols_l, rows_l, to_scale).highlight(BLACK)
        filled_square.save_state()
        filled_square.scale(0.9, about_point = corner)
        self.play(
            ReplacementTransform(omega1_src, omega1),
            MoveFromSaved(to_scale),
            MoveFromSaved(cols_l),
            MoveFromSaved(rows_l),
            MoveFromSaved(filled_square),
            Animation(title),
            Animation(square),
        )
        self.remove(to_scale, cols_l, rows_l)

        brace = BraceText(filled_square, "countable", LEFT)
        #self.wait_to(46.5)
        self.play(brace.creation_anim())

        next_title = TexMobject("\kappa\cdot\\kappa=\kappa")
        VGroup(next_title[::2]).highlight(card_color)
        next_title.to_corner(UP+RIGHT)

        self.dither(2)
        #self.wait_to(60+3.5)
        title.save_state()
        next_title.save_state()
        shift = UP
        next_title.shift(-shift)
        title.shift(shift)
        for t in (title, next_title): t.set_fill(opacity = 0)
        self.play(
            next_title.restore,
            MoveFromSaved(title),
        )
        self.remove(title)
        #self.wait_to(60+7.5)
        self.play(FadeOut(VGroup(
            omega1, omega1_l, square, filled_square, brace,
        )))

class CardinalSquare(Scene):
    def construct(self):

        to_prove = TexMobject("\\kappa\cdot\\kappa=\kappa")
        VGroup(to_prove[::2]).highlight(card_color)
        to_prove.to_corner(UP+RIGHT)
        self.add(to_prove)

        card_height = 0.6
        ordinals = LongOrdinal(
            color = ord_color,
            gradient = (BLACK, "default", "default"),
            height = 0.5,
            x0 = -5,
            x1 = SPACE_WIDTH+1,
            ordinal_end = 0.3,
            line_start = 0.15,
        )
        self.play(ordinals.creation_anim())

        card_bar_template = Line(ORIGIN, card_height*2*DOWN, color = RED)
        card_bars = [ordinals[1][1][0]]
        start_point = card_bars[0].get_center()
        for i in range(3):
            point = start_point + 3.2*(i+1)*RIGHT
            card_bars.append(Line(
                point, point,
                stroke_width = 0,
                color = card_color,
            ))

        labels = []
        for i,bar in enumerate(card_bars):
            card_bar_template.move_to(bar)
            animations = [Transform(bar, card_bar_template, runt_time = 0.5),]
            if i < 3:
                label = TexMobject("\\aleph_{}".format(i))
                label.highlight(RED)
                label.next_to(card_bar_template, UP)
                animations.append(FadeIn(label))
                labels.append(label)

            self.play(*animations)

        ordinals.add(VGroup(card_bars[1:]))
        card_bars = VGroup(card_bars).copy()

        #self.wait_to(5)
        self.play(
            VGroup(card_bars, labels).to_edge, UP,
        )

        cardinals = OrdinalFiniteProd(
            OrdinalOmega, 3,
            x0 = -5, x1 = SPACE_WIDTH+1,
            height = 0.6,
        )
        cardinals.highlight(card_color)
        cardinals.move_to(card_bars, coor_mask = Y_MASK)

        cardinals_src = cardinals.copy()
        cardinals_src.behind_edge(RIGHT)
        cardinals_src[0].add_to_back(*card_bars)

        labels = VGroup(labels)
        labels.save_state()
        for label, bar in zip(labels, cardinals[0]):
            label.next_to(bar, UP)
        for label in labels[1:]: label.set_fill(opacity = 0)

        self.play(
            ReplacementTransform(cardinals_src, cardinals),
            MoveFromSaved(labels),
            FadeOut(ordinals),
        )
        self.remove(*labels[1:])
        self.dither()

        green_card = VGroup(
            cardinals[0],
            cardinals[1][:3],
        ).copy()
        green_card.highlight(GREEN)

        current_card = cardinals[1][3]
        print(self.current_scene_time)
        #self.wait_to(8.5)
        for bar in green_card[0][:2]: self.play(ShowCreation(bar), run_time = 0.5)
        self.play(ShowCreation(VGroup(green_card[0][2:])))
        for bar in green_card[1]: self.play(ShowCreation(bar), run_time = 0.5)

        bar_label = TexMobject("\\kappa").highlight(card_color)
        bar_label.next_to(current_card, UP)
        #self.wait_to(14)
        self.play(Write(bar_label))
        #self.wait_to(16.5)

        brace = BraceText(green_card, "verified", DOWN)
        brace.desc.highlight(GREEN)
        self.play(brace.creation_anim())

        self.dither()
        #self.wait_to(21)
        self.play(FadeOut(brace))

        cardinal = LongOrdinal(height = 0.8)
        cardinal.next_to(cardinals, DOWN, coor_mask = Y_MASK)

        bar = current_card.copy()
        bar.save_state()
        bar.move_to(cardinal, coor_mask = Y_MASK)
        self.play(MoveFromSaved(bar))
        rect = Rectangle(
            width = 0,
            height = bar.get_height(),
            color = card_color,
            stroke_width = 0,
            fill_opacity = 1,
        ).move_to(bar)
        rect.target = Rectangle(
            color = WHITE,
            stroke_width = 0,
            fill_opacity = 0,
        ).replace(Line(
            cardinal[1].get_edge_center(RIGHT),
            cardinal[0].get_edge_center(RIGHT),
        ), stretch = True)
        cardinal[0].save_state()
        cardinal[0].scale(0).move_to(bar).highlight(card_color)
        self.play(
            cardinal[0].restore,
            ReplacementTransform(bar, cardinal[1]),
            MoveToTarget(rect),
        )
        self.remove(rect)

        last_bar = cardinal[1][0][0].copy().next_to(cardinal)
        #self.wait_to(25)
        self.play(ShowCreation(last_bar))

        #self.wait_to(28.5)
        self.play(ApplyMethod(last_bar.next_to, cardinal, LEFT, path_arc = -np.pi*0.6))

        omega = cardinal[1][0]
        omega_src = omega.copy()
        omega_src.add_to_back(last_bar)
        #self.wait_to(30.5)
        self.remove(omega)
        self.play(ReplacementTransform(omega_src, omega))

        #self.wait_to(40.8)
        self.play(FadeOut(cardinal))

        square = Square(side_length = 4.5)
        square_l = TexMobject("\\kappa\\times\\kappa")
        VGroup(square_l[::2]).highlight(card_color)
        square.to_edge(DOWN)
        square_l.next_to(square, LEFT, aligned_edge = DOWN)
        self.play(
            ShowCreation(square),
            FadeIn(square_l),
        )

        buff = SMALL_BUFF

        dot = Dot(RIGHT, color = YELLOW)
        dot.save_state()
        dot.scale_in_place(2)
        dot.set_fill(opacity = 0)
        self.play(dot.restore)
        subsquare = Square(
            side_length = dot.get_edge_center(RIGHT)[0]
            - square.get_edge_center(LEFT)[0],
            color = GREEN,
        )
        subsquare.shift(
            square.get_corner(UP+LEFT)
            - subsquare.get_corner(UP+LEFT)
            + buff*(DOWN+RIGHT)
        )
        #self.wait_to(45)
        self.play(ShowCreation(subsquare))

        subsquare_l = TexMobject("<\\kappa")
        subsquare_l[1].highlight(card_color)
        subsquare_l.next_to(subsquare, LEFT, buff = buff + MED_SMALL_BUFF + buff)
        #self.wait_to(50.3)
        self.play(Write(subsquare_l))

        x = square.get_edge_center(LEFT)[0]-buff
        bar = min(green_card[0], key = lambda bar: abs(bar.get_center()[0]-x))
        side = Line(
            subsquare[0].get_edge_center(UP+LEFT),
            subsquare[0].get_edge_center(DOWN+LEFT),
        ).highlight(GREEN).next_to(subsquare_l, RIGHT, buff = buff)

        #self.wait_to(54.6)
        self.play(ReplacementTransform(bar.copy(), side))

        #self.wait_to(58)
        self.play(
            side.move_to, subsquare.get_edge_center(RIGHT),
            subsquare.set_fill, GREEN, 0.2,
            subsquare_l.move_to, subsquare,
        )
        self.remove(side)

        #self.wait_to(60+3)

        subsquare_dest = Square(
            side_length = square.side_length-2*buff,
            color = subsquare.color,
            fill_opacity = subsquare.fill_opacity,
        ).move_to(square)

        subsquare_l.save_state()
        subsquare_l.shift(
            subsquare_dest.get_center() - subsquare_l[1].get_center(),
        )
        subsquare_l[0].set_fill(opacity = 0)
        self.play(
            Transform(subsquare, subsquare_dest),
            MoveFromSaved(subsquare_l),
        )
        self.dither(2)
        #self.wait_to(60+18)

class Takeovers(Scene):
    def construct(self):

        title = TextMobject("Summary").scale(1.2).to_edge(UP)
        self.add(title)
        
        #series = VideoSeries(num_videos = 16).to_edge(UP)
        #series.save_state()
        #series.behind_edge(UP)
        #self.play(series.restore)
        #basic_chap = VGroup(series[:7])
        #formal_chap = VGroup(series[7:14])
        #advanced_chap = VGroup(series[14:])

        #brace = Brace(basic_chap, DOWN)
        #self.wait_to(3.5)
        #self.play(
        #    basic_chap.highlight, YELLOW,
        #    GrowFromCenter(brace),
        #)

        basic_stuff = self.play_basic_infinity()
        #self.wait_to(14)
        self.dither()
        self.play(
            FadeOut(basic_stuff),
            #basic_chap.highlight, series.color,
            #formal_chap.highlight, YELLOW,
            #Transform(brace, Brace(formal_chap, DOWN))
        )
        formal_stuff = self.play_formal_stuff()
        #self.wait_to(25.5)
        self.dither()
        self.play(
            FadeOut(formal_stuff),
            #formal_chap.highlight, series.color,
            #advanced_chap.highlight, YELLOW,
            #Transform(brace, Brace(advanced_chap, DOWN))
        )
        advanced_stuff = self.play_advanced()
        #self.wait_to(50)
        self.dither()
        self.play(
            FadeOut(advanced_stuff),
            #FadeOut(brace),
            #series.behind_edge, UP,
        )

    def play_basic_infinity(self):
        ordinal = OrdinalFiniteProd(OrdinalOmega, 2)
        ordinal[0][0].highlight(GREEN)
        ordinal[1][0].highlight(YELLOW)
        self.play(ShowCreation(ordinal))
        cardinals = TexMobject("|\\omega|","=","|\\mathbb Q|","<","|\\mathbb R|")
        VGroup(cardinals[::2]).highlight(RED)
        card_brace = Brace(ordinal[0], DOWN)
        cardinals.shift(card_brace.get_tip() - cardinals[0].get_edge_center(UP))
        self.play(
            GrowFromCenter(card_brace),
            FadeIn(cardinals[0]),
        )
        self.play(Write(VGroup(cardinals[1:]), run_time = 2))
        omega1 = Omega1()
        for subord in omega1[1]: subord[0].highlight(YELLOW)
        omega1[1][0][0].highlight(GREEN)
        omega1_src = omega1.copy()
        omega1_src.next_to(ordinal)
        omega1_src.highlight(BLACK)
        omega1_src[1].add_to_back(*ordinal)
        #print(self.current_scene_time)
        #self.wait_to(9)
        self.play(ReplacementTransform(omega1_src, omega1))
        self.dither()
        return VGroup(omega1, card_brace, cardinals)

    def play_formal_stuff(self):

        pair = TexMobject("(2,3)")
        pair[0].highlight(YELLOW)
        pair[-1].highlight(YELLOW)
        pair[1].highlight(PURPLE)
        pair[3].highlight(RED)

        pair_copy = pair.copy().next_to(self.make_pair(4), DOWN, 0.5)
        self.play(Write(pair_copy))
        self.play(ReplacementTransform(pair_copy.copy(), pair))

        punctuation = VGroup(pair[::2])
        punctuation.save_state()
        punctuation[1].set_fill(opacity = 0)

        two_rect = SurroundingRectangle(pair[1], color = BLACK)
        three_rect = SurroundingRectangle(pair[3], color = BLACK)
        rect = SurroundingRectangle(VGroup(pair[1:-1]), color = BLACK)

        pair_dest = self.make_pair(0)
        rect_dest = pair_dest[2]
        punctuation[0].replace(Line(
            rect_dest.get_corner(LEFT+UP),
            rect_dest.get_corner(LEFT+DOWN),
        ), stretch = True)
        punctuation[2].replace(Line(
            rect_dest.get_corner(RIGHT+UP),
            rect_dest.get_corner(RIGHT+DOWN),
        ), stretch = True)
        pair_src = VGroup(two_rect, three_rect, rect, pair[1], pair[1].copy(), pair[3])
        run_time = 0.7
        self.play(
            ReplacementTransform(pair_src, pair_dest),
            MoveFromSaved(punctuation),
            run_time = run_time,
        )
        self.remove(pair_dest, punctuation)
        for i in range(4):
            pair = self.make_pair(i, True)
            pair_dest = self.make_pair(i+1)
            self.play(Transform(pair, pair_dest), run_time = run_time)
            self.remove(pair)
        
        pair = self.make_pair(4)
        self.add(pair)
        self.dither()
        return VGroup(pair, pair_copy)

    def make_pair(self, depth, inner_envelope = False):
        two = self.make_two(depth, inner_envelope)
        two2 = two.copy()
        three = self.make_three(depth, inner_envelope)
        two_rect = SurroundingRectangle(two, color = WHITE)
        three_rect = SurroundingRectangle(
            VGroup(
                two2, three,
            ).arrange_submobjects(),
            color = WHITE,
        )
        rect = SurroundingRectangle(
            VGroup(
                VGroup(two, two_rect),
                VGroup(two2, three, three_rect),
            ).arrange_submobjects(RIGHT),
            color = YELLOW,
        )
        return VGroup(two_rect, three_rect, rect, two, two2, three)

    def make_three(self, depth, inner_envelope):
        color = RED
        if depth <= 0:
            result = TexMobject('3').highlight(color)
            if inner_envelope and depth == 0:
                return VGroup(result)
            return result

        two = self.make_two(depth, inner_envelope, arrangement = RIGHT)
        one = self.make_one(depth, inner_envelope)
        zero = self.make_zero(depth, inner_envelope)
        rect = SurroundingRectangle(
            VGroup(
                VGroup(
                    zero, one,
                ).arrange_submobjects(RIGHT),
                two,
            ).arrange_submobjects(DOWN),
            color = color,
        )
        return VGroup(rect, zero, one, two)

    def make_two(self, depth, inner_envelope, arrangement = DOWN):
        color = PURPLE
        if depth <= 1:
            result = TexMobject('2').highlight(color)
            if inner_envelope and depth == 1:
                return VGroup(result)
            return result
        one = self.make_one(depth, inner_envelope)
        zero = self.make_zero(depth, inner_envelope)
        rect = SurroundingRectangle(
            VGroup(
                zero, one,
            ).arrange_submobjects(arrangement),
            color = color
        )
        return VGroup(rect, zero, one)

    def make_one(self, depth, inner_envelope):
        color = BLUE
        if depth <= 2:
            result = TexMobject('1').highlight(color)
            if inner_envelope and depth == 2:
                return VGroup(result)
            return result
        zero = self.make_zero(depth, inner_envelope)
        rect = SurroundingRectangle(
            zero,
            color = color
        )
        return VGroup(rect, zero)

    def make_zero(self, depth, inner_envelope):
        color = GREY
        if depth <= 3:
            result = TexMobject('0').highlight(color)
            if inner_envelope and depth == 3:
                return VGroup(result)
            return result
        return Square(side_length = 0.5, color = color)

    def play_advanced(self):

        circle = Circle(color = BLUE)
        angles = np.array((0.1, 0.5, 0.8))*(2*np.pi)
        dots = VGroup([
            Dot(rotate_vector(RIGHT, angle), color = YELLOW)
            for angle in angles
        ])
        dots.save_state()
        for dot in dots: dot.scale_in_place(0)

        self.play(
            ShowCreation(circle),
            ApplyMethod(dots.restore, submobject_mode = "one_at_a_time"),
        )
        #self.wait_to(35)
        self.play(FadeOut(VGroup(circle, dots)))

        reals = NumberLine(min_x = -3.99, max_x = 3.99).shift(UP)
        ordinal = LongOrdinal(color = RED).shift(DOWN)
        self.play(ShowCreation(reals))

        #self.wait_to(42)

        bars = ordinal[1].family_members_with_points()
        segments = ordinal[0].family_members_with_points()
        for bar in bars:
            bar.priority = 100
        for segment in segments:
            segment.priority = np.sum(segment.stroke_rgb)

        dest_mobjects = sorted(bars + segments, key = lambda mob: mob.get_center()[0])
        reals_line = reals.main_line
        self.remove(reals_line)
        reals.remove(reals_line)

        src_mobjects = reals.family_members_with_points()
        choped_line = GradientLine(
            reals_line.get_start(), reals_line.get_end(),
            reals.color, reals.color,
            segment_num = len(dest_mobjects) - len(src_mobjects)
        )
        src_mobjects += choped_line.submobjects

        random.shuffle(src_mobjects)
        for src, dest in zip(src_mobjects, dest_mobjects):
            src.priority = dest.priority

        def order_f(mob):
            if hasattr(mob, "priority"):
                return mob.priority
            return -1

        src_mobjects = VGroup(src_mobjects)
        dest_mobjects = VGroup(dest_mobjects)
        self.play(
            Transform(
                src_mobjects, dest_mobjects,
                submobject_mode = "lagged_start",
            ),
            run_time = 2,
            order_f = order_f,
        )

        return src_mobjects

class Thanks(Scene):

    def construct(self):

        title = TextMobject("Thanks").scale(1.5).to_edge(UP)
        self.play(Write(title, run_time = 2))

        note_icon = SVGMobject(file_name = "note_icon")
        note_icon.scale_to_fit_width(1.5)
        radek = VGroup(
            note_icon,
            TextMobject("Radek Olšák"),
        ).arrange_submobjects(DOWN, buff = 0.5).to_edge(LEFT)
        grant = TextMobject("Grant Sanderson\\\\(3blue1brown)").to_edge(RIGHT)
        self.play(FadeIn(radek, submobject_mode = "lagged_start"))
        #self.wait_to(6)
        self.play(FadeIn(grant, submobject_mode = "lagged_start"))

        viewers = TextMobject("The viewers").scale(1.3).to_edge(DOWN)
        #self.wait_to(13)
        self.play(Write(viewers))

        #self.wait_to(22)
        # !!! I don't know how to translate this
        wish = TextMobject("Mějte se nekonečně!").scale_to_fit_width(8)
        self.play(
            GrowFromCenter(wish),
            title.behind_edge, UP,
            radek.behind_edge, LEFT,
            grant.behind_edge, RIGHT,
            viewers.behind_edge, DOWN,
        )
        #self.wait_to(24.5)
