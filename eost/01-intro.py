#!/usr/bin/env python

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
import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo
from topics.objects import BraceText
import eost.deterministic

class Chapter1OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 1\\\\ Introduction",
    }

class Chapter1OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "From his","paradise","that Cantor with us unfolded, we hold our breath in awe; knowing, we shall","not be expelled."
        ],
        "highlighted_quote_terms" : {
            "paradise" : YELLOW,
            "not be expelled" : GREEN,
        },
        "author" : "David Hilbert"
    }

class CantorScene(Scene):

    def construct(self):

        #self.force_skipping()

        title = TextMobject("Set","Theory")
        title.scale(1.3)
        title.to_edge(UP)
        self.add(title)
        self.dither()
        cantor = ImageMobject("Georg_Cantor2")
        cantor.scale(0.5)
        cantor_desc = TextMobject("Georg Cantor")
        cantor_desc.next_to(cantor, DOWN)
        VGroup(cantor, cantor_desc).to_corner(UP+RIGHT)
        self.add(cantor)
        self.play(FadeIn(cantor),
                  FadeIn(cantor_desc, submobject_mode = "lagged_start"))
        self.dither()
        studies0 = TextMobject("Study of","infinity")
        studies0[1].highlight(YELLOW)
        studies0.scale(1.3)
        studies0.shift(LEFT*cantor_desc.get_width()/2 + UP)
        self.play(FadeIn(studies0[0]), Write(studies0[1]))
        self.dither()

        studies1 = TextMobject("Study of","infinite","sets")
        studies1.scale(1.3)
        studies1.move_to(studies0)
        studies1[1].highlight(YELLOW)

        sets_ori = title[0].copy()
        s = studies1[-1][-1].copy()
        s.shift(sets_ori[-1].get_center() - studies1[-1][-2].get_center())
        s.set_fill(opacity = 0)
        sets_ori.add(s)
        studies0.add(sets_ori)
        self.play(ReplacementTransform(studies0, studies1))
        self.dither()

        self.play(studies1.next_to, title, DOWN,
                  FadeOut(cantor),
                  FadeOut(cantor_desc))
        
        self.dither()

class HotelScene(Scene):

    def construct(self):
        title = TextMobject("Set","Theory")
        title.scale(1.3)
        title.to_edge(UP)
        subtitle = TextMobject("Study of","infinite","sets")
        subtitle[1].highlight(YELLOW)
        subtitle.scale(1.3)
        subtitle.next_to(title, DOWN)
        self.add(title, subtitle)

        bus = SVGMobject(file_name = "bus")
        bus[0].set_stroke(width = 0)
        bus[0].set_fill(color = BLACK, opacity = 1)
        bus[1].set_stroke(width = 0)
        bus[1].set_fill(color = WHITE, opacity = 1)

        buses_inf = SVGMobject(file_name = "buses_inf")
        buses_inf.to_edge(DOWN)
        buses_inf.set_stroke(width = 0)
        buses_inf.set_fill(color = WHITE, opacity = 1)

        constelation = SVGMobject(file_name = "buses_constelation",
                                  initial_scale_factor = 0.02)
        constelation.set_stroke(color = WHITE, width = DEFAULT_POINT_THICKNESS)
        constelation.set_fill(color = BLACK, opacity = 0.5)
        constelation.to_corner(LEFT+DOWN)

        buses = [buses_inf.replace(constelation[0])]
        for template in constelation[1:]:
            buses.append(bus.copy().replace(template))
        buses = VGroup(*buses)
        buses_src = buses.copy()
        for bus_src in buses_src:
            bus_src.to_edge(LEFT)
        buses_src.behind_edge(LEFT)
        buses_src.shift(UP)

        self.play(ReplacementTransform(buses_src, buses), run_time = 2)
        self.revert_to_original_skipping_status()
        self.dither()

        hotel = SVGMobject(file_name = "hotel",
                           initial_scale_factor = 0.007,
                           unpack_groups = False)
        hotel.to_corner(RIGHT+DOWN)
        self.play(
            DelayedAnimGroup(
                ShowCreation(hotel[1]),
                ShowCreation(hotel[0]),
                run_time = 1.5))
        self.play(FadeIn(hotel[3], submobject_mode = "lagged_start"),
                  *map(ShowCreation, hotel[2].submobjects))
        self.dither()

        buses_hotel = VGroup(buses, hotel)
        self.play(buses_hotel.behind_edge, DOWN)
        self.dither()

class PrisonerScene(Scene):

    def construct(self):
        title = TextMobject("Set","Theory")
        title.scale(1.3)
        title.to_edge(UP)
        subtitle = TextMobject("Study of","infinite","sets")
        subtitle[1].highlight(YELLOW)
        subtitle.scale(1.3)
        subtitle.next_to(title, DOWN)
        self.add(title, subtitle)

        prisoner = SVGMobject(file_name = "prisoner",
                              initial_scale_factor = 0.04)
        prisoner.set_color(WHITE)
        prisoner.to_corner(LEFT+DOWN)

        prisoners = []
        corner = DOWN+RIGHT
        limit_point = corner * (SPACE_WIDTH, SPACE_HEIGHT, 0)
        limit_point -= corner * DEFAULT_MOBJECT_TO_EDGE_BUFFER
        ratio = 0.88
        hat = prisoner[-2]
        bubble = prisoner[-1]
        eye = prisoner[2]
        eye.set_fill(opacity = 1)
        colors = [BLUE, YELLOW]
        hat.set_fill(opacity = 0.5)
        hat.set_stroke(width = DEFAULT_POINT_THICKNESS)
        bubble.set_fill(opacity = 0.5)
        for i in range(30):
            eye.set_stroke(width = 0)
            hat_color = random.randint(0,1)
            if i < 2: bubble_color = 1-hat_color
            else: bubble_color = hat_color
            hat.set_fill(colors[hat_color])
            bubble.set_fill(colors[bubble_color])

            prisoners.append(prisoner.copy())
            prisoner.scale(ratio, about_point = limit_point)
            prisoner.set_stroke(width = prisoner.stroke_width * ratio)

        without_bubbles = VGroup(*[
            VGroup(*prisoner[:-1])
            for prisoner in prisoners
        ])
        bubbles = VGroup(*[
            prisoner[-1]
            for prisoner in prisoners
        ])
        bubbles_src = bubbles.copy()
        for bubble in bubbles_src:
            bubble.scale_about_point(0, bubble.points[0])

        self.play(FadeIn(VGroup(*without_bubbles),
                         submobject_mode = "lagged_start",
                         run_time = 2))
        self.dither()
        self.play(ReplacementTransform(bubbles_src, bubbles,
                  submobject_mode = "one_at_a_time",
                  run_time = 2))
        self.dither()

        self.play(FadeOut(VGroup(title, subtitle, *prisoners)))

class TwoSetTheoryRoles(Scene):

    def construct(self):

        #self.force_skipping()

        bubble = SVGMobject(file_name = "thought_bubble",
                            initial_scale_factor = 0.31)
        bubble.set_color(WHITE)
        bubble.stretch(1.25, 0)
        bubble.to_corner(DOWN+RIGHT)
        self.play(ShowCreation(VGroup(*bubble[:2])))
        self.play(ShowCreation(bubble[2]))
        self.dither()

        subbubbles = self.make_fractal(bubble[-1], [0.8*LEFT, 0.8*RIGHT])
        self.play(ShowCreation(subbubbles, submobject_mode = "all_at_once", run_time = 2))
        self.dither()

        main_rect = Rectangle(width = 2*SPACE_WIDTH-1, height = 2*SPACE_HEIGHT-1)
        rect_template = main_rect.copy()
        rect_template.stretch_about_point(0.5, 1, rect_template.get_edge_center(UP))
        subrects = self.make_fractal(rect_template, [0.9*LEFT, 0.9*RIGHT], ratio = (0.45, 0.8, 0.6))

        self.play(ReplacementTransform(bubble[-1], main_rect),
                  ReplacementTransform(subbubbles, subrects),
                  bubble[0].behind_edge, DOWN,
                  bubble[1].behind_edge, DOWN,
                  run_time = 2)
        self.dither()

        implications = TexMobject("\Rightarrow\Leftarrow")
        implications.arrange_submobjects(DOWN, buff = 0.5)
        implications.rotate(-np.pi/2)
        contradiction = VGroup(
            TexMobject("X\\in X"),
            implications,
            TexMobject("X\\not\\in X"),
        )
        contradiction.arrange_submobjects(DOWN)
        contradiction.to_corner(LEFT+DOWN, buff = 1)
        contradiction.shift(RIGHT)
        contradiction.add(implications[1])
        implications.remove(implications[1])

        self.revert_to_original_skipping_status()
        self.dither()
        self.play(FadeIn(contradiction, submobject_mode = "lagged_start"))
        self.dither()

        questionmarks = TextMobject("???")
        questionmarks.next_to(contradiction, buff = 0.5)
        self.play(Write(questionmarks))
        self.dither()
        contradiction.add(questionmarks)

        cross = Cross().set_color(RED)
        cross.scale((
            contradiction.get_width() / cross.get_width(),
            contradiction.get_height() / cross.get_height(),
            1,
        ))
        cross.move_to(contradiction)

        title = TextMobject("Set Theory").scale(1.3).to_edge(UP)
        division = DashedLine(title.get_edge_center(DOWN) + 0.2*DOWN, SPACE_HEIGHT*DOWN)

        self.play(
            contradiction.highlight, DARK_GREY,
            ShowCreation(cross),
        )
        axioms = TextMobject("Axioms")
        axioms.next_to(division)
        self.play(Write(axioms))
        self.dither()

        left_rect, right_rect = [], []
        for rect in subrects:
            if rect.get_center()[0] < 0: left_rect.append(rect)
            else: right_rect.append(rect)

        left_rect = VGroup(*left_rect)
        right_rect = VGroup(*right_rect)

        self.play(FadeOut(VGroup(right_rect, main_rect, contradiction, cross)))
        self.play(
            ShowCreation(division),
            UnapplyMethod(title.behind_edge, UP),
            left_rect.to_edge, DOWN, 0.8,
        )
        self.dither()

        theory_of_infinity = TextMobject("Theory of Infinity").highlight(BLUE)
        foundations_of_mathematics = TextMobject("Foundations of\\\\ Mathematics",
                                                 alignment = "\\raggedright")
        theory_of_infinity.next_to(division, LEFT, aligned_edge = UP)
        foundations_of_mathematics.next_to(division, RIGHT, aligned_edge = UP)
        VGroup(theory_of_infinity, foundations_of_mathematics).shift(0.2*DOWN)

        self.play(FadeIn(theory_of_infinity), run_time = 2, submobject_mode = "lagged_start")
        self.dither()
        self.play(FadeIn(foundations_of_mathematics), run_time = 2, submobject_mode = "lagged_start")
        self.dither()

    def make_fractal(self, base, points, layers_num = 8, ratio = (0.4, 0.4, 0.6)):
        
        last_layer = [base]
        result = []

        stroke_ratio = ratio[-1]
        ratio = np.array(ratio)
        ratio[-1] = 1

        for layer_index in range(layers_num):
            color = [BLUE, PURPLE, RED, ORANGE, YELLOW, GREEN][layer_index%6]
            cur_layer = []
            
            for last_el in last_layer:
                for point in points:
                    next_el = last_el.copy()
                    next_el.highlight(color)
                    next_el.scale_about_point(ratio, next_el.get_relative_point(point))
                    next_el.stroke_width *= stroke_ratio
                    result.append(next_el)
                    cur_layer.append(next_el)
            last_layer = cur_layer

        return VGroup(*result)

class ChapterList(Scene):

    def construct(self):
        series = VideoSeries(num_videos = 16).to_edge(UP)
        self.add(series)

        brace = BraceText(series[:7], "Theory of Infinity")
        self.play(brace.creation_anim())

        self.dither()
        self.play(brace.change_brace_desc, series[7:14], "Foundations of Mathematics")
        self.dither()

        brace_dest = brace.copy()
        brace_dest.change_brace_desc(series[14:16], "Tools")
        brace_dest.desc.to_edge(RIGHT)
        self.play(ReplacementTransform(brace, brace_dest))
        brace = brace_dest

        self.dither()

class InfinityBasics(Scene):

    def construct(self):

        #self.force_skipping()
        
        question = TextMobject("What is Infinity?")
        question.scale(1.3)
        question.to_edge(UP)
        question1 = question.copy()

        self.play(Write(question))
        self.dither()

        infty_symbol = TexMobject('\\infty')
        infty_symbol.scale(5)
        self.play(Write(infty_symbol))
        self.dither()

        self.play(FadeOut(infty_symbol))
        question2 = TextMobject("What is infinite?")
        question2.scale(1.3)
        question2.to_edge(UP)

        self.play(ReplacementTransform(question, question2))
        self.dither()

        answer = TextMobject("That what is not","finite").scale(1.3)
        answer.next_to(question2, DOWN, buff = 0.5)
        answer_ori = answer.copy()
        answer_ori.shift(DOWN)
        answer_ori.highlight(BLACK)

        self.play(ReplacementTransform(answer_ori, answer))
        self.dither()

        finite_def = BraceText(answer[-1], "possible to express\\\\ by a natural number")
        self.play(finite_def.creation_anim())
        self.dither(2)

        dots5 = VGroup(*[Dot(color = BLUE) for _ in range(5)])
        dots5.arrange_submobjects(buff = 0.5)
        set5 = VGroup(VGroup(dots5), SurroundingRectangle(dots5, color = WHITE, buff = 0.3))

        dots100 = VGroup(*[
            VGroup(*[
                Dot(color = BLUE)
                for _ in range(10)
            ]).arrange_submobjects()
            for _ in range(10)
        ]).arrange_submobjects(DOWN)
        set100 = VGroup(dots100, SurroundingRectangle(dots100, color = WHITE))

        set100.to_corner(DOWN+LEFT)
        set5.move_to(set100)
        brace5 = BraceText(set5, "5", UP)
        self.play(FadeIn(set5), brace5.creation_anim())
        self.dither()
        self.play(brace5.change_desc, "finite")
        self.dither()
        self.play(FadeOut(brace5))

        brace100 = BraceText(set100, "100", RIGHT)
        self.play(
            ReplacementTransform(set5, set100),
            brace100.creation_anim(),
        )
        self.dither()
        self.play(brace100.change_desc, "finite")
        self.dither()
        self.play(FadeOut(VGroup(brace100, set100)))

        numbers = VGroup(*[
            TexMobject(str(i))
            for i in range(100)
        ])
        pseudo_num = SurroundingRectangle(numbers[-1], buff = 0, stroke_width = 0, fill_opacity = 1)
        numbers.gradient_highlight(BLUE, BLACK)
        numbers.arrange_submobjects(buff = 0.5)

        numbers.shift(-numbers.get_edge_center(LEFT))

        def perspective_shift(point):
            camera_distance = 10.0
            ratio = camera_distance / (camera_distance + point[0])
            return point*ratio

        numbers.apply_function(perspective_shift, maintain_smoothness = False)
        numbers.stretch_to_fit_width(2*SPACE_WIDTH-2)
        numbers.center()
        numbers.shift(0.5*LEFT)
        rect_inf = Rectangle(width = -2*numbers.get_edge_center(LEFT)[0] + 0.5,
                             height = numbers.get_height() + 0.5)
        set_inf = VGroup(rect_inf, numbers)
        set_inf.to_edge(DOWN)

        brace_inf = BraceText(set_inf, "infinite", UP, desc_scale = 1.3)
        self.play(FadeIn(set_inf), GrowFromCenter(brace_inf.brace))
        self.dither()
        self.play(Write(brace_inf.desc))
        self.dither()

        self.revert_to_original_skipping_status()
        self.play(FadeOut(VGroup(numbers, brace_inf)))

        set0 = Square(side_length = 1).move_to(set_inf)
        brace0 = BraceText(set0, "finite", UP)
        self.play(ReplacementTransform(rect_inf, set0))
        self.play(brace0.creation_anim())
        self.dither()
        self.play(brace0.change_desc, '0')
        self.dither(2)

        self.play(FadeOut(VGroup(set0, brace0, answer, finite_def)), ReplacementTransform(question2, question1))
        self.dither()
        self.play(Write(TextMobject("Not just a number...")))
        self.dither(3)

class GridColoring(Scene):

    def construct(self):

        self.grid_size = 5
        self.square_size = 0.8

        inf_grid = self.make_infinite_grid()
        self.add_foreground_mobjects(inf_grid[1])
        squares = inf_grid[0]
        self.dither()

        colors = [rgb_to_color(square.fill_rgb) for square in squares]
        squares.highlight(BLACK)
        self.play(
            self.turn_squares(squares, colors),
            run_time = 3,
        )
        self.dither()

        return

        self.force_skipping()
        
        squares, border, lines = self.make_finite_grid()

        self.add(squares)
        self.play(ShowCreation(border))
        self.play(ShowCreation(lines, submobject_mode = "lagged_start", run_time = 1.5))
        self.add_foreground_mobjects(border, lines)
        self.dither()

        squares_flatten = list(it.chain(*squares))
        self.color_list = [YELLOW]*(self.grid_size**2)
        for i in range(0, self.grid_size**2, self.grid_size):
            self.dominate(BLUE, range(i, i+self.grid_size))

        h_arrows = VGroup(*[Arrow(ORIGIN, 2*RIGHT, color = BLUE)
                            for _ in range(self.grid_size)])

        for h_arrow, row in zip(h_arrows, squares): h_arrow.next_to(row, LEFT)

        self.revert_to_original_skipping_status()
        self.play(
            self.turn_squares(squares_flatten, self.color_list),
            FadeIn(h_arrows, submobject_mode = "lagged_start"),
            run_time = 2,
        )
        self.dither()

        return

    def dominate(self, color, indices):
        total_num = len(indices)
        color_num = len(filter(lambda i: self.color_list[i] == color, indices))

        while color_num*2 <= total_num:
            i = random.choice(indices)
            if self.color_list[i] == color: continue
            color_num += 1
            self.color_list[i] = color

    def turn_squares(self, square_list, color_list):

        squares = VGroup(*square_list)
        squares_dest = squares.copy()

        for square, square_dest, color in zip(squares, squares_dest, color_list):
            square.color = color
            square_dest.set_color(color)

        for square in squares:
            square.rotate_in_place(np.pi/2)
            square.stretch_in_place(-1, 0)

        return Transform(squares, squares_dest, submobject_mode = "lagged_start")

    def make_finite_grid(self):

        border_size = self.grid_size * self.square_size
        border = Square(side_length = border_size)
        lines_h = VGroup(*[
            Line(0.5*LEFT*border_size, 0.5*RIGHT*border_size)
            for _ in range(self.grid_size-1)
        ]).arrange_submobjects(DOWN, buff = self.square_size)
        lines_v = VGroup(*[
            Line(0.5*UP*border_size, 0.5*DOWN*border_size)
            for _ in range(self.grid_size-1)
        ]).arrange_submobjects(buff = self.square_size)

        squares = VGroup(*[
            VGroup(*[
                Square(side_length = self.square_size, color = BLACK)
                for _ in range(self.grid_size)
            ]).arrange_submobjects(buff = 0)
            for _ in range(self.grid_size)
        ]).arrange_submobjects(DOWN, buff = 0)
        squares.set_stroke(width = 0)
        squares.set_fill(opacity = 0.5)

        return squares, border, VGroup(lines_h, lines_v)

    def make_infinite_grid(self):

        lines = []

        x = self.square_size/2
        while x < SPACE_WIDTH+0.5:
            lines += [
                Line(x*direction + SPACE_HEIGHT*UP, x*direction + SPACE_HEIGHT*DOWN)
                for direction in [LEFT, RIGHT]
            ]
            x += self.square_size

        y = self.square_size/2
        while y < SPACE_HEIGHT+0.5:
            lines += [
                Line(y*direction + SPACE_WIDTH*LEFT, y*direction + SPACE_WIDTH*RIGHT)
                for direction in [UP, DOWN]
            ]
            y += self.square_size

        dist = -0.5
        num = 1
        squares = []
        while dist < max(SPACE_WIDTH, SPACE_HEIGHT):
            square_line = VGroup(*[
                Square(side_length = self.square_size, fill_opacity = 0.5, stroke_width = 0)
                for _ in range(num)
            ])

            square_line.arrange_submobjects(buff = 0)
            square_line.shift(0.5*self.square_size*(LEFT + DOWN*num))
            square_lines = [
                square_line.copy().rotate(np.pi/2 * i)
                for i in range(4)
            ]
            for square_line, color in zip(square_lines, [YELLOW, BLUE]*2):
                square_line.highlight(color)
                square_line.shift(0.5*self.square_size*(UP+RIGHT))

            squares += it.chain(*square_lines)

            dist += self.square_size
            num += 2

        return VGroup(VGroup(*squares), VGroup(*lines))
