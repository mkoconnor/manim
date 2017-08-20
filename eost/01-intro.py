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
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo
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
