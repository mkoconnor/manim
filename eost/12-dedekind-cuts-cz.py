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
