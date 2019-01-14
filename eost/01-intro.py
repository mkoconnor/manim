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
from topics.objects import BraceText, Counter
import eost.deterministic

class Chapter1OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 1\\\\ Introduction",
    }

class Chapter1OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Set theory has a dual role in mathematics. In pure mathematics, it is the place where questions about infinity are studied. Although this is a fascinating study of permanent interest, it does not account for the importance of set theory in applied areas. There the importance stems from the fact that set theory provides an incredibly versatile toolbox for building mathematical models of various phenomena."
        ],
        "author" : "Jon Barwise, Lawrence Moss",
        "fade_in_kwargs" : {
            "submobject_mode" : "lagged_start",
            "rate_func" : None,
            "lag_factor" : 4,
            "run_time" : 9,
        },
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
        #self.dither()

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
        #self.dither()
        self.play(FadeIn(contradiction, submobject_mode = "lagged_start"))
        #self.dither()

        questionmarks = TextMobject("???")
        questionmarks.next_to(contradiction, buff = 0.5)
        #self.play(Write(questionmarks))
        #self.dither()
        #contradiction.add(questionmarks)

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

        answer = TextMobject("That which is not","finite").scale(1.3)
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
        self.dither(2)

        self.revert_to_original_skipping_status()
        self.play(FadeOut(VGroup(numbers, brace_inf, rect_inf, answer, finite_def)), ReplacementTransform(question2, question1))

        #set0 = Square(side_length = 1).move_to(set_inf)
        #brace0 = BraceText(set0, "finite", UP)
        #self.play(ReplacementTransform(rect_inf, set0))
        #self.play(brace0.creation_anim())
        #self.dither()
        #self.play(brace0.change_desc, '0')
        #self.dither(2)

        #self.play(FadeOut(VGroup(set0, brace0, answer, finite_def)), ReplacementTransform(question2, question1))
        self.dither()
        self.play(Write(TextMobject("Not just a number...")))
        self.dither(3)

class TurnSquares(Transform):
    CONFIG = {
        "submobject_mode" : "lagged_start",
        "rate_func"       : None,
        "omit_unchanged"  : True,
    }
    def __init__(self, square_list, color_list, **kwargs):

        digest_config(self, kwargs)
        if self.omit_unchanged:
            unchanged = [
                (color_to_rgb(dest_color) == color_to_rgb(square.color)).all()
                for square,dest_color in zip(square_list, color_list)
            ]
            square_list = [
                square
                for i, square in enumerate(square_list)
                if not unchanged[i]
            ]
            color_list = [
                color
                for i, color in enumerate(color_list)
                if not unchanged[i]
            ]

        squares = VGroup(*square_list)
        squares_dest = squares.copy()

        for square, square_dest, color in zip(squares, squares_dest, color_list):
            square_dest.set_color(color)

        for square in squares:
            square.rotate_in_place(np.pi/2)
            square.stretch_in_place(-1, 0)

        Transform.__init__(self, squares, squares_dest)

    def clean_up(self, surrounding_scene = None):
        families = self.get_all_families_zipped()
        for submob, start, end in families:
            submob.color = end.color

        Transform.clean_up(self, surrounding_scene)
        if surrounding_scene is not None:
            surrounding_scene.mobjects.remove(self.mobject)

    def update_submobject(self, submob, start, end, alpha):
        if alpha < 0.5:
            start.set_fill(start.color)
            end.set_fill(WHITE)
        else:
            start.set_fill(WHITE)
            end.set_fill(end.color)

        submob.interpolate(start, end, alpha, self.path_func)
        return self

def make_inf_grid_lines(square_size):

    lines = []

    x = square_size/2
    while x < SPACE_WIDTH+0.5:
        lines += [
            Line(x*direction + SPACE_HEIGHT*UP, x*direction + SPACE_HEIGHT*DOWN)
            for direction in [LEFT, RIGHT]
        ]
        x += square_size

    y = square_size/2
    while y < SPACE_HEIGHT+0.5:
        lines += [
            Line(y*direction + SPACE_WIDTH*LEFT, y*direction + SPACE_WIDTH*RIGHT)
            for direction in [UP, DOWN]
        ]
        y += square_size

    return VGroup(*lines)

class FinGridColoring(Scene):

    def construct(self):

        self.grid_size = 5
        self.square_size = 0.8

        #self.force_skipping()
        
        self.squares, border, lines = self.make_finite_grid()

        self.play(ShowCreation(border))
        self.play(ShowCreation(lines, submobject_mode = "lagged_start", run_time = 1.5))
        self.add_foreground_mobjects(border, lines)
        self.dither()

        self.colors = np.full([self.grid_size, self.grid_size],
                              YELLOW, dtype = object)
        for i in range(0, self.grid_size):
            self.dominate(BLUE, self.row_indices([i]))

        h_arrows = VGroup(*[Arrow(ORIGIN, 2*RIGHT, color = BLUE)
                            for _ in range(self.grid_size)])
        v_arrows = VGroup(*[Arrow(ORIGIN, 2*UP, color = YELLOW)
                            for _ in range(self.grid_size)])
        for h_arrow, row in zip(h_arrows, self.squares):
            h_arrow.next_to(row[0], LEFT)
        for v_arrow, square in zip(v_arrows, self.squares[-1]):
            v_arrow.next_to(square, DOWN)

        self.play(
            self.turn_indices(self.row_indices(range(self.grid_size))),
            FadeIn(h_arrows, submobject_mode = "lagged_start", rate_func = None),
            run_time = 2,
        )
        self.dither()

        satisfied_columns = [
            i for i in range(self.grid_size)
            if self.dominant(self.column_indices([i])) == YELLOW
        ]
        unsatisfied_columns = [
            i for i in range(self.grid_size)
            if self.dominant(self.column_indices([i])) != YELLOW
        ]
        satisfied_v_arrows = VGroup(*[
            v_arrows[i] for i in satisfied_columns
        ])
        unsatisfied_v_arrows = VGroup(*[
            v_arrows[i] for i in unsatisfied_columns
        ])

        self.play(FadeIn(satisfied_v_arrows))
        self.dither()

        for i in unsatisfied_columns:
            self.dominate(YELLOW, self.column_indices([i]))

        broken_rows = [
            i for i in range(self.grid_size)
            if self.dominant(self.row_indices([i])) != BLUE
        ]
        broken_h_arrows = VGroup(*[
            h_arrows[i] for i in reversed(broken_rows)
        ])

        self.play(
            self.turn_indices(self.column_indices(unsatisfied_columns)),
            FadeIn(unsatisfied_v_arrows),
            FadeOut(broken_h_arrows),
            submobject_mode = "lagged_start",
            run_time = 2,
            rate_func = None,
        )
        self.dither(2)

        inequality1 = VGroup(
            self.squares[0,0].copy(),
            TexMobject('>'),
            self.squares[0,0].copy(),
        )
        #inequality1[1].scale(2)
        inequality1.arrange_submobjects(buff = 0.25)
        inequality2 = inequality1.copy()
        inequality1[0].set_color(BLUE)
        inequality1[2].set_color(YELLOW)
        inequality2[0].set_color(YELLOW)
        inequality2[2].set_color(BLUE)

        inequalities = VGroup(inequality1, inequality2)
        inequalities.arrange_submobjects(buff = 1.5)
        inequalities.to_edge(UP)

        self.play(FadeIn(inequality1))
        self.dither()
        self.play(FadeIn(inequality2))
        self.dither()

        h_arrows.remove(*broken_h_arrows)
        inf_lines = make_inf_grid_lines(self.square_size)

        self.revert_to_original_skipping_status()
        self.play(
            FadeOut(VGroup(inequalities, v_arrows, h_arrows)),
            FadeOut(VGroup(*self.squares.flatten())),
            FadeIn(inf_lines),
        )
        self.dither()

    def turn_indices(self, indices):
        indices = zip(*indices)
        return TurnSquares(self.squares[indices], self.colors[indices])
    
    def row_indices(self, row_index_list):
        return [(i,j) for i in row_index_list for j in range(self.grid_size)]
    def column_indices(self, column_index_list):
        return [(i,j) for j in column_index_list for i in reversed(range(self.grid_size))]

    def dominate(self, color, indices):
        total_num = len(indices)
        color_num = len(filter(lambda i: self.colors[i] == color, indices))

        while color_num*2 <= total_num:
            i = random.choice(indices)
            if self.colors[i] == color: continue
            color_num += 1
            self.colors[i] = color

    def dominant(self, indices):
        yellow_num = 0
        blue_num = 0
        for i in indices:
            if self.colors[i] == YELLOW: yellow_num += 1
            if self.colors[i] == BLUE: blue_num += 1

        if yellow_num < blue_num: return BLUE
        return YELLOW

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

        # convert VGroup into np array
        squares_np = np.empty([self.grid_size, self.grid_size], dtype = object)
        squares_np[:,:] = squares
        
        return squares_np, border, VGroup(lines_h, lines_v)

class InfGridColoring(Scene):

    def construct(self):

        #self.force_skipping()

        self.square_size = 0.8

        inf_grid = self.make_infinite_grid()
        self.add_foreground_mobjects(inf_grid[1])
        self.squares = inf_grid[0]
        self.dither()

        colors = [rgb_to_color(square.fill_rgb) for square in self.squares]
        for square in self.squares: square.set_color(BLACK)

        row = self.select_square_line(0)
        row_colors = self.generate_colors(row, main_blue = True)

        column = self.select_square_line(1)
        column_colors = self.generate_colors(column, main_blue = False)

        self.play(TurnSquares(row, row_colors))
        self.dither(2)
        self.play(TurnSquares(column, column_colors))
        self.dither(3)

        #counter = Counter()
        #counter.count_from(5, self)
        #self.dither()

        self.play(
            TurnSquares(self.squares, colors),
            run_time = 3,
            rate_func = None,
        )
        self.dither()

        self.revert_to_original_skipping_status()

        row = self.select_square_line(0, -2)
        self.play(row.set_fill, None, 1)
        self.dither()
        self.play(row.set_fill, None, 0.5)

        column_index = -4
        column = self.select_square_line(1, column_index)
        self.play(column.set_fill, None, 1)

        ori_size = self.square_size
        self.square_size = 0.5
        self.remove(inf_grid)

        inf_grid = self.make_infinite_grid()
        self.squares = inf_grid[0]
        self.add_foreground_mobjects(inf_grid[1])
        column = self.select_square_line(1, column_index)
        column.set_fill(opacity = 1)

        self.play(UnapplyMethod(inf_grid.scale, ori_size / self.square_size))
        self.dither(5)

    def select_square_line(self, dim, pos = 0):
        squares = filter(lambda square: abs(square.get_center()[1-dim] / self.square_size
                                            - pos) < 0.5,
                         self.squares)
        squares.sort(key = lambda square: square.get_center()[1-dim], reverse = (dim == 0))

        return VGroup(*squares)

    def generate_colors(self, squares, main_blue = True, minor_num = 3):
        colors = [YELLOW, BLUE]
        if main_blue: colors.reverse()
        main_color, other_color = colors

        colors = [main_color]*len(squares)
        for _ in range(minor_num):
            i = random.randint(len(colors)//2 - 4, len(colors)//2 + 3)
            colors[i] = other_color

        return colors

    def make_infinite_grid(self):

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

        return VGroup(VGroup(*squares), make_inf_grid_lines(self.square_size))
