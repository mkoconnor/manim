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

class Chapter12OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 12\\\\Reálná čisla jako Dedekindovy řezy",
    }

class Chapter12OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Čísla jsou svobodným výtvorem lidského ducha.",
        ],
        "author" : "Richard Dedekind"
    }

class ChainProblem(Scene):
    def construct(self):

        title = TextMobject("Úloha o nespočetném řetězci")
        title.to_edge(UP)
        self.add(title)

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

        base_set.to_edge(LEFT)
        base_label = TexMobject('3').next_to(base_set, DOWN)
        self.play(
            FadeIn(base_label),
            FadeIn(base_elements),
            ShowCreation(base_rect),
        )
        poset_rect = SurroundingRectangle(poset_elements, color = YELLOW)
        poset_label = TexMobject("\\mathcal P(3)").next_to(poset_rect, DOWN)
        self.play(
            FadeIn(poset_label),
            FadeIn(poset_elements),
            ShowCreation(poset_rect),            
        )

        self.dither()
        self.play(
            FadeOut(poset_rect),
            ShowCreation(poset_edges),
        )

        poset_elements_backup = poset_elements.copy()
        poset_elements.save_state()
        poset_edges.save_state()
        highlighted = VGroup(
            poset_dict[0,],
            poset_dict[1,2],
        )
        poset_elements.highlight(DARK_GREY)
        highlighted.highlight(YELLOW)

        self.play(
            poset_edges.highlight, DARK_GREY,
            MoveFromSaved(poset_elements)
        )
        incomparable = TextMobject("neporovnatelné").highlight(RED)
        incomparable.add_background_rectangle()
        self.play(FadeIn(incomparable, submobject_mode = "lagged_start"))

        self.dither()
        self.play(
            Transform(poset_elements, poset_elements_backup),
            poset_edges.restore,
            FadeOut(incomparable),
        )

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

        edge = middle_edges[2]
        chain_edges, chain_elements = get_chain(edge)
        grey_edges = VGroup(*poset_edges)
        grey_edges.remove(*chain_edges)
        grey_elements = VGroup(itertools.chain(*poset_elements))
        grey_elements.remove(*chain_elements)

        self.play(
            grey_edges.highlight, GREY,
            grey_elements.highlight, GREY,
            ApplyMethod(chain_edges.highlight, YELLOW, submobject_mode = "one_at_a_time"),
            ApplyMethod(chain_elements.highlight, YELLOW, submobject_mode = "lagged_start"),
        )

        self.dither()
        for edge in middle_edges:

            poset_elements.highlight(GREY)
            poset_edges.highlight(GREY)
            VGroup(get_chain(edge)).highlight(YELLOW)

            self.dither(0.5)

        brace = BraceDesc(poset_elements, "3+1", RIGHT)
        self.play(brace.creation_anim())

        self.dither()

        self.play(FadeOut(VGroup(
            brace, poset_edges, poset_elements,
            base_set, base_label,
        )))

        label_dest = TexMobject("\\mathcal P(\\omega)").move_to(poset_label)
        poset_rect.stretch_in_place(1.5, 0)
        self.play(
            Transform(poset_label, label_dest),
            GrowFromCenter(poset_rect),
        )

        self.play(poset_rect.set_fill, None, 0.1)
        continuum = TexMobject("\\mathfrak c").scale(2).next_to(poset_rect.get_corner(UP+LEFT), DOWN+RIGHT, buff = 1)
        self.play(Write(continuum))


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
        self.play(ShowCreation(chain))

        self.dither()
        self.play(FadeOut(chain))

        bound = 3.5
        reals = NumberLine(x_min = -bound, x_max = bound).shift(0.5*DOWN)
        reals_label = TexMobject("\\mathbb R").next_to(reals, DOWN, aligned_edge = RIGHT)
        self.play(ShowCreation(reals), FadeIn(reals_label))

        self.dither()
