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

def make_naturals():
    naturals = VGroup(TexMobject(str(n)) for n in range(18)).arrange_submobjects(buff = 0.5)
    nat_rect = SurroundingRectangle(naturals, color = GREEN)
    nat_l = TexMobject("\\omega").highlight(GREEN).next_to(nat_rect, LEFT)
    return VGroup(naturals, nat_rect, nat_l).to_corner(UP+LEFT)

col_a = BLUE
col_b = RED

col_nat = GREEN
col_int = BLUE
col_rat = "#FF50FF"
col_real = RED

class NaturalsAddition(Scene):
    def construct(self):

        nat_g = make_naturals()
        naturals, nat_rect, nat_l = nat_g
        self.add(nat_g)

        col_a = BLUE
        col_b = RED
        a = 5
        b = 3

        label_a = naturals[a].copy()
        label_b = naturals[b].copy()
        label_a.save_state()
        label_b.save_state()
        VGroup(label_a, label_b).arrange_submobjects(DOWN, buff=1).shift(LEFT)

        self.play(MoveFromSaved(label_a))
        self.play(MoveFromSaved(label_b))

        el_a = VGroup(naturals[:a]).copy().next_to(label_a, buff = 0.5)
        el_b = VGroup(naturals[:b]).copy().next_to(label_b, buff = 0.5)
        rect_a = SurroundingRectangle(el_a, color = WHITE, buff = 0.2)
        rect_b = SurroundingRectangle(el_b, color = WHITE, buff = 0.2)
        set_a = VGroup(el_a, rect_a)
        set_b = VGroup(el_b, rect_b)

        self.play(FadeIn(set_a), FadeIn(set_b))

        pairs_ab = VGroup(
            VGroup(TexMobject("({},{})".format(num,i)) for num in range(x)).arrange_submobjects()
            for i,x in enumerate((a,b))
        )

        pairs_src = pairs_ab.copy()
        pairs_src.set_fill(opacity = 0)
        for pairs, elements in zip(pairs_src, (el_a, el_b)):
            for pair, el in zip(pairs, elements):
                pair.shift(el.get_center() - pair[1].get_center())
                pair[1].set_fill(opacity = 1)
            self.remove(elements)
            self.add(pairs)

        set_a = VGroup(pairs_ab[0], rect_a)
        set_b = VGroup(pairs_ab[1], rect_b)

        pairs_ab.highlight(GREY)
        for pairs, col, src in zip(pairs_ab, (col_a, col_b), (el_a, el_b)):
            for pair in pairs:
                pair[1].highlight(WHITE)
                pair[3].highlight(col)
            pairs.scale(0.6)
            pairs.shift(src.get_edge_center(LEFT) - pairs.get_edge_center(LEFT))

        self.play(
            ReplacementTransform(pairs_src[0], pairs_ab[0]),
            Transform(rect_a, SurroundingRectangle(pairs_ab[0], color = WHITE, buff = 0.2)),
        )
        self.play(
            ReplacementTransform(pairs_src[1], pairs_ab[1]),
            Transform(rect_b, SurroundingRectangle(pairs_ab[1], color = WHITE, buff = 0.2)),
        )
        self.dither()

        labels = []
        labels_dest = []
        for label, pairs in zip((label_a, label_b), pairs_ab):
            element = pairs[0][3].copy()
            rect = SurroundingRectangle(element, color = GREY)
            label_src = VGroup(label, TexMobject("\\times"), [rect, element])
            label_src.arrange_submobjects(center = False)
            label_dest = label_src.copy()
            point = label.get_edge_center(RIGHT)
            label_dest.shift(point - label_src.get_edge_center(RIGHT))
            label_hidden = VGroup(label_src[1:])
            label_hidden.highlight(BLACK)
            label_hidden.scale_about_point(0, point)
            labels.append(label_src)
            labels_dest.append(label_dest)

        self.play(Transform(labels[0], labels_dest[0]))
        self.play(Transform(labels[1], labels_dest[1]))

        self.dither()

        labels[1].save_state()
        union_label = VGroup(labels[0], TexMobject('\\cup'), labels[1])
        union_label.arrange_submobjects(LEFT, center = False, aligned_edge = DOWN)
        
        set_a.save_state()
        set_b.save_state()
        set_a.move_to(set_b, coor_mask = Y_MASK)
        set_b.next_to(set_a, LEFT)
        self.play(
            MoveFromSaved(set_a),
            MoveFromSaved(set_b),
            MoveFromSaved(labels[1], path_arc = -np.pi/3),
        )
        union_rect = SurroundingRectangle(VGroup(set_a, set_b))
        self.play(
            FadeIn(union_label[1]),
            ShowCreation(union_rect),
            FadeOut(VGroup(rect_a, rect_b)),
        )

        sum_el = VGroup(naturals[:a+b]).copy()
        matching = []

        for src, dest in zip(sum_el, pairs_ab[1].submobjects + pairs_ab[0].submobjects):
            src.move_to(dest)
            src.shift(1.5*DOWN)
            matching.append(Line(src, dest, buff = 0.1))
        matching = VGroup(matching)

        sum_rect = SurroundingRectangle(sum_el, color = GREY)
        sum_label = TexMobject("{}+{} = {}".format(a,b,a+b)).next_to(sum_rect, DOWN)
        self.play(
            FadeIn(sum_rect),
            FadeIn(sum_el),
            ShowCreation(matching, submobject_mode = "all_at_once"),
        )
        self.play(Write(sum_label))
        self.dither()
        self.play(FadeOut(VGroup(
            sum_rect, sum_el, sum_label,
            pairs_ab,
            union_label, union_rect,
            matching,
        )))

class NaturalsMultiplication(Scene):
    def construct(self):
        
        nat_g = make_naturals()
        naturals, nat_rect, nat_l = nat_g
        self.add(nat_g)

        a = 5
        b = 3

        #self.add(label_a, label_b)
        product_pairs = VGroup(
            VGroup(
                TexMobject("({},{})".format(x,y))
                for y in range(b)
            ).arrange_submobjects(UP, buff = 0.5)
            for x in range(a)
        ).arrange_submobjects(RIGHT)

        product_pairs.highlight(GREY)
        for column in product_pairs:
            for el in column:
                el[1].highlight(col_a)
                el[3].highlight(col_b)

        product_pairs.scale(0.7)
        product_rect = SurroundingRectangle(product_pairs, buff = 0.2)
        product_label = TexMobject("{}\\times{}".format(a,b)).next_to(product_rect, UP)
        product_label[0].highlight(col_a)
        product_label[2].highlight(col_b)

        self.play(
            FadeIn(product_label),
            FadeIn(product_pairs),
            ShowCreation(product_rect),
        )

        in_line = []
        for column in product_pairs:
            next_el = list(column.submobjects)
            random.shuffle(next_el)
            in_line += next_el

        in_line = VGroup(in_line)
        in_line.save_state()
        in_line.arrange_submobjects()
        in_line.scale(0.8)
        product_label.save_state()
        product_label.next_to(in_line, UP)

        self.play(
            Transform(product_rect, SurroundingRectangle(in_line)),
            MoveFromSaved(product_label),
            MoveFromSaved(in_line),
        )

        aproduct_el = VGroup(naturals[:a*b]).copy()
        matching = []

        for src, dest in zip(aproduct_el, in_line):
            src.move_to(dest)
            src.shift(1.5*DOWN)
            matching.append(Line(src, dest, buff = 0.1))
        matching = VGroup(matching)

        aproduct_rect = SurroundingRectangle(aproduct_el, color = GREY)
        aproduct_label = TexMobject("{}\\cdot{} = {}".format(a,b,a*b)).next_to(aproduct_rect, DOWN)

        self.play(
            FadeIn(aproduct_rect),
            FadeIn(aproduct_el),
            ShowCreation(matching, submobject_mode = "all_at_once"),
        )
        self.play(FadeIn(aproduct_label))

        self.dither()
        self.play(FadeOut(VGroup(
            product_label, product_pairs, product_rect,
            aproduct_el, aproduct_rect, aproduct_label,
            matching,
        )))

class Integers(Scene):
    def construct(self):

        nat_g = make_naturals()
        self.add(nat_g)

        nat2_g = nat_g.copy()
        nat_gg = VGroup(nat_g, nat2_g)
        nat_gg.save_state()
        nat_gg.arrange_submobjects(DOWN, buff = 1, center = False)

        pair_scale = 0.6
        pairs_g = []
        for i, group in enumerate(nat_gg):
            naturals, rect, label = group
            pairs = VGroup(
                TexMobject("({},{})".format(num,i))
                for num in range(len(naturals))
            ).arrange_submobjects()
            pairs.highlight(GREY).scale(pair_scale)
            for pair in pairs:
                pair[1].highlight(WHITE)
                pair[3].highlight([col_a,col_b][i])
            pairs.shift(- pairs[0].get_center())
            pairs_g.append(pairs)

        nat_gg.shift(pairs_g[0].get_edge_center(LEFT)-nat2_g[0].get_edge_center(LEFT))

        self.play(
            MoveFromSaved(nat_gg),
            run_time = 1.5
        )
        self.dither()

        for pairs, group in zip(pairs_g, nat_gg):
            pairs.move_to(group, coor_mask = Y_MASK)
            pairs.save_state()
            pairs.set_fill(opacity = 0)
            for pair, num in zip(pairs, group[0]):
                pair.scale(1/pair_scale)
                pair.shift(num.get_center() - pair[1].get_center())
                pair[1].set_fill(opacity = 1)

        for pair, group in zip(pairs_g, nat_gg):
            naturals = group[0]
            self.remove(naturals)
            group.remove(naturals)
            group.submobjects.insert(0, pair)

        times = TexMobject("\\times")
        new_labels = VGroup()
        new_labels_dest = VGroup()
        for pairs, group in zip(pairs_g, nat_gg):
            label = group.submobjects.pop()
            num = pairs.saved_state[0][-2].copy()
            num = VGroup(SurroundingRectangle(num, color = WHITE), num)
            new_label = VGroup(label, times.copy(), num)
            new_label_dest = new_label.copy()
            new_label_dest.arrange_submobjects()
            new_label_dest.next_to(label.get_edge_center(RIGHT), LEFT, buff = 0)
            group.add(new_label)
            new_mob = VGroup(new_label[1:])
            new_mob.scale(0).next_to(label).highlight(BLACK)

            new_labels.add(new_label)
            new_labels_dest.add(new_label_dest)

        self.play(
            Transform(new_labels, new_labels_dest),
            pairs_g[0].restore, pairs_g[1].restore,
        )

        self.dither()

        pos, neg = nat_gg
        neg.save_state()
        neg.scale_about_point(-1, neg[0][0].get_center())
        for mob in neg[0].submobjects + [neg[2]]:
            mob.scale_in_place(-1)

        self.play(MoveFromSaved(neg, path_arc = -np.pi), run_time = 1.5)

        self.dither()
        to_remove = neg[0][0]
        neg[0].remove(to_remove)
        to_remove.save_state()
        to_remove.shift(DOWN)
        to_remove.set_fill(opacity = 0)
        self.play(MoveFromSaved(to_remove))

        self.dither()

        pairs_g, rects, labels = VGroup(zip(pos, neg))
        center = rects.get_center()
        pairs_g.save_state()
        integer_label = TexMobject("\\mathbb Z").move_to(pos[0][0])
        integer_label.next_to(rects, UP, coor_mask = Y_MASK)
        integer_label.highlight(BLACK)
        integer_label.save_state()

        for pairs in pairs_g: pairs.move_to(center, coor_mask = Y_MASK)
        rects.save_state()
        lines = VGroup()
        lines_dest = VGroup()
        for rect in rects:
            lines.add(*[
                Line(*map(rect.get_corner, (LEFT+d, RIGHT+d)), color = GREEN)
                for d in (UP, DOWN)
            ])
            rect.save_state()
            rect.move_to(center, coor_mask = Y_MASK)
            rect.highlight(BLACK, family = False)
            lines_dest.add(*[
                Line(*map(rect.get_corner, (LEFT+d, RIGHT+d)), color = GREEN)
                for d in (UP, DOWN)
            ])

        integer_label.next_to(rects, UP, coor_mask = Y_MASK)
        integer_label.highlight(WHITE)
        integer_rect = SurroundingRectangle(rects, buff = 0, color = GREEN)

        self.play(
            FadeOut(labels),
            MoveFromSaved(integer_label),
            MoveFromSaved(rects),
            MoveFromSaved(pairs_g),
            Transform(lines, lines_dest, remover = True)
        )
        self.add(integer_rect)
        self.dither()

        pos, neg = pairs_g

        pos.save_state()
        neg.save_state()
        minus = TexMobject('-')
        minuses = []
        minuses_dest = []
        pos.save_state()
        neg.save_state()
        numbers = []
        for pair in pos:
            p = pair.get_center()
            pair.set_fill(opacity = 0)
            n = pair[1]
            n.scale(0.9/pair_scale)
            n.move_to(p)
            n.set_fill(opacity = 1)
            numbers.append(n)

        for pair in neg:
            p = pair.get_center()
            minuses.append(minus.copy().highlight(BLACK).scale(pair_scale).next_to(pair, LEFT, buff = 0))
            pair.set_fill(opacity = 0)
            n = pair[1]
            n.scale(0.9/pair_scale)
            n = VGroup(minus.copy(), n).arrange_submobjects(buff = 0.1)
            n.move_to(p)
            n.set_fill(opacity = 1)
            numbers.append(n)
            minuses_dest.append(n[0])

        minuses = VGroup(minuses)
        minuses_dest = VGroup(minuses_dest)
        numbers = VGroup(numbers)

        self.play(
            MoveFromSaved(pos),
            MoveFromSaved(neg),
            ReplacementTransform(minuses, minuses_dest),
        )
        self.remove(pos, neg)
        self.add(numbers)
        self.dither()

        arithmetics = [
            "(a)+(b) = (a+b)",
            "(-a)+(-b) = -(a+b)",
            "(-a)+(b) = (b-a)\hbox{ nebo }-(a-b)",
            "(a)+(-b) = (a-b)\hbox{ nebo }-(b-a)",
            "0\cdot x = 0",
            "(a)\cdot(b) = (a\cdot b)",
            "(-a)\cdot(-b) = (a\cdot b)",
            "(-a)\cdot(b) = -(a\cdot b)",
            "(a)\cdot(-b) = -(a\cdot b)",
        ]
        addition_rules = arithmetics[:4]
        mul_rules = arithmetics[4:]

        def equations_to_mob(rules):
            rules = [
                "   "+rule.replace(' = ', ' &= ')+"\\cr\n"
                for rule in rules
            ]
            tex = "".join(rules)
            return TexMobject(tex).scale(0.7)

        addition_mob = equations_to_mob(addition_rules)
        mul_mob = equations_to_mob(mul_rules)
        rules_mob = VGroup(addition_mob, mul_mob)
        rules_mob.arrange_submobjects(aligned_edge = UP, buff = 2).to_edge(DOWN)

        self.play(FadeIn(rules_mob, run_time = 3, submobject_mode = "lagged_start"))
        self.dither(4)

class Fractions(Scene):
    def construct(self):

        title = TextMobject("Racionální čísla").to_edge(UP)
        self.add(title)

        ratio = TexMobject("\\frac ab").scale(1.5)
        ratio[0].highlight(col_a)
        ratio[2].highlight(col_b)

        pair = TexMobject("(a,b)").scale(1.5)
        pair[1].highlight(col_a)
        pair[3].highlight(col_b)

        VGroup(ratio, pair).arrange_submobjects(DOWN)

        self.play(Write(ratio))
        self.dither()

        lbracket = pair[0].copy().next_to(ratio[0], LEFT).set_fill(opacity = 0)
        rbracket = pair[-1].copy().next_to(ratio[-1], RIGHT).set_fill(opacity = 0)
        pair_src = VGroup([lbracket] + ratio.copy().submobjects + [rbracket])
        self.play(ReplacementTransform(pair_src, pair))

        self.dither()

        restrictions = VGroup(
            TextMobject("$a,b$ celá"),
            TexMobject("b\\neq 0"),
            TextMobject("základní tvar"),
        ).arrange_submobjects(DOWN, aligned_edge = LEFT)
        restrictions.to_edge(RIGHT)
        restrictions[0][0].highlight(col_a)
        for i,j in ((0,2), (1,0)):
            restrictions[i][j].highlight(col_b)

        self.play(FadeIn(VGroup(restrictions[:2]), submobject_mode = "lagged_start"))
        formulas = [
            "(a,b)*(c,d) = (a*c, b*d)",
            "(a,b)+(c,d) = (a*d +b*c, b*d)",
        ]
        formulas_chars = (formulas[0]+formulas[1]).replace(' ', '')
        formulas_tex = [
            formula.replace('=', '&=').replace('*', '\\cdot ')+"\\cr"
            for formula in formulas
        ]
        formulas_mob = TexMobject(formulas_tex).to_corner(DOWN+LEFT)
        c = WHITE
        mob_chars = formulas_mob[0].submobjects + formulas_mob[1].submobjects
        for mob, char in zip(mob_chars, formulas_chars):
            if char == '(': c = col_a
            elif char == ',': c = col_b
            elif char == ')': c = WHITE
            else: mob.highlight(c)

        self.play(FadeIn(formulas_mob))

        self.dither()
        self.play(FadeOut(VGroup(ratio, pair)))

        eq_fracs = TexMobject(r"\frac{-1}2=", r"\frac{-3}6 = \frac2{-4}")
        neq_pairs = TexMobject("(-1,2)\quad", r"(-3,6)\neq(2,-4)")

        VGroup(eq_fracs, neq_pairs).arrange_submobjects(DOWN)
        for mob in eq_fracs, neq_pairs:
            mid = mob[1][len(mob[1])//2]
            mob.shift(-mid.get_center() * X_MASK)

        VGroup(
            eq_fracs[0][:2],
            eq_fracs[1][:2],
            eq_fracs[1][5],
            neq_pairs[0][1:3],
            neq_pairs[1][1:3],
            neq_pairs[1][-5],
        ).highlight(col_a)
        VGroup(
            eq_fracs[0][3],
            eq_fracs[1][3],
            eq_fracs[1][-2:],
            neq_pairs[0][4],
            neq_pairs[1][4],
            neq_pairs[1][-3:-1],
        ).highlight(col_b)

        self.play(Write(eq_fracs[1]))
        self.play(Write(neq_pairs[1]))

        self.play(FadeIn(restrictions[-1], submobject_mode = "lagged_start"))
        self.dither()
        self.play(FadeIn(eq_fracs[0]))

        self.dither()
        self.play(
            FadeIn(neq_pairs[0]),
            neq_pairs[1].highlight, DARK_GREY,
        )
        std_template = TextMobject("std")

        inserted = VGroup()
        inserted_dest = VGroup()
        formulas_mob.save_state()
        for formula in formulas_mob:
            i = 12
            std = std_template.copy()
            point = formula[i].get_edge_center(LEFT)
            std.next_to(formula[1].get_edge_center(DOWN) - std[0].get_edge_center(DOWN))
            std.next_to(point, buff = 0, coor_mask = X_MASK)
            VGroup(formula[i:]).next_to(std, buff = 0.1, coor_mask = X_MASK)
            inserted_dest.add(std.copy())
            std.highlight(BLACK)
            std.scale_about_point(0, point)
            inserted.add(std)

        self.play(
            Transform(inserted, inserted_dest),
            MoveFromSaved(formulas_mob),
        )
        self.dither(4)

        self.play(FadeOut(VGroup(
            restrictions, formulas_mob,
            eq_fracs, neq_pairs,
            inserted,
        )))

class Factorization(Scene):
    def construct(self):

        title = TextMobject("Racionální čísla").to_edge(UP)
        self.add(title)

        pairs_a = VGroup(
            TexMobject("(-1,2)"),
            TexMobject("(2,-4)"),
            TexMobject("(-3,6)"),
            TexMobject("\\vdots"),
        ).arrange_submobjects(DOWN)
        pairs_a.shift(3*LEFT)
        rect_a = SurroundingRectangle(pairs_a, color = col_a, buff = 0.3)
        self.play(FadeIn(pairs_a[0]))
        self.play(FadeIn(pairs_a[1]))
        self.play(FadeIn(pairs_a[2]))
        self.play(FadeIn(pairs_a[3]))
        self.dither()
        self.play(ShowCreation(rect_a))

        label_a = TexMobject("a = \\frac{-1}{2}")
        label_a[0].highlight(col_a)
        label_a.next_to(rect_a, DOWN)

        self.play(Write(label_a[0]))
        self.play(FadeIn(VGroup((label_a[1:]))))
        label_dest = TexMobject("a = \\frac{2}{-4}")
        label_dest[0].highlight(col_a)
        label_dest.shift(label_a[0].get_center() - label_dest[0].get_center())
        minus = label_dest.submobjects.pop(4)
        label_dest.submobjects.insert(2, minus)
        self.play(Transform(label_a, label_dest))
        self.dither()

        pairs_b = VGroup(
            TexMobject("(1,3)"),
            TexMobject("(2,6)"),
            TexMobject("(3,9)"),
            TexMobject("\\vdots"),
        ).arrange_submobjects(DOWN)
        rect_b = SurroundingRectangle(pairs_b, color = col_b, buff = 0.3)
        label_b = TexMobject("b = \\frac13")
        label_b[0].highlight(col_b)
        label_b.next_to(rect_b, DOWN)
        group_b = VGroup(pairs_b, rect_b, label_b)

        self.play(FadeIn(group_b))

        label_ab = TexMobject("a\cdot b")
        label_ab[0].highlight(col_a)
        label_ab[-1].highlight(col_b)
        label_ab.move_to(label_b)

        pairs_ab = VGroup(
            TexMobject("(-1\\cdot2,2\\cdot6)"),
            TexMobject("(-1,6)"),
            TexMobject("(1,-6)"),
            TexMobject("\\vdots"),
        ).arrange_submobjects(DOWN)
        for i in 1,2,6: pairs_ab[0][i].highlight(col_a)
        for i in 4,8: pairs_ab[0][i].highlight(col_b)
        rect_ab = SurroundingRectangle(pairs_ab, buff = 0.3)
        group_ab = VGroup(pairs_ab, rect_ab, label_ab)
        group_ab.next_to(group_b, buff = 1, coor_mask = X_MASK)

        cdot = TexMobject("\\cdot").move_to(
            (rect_a.get_edge_center(RIGHT)+rect_b.get_edge_center(LEFT))/2)
        eq = TexMobject("=").move_to(
            (rect_b.get_edge_center(RIGHT)+rect_ab.get_edge_center(LEFT))/2)
        self.add(cdot, eq)

        self.play(FadeIn(cdot), FadeIn(eq), Write(label_ab))

        sample_a = pairs_a[0].copy()
        sample_a.save_state()
        sample_a.move_to(pairs_ab[0])
        for i in 1,2,4: sample_a[i].highlight(col_a)
        sample_b = pairs_b[1].copy()
        sample_b.save_state()
        sample_b.move_to(pairs_ab[1])
        for i in 1,3: sample_b[i].highlight(col_b)

        self.play(MoveFromSaved(sample_a, path_arc = -np.pi/3))
        self.play(MoveFromSaved(sample_b))
        self.dither()

        sample_a_dest = VGroup(
            pairs_ab[0][i] for i in (0,1,2,5,6,9)
        )
        sample_b_dest = VGroup(
            pairs_ab[0][i] for i in (0,4,5,8,9)
        )
        self.play(
            FadeIn(pairs_ab[0][3]), FadeIn(pairs_ab[0][7]), # dots
            Transform(sample_a, sample_a_dest),
            Transform(sample_b, sample_b_dest),
        )
        self.remove(sample_a, sample_b)
        self.add(pairs_ab[0])
        self.dither()

        self.play(
            ShowCreation(rect_ab),
            FadeIn(VGroup(pairs_ab[1:]), submobject_mode = "lagged_start"),
        )
        self.dither(2)

        self.play(FadeOut(group_ab))
        plus = TexMobject('+').move_to(cdot)
        self.play(Transform(cdot, plus))
        self.remove(cdot)
        self.add(plus)

        pairs_ab = VGroup(
            TexMobject("(-3+2,6)"),
            TexMobject("(1,-6)"),
            TexMobject("(-2,12)"),
            TexMobject("\\vdots"),
        ).arrange_submobjects(DOWN)
        for i in 1,2: pairs_ab[0][i].highlight(col_a)
        for i in 4,: pairs_ab[0][i].highlight(col_b)
        rect_ab = SurroundingRectangle(pairs_ab, buff = 0.3)
        label_ab = TexMobject("a + b")
        label_ab[0].highlight(col_a)
        label_ab[-1].highlight(col_b)
        label_ab.move_to(label_b)
        group_ab = VGroup(pairs_ab, rect_ab, label_ab)
        group_ab.next_to(eq, buff = 0.3, coor_mask = X_MASK)

        self.play(Write(label_ab))

        sample_a = pairs_a[2].copy()
        sample_a.save_state()
        for i in 1,2,4: sample_a[i].highlight(col_a)
        sample_b = pairs_b[1].copy()
        sample_b.save_state()
        for i in 1,3: sample_b[i].highlight(col_b)
        samples = VGroup(sample_b, sample_a)
        samples.arrange_submobjects(DOWN, aligned_edge = RIGHT)
        samples.move_to(VGroup(pairs_ab[:2]))

        self.play(
            MoveFromSaved(sample_a, path_arc = np.pi/3),
            MoveFromSaved(sample_b),
        )
        self.play(
            FocusOn2(sample_a[-2]),
            FocusOn2(sample_b[-2]),
        )
        self.dither()

        sample_a_dest = VGroup(
            pairs_ab[0][i] for i in (0,1,2,5,6,7)
        )
        sample_b_dest = VGroup(
            pairs_ab[0][i] for i in (0,3,4,5,6,7)
        )
        self.play(
            FadeIn(pairs_ab[0][3]), # plus
            Transform(sample_a, sample_a_dest),
            Transform(sample_b, sample_b_dest),
        )
        self.remove(sample_a, sample_b)
        self.add(pairs_ab[0])
        self.dither()

        self.play(
            ShowCreation(rect_ab),
            FadeIn(VGroup(pairs_ab[1:]), submobject_mode = "lagged_start"),
        )
        self.dither(2)

def gcd(a,b):
    while b>0:
        a,b = b,a%b
    return a

class Extensions(Scene):
    def construct(self):

        bound = int(SPACE_WIDTH)+1

        nat_shift = 2
        naturals = VGroup([
            TexMobject(str(i)).move_to(X_MASK*i)
            for i in range(int(nat_shift+SPACE_WIDTH+1))
        ])
        naturals.highlight(col_nat)
        naturals.to_edge(UP).shift(nat_shift*LEFT)

        integers = []
        for k in range(-bound+1, bound):
            if k < 0: num = str(k)
            else: num = "+{}".format(k)
            num = TexMobject(num)
            num.move_to(X_MASK * k)
            integers.append(num)

        integers = VGroup(integers)
        integers.highlight(col_int)

        sizes = 0.7, 0.7, 0.4, 0.4
        rationals = []
        for denom, scale in zip(range(1,5), sizes):
            row = []
            for nom in range(-denom*bound+1, denom*bound):
                if gcd(denom, abs(nom)) > 1: continue
                num = TexMobject("\\frac{%d}{%d}" % (nom,denom) )
                num.scale(scale)
                num.move_to(X_MASK * float(nom)/denom)
                row.append(num)
            rationals.append(row)
        rationals = VGroup(rationals)
        for row1, row2, buff in zip(rationals, rationals[1:], (0.2, 0.2, 0.1, 0.1)):
            row2.next_to(row1, DOWN, buff = buff, coor_mask = Y_MASK)
        rationals.to_edge(DOWN, buff = 0.1)
        rationals.highlight(col_rat)

        integers.move_to((naturals.get_edge_center(DOWN) + rationals.get_edge_center(UP))/2,
                         coor_mask = Y_MASK)

        int_zero_index = len(integers) // 2
        arrow = Arrow(
            naturals[0].get_edge_center(DOWN),
            integers[int_zero_index].get_edge_center(UP),
        )
        nat_to_int = VGroup(
            arrow.copy().shift(num.get_center() - naturals[0].get_center())
            for num in naturals
        )

        int_to_rat = VGroup(
            Arrow(num_i, num_r)
            for num_i, num_r in zip(integers[int_zero_index:], rationals[0][int_zero_index:])
        )

        self.play(ShowCreation(naturals))
        self.dither()
        self.play(ShowCreation(integers))
        self.dither()
        self.play(*map(ShowCreation, nat_to_int))
        self.dither(2)

        self.play(FadeIn(rationals, submobject_mode = "lagged_start"))
        self.play(*map(ShowCreation, int_to_rat))
        self.dither(2)

        self.play(FadeOut(VGroup(nat_to_int, int_to_rat)))

        nat3_src = naturals[3]
        nat3 = nat3_src.copy()
        int3_src = integers[int_zero_index+3]
        int3 = int3_src.copy()
        rat3_src = rationals[0][int_zero_index+3]
        rat3 = rat3_src.copy()

        examples = VGroup(nat3, int3, rat3)
        examples.arrange_submobjects(DOWN, aligned_edge = RIGHT, coor_mask = X_MASK)
        examples.to_edge(LEFT)

        eqs = VGroup(
            TexMobject('=').next_to(example)
            for example in examples
        )

        nat_elements = VGroup(TexMobject(str(i)) for i in range(3))
        nat_elements.arrange_submobjects(buff = 0.3)
        nat_rect = SurroundingRectangle(nat_elements, color = col_nat)
        nat_meaning = VGroup(
            nat_elements,
            nat_rect,
        )
        int_meaning = TexMobject("(3, 0)")
        for i in 0,-1: int_meaning[i].highlight(col_int)

        rat_pairs = VGroup(
            TexMobject("(+3,+1)"),
            TexMobject("(-3,-1)"),
            TexMobject("(+6,+2)"),
            TexMobject("(-6,-2)"),
            TexMobject("(+9,+3)"),
            TexMobject("(-9,-3)"),
        )
        rat_pairs.arrange_submobjects(DOWN)
        rat_rect = SurroundingRectangle(rat_pairs, color = col_rat)
        rat_meaning = VGroup(
            rat_pairs,
            rat_rect,
        )
        
        meanings = VGroup(nat_meaning, int_meaning, rat_meaning)

        for meaning, eq in zip(meanings, eqs):
            meaning.next_to(eq)
        rat_meaning.next_to(rat3, aligned_edge = UP, coor_mask = Y_MASK)
        rat_meaning.shift(UP)

        naturals.remove(nat3_src)
        self.play(FadeOut(naturals), ReplacementTransform(nat3_src, nat3))
        self.play(
            FadeIn(VGroup(eqs[0], nat_elements), submobject_mode = "lagged_start"),
            ShowCreation(nat_rect),
        )
        self.dither()
        integers.remove(int3_src)
        self.play(FadeOut(integers), ReplacementTransform(int3_src, int3))
        self.play(FadeIn(VGroup(eqs[1], int_meaning), submobject_mode = "lagged_start"))
        self.dither()
        rationals[0].remove(rat3_src)
        self.play(FadeOut(rationals), ReplacementTransform(rat3_src, rat3))
        self.play(
            FadeIn(VGroup(eqs[2], rat_pairs), submobject_mode = "lagged_start"),
            ShowCreation(rat_rect),
        )
        self.dither(2)

        self.play(FadeOut(VGroup(examples, eqs, meanings)))

class RealNumbers(Scene):

    def num_pointer(self, num_str, num, direction = DOWN, pointer_color = WHITE):
        pointer = TrianglePointer(color = pointer_color)
        if direction[1] < 0: pointer.scale(-1)
        result = VGroup(
            pointer,
            TexMobject(num_str),
        ).arrange_submobjects(direction)
        result.num = num
        result.next_to(self.numberline.number_to_point(num), direction, buff = 0)
        return result

    def make_irac(self):
        return self.num_pointer("\\sqrt2", np.sqrt(2), UP, col_real)
    def make_frac(self, nom, denom):
        return self.num_pointer("\\frac{%d}{%d}"%(nom, denom), float(nom)/denom,
                                pointer_color = col_rat)

    def scale_line(self, scale, about = 0):
        self.numberline.save_state()
        self.pointers.save_state()
        self.numberline.stretch_about_point(
            scale, 0,
            self.numberline.number_to_point(about))
        for pointer in self.pointers:
            pointer.move_to(self.numberline.number_to_point(pointer.num),
                            coor_mask = X_MASK)
        self.play(
            MoveFromSaved(self.numberline),
            MoveFromSaved(self.pointers)
        )

    def change_approx(self, nom1,denom1, nom2,denom2):
        smaller_dest = self.make_frac(nom1, denom1)
        bigger_dest = self.make_frac(nom2, denom2)
        self.play(
            Transform(self.smaller, smaller_dest),
            Transform(self.bigger, bigger_dest),
        )
        self.smaller.num = smaller_dest.num
        self.bigger.num = bigger_dest.num
    
    def construct(self):

        self.numberline = NumberLine(unit_size = 1)
        self.play(ShowCreation(self.numberline))
        numberline_ori = self.numberline

        sqrt2 = self.make_irac()
        sqrt2.save_state()
        sqrt2.shift(0.5*UP)
        sqrt2.set_fill(opacity = 0)
        self.play(sqrt2.restore)

        self.dither()

        self.smaller = self.make_frac(1,1)
        self.bigger = self.make_frac(3,2)
        self.pointers = VGroup(sqrt2, self.smaller, self.bigger)
        self.smaller.save_state()
        self.smaller.shift(LEFT*0.5).set_fill(opacity = 0)
        self.bigger.save_state()
        self.bigger.shift(RIGHT*0.5).set_fill(opacity = 0)
        self.play(self.smaller.restore, self.bigger.restore)
        self.scale_line(5, np.sqrt(2))
        self.change_approx(4,3,  3,2)
        self.scale_line(2, np.sqrt(2))
        self.change_approx(11,8,  13,9)

        self.dither(2)

        self.play(FadeOut(VGroup(self.smaller, self.bigger)))

        rat_dots = VGroup(
            Dot(interpolate(SPACE_WIDTH*LEFT, SPACE_WIDTH*RIGHT, alpha), radius = 0.05)
            for alpha in np.linspace(0, 1, 100)
        )
        rat_dots.shift(0.2*DOWN)
        rat_dots.highlight(GREY)
        self.play(FadeIn(rat_dots))
        split = sqrt2.get_center()[0]
        smaller_dots = VGroup(filter(lambda dot: dot.get_center()[0] < split, rat_dots))
        bigger_dots = VGroup(filter(lambda dot: dot.get_center()[0] >= split, rat_dots))
        smaller_dots.submobjects.reverse()

        self.play(bigger_dots.highlight, col_rat, submobject_mode = "one_at_a_time")
        self.dither()
        self.play(bigger_dots.highlight, GREY)

        self.play(smaller_dots.highlight, col_rat, submobject_mode = "one_at_a_time")
        self.dither()

        smaller_ori = smaller_dots
        smaller_dots = smaller_dots.copy()
        smaller_dots.save_state()
        smaller_dots.shift(2*DOWN)
        self.play(MoveFromSaved(smaller_dots))
        smaller_rect = SurroundingRectangle(smaller_dots, buff = 0.3, color = col_real)
        real_label = sqrt2[1].copy().next_to(smaller_rect)
        self.play(ShowCreation(smaller_rect), FadeIn(real_label))

        self.dither(5)

        self.play(
            FadeOut(VGroup(
                self.numberline, sqrt2, smaller_dots, smaller_rect, real_label,
            )),
            rat_dots.highlight, GREY,
        )

        smaller_dots = smaller_ori

        subset = [smaller_dots[0]]
        for dot in smaller_dots[1:]:
            if random.random() < 0.15:
                subset.append(dot)
        unselected = VGroup(smaller_dots[:])
        unselected.remove(*subset)
        subset = VGroup(subset)
        subset.save_state()
        subset.highlight(col_rat)
        subset.shift(0.1*UP)

        reals_definition = VGroup(
            TextMobject("Reálné číslo $=$ Podmnožina $\\mathbb Q$"),
            TextMobject("$\\bullet$ s každým prvkem všechny menší,"),
            TextMobject("$\\bullet$ není prázdná, ani celé $\\mathbb Q$,"),
            TextMobject("$\\bullet$ nemá nejmenší prvek."),
        )
        reals_definition.arrange_submobjects(DOWN, aligned_edge = LEFT)
        reals_definition.to_corner(UP+LEFT)

        self.play(
            FadeIn(reals_definition[0], submobject_mode = "lagged_start"),
            MoveFromSaved(subset),
        )
        self.dither()
        self.play(
            FadeIn(reals_definition[1], submobject_mode = "lagged_start"),
        )
        smaller_dots.save_state()
        unselected.highlight(col_rat).shift(0.1*UP)
        self.play(MoveFromSaved(smaller_dots, submobject_mode = "one_at_a_time"))
        self.dither()
        self.play(
            FadeIn(reals_definition[2], submobject_mode = "lagged_start"),
        )
        self.dither()
        self.play(
            FadeIn(reals_definition[3], submobject_mode = "lagged_start"),
        )

        bigger_ini = VGroup(bigger_dots[:8])
        pointer = TrianglePointer(color = col_real).scale(-1)
        bigger_ini.save_state()
        VGroup(bigger_ini[:-1]).shift(0.1*UP).highlight(col_rat)
        bigger_ini[-1].shift(0.1*DOWN).highlight(WHITE)
        pointer.next_to(bigger_ini[-1], DOWN, buff = 0.1)
        pointer.save_state()
        pointer.move_to(smaller_dots[0], coor_mask = X_MASK)
        pointer.set_fill(opacity = 0)
        self.play(
            pointer.restore,
            MoveFromSaved(bigger_ini, submobject_mode = "lagged_start"),
        )
        self.dither()
        bigger_ini[-1].save_state()
        bigger_ini[-1].shift(0.1*UP).highlight(GREY)
        self.play(MoveFromSaved(bigger_ini[-1]))

        self.dither()

class RealsOperations(Scene):
    def construct(self):

        denom = 6
        nominators = range(-1-int(SPACE_WIDTH*denom), int(SPACE_WIDTH*denom)+2)
        dots = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05)
            for nom in nominators
        )
        dots.highlight(col_rat)
        for dot, nom in zip(dots, nominators): dot.nom = nom

        self.x_num = 2.7
        self.y_num = 1.8
        
        dots_x = VGroup(dot for dot in dots if float(dot.nom)/denom < self.x_num).copy()
        dots_y = VGroup(dot for dot in dots if float(dot.nom)/denom < self.y_num).copy()

        self.x_shift = UP
        self.y_shift = DOWN
        dots_x.shift(self.x_shift)
        dots_y.shift(self.y_shift)

        x_label = TexMobject('x').next_to(dots_x)
        y_label = TexMobject('y').next_to(dots_y)

        self.play(
            ShowCreation(VGroup(dots_x, dots_y)),
            FadeIn(VGroup(x_label, y_label), submobject_mode = "one_at_a_time"),
        )
        self.dither()

        dots_xy = VGroup(dot for dot in dots
                         if float(dot.nom)/denom < self.x_num+self.y_num).copy()
        dots_xy.to_edge(UP, buff = 1)
        xy_label = TexMobject('x+y').next_to(dots_xy)

        sample_x = next(dot for dot in reversed(dots_x) if dot.nom == 8)
        sample_x_label = TexMobject("\\frac 43").scale(0.8).next_to(sample_x, DOWN)
        self.play(FadeIn(sample_x_label), sample_x.highlight, YELLOW)
        self.play(sample_x.shift, 0.2*UP, rate_func = there_and_back, run_time = 0.5)

        sample_y = next(dot for dot in reversed(dots_y) if dot.nom == 3)
        sample_y_label = TexMobject("\\frac 12").scale(0.8).next_to(sample_y, DOWN)
        self.play(FadeIn(sample_y_label), sample_y.highlight, YELLOW)
        self.play(sample_y.shift, 0.2*UP, rate_func = there_and_back, run_time = 0.5)

        sample_xy = next(dot for dot in reversed(dots_xy) if dot.nom == 11)
        sample_xy_label = TexMobject("\\frac {11}{6}").scale(0.8).next_to(sample_xy, DOWN)
        sample_xy.highlight(YELLOW)

        sample_src = VGroup(sample_x, sample_y).copy()
        label_src = VGroup(sample_x_label, sample_y_label).copy()
        self.play(
            Transform(sample_src, VGroup(sample_xy)),
            Transform(label_src, VGroup(sample_xy_label)),
            FadeIn(xy_label),
        )
        self.remove(label_src, sample_src)
        self.add(sample_xy, sample_xy_label)

        self.dither(2)

        src = []
        dest = []
        dot_list = list(dots_xy)
        random.shuffle(dot_list)
        for dot in dot_list:
            if dot == sample_xy: continue

            src.append(self.get_addition_src(dot))
            dest.append((dot.copy(), dot.copy()))

        src = VGroup(src)
        dest = VGroup(dest)

        self.play(Transform(src, dest, submobject_mode = "lagged_start", run_time = 3))
        self.remove(src)
        self.add(dots_xy)
        self.dither(5)

        self.play(FadeOut(VGroup(
            dots_xy, xy_label,
            sample_xy_label, sample_x_label, sample_y_label,
        )))

        arrow_x = Arrow(ORIGIN, 1.5*LEFT).next_to(dots_x, DOWN).to_edge(LEFT, buff = 0.2)
        arrow_y = arrow_x.copy().next_to(dots_y, DOWN, coor_mask = Y_MASK)
        minus_lot_x = TexMobject('-','1','000').next_to(arrow_x)
        minus_lot_y = minus_lot_x.copy().next_to(arrow_y)

        self.play(ShowCreation(arrow_x), FadeIn(minus_lot_x))
        self.play(ShowCreation(arrow_y), FadeIn(minus_lot_y))
        self.dither()

        arrow_plus_lot = Arrow(ORIGIN, 1.5*RIGHT).to_edge(RIGHT, buff = 0.2)
        plus_lot = TexMobject('+','1','000000').next_to(arrow_plus_lot, LEFT)

        self.play(
            Transform(minus_lot_x.copy(), plus_lot),
            Transform(minus_lot_y.copy(), plus_lot),
            Transform(arrow_x.copy(), arrow_plus_lot, path_arc = -np.pi*0.3),
            Transform(arrow_y.copy(), arrow_plus_lot, path_arc = np.pi*0.3),
        )
        self.remove(*self.mobjects_from_last_animation)
        self.add(arrow_plus_lot, plus_lot)
        self.dither()

        dots_xy = VGroup(dot for dot in dots
                         if float(dot.nom)/denom < self.x_num+self.y_num).copy()
        dots_xy.to_edge(UP, buff = 1)
        xy_label = TexMobject('xy').next_to(dots_xy)

        self.play(FadeIn(xy_label))
        self.dither(2)

        self.play(FadeOut(VGroup(
            arrow_plus_lot, arrow_x, arrow_y,
            minus_lot_x, minus_lot_y, plus_lot,
        )))
        x_positive = VGroup(dot for dot in dots_x if dot.nom >= 0)
        x_negative = VGroup(dot for dot in dots_x if dot.nom < 0)
        y_positive = VGroup(dot for dot in dots_y if dot.nom >= 0)
        y_negative = VGroup(dot for dot in dots_y if dot.nom < 0)
        x_negative.submobjects.reverse()
        y_negative.submobjects.reverse()
        self.play(
            FadeOut(x_negative, submobject_mode = "one_at_a_time"),
            FadeOut(y_negative, submobject_mode = "one_at_a_time"),
        )
        self.dither()
        self.play(
            FadeIn(sample_x_label),
            FadeIn(sample_y_label),
        )

        xy_positive = VGroup(dot for dot in dots_xy if dot.nom >= 0)
        sample_xy = next(dot for dot in xy_positive if dot.nom == 4)
        sample_xy_label = TexMobject("\\frac 23").scale(0.8).next_to(sample_xy, DOWN)
        sample_xy.highlight(YELLOW)

        sample_src = VGroup(sample_x, sample_y).copy()
        label_src = VGroup(sample_x_label, sample_y_label).copy()
        self.play(
            Transform(sample_src, VGroup(sample_xy)),
            Transform(label_src, VGroup(sample_xy_label)),
        )
        self.remove(label_src, sample_src)
        self.add(sample_xy, sample_xy_label)
        self.dither()

        src = []
        dest = []
        dot_list = list(xy_positive)
        random.shuffle(dot_list)
        for dot in dot_list:
            if dot == sample_xy: continue

            src.append(self.get_multiplication_src(dot))
            dest.append((dot.copy(), dot.copy()))

        src = VGroup(src)
        dest = VGroup(dest)

        self.play(Transform(src, dest, submobject_mode = "lagged_start", run_time = 3))
        self.remove(src)
        self.add(xy_positive)
        self.dither()
        
        xy_negative = VGroup(dot for dot in reversed(dots_xy) if dot.nom < 0)
        self.play(FadeIn(xy_negative, submobject_mode = "one_at_a_time"))

        self.dither(2)
        self.play(FadeOut(VGroup(
            dots_xy, xy_label, sample_xy_label,
            x_positive, x_label, sample_x_label,
            y_positive, y_label, sample_y_label,
        )))

    def get_addition_src(self, dot):

        res = dot.get_center()[0]

        x = interpolate(res - self.y_num, self.x_num, np.random.random())
        y = res-x
        x = x*X_MASK + self.x_shift
        y = y*X_MASK + self.y_shift
        return VGroup(
            Dot(p, radius = 0.05, fill_opacity = 0)
            for p in (x,y)
        )

    def get_multiplication_src(self, dot):

        res = dot.get_center()[0]

        if res < 0 or np.isclose(res, 0):
            x,y = 0,0
        else:
            x = np.exp(interpolate(np.log(res) - np.log(self.y_num),
                                   np.log(self.x_num), np.random.random()))
            y = res/x

        x = x*X_MASK + self.x_shift
        y = y*X_MASK + self.y_shift
        return VGroup(
            Dot(p, radius = 0.05, fill_opacity = 0)
            for p in (x,y)
        )

class RealSupremum(Scene):
    def construct(self):

        title = TextMobject("Supremum").to_edge(UP)
        self.play(UnapplyMethod(title.behind_edge, UP))

        real_line = NumberLine()
        self.play(ShowCreation(real_line))

        fset = VGroup(Line(ORIGIN, DOWN) for _ in range(5))
        fset.highlight(col_real)
        fset.arrange_submobjects( buff = 0.4)
        fset.shift(RIGHT*1.1)

        self.play(ShowCreation(fset))

        pointer = TrianglePointer(color = YELLOW)
        pointer.next_to(fset[-1], UP, buff = 0.1)
        pointer.save_state()
        pointer.shift(1.5*LEFT)
        pointer.set_fill(opacity = 0)
        self.play(pointer.restore)

        infset = OrdinalOmega(height = 0.5, x0 = -1.1, x1 = np.e)
        infset.highlight(col_real)
        self.play(FadeOut(fset))
        self.play(FadeIn(infset))
        supremum = DashedLine(ORIGIN, DOWN, color = YELLOW).move_to(X_MASK*np.e)
        self.play(pointer.next_to, supremum, UP, 0.1)
        self.play(ShowCreation(supremum))

        self.dither()

        c1 = 0.6*DOWN
        c2 = 2*DOWN

        infset_cuts = []
        for bar in infset:

            x = bar.x0
            q = (bar.x0 - infset.x0)/(infset.x1 - infset.x0)
            line = Line(SPACE_WIDTH*LEFT, x*X_MASK, color = col_rat)
            line.shift(c1+c2*q)
            line.set_stroke(width = bar.thickness)
            line.fade(q)
            infset_cuts.append(line)

        infset_cuts = VGroup(infset_cuts)

        infset_dest = infset.copy()
        for bar, line in zip(infset_dest, infset_cuts):
            bar.scale(0).move_to(line.get_end())

        infset_bg = infset.copy().highlight(DARK_GREY)
        self.add(infset_bg)
        self.play(
            Transform(infset, infset_dest, submobject_mode = "one_at_a_time"),
            FadeIn(infset_cuts, submobject_mode = "one_at_a_time"),
            run_time = 2,
        )
        self.dither()

        dest_point = infset_cuts[0].get_center()
        infset_cuts.add(
            Line(SPACE_WIDTH*LEFT, supremum.get_center(),
                 color = BLACK).shift(c1+c2)
        )
        infset_cuts.submobjects.reverse()
        self.dither()

        infset_cuts.save_state()
        for line in infset_cuts:
            line.move_to(dest_point, coor_mask = Y_MASK)
            line.set_stroke(width = DEFAULT_POINT_THICKNESS)
            line.set_color(col_rat)

        self.play(MoveFromSaved(infset_cuts))

        self.remove(infset_cuts)
        supremum_cut = infset_cuts[0]
        self.add(supremum_cut)
        self.dither()

class Summary(Scene):
    def construct(self):

        denom = 6
        nominators = range(-1-int(SPACE_WIDTH*denom), int(SPACE_WIDTH*denom)+2)
        dots = VGroup(
            Dot(X_MASK * float(nom) / denom, radius = 0.05)
            for nom in nominators
        )
        for dot, nom in zip(dots, nominators): dot.nom = nom

        pi_dots = VGroup(dot for dot in dots if float(dot.nom) / denom < np.pi)
        pi_dots.highlight(col_rat)
        pi_rect = SurroundingRectangle(pi_dots, buff = 0.3, color = col_real)
        pi_label = TexMobject("\\pi").next_to(pi_rect)

        VGroup(pi_dots, pi_rect, pi_label).to_edge(UP)
        self.play(Write(pi_label))
        self.dither()
        self.play(ShowCreation(pi_rect), FadeIn(pi_dots))
        
        rat_sample = next(dot for dot in reversed(pi_dots) if dot.nom == -3)
        rat_sample_label = TexMobject("\\frac {-1}2")

        rat_sample_label.move_to(rat_sample)
        rat_sample_label.next_to(pi_rect, DOWN, coor_mask = Y_MASK)

        rat_sample.save_state()
        self.play(
            rat_sample.shift, 0.15*DOWN,
            FadeIn(rat_sample_label),
        )

        pairs = []
        for ext in 1,-1,-2,2,3,-3,-4,4:
            pair = TexMobject('(',str(-1*ext),',',str(2*ext),')')
            pair[1].highlight(col_int)
            pair[3].highlight(col_int)
            pairs.append(pair)

        pairs = VGroup(pairs).arrange_submobjects()
        pairs_rect = SurroundingRectangle(pairs, color = col_rat, buff = 0.2)
        pairs_g = VGroup(pairs, pairs_rect)
        pairs_g.next_to(rat_sample_label, DOWN)
        pairs_g.to_edge(LEFT)

        self.play(
            ShowCreation(pairs_rect),
            FadeIn(pairs, submobject_mode = "lagged_start"),
        )

        pair_ori = pairs[3]
        pair = pair_ori.copy()
        pair.shift(2.5*DOWN)
        pair.scale_in_place(1.5)
        arrow = Arrow(pair_ori, pair)
        pair.shift(X_MASK*(arrow.get_center() - pair[2].get_center()))
        self.play(
            ShowCreation(arrow),
            ReplacementTransform(pair_ori.copy(), pair),
        )

        self.dither()
        
        nom_pair = TexMobject("(2,1)")
        denom_pair = TexMobject("(4,0)")
        for p in nom_pair, denom_pair:
            for i in 0,-1: p[i].highlight(col_int)
            for i in 1,-2: p[i].highlight(col_nat)

        nom_pair.next_to(pair[1].get_edge_center(RIGHT), LEFT, buff = 0)
        pair[0].save_state()
        pair[0].next_to(nom_pair, LEFT, buff = 0.05)
        nom_pair_src = VGroup(
            nom_pair[0].copy(),
            pair[1][1],
            nom_pair[2].copy(),
            pair[1][0],
            nom_pair[4].copy(),
        )
        VGroup(nom_pair_src[::2]).set_fill(opacity = 0)
        nom_pair_src[0].next_to(pair[1], LEFT, buff = 0)
        nom_pair_src[2].next_to(pair[1], RIGHT, buff = 0)
        nom_pair_src[4].next_to(pair[1], RIGHT, buff = 0)
        pair.remove(pair[1])

        self.play(
            MoveFromSaved(pair[0]),
            ReplacementTransform(nom_pair_src, nom_pair),
        )
        
        #self.dither()

        main_num = pair[-2][0]
        denom_pair.next_to(main_num.get_edge_center(LEFT), RIGHT,  buff = 0)
        pair[-1].save_state()
        pair[-1].next_to(denom_pair, RIGHT, buff = 0.05)

        denom_pair_src = nom_pair.copy()
        denom_pair_src.set_fill(opacity = 0)

        pair.remove(main_num)
        denom_pair_src.submobjects[1] = main_num

        denom_pair_src[0].next_to(main_num, LEFT, buff = 0)
        VGroup(denom_pair_src[2:]).stretch_about_point(0,0,main_num.get_edge_center(RIGHT))

        self.play(
            MoveFromSaved(pair[-1]),
            ReplacementTransform(denom_pair_src, denom_pair),
        )

        self.dither(4)

        self.play(FadeOut(VGroup(
            nom_pair, denom_pair, pair,
            arrow,
            pairs, pairs_rect,
            rat_sample_label,
            pi_dots, pi_rect, pi_label,
        )))

class ChainSolution(Scene):
    def construct(self):

        title = TextMobject("Úloha o nespočetném řetězci")
        title.to_edge(UP)
        self.play(UnapplyMethod(title.behind_edge, UP))

        poset_rect = Rectangle(width = 7.5, height = 4.5, color = col_real)
        poset_label = TexMobject("\\mathcal P(\\mathbb Q)")
        poset_label.next_to(poset_rect, aligned_edge = UP)
        self.play(ShowCreation(poset_rect), FadeIn(poset_label))

        bound = 3.5
        reals = NumberLine(x_min = -bound, x_max = bound)
        reals.rotate(np.pi/6)
        reals_label = TexMobject("\\mathbb R")
        reals_label.next_to(reals.get_edge_center(RIGHT), LEFT, buff = 0)
        reals_label.shift(UP)
        self.play(ShowCreation(reals), FadeIn(reals_label))

        real_dots = VGroup(
            TrianglePointer(color = RED).rotate(np.pi*(1+1./6)).tip_to(reals.number_to_point(x))
            for x in (0.7, 1.6)
        )
        real_dots.save_state()
        for dot in real_dots:
            dot.tip_to(reals.main_line.get_start())
            dot.set_fill(opacity = 0)

        self.play(real_dots.restore)

        rat_lines = []
        for dot in real_dots:
            line_start = dot.get_tip()
            line_end = reals.main_line.get_start()*X_MASK + line_start*Y_MASK
            rat_lines.append(Line(line_start, line_end, color = col_rat))

        rat_lines = VGroup(rat_lines)
        self.play(ShowCreation(rat_lines[0]))
        self.play(ShowCreation(rat_lines[1]))

        self.dither(2)

        conversation = Conversation(self)
        conversation.add_bubble("Ale ptali jsme se na $\\mathcal P(\\omega)$.")
        conversation.add_bubble("Množiny $\\mathbb Q$ a $\\omega$ mají stejnou mohutnost.")

        self.dither(2)
