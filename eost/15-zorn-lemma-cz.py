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
from topics.chat_bubbles import Conversation

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic
import importlib

class Chapter15OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 15\\\\ Ekvivalenty axiomu výběru",
    }

class Chapter15OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Axiom výběru","zjevně platí,","princip dobrého uspořádání","zjevně neplatí, a","Zornovo lemma","-- těžko říct."
        ],
        "highlighted_quote_terms" : {
            "Axiom výběru" : GREEN,
            "princip dobrého uspořádání" : ORANGE,
            "Zornovo lemma" : YELLOW_D,
        },
        "author" : "Jerry Bona"
    }

class ReminderScene(Scene):
    def construct(self):

        title = TextMobject("Formální rekurze").to_edge(UP).scale(1.2)
        title.to_edge(UP)

        ind_title = TextMobject("Indukce")
        ind_subtitle = TextMobject("$=$ důkaz sporem")
        ordinal = OrdinalOmega(x0 = -3, x1 = 3)
        pointer = TrianglePointer().scale(-1).highlight(RED)
        ind_group = VGroup(ind_title, ind_subtitle, ordinal, pointer)
        ind_group.arrange_submobjects(DOWN)
        ind_rect = SurroundingRectangle(ind_group, color = WHITE)
        ind_rect.stretch_in_place(1.2,0)
        ind_group.add(ind_rect)
        ind_group.to_corner(DOWN+RIGHT)

        unique_rules = TextMobject("Jednoznačný\\\\předpis").to_corner(LEFT+DOWN)
        axiom_of_choice = TextMobject("Axiom\\\\výběru")
        axiom_of_choice.next_to(unique_rules, UP, buff = 1.5)

        p0 = ind_title.get_edge_center(UP)
        p1 = title.get_edge_center(DOWN)
        arrow_ind = Arrow(p0,p1)

        p0 = unique_rules.get_edge_center(RIGHT)
        p1 = ind_rect.get_edge_center(LEFT)
        p1 = p0*Y_MASK + p1*X_MASK
        arrow_uniq = Arrow(p0,p1)

        p0 = axiom_of_choice.get_edge_center(DOWN)
        p1 = unique_rules.get_edge_center(UP)
        arrow_ac = Arrow(p0,p1)

        red_split = 10
        VGroup(ordinal[:red_split]).highlight(GREEN)
        VGroup(ordinal[red_split:]).highlight(RED)
        pointer.move_to(ordinal[red_split], coor_mask = X_MASK)

        everything = VGroup(
            title, ind_group,
            unique_rules, axiom_of_choice,
            arrow_ind, arrow_uniq, arrow_ac,
        )
        self.play(FadeIn(everything))

        ordinal3 = OrdinalFiniteProd(OrdinalOmega, 3, x0 = -3, x1 = 3)
        ordinal3.shift(
            ordinal[0].get_center() - ordinal3[0][0].get_center()
        )
        ordinal3_src = VGroup(ordinal3[1:]).copy()
        ordinal3_src.scale_about_point(0, ordinal3.get_edge_center(RIGHT))
        ordinal3_src.add_to_back(ordinal.copy())
        self.remove(ordinal)
        self.play(
            ReplacementTransform(ordinal3_src, ordinal3)
        )

        red_split = 3
        VGroup(ordinal3[0], ordinal3[1][:red_split]).highlight(GREEN)
        VGroup(ordinal3[2], ordinal3[1][red_split:]).highlight(RED)
        pointer_dest = pointer.copy()
        pointer_dest.move_to(ordinal3_src[1][red_split], coor_mask = X_MASK)
        self.play(Transform(pointer, pointer_dest))
        self.dither()

        ind_group.remove(ordinal)
        ind_group.add(ordinal3)

        self.play(FadeOut(everything))

color_A = RED
color_B = BLUE
shift_B = 1.5*DOWN

def make_sets_AB():
    set_A = Line(4*LEFT, 4*RIGHT, color = color_A)
    set_B = Line(4*LEFT, 4*RIGHT, color = color_B)
    set_B.shift(shift_B)

    label_A = TexMobject("A").highlight(color_A).next_to(set_A, LEFT)
    label_B = TexMobject("B").highlight(color_B).next_to(set_B, LEFT)

    return set_A, set_B, label_A, label_B

class IntroExample(Scene):
    def construct(self):

        series = VideoSeries(num_videos = 16).to_edge(UP)
        series[2].highlight(YELLOW)
        series.save_state()
        series.behind_edge(UP)
        self.play(
            series.restore
        )
        question = TextMobject("Jsou libovolné dvě množiny porovnatelné?")
        question.next_to(series, DOWN, buff = 0.6)
        question.to_edge(LEFT)
        self.play(FadeIn(question, submobject_mode = "lagged_start"))
        self.dither()

        set_A, set_B, label_A, label_B = make_sets_AB()
        label_A_ori = label_A.copy()
        label_B_ori = label_B.copy()

        self.play(FadeIn(label_A), ShowCreation(set_A))
        self.play(FadeIn(label_B), ShowCreation(set_B))

        self.dither()
        p0 = set_B.get_start()
        p1 = set_B.get_end()
        dots_B = VGroup([
            Dot(interpolate(p0,p1,alpha)).highlight(color_B)
            for alpha in np.linspace(0,1,20)
        ])

        p0 = set_A.get_start()
        p1 = set_A.get_end()
        p0, p1 = [interpolate(p0, p1, alpha) for alpha in (0.3, 0.7)]
        points_A = [
            interpolate(p0,p1,alpha)
            for alpha in np.linspace(0,1,len(dots_B))
        ]
        matching = VGroup([
            Line(p, dot.get_center())
            for p, dot in zip(points_A, dots_B)
        ])
        self.play(ShowCreation(matching, submobject_mode = "all_at_once"))
        self.remove(set_B)
        self.add(dots_B)

        self.dither()
        self.play(FadeOut(VGroup(matching)))

        #omega2 = VGroup(
        #    LimitOrdinal(lambda **kwargs: OrdinalOmega(**kwargs),
        #                 q = (0.9, 0.7, 0.8), x0 = -4, x1 = 0, height = 0.5),
        #    Dot(RIGHT),
        #    TexMobject("\\omega_1"),
        #)
        #omega2[-1].next_to(omega2[-2], UP)
        #omega2.highlight(color_A)
        #omega2.add_to_back(GradientLine(3*LEFT, 4*RIGHT, BLACK, color_A))
        omega2 = LongOrdinal(height = 0.5, color = color_A)
        omega1_dot = Dot(RIGHT).highlight(color_A)
        omega1_label = TexMobject("\\omega_1").highlight(color_A).next_to(omega1_dot, UP)
        omega2.add(omega1_dot, omega1_label)

        omega2_size = TexMobject("\\aleph_2 = |","\\omega_2","|").next_to(omega2, LEFT)
        omega2_l = omega2_size[1]
        omega2_size.remove(omega2_l)
        omega2_l.highlight(color_A)

        self.play(
            FadeOut(set_A),
            FadeIn(omega2),
            ReplacementTransform(label_A, omega2_l),
        )
        self.dither()

        reals = NumberLine(x_min = -3.9, x_max = 3.9)
        reals.add_numbers()
        reals.highlight(color_B)
        reals.shift(shift_B)

        reals_size = TexMobject("\\aleph_1 \\leq |","\\mathbb R","|")
        reals_l = reals_size[1]
        reals_size.shift(omega2_l.get_center() - reals_l.get_center())
        reals_size.shift(shift_B)
        reals_size.remove(reals_l)
        reals_l.highlight(color_B)

        self.play(
            FadeOut(dots_B),
            FadeIn(reals),
            ReplacementTransform(label_B, reals_l),
        )
        self.dither()

        self.play(Write(omega2_size))
        self.play(Write(reals_size))
        self.dither()

        inequalities = VGroup([
            TexMobject(ineq) for ineq in ("=","<",">")
        ])
        inequalities.scale(1.5)
        inequalities.rotate(-np.pi/2)
        inequalities.shift(0.5*shift_B)

        ineq = inequalities[0].copy()
        self.play(FadeIn(ineq))
        self.play(Transform(ineq, inequalities[1]))
        self.play(Transform(ineq, inequalities[2]))
        self.dither()

        self.play(
            FadeOut(VGroup(
                omega2_size,
                reals_size,
                ineq,
                omega2,
                reals,
            )),
            FadeIn(VGroup(
                set_A,
                set_B,
            )),
            ReplacementTransform(omega2_l, label_A_ori),
            ReplacementTransform(reals_l, label_B_ori),
            VGroup(
                series,
                question,
            ).behind_edge, UP,
        )
        self.dither()

class MatchingConstruction(Scene):
    def construct(self):

        set_A, set_B, label_A, label_B = make_sets_AB()
        self.add(set_A, set_B, label_A, label_B)

        ordinal_fwd = OrdinalOmega(x0=0, x1=4)
        ordinal_rev = ordinal_fwd.copy().scale(-1)
        ordinal_rev.remove(ordinal_rev[0])
        #self.add(ordinal, ordinal_rev)

        dots = VGroup([
            [
                Dot(bar.get_center()).scale_in_place(bar.get_height()/2)
                for bar in ordinal
            ]
            for ordinal in (ordinal_fwd, ordinal_rev)
        ])
        dots.highlight(color_A)

        y_B = set_B.get_start()[1]
        x0_B = set_B.get_start()[0]
        x1_B = set_B.get_end()[0]
        def random_B_point(bar):
            x0 = max(bar.get_center()[0]-1, x0_B)
            x1 = min(bar.get_center()[0]+1, x1_B)
            p0,p1 = (np.array([x,y_B,0]) for x in (x0,x1))
            return interpolate(p0, p1, np.random.random())

        np.random.random()
        matching = VGroup([
            [
                Line(bar.get_center(), random_B_point(bar)).set_stroke(width = bar.thickness)
                for bar in ordinal
            ]
            for ordinal in (ordinal_fwd, ordinal_rev)
        ])

        for i in range(5):
            self.play(ShowCreation(matching[0][i]), run_time = 0.5)
        self.play(ShowCreation(VGroup(matching[0][i+1:])))
        self.dither()
        for i in range(5):
            self.play(ShowCreation(matching[1][i]), run_time = 0.5)
        self.play(ShowCreation(VGroup(matching[1][i+1:])))
        self.remove(set_A)
        self.add(dots)
        self.dither()
        ineq = TexMobject("\\leq")
        ineq.rotate(-np.pi/2)
        ineq.move_to((label_A.get_center()+ label_B.get_center())/2)
        self.play(Write(ineq))
        self.dither()

        conversation = Conversation(self)
        anim = conversation.add_bubble_anim("A co když ani jednu množinu nikdy nevyčerpáme?")

        self.remove(dots, ineq)
        picture = VGroup(set_A, set_B, label_A, label_B, matching)
        self.play(
            picture.shift, UP,
            anim,
        )
        self.dither()

        ordinals = OrdinalClass()
        ordinals.to_edge(UP)
        ordinals_l = TexMobject("\mathbb On").next_to(ordinals, LEFT, buff = 0.5)

        self.play(FadeOut(matching))
        self.play(
            ordinals.creation_anim(),
            FadeIn(ordinals_l),
        )
        p0 = ordinals.get_corner(LEFT+DOWN)
        p0 += 0.3*(RIGHT+DOWN)
        p1 = set_A.get_corner(LEFT+UP)
        p1 += 0.3*(RIGHT+UP)
        arrows = VGroup([
            Arrow(p0 + 0.3*RIGHT*i, p1 + 1.3*RIGHT*i)
            for i in range(3)
        ])
        self.play(ShowCreation(arrows))

        def random_point(line):
            return interpolate(line.get_start(), line.get_end()+LEFT, np.random.random())

        matching = VGroup([
            Line(random_point(set_A), random_point(set_B), stroke_width = 1)
            for _ in range(200)
        ])
        self.play(ShowCreation(matching))
        self.dither()

        arrows_dest = arrows.copy()
        for arrow in arrows_dest: arrow.rotate_in_place(np.pi)
        self.play(Transform(arrows, arrows_dest, path_arc = np.pi))
        self.dither()

        rect = SurroundingRectangle(VGroup(set_A, set_B))
        self.play(ShowCreation(rect))
        rect_dest = SurroundingRectangle(ordinals)
        self.play(Transform(rect, rect_dest))

        contradiction = TextMobject("Spor").highlight(YELLOW)
        contradiction.next_to(rect, DOWN, aligned_edge = RIGHT)
        contradiction.shift(0.5*RIGHT)
        self.play(Write(contradiction))
        self.dither()

def make_zorn_lemma_box():
    chain_condition = TextMobject("Každý","řetězec\\\\","má","horní mez")
    chain_condition[1].highlight(GREEN)
    chain_condition[3].highlight(YELLOW)
    consequence = TextMobject("$\\Rightarrow$", "Maximum")
    consequence.next_to(chain_condition, DOWN)
    zorn_lemma_rect = SurroundingRectangle(VGroup(chain_condition, consequence))
    zorn_lemma_label = TextMobject("Zornovo lemma").highlight(YELLOW)
    zorn_lemma_label.next_to(zorn_lemma_rect, DOWN, aligned_edge = LEFT)
    zorn_lemma = VGroup(
        chain_condition,
        consequence,
        zorn_lemma_rect,
        zorn_lemma_label,
    )
    zorn_lemma.to_corner(UP+LEFT)

    return zorn_lemma

class MatchingPoset(Scene):
    def construct(self):

        layers_code = [
            ("---",),
            ("--3","2--","1--","-1-","-3-","-2-","--2","--1","3--"),
            ("2-3","-13","21-","1-3","-23","23-","12-","2-1","13-","-31","1-2","-12","-32","-21","31-","32-","3-2","3-1"),
            ("213","123","231","132","312","321"),
        ]
        lines_code = []
        for i in range(len(layers_code)-1):
            for j1,c1 in enumerate(layers_code[i]):
                for j2,c2 in enumerate(layers_code[i+1]):
                    for l1,l2 in zip(c1,c2):
                        if l1 not in (l2,'-'): break
                    else:
                        lines_code.append((i,j1,j2))

        layers_boxes = VGroup([
            [ self.make_matching(code) for code in layer]
            for layer in layers_code
        ])
        layers_boxes[3].arrange_submobjects(buff = 1.2)
        layers_boxes[2].arrange_submobjects(buff = 0.3)
        layers_boxes[1].arrange_submobjects(buff = 0.6)
        layers_boxes.arrange_submobjects(UP, buff = 1.5)
        #layers_boxes.to_corner(LEFT+DOWN)
        layers_boxes.to_edge(LEFT)

        lines_boxes = []
        line_buff = 0.1
        for i,j1,j2 in lines_code:
            bot = layers_boxes[i][j1]
            bot0 = bot.get_center()
            top = layers_boxes[i+1][j2]
            top0 = top.get_center()

            if top0[0] > bot0[0]: right = 1
            else: right = -1
            direction = right*RIGHT

            bot1 = bot.get_corner(UP+direction)
            top1 = top.get_corner(DOWN-direction)

            line0 = Line(bot0, top0)
            line0.scale_in_place((top1[1]-bot1[1]-2*line_buff) / line0.get_height())
            line1 = Line(bot1, top1, buff = line_buff)
            if right*(line0.get_start()[0] - line1.get_start()[0]) < 0:
                line = line0
            else: line = line1

            lines_boxes.append(line)
        lines_boxes = VGroup(lines_boxes)

        #self.add(layers_boxes, lines_boxes)
        #self.add(self.make_matching("2-1", mikro = False).to_edge(RIGHT))

        code1 = "1-2"
        code2 = "-32"
        def single_meet(l1, l2):
            if l1 != l2: return '-'
            else: return l1
        def single_join(l1, l2):
            if l1 == '-': return l2
            else: return l1

        code_meet = ''.join(single_meet(l1,l2) for l1,l2 in zip(code1, code2))
        code_join = ''.join(single_join(l1,l2) for l1,l2 in zip(code1, code2))

        box1 = self.make_matching(code1, False)
        box2 = self.make_matching(code2, False)
        box_meet = self.make_matching(code_meet, False)
        box_join = self.make_matching(code_join, False)

        boxes_mid = VGroup(box1, box2).arrange_submobjects(buff = 0.5)
        boxes = VGroup(box_meet, boxes_mid, box_join).arrange_submobjects(UP, buff = 0.8)

        y0 = box_meet.get_edge_center(UP)[1]
        y1 = boxes_mid.get_edge_center(DOWN)[1]
        y2 = boxes_mid.get_edge_center(UP)[1]
        y3 = box_join.get_edge_center(DOWN)[1]
        x0 = box1.get_center()[0]
        x1 = box_join.get_corner(LEFT+UP)[0]
        x2 = box_join.get_corner(RIGHT+UP)[0]
        x3 = box2.get_center()[0]
        x1,x2 = [interpolate(x1,x2,alpha) for alpha in 0.3, 0.7]
        lines = VGroup(
            Line(np.array([x1,y0,0]), np.array([x0,y1,0]), buff = 0.2),
            Line(np.array([x2,y0,0]), np.array([x3,y1,0]), buff = 0.2),
            Line(np.array([x0,y2,0]), np.array([x1,y3,0]), buff = 0.2),
            Line(np.array([x3,y2,0]), np.array([x2,y3,0]), buff = 0.2),
        )

        index1 = layers_code[2].index(code1)
        index2 = layers_code[2].index(code2)
        index_meet = layers_code[1].index(code_meet)
        index_join = layers_code[3].index(code_join)
        layers_boxes_src = VGroup([
            [ self.make_matching(code, False) for code in layer]
            for layer in layers_code
        ])
        for layer in layers_boxes_src:
            layer.arrange_submobjects()

        layers_boxes_src[1].shift(box_meet.get_center() - layers_boxes_src[1][index_meet].get_center())
        layers_boxes_src[3].shift(box_join.get_center() - layers_boxes_src[3][index_join].get_center())
        layers_boxes_src[0].shift(2*box_meet.get_center() - boxes_mid.get_center() - layers_boxes_src[0][0].get_center())
        VGroup(layers_boxes_src[2][:index1]).shift(box1.get_center() - layers_boxes_src[2][index1].get_center())
        VGroup(layers_boxes_src[2][index2:]).shift(box2.get_center() - layers_boxes_src[2][index2].get_center())
        for i,box in enumerate(layers_boxes_src[2][index1:index2]):
            box.move_to(interpolate(
                box1.get_center(),
                box2.get_center(),
                float(i)/(index2-index1)
            ))

        layers_boxes_src.highlight(BLACK)
        layers_boxes_src[1].submobjects[index_meet] = box_meet
        layers_boxes_src[3].submobjects[index_join] = box_join

        lines_src = []
        for i,j1,j2 in lines_code:
            if i == 1 and j1 == index_meet and j2 == index1: line = lines[0]
            elif i == 1 and j1 == index_meet and j2 == index2: line = lines[1]
            elif i == 2 and j1 == index1 and j2 == index_join: line = lines[2]
            elif i == 2 and j1 == index2 and j2 == index_join: line = lines[3]
            else:
                line = Line(
                    layers_boxes_src[i][j1].get_edge_center(UP)+0.2*UP,
                    layers_boxes_src[i+1][j2].get_edge_center(DOWN)+0.2*DOWN,
                    stroke_width = 0,
                )
            lines_src.append(line)
        lines_src = VGroup(lines_src)

        layers_boxes_src[2].remove(layers_boxes_src[2][index1], layers_boxes_src[2][index2])
        layer2_ori = list(layers_boxes[2].submobjects)
        boxes_mid_dest = VGroup(layers_boxes[2][index1], layers_boxes[2][index2])
        layers_boxes[2].remove(*boxes_mid_dest)

        line_A = Line(ORIGIN, RIGHT)
        line_A.highlight(color_A)
        line_A.move_to(box1[2])
        label_A = TexMobject("A").next_to(line_A, LEFT).highlight(color_A)
        line_B = line_A.copy()
        line_B.highlight(color_B)
        line_B.move_to(box1[3])
        label_B = TexMobject("B").next_to(line_B, LEFT).highlight(color_B)

        set_lines = VGroup(line_A, line_B)
        labels = VGroup(label_A, label_B)
        self.play(
            FadeIn(labels),
            ShowCreation(set_lines),
            submobject_mode = "lagged_start",
        )
        self.play(
            FadeOut(set_lines),
            FadeIn(VGroup(box1[2:])),
        )
        self.play(ShowCreation(box1[1]))
        self.dither()
        box1[0].set_fill(opacity = 0)
        self.play(
            ShowCreation(box1[0]),
            ShowCreation(VGroup(box_join, box2, box_meet),
                         submobject_mode = "lagged_start"),
        )
        box1[0].set_fill(opacity = 1)
        self.remove(box1)
        self.add(box1)

        self.play(ShowCreation(lines))
        self.dither()

        self.remove(labels)
        self.play(
            ReplacementTransform(lines_src, lines_boxes),
            ReplacementTransform(layers_boxes_src, layers_boxes),
            ReplacementTransform(boxes_mid, boxes_mid_dest),
            run_time = 2,
        )
        layers_boxes[2].submobjects = layer2_ori
        self.dither()

        box_min = layers_boxes[0][0]
        zoom_min = self.make_zoom(box_min, buff = 0.7)
        text_min = TextMobject("Minimum").next_to(box_min, buff = 2)
        arrow_min = Arrow(text_min, box_min)
        self.play(
            self.zoom_anim(zoom_min),
            ShowCreation(arrow_min),
            FadeIn(text_min),
        )
        self.dither()

        box_max = layers_boxes[3][-1]
        zoom_max = [
            self.make_zoom(box, buff = 0.7, side = DOWN)
            for box in layers_boxes[3]
        ]
        text_max = TextMobject("Maxima").next_to(box_max, buff = 1.5)
        arrow_max = Arrow(text_max, box_max)
        self.play(
            ShowCreation(arrow_max),
            FadeIn(text_max),
            *[self.zoom_anim(zoomed) for zoomed in zoom_max]
        )

        self.dither()
        self.play(
            FadeOut(VGroup(
                text_min, text_max,
                arrow_min, arrow_max,
            )),
            self.unzoom_anim(zoom_min),
            *[self.unzoom_anim(zoomed) for zoomed in zoom_max]
        )
        self.remove(zoom_min, *zoom_max)
        self.dither()

        layers_boxes_light = layers_boxes.copy()
        layers_boxes_black = layers_boxes.copy().highlight(BLACK)
        layers_boxes_dest = layers_boxes.copy()
        small_box = layers_boxes_dest[0][0]
        small_box.save_state()
        for sm1, sm2 in zip(layers_boxes_dest.submobject_family(), layers_boxes_black.submobject_family()):
            sm1.interpolate_color(sm2, sm1, 0.3)
        small_box.restore()

        self.play(
            Transform(layers_boxes, layers_boxes_dest),
            lines_boxes.fade, 0.7,
        )
        big_box = self.make_matching(small_box.code, mikro = False)
        big_box.move_to(small_box)
        big_box.to_edge(RIGHT)
        self.play(ReplacementTransform(small_box.copy(), big_box))
        self.dither()

        box_index = 0
        for layer_index in range(1,4):
            available = [
                j2
                for i,j1,j2 in lines_code
                if i == layer_index-1 and j1 == box_index
            ]
            last_box_index = box_index
            box_index = random.choice(available)
            line_index = lines_code.index((layer_index-1, last_box_index, box_index))
            small_box = layers_boxes[layer_index][box_index]
            big_box_dest = big_box.copy().move_to(small_box, coor_mask = Y_MASK)
            line = lines_boxes[line_index].copy()
            self.add(line)
            lines_boxes[line_index].highlight(WHITE)
            self.play(
                Transform(small_box, layers_boxes_light[layer_index][box_index]),
                Transform(big_box, big_box_dest),
                ShowCreation(lines_boxes[line_index])
            )
            self.remove(line)

            self.remove(big_box)
            big_box = self.make_matching(small_box.code, mikro = False)
            big_box.move_to(small_box).to_edge(RIGHT)
            self.add(big_box)
            last_code = layers_code[layer_index-1][last_box_index]
            code = layers_code[layer_index][box_index]
            mline_index = 0
            for c1,c2 in zip(last_code, code):
                if c2 == '-': continue
                if c1 == '-': break
                mline_index += 1

            mline = big_box[1][mline_index]
            self.remove(mline)
            self.play(ShowCreation(mline))

        self.dither()
        self.play(FadeOut(big_box))

        layers_dots = VGroup([
            [Dot(color = GREEN) for code in layer]
            for layer in layers_code
        ])
        layers_dots[3].arrange_submobjects(buff = 1.2)
        layers_dots[2].arrange_submobjects(buff = 0.3)
        layers_dots[1].arrange_submobjects(buff = 0.6)
        layers_dots.arrange_submobjects(UP, buff = 1.5)

        lines_dots = []
        for i,j1,j2 in lines_code:
            lines_dots.append(Line(
                layers_dots[i][j1].get_center(),
                layers_dots[i+1][j2].get_center(),
                buff = 0.2,
            ))
        lines_dots = VGroup(lines_dots)

        light_lines_boxes = []
        light_lines_dots = []
        for line_box, line_dot in zip(lines_boxes, lines_dots):
            line_dot.highlight(rgb_to_color(line_box.stroke_rgb))
            if line_box.stroke_rgb[0] == 1:
                light_lines_boxes.append(line_box)
                light_lines_dots.append(line_dot)

        lines_boxes.remove(*light_lines_boxes)
        lines_boxes.add(*light_lines_boxes)
        lines_dots.remove(*light_lines_dots)
        lines_dots.add(*light_lines_dots)

        for layer_boxes, layer_dots in zip(layers_boxes, layers_dots):
            for box, dot in zip(layer_boxes, layer_dots):
                dot.highlight(rgb_to_color(box[0].stroke_rgb))

        self.dither()

        VGroup(lines_dots, layers_dots).move_to(layers_boxes)
        self.play(
            ReplacementTransform(lines_boxes, lines_dots),
            ReplacementTransform(layers_boxes, layers_dots),
            run_time = 2,
        )
        self.dither()
        poset = VGroup(layers_dots, lines_dots)
        self.play(poset.shift, 4*DOWN)
        self.dither()

        last_dot = layers_dots[-1][box_index]
        quotient = 0.8
        dy = 0.6
        min_x = -1
        max_x = 0.2
        buff = 0.2
        sw_quotient = 0.9
        stroke_width = DEFAULT_POINT_THICKNESS

        seq_dots = []
        seq_lines = []
        seq = []
        for _ in range(50):
            dot = last_dot.copy()
            dot.scale_in_place(quotient)
            dot.shift(dy*UP + RIGHT*interpolate(min_x, max_x, np.random.random()))
            line = Line(
                last_dot,
                dot,
                buff = buff,
                stroke_width = stroke_width,
            )
            seq += [line, dot]
            seq_lines.append(line)
            seq_dots.append(dot)
            dy *= quotient
            min_x *= quotient
            max_x *= quotient
            buff *= quotient
            stroke_width *= sw_quotient
            last_dot = dot

        seq = VGroup(seq)
        self.play(ShowCreation(seq))
        self.dither()

        zorn_lemma = make_zorn_lemma_box()
        chain_condition, consequence, zorn_lemma_rect, zorn_lemma_label = zorn_lemma
        self.play(Write(chain_condition))
        self.dither()

        chains = VGroup([self.make_abstract_chain() for i in range(5)])
        chains.arrange_submobjects(buff = 0.5)
        chains.shift(VGroup(seq_dots[-1], layers_dots[3][0]).get_corner(UP+LEFT)
                     - chains.get_corner(UP+LEFT))

        self.play(ShowCreation(
            chains,
            submobject_mode = "lagged_start",
            run_time = 2,
        ))
        self.dither()
        upper_bounds = VGroup([
            Dot(chain.get_start(), color = YELLOW)
            for chain in chains
        ])
        for i, dot in enumerate(upper_bounds[2:]):
            dot.shift(0.2*(2-i)*UP)
        upper_bounds.save_state()
        upper_bounds.shift(0.5*UP)
        upper_bounds.set_fill(opacity = 0)
        self.play(
            upper_bounds.restore,
            submobject_mode = "lagged_start",
            run_time = 2,
        )
        self.dither()

        ordinal = LongOrdinal(
            height = 0.5,
            color = GREEN,
            x0 = -2, x1 = 2,
        )
        for subord in ordinal[1]: subord[0].highlight(YELLOW)
        ordinal.rotate(np.pi/2)
        ordinal.next_to(seq_dots[-1], UP)
        first_bar = ordinal[1][0][0]
        ordinal[1][0].remove(first_bar)
        limit_dot = Dot(first_bar.get_center(), color = YELLOW)
        self.play(ShowCreation(first_bar), FadeIn(limit_dot))
        self.dither()

        shift = DOWN*ordinal.get_height()
        ordinal.shift(shift)
        picture = VGroup(
            poset, seq, chains, upper_bounds, first_bar, limit_dot
        )
        self.play(picture.shift, shift)
        self.remove(poset)
        picture.remove(poset)
        self.add_foreground_mobjects(limit_dot)
        self.play(
            ordinal.creation_anim()
        )
        self.dither()
        maximum_dot = Dot(ordinal.get_edge_center(UP), color = GREEN)
        maximum_l = TextMobject("Maximum")
        maximum_l.next_to(maximum_dot, UP, aligned_edge = LEFT)
        self.play(
            GrowFromCenter(maximum_dot),
            FadeIn(maximum_l, submobject_mode = "lagged_start"),
        )
        self.play(
            ReplacementTransform(maximum_l.copy(), consequence[1]),
            FadeIn(consequence[0]),
        )
        self.play(
            ShowCreation(zorn_lemma_rect),
            Write(zorn_lemma_label),
        )
        self.dither()
        picture.add_to_back(ordinal)
        picture.add(maximum_dot, maximum_l)
        self.play(FadeOut(picture))

    def make_matching(self, code, mikro = True):

        w = 0.3
        h = 0.3
        set_A = VGroup([
            Dot(interpolate(w*LEFT, w*RIGHT, alpha)) for alpha in (0,0.5,1)
        ])
        set_B = set_A.copy()
        set_A.shift(h*UP)
        set_B.shift(h*DOWN)
        set_A.highlight(color_A)
        set_B.highlight(color_B)

        if mikro: line_buff = 0.1
        else: line_buff = 0.15
        matching = []
        for a,c in enumerate(code):
            if c == '-': continue
            b = int(c)-1
            matching.append(Line(
                set_A[a].get_center(),
                set_B[b].get_center(),
                buff = line_buff,
            ))

        matching = VGroup(matching)
        result = VGroup(
            matching, set_A, set_B, 
        )
        if len(matching) == 0: result.remove(matching)
        result.code = code

        kwargs = {"stroke_color": GREEN, "fill_color": BLACK, "fill_opacity": 1}
        if mikro:
            result.scale(0.3)
            matching.set_stroke(width = 0.3*DEFAULT_POINT_THICKNESS)
            kwargs["buff"] = 0.05

        result.add_to_back(SurroundingRectangle(result, **kwargs))

        return result

    def make_abstract_chain(self, length = 5, osc1 = 0.5, osc2 = 0.5, midpoints = 2, color = GREEN):
        points = []
        y_seq = np.linspace(length, 0, 3*(midpoints+2))
        for i in range(0,len(y_seq),3):
            y1,y2,y3 = y_seq[i:i+3]
            x = interpolate(-osc1, osc1, np.random.random())
            x2 = interpolate(-osc2, osc2, np.random.random())
            points += [[x-x2,y1,0],[x,y2,0],[x+x2,y3,0]]

        points = np.array(points[1:-1])
        chain = Line(UP, DOWN, color = color)
        chain.points = points

        return chain

    def make_zoom(self, box, side = UP, buff = 0.5):

        side2 = np.array([side[1], side[0], 0])
        zoomed = self.make_matching(box.code, mikro = False)
        zoomed.next_to(box, side, buff = buff)

        lines = [
            Line(box.get_corner(x-side), zoomed.get_corner(x-side),
                 color = GREEN, stroke_width = 0.6*DEFAULT_POINT_THICKNESS)
            for x in (side2, -side2)
        ]
        bg = Polygon(
            lines[0].get_start(), lines[0].get_end(),
            lines[1].get_end(), lines[1].get_start(),
            stroke_width = 0,
            color = BLACK,
            fill_opacity = 0.6,
        )
        return VGroup(bg, box.copy(), zoomed, lines)
    
    def play_zoom(self, zoomed):
        self.play(self.zoom_anim(zoomed))

    def zoom_anim(self, zoomed):
        bg, small_box, big_box, lines = zoomed
        bg_src = Polygon(
            lines[0].get_start(), lines[0].get_start(),
            lines[1].get_start(), lines[1].get_start(),
            stroke_width = 0,
            color = BLACK,
            fill_opacity = 0.6,
        )
        return AnimationGroup(
            ReplacementTransform(bg_src, bg),
            ShowCreation(lines, submobject_mode = "all_at_once"),
            ReplacementTransform(small_box.copy(), big_box),
        )

    def play_unzoom(self, zoomed):
        self.play(self.unzoom_anim(zoomed))
        self.remove(zoomed)

    def unzoom_anim(self, zoomed):
        bg, small_box, big_box, lines = zoomed
        bg_dest = Polygon(
            lines[0].get_start(), lines[0].get_start(),
            lines[1].get_start(), lines[1].get_start(),
            stroke_width = 0,
            color = BLACK,
            fill_opacity = 0.6,
        )
        return AnimationGroup(
            Transform(bg, bg_dest),
            Uncreate(lines, submobject_mode = "all_at_once"),
            Transform(big_box, small_box),
        )

class ZornLemmaExample1(Scene):
    def construct(self):

        zorn_lemma = make_zorn_lemma_box()

        sets_AB = VGroup(make_sets_AB())
        set_A, set_B, label_A, label_B = sets_AB
        sets_AB.remove(set_A)
        ordinal_fwd = OrdinalOmega(x0=0, x1=4)
        ordinal_rev = ordinal_fwd.copy().scale(-1)
        ordinal_rev.remove(ordinal_rev[0])
        sets_AB.add(ordinal_fwd, ordinal_rev)
        sets_AB.shift(DOWN)
        sets_AB.remove(ordinal_fwd, ordinal_rev)

        dots = [
            [
                Dot(bar.get_center()).scale_in_place(bar.get_height()/2)
                for bar in ordinal
            ]
            for ordinal in (ordinal_fwd, ordinal_rev)
        ]
        dots_A = VGroup(dots[0]+dots[1])
        dots_A.highlight(color_A)
        dots_A.submobjects.sort(key = lambda mob: mob.get_center()[0])

        y_B = set_B.get_start()[1]
        x0_B = set_B.get_start()[0]
        x1_B = set_B.get_end()[0]
        def random_B_point(bar):
            x0 = max(bar.get_center()[0]-1, x0_B)
            x1 = min(bar.get_center()[0]+1, x1_B)
            p0,p1 = (np.array([x,y_B,0]) for x in (x0,x1))
            return interpolate(p0, p1, np.random.random())

        np.random.random()
        matching = VGroup([
            [
                Line(bar.get_center(), random_B_point(bar)).set_stroke(width = bar.thickness)
                for bar in ordinal
            ]
            for ordinal in (ordinal_fwd, ordinal_rev)
        ])
        sets_AB.add_to_back(matching)
        sets_AB.add(dots_A)

        self.add(zorn_lemma)

        self.play(
            FadeIn(label_A),
            FadeIn(label_B),
            ShowCreation(dots_A, rate_func = None),
            ShowCreation(set_B),
        )
        self.add_foreground_mobjects(dots_A, set_B)
        self.play(ShowCreation(VGroup(matching[0][:5]), submobject_mode = "all_at_once"))
        self.dither()

        self.play(ShowCreation(VGroup(matching[0][5:], matching[1]), submobject_mode = "all_at_once"))

        rect = SurroundingRectangle(VGroup(dots_A, set_B), color = GREEN)
        maximum_l_src = zorn_lemma[1][1]
        maximum_l = maximum_l_src.copy().next_to(rect, UP)
        arrow_conseq = Arrow(maximum_l_src, maximum_l)
        self.play(
            ReplacementTransform(maximum_l_src.copy(), maximum_l),
            ShowCreation(arrow_conseq),
            FadeIn(rect),
        )
        self.dither()

        condition = zorn_lemma[0][1]
        to_verify = TextMobject("Ověřit").move_to(condition).move_to(ORIGIN, coor_mask = X_MASK)
        arrow_cond = Arrow(to_verify, condition)
        self.play(
            FadeIn(to_verify),
            ShowCreation(arrow_cond),
        )
        self.dither()

        self.play(FadeOut(VGroup(sets_AB, rect, arrow_conseq, maximum_l)))
        self.mini_sets = VGroup(matching[0], dots, set_B).scale(0.5)

        self.chain = Line(ORIGIN, 5*DOWN, color = GREEN).to_corner(RIGHT+DOWN)
        self.add(self.chain)

        dots = VGroup([self.make_chain_dot(i) for i in range(20)])

        index1 = 3
        index2 = 8
        dot1 = self.make_chain_dot(index1)
        matching1 = self.make_partial(index1)
        dot2 = self.make_chain_dot(index2)
        matching2 = self.make_partial(index2)

        self.play(
            FadeIn(matching1),
            FadeIn(matching2),
            Write(dot1),
            Write(dot2),
        )

        matching1.save_state()
        matching2.save_state()
        dest_point = (matching1.get_center() + matching2.get_center())/2 + LEFT
        self.play(
            matching1.move_to, dest_point,
            matching2.move_to, dest_point,
        )
        self.dither()
        self.play(
            matching1.restore,
            matching2.restore,
        )
        dot_union = Dot(self.chain.get_start(), color = YELLOW)
        sets_union = self.mini_sets.copy().next_to(dot_union, LEFT)
        indices = list(range(len(self.mini_sets[0])))
        indices.remove(index1)
        indices.remove(index2)
        chain_dots = VGroup([
            self.make_chain_dot(i).set_fill(opacity = 0.0)
            for i in indices
        ])
        matchings = []
        matchings_dest = []
        last_y = 100
        dest = sets_union[0][0].get_center()
        for index, dot in reversed(zip(indices, chain_dots)):
            y = dot.get_center()[1]
            if last_y-y >= 0.15:
                dot.set_fill(opacity = 0.3)
                if index == 0: break
                matching = self.make_partial(index)
                #matchings_dest.append(matching.copy().shift(dest - matching[0].get_center()))
                matchings_dest.append(matching.copy().next_to(dot_union, LEFT))
                matching.highlight(BLACK)
                matchings.append(matching)
                last_y = y

        matchings = VGroup(matchings)
        matchings_dest = VGroup(matchings_dest)

        self.play(
            Transform(chain_dots, VGroup(dot_union)),
            Transform(matchings, matchings_dest),
            Transform(dot1, dot_union),
            Transform(dot2, dot_union),
            matching1.next_to, dot_union, LEFT,
            matching2.next_to, dot_union, LEFT,
            run_time = 2,
        )
        self.remove(chain_dots, matchings, dot1, matching1, dot2, matching2)
        self.add(dot_union, sets_union)
        self.dither()

        dot_A = sets_union[1][1][3]
        r = 0.3
        center = dot_A.get_center()*X_MASK + sets_union[2].get_center()*Y_MASK
        points = [center+r*d for d in (LEFT, RIGHT)]
        self.add_foreground_mobjects(dot_A, sets_union[2])
        wrong_lines = VGroup([
            Line(dot_A.get_center(), p1, color = YELLOW) for p1 in points
        ])
        for line in wrong_lines:
            self.play(ShowCreation(line))
        wrong_lines_copy = wrong_lines.copy()
        self.add(wrong_lines_copy, dot_A, sets_union[2])

        wrong_lines = VGroup([
            VGroup(
                line,
                dot_A.copy(),
                dot_A.copy().move_to(line.get_end()).highlight(color_B),
            )
            for line in wrong_lines
        ])
        y_shifts = [2.5, 4]
        chain_dots = [
            dot_union.copy().highlight(WHITE).shift(DOWN*y_shift)
            for y_shift in y_shifts
        ]
        for line, dot, y_shift in zip(wrong_lines, chain_dots, y_shifts):
            self.play(
                line.shift, DOWN*y_shift,
                ReplacementTransform(dot_union.copy(), dot),
            )
        self.dither()
        wrong_lines_copy2 = wrong_lines.copy()
        self.add(wrong_lines_copy2)

        wrong_lines_dest = wrong_lines.copy()
        for line, d in zip(wrong_lines_dest, (DOWN, UP)):
            line.shift(d*(y_shifts[1]-y_shifts[0])/2 + LEFT)

        self.play(Transform(wrong_lines, wrong_lines_dest))
        self.dither()
        self.play(FadeOut(VGroup(
            wrong_lines, wrong_lines_copy, wrong_lines_copy2,
            chain_dots,
            dot_union, sets_union,
            arrow_cond, to_verify,
            self.chain,
        )))

    def make_chain_dot(self, index):

        source = self.mini_sets[1][0]
        pos0 = source.get_edge_center(LEFT)[0]
        pos1 = source.get_edge_center(RIGHT)[0]
        pos_dot = source[index].get_center()[0]

        alpha = (pos_dot - pos0) / (pos1 - pos0)
        return Dot(interpolate(self.chain.get_end(), self.chain.get_start(), alpha))

    def make_partial(self, index):

        result = self.mini_sets.copy()
        result[0].submobjects = result[0].submobjects[:index]
        result.next_to(self.make_chain_dot(index), LEFT)

        return result

class ZornLemmaGeneralUsage(Scene):

    def construct(self):
        zorn_lemma = make_zorn_lemma_box()
        self.add(zorn_lemma)

        part_label = TextMobject("Částečná\\\\řešení")
        part_label.highlight(GREEN)
        part1 = Line(2*DOWN, UP+2*RIGHT, color = GREEN)
        part1.points[2][0] = part1.points[3][0]
        part1.points[1][0] += 1
        part1.shift(0.2*UP)
        part2 = part1.copy().stretch(-1,0)

        p0 = part2.get_end()
        p1 = part1.get_end()
        dots_sol = VGroup([
            Dot(interpolate(p0, p1, alpha), color=  YELLOW)
            for alpha in np.linspace(0,1,15)
        ])
        label_sol = TextMobject("Řešení")
        label_sol.highlight(YELLOW)
        label_sol.next_to(dots_sol, UP)
        poset = VGroup(
            part_label, part1, part2,
            dots_sol, label_sol,
        )
        poset.shift(UP)

        self.play(
            FadeIn(part_label),
            ShowCreation(part1),
            ShowCreation(part2),
        )
        self.play(
            FadeIn(dots_sol),
            FadeIn(label_sol, submobject_mode = "lagged_start"),
        )

        ordinal = OrdinalOmega(x0 = -2, x1 = 3)
        chain = Line(RIGHT*ordinal.x1, RIGHT*ordinal.x0, color = GREEN)
        dots_chain = VGroup([
            Dot(bar.get_center(), fill_opacity = 0)
            for bar in ordinal
        ])
        chain_g = VGroup(chain, dots_chain)
        chain_g.rotate(np.pi/2)
        chain_g.to_edge(RIGHT)

        self.play(ShowCreation(chain))

        dots_compatible = VGroup(dots_chain[4:13:3])
        dots_compatible.set_fill(opacity = 1)
        self.play(ShowCreation(dots_compatible))
        comp_label = TextMobject("Kompatibilita").next_to(dots_compatible, LEFT)
        dot_center = Dot((dots_compatible[0].get_center() + dots_compatible[-1].get_center())/2)
        dots_compatible.save_state()
        self.play(
            Transform(dots_compatible, VGroup(dot_center)),
            FadeIn(comp_label),
        )
        self.play(dots_compatible.restore)
        self.dither()

        dot_union = Dot(chain.get_start(), color = YELLOW)
        label_union = TextMobject("Sjednocení")
        label_union.highlight(YELLOW)
        label_union.next_to(dot_union, LEFT)

        label_union_src = VGroup([
            label_union.copy().next_to(dot, LEFT).set_fill(opacity = 0)
            for dot in dots_chain
        ])
        self.play(
            Transform(label_union_src, VGroup(label_union)), 
            Transform(dots_chain, VGroup(dot_union)),
            run_time = 1,
        )
        self.remove(label_union_src, dots_chain)
        self.add(label_union, dot_union)
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("V čem je to jednodušší než přímo použít rekurzi?")
        conversation.add_bubble("Není třeba znát teorii množin.")
        self.dither()

class HowMathWorks(Scene):

    def construct(self):
        stickman = SVGMobject(
            file_name = "seminar-trailer/stickman",
        ).scale(0.007).highlight(WHITE)
        cloud = SVGMobject(file_name = "seminar-trailer/cloud")

        ordinal = OrdinalFiniteProd(OrdinalOmega, 3, x0 = -1.5, x1 = 1.5, height = 0.5)
        for subord in ordinal: subord[0].highlight(YELLOW)
        ordinal[0][0].highlight(GREEN)

        impl = TexMobject("\\Rightarrow").next_to(ordinal, DOWN)
        zorn_lemma = TextMobject("Zornovo lemma").next_to(impl, DOWN)
        set_theory = VGroup(ordinal, impl, zorn_lemma)
        set_theory.move_to(cloud)
        set_theory.scale(0.8)
        cloud.scale(set_theory.get_width() / cloud.get_width() * 1.3)
        set_theory.shift(0.1*UP)
        cloud = VGroup(
            cloud,
            set_theory,
        )
        cloud.to_corner(UP+LEFT, buff = 1)
        stickman.next_to(cloud, DOWN)

        stickman.save_state()
        stickman.behind_edge(DOWN)
        self.play(
            FadeIn(cloud),
            stickman.restore,
        )

        self.dither()

        colors = [BLUE, PURPLE, ORANGE]
        consequences = ["báze vektorového\\\\prostoru", "netriviální\\\\ultrafiltr", "kostra grafu"]
        boxes = VGroup([
            VGroup(
                zorn_lemma.copy(),
                impl.copy().highlight(color),
                TextMobject(conseq).highlight(color),
                stickman.copy().highlight(color),
            ).arrange_submobjects(DOWN).scale(0.8)
            for conseq, color in zip(consequences, colors)
        ])
        box0, box1, box2 = boxes
        box2.to_corner(UP+RIGHT).shift(0.5*DOWN)
        box1.to_edge(UP)
        box0.move_to((box1.get_center() + box2.get_center())/2)
        box0.shift(1.5*DOWN)

        self.play(ReplacementTransform(
            VGroup(zorn_lemma.copy()),
            VGroup([box[0] for box in boxes]),
        ))
        self.dither()

        self.appear_box(box1)
        self.appear_box(box2)
        self.appear_box(box0)
        self.dither()

    def appear_box(self, box):
        stickman = box[-1]
        stickman.save_state()
        stickman.highlight(BLACK)
        stickman.shift(DOWN)
        self.play(
            stickman.restore,
            FadeIn(VGroup(box[1:-1])),
        )

class ZornLemmaToAC(Scene):

    def construct(self):

        self.force_skipping()
        
        title = TextMobject("Axiom výběru").to_corner(LEFT+UP)
        self.add(title)

        lines = OrdinalOmega(x0=0, x1 = 2.5, height = 1.5)
        lines = VGroup(lines.family_members_with_points())
        lines.rotate(-np.pi/2)
        lines.highlight(BLUE)
        lines.center().shift(UP)
        self.play(FadeIn(lines))

        choice = self.make_choice(lines)
        connections, dots = choice
        dots.save_state()
        for dot, line in zip(dots, lines):
            dot.move_to(line.get_end())
            dot.set_fill(opacity = 0)

        self.dither()
        self.play(dots.restore, run_time = 1.5)
        self.dither()
        self.play(ShowCreation(connections), run_time = 2)
        self.dither()

        partial = VGroup(
            lines.copy(),
            dots[:4],
            connections[:4],
        ).copy()
        partial.save_state()
        partial.to_edge(DOWN)
        partial.shift(UP+4*LEFT)
        partial_l = TextMobject("Částečné\\\\výběry")
        partial_l.next_to(lines, DOWN, buff = 0.5)

        poset_line = Line(
            lines.get_edge_center(LEFT),
            partial[0].get_corner(UP+RIGHT) + (UP+RIGHT)*0.2
        )
        self.play(
            MoveFromSaved(partial),
            ShowCreation(poset_line),
            FadeIn(partial_l),
        )
        self.add(partial)
        self.add(poset_line)
        self.dither()

        maximum_l = TextMobject("Maxima")
        maximum_l.next_to(connections, UP)
        maximum_l.highlight(YELLOW)
        self.play(FadeIn(maximum_l, submobject_mode = "lagged_start"))
        self.dither()

        chain = Line(1.7*UP, 2*DOWN, color = GREEN).to_edge(RIGHT)
        chain_choice = self.make_choice(lines)
        chain_choice = VGroup(chain_choice[0][3:], chain_choice[1][2:])
        chain_dot = Dot(chain.get_end()+0.5*UP)
        chain_preview = VGroup(lines.copy(), chain_choice)
        chain_preview.next_to(chain_dot, LEFT)
        chain_preview.shift(DOWN)
        chain_obj = VGroup(chain_preview, chain_dot)

        for conn in chain_choice[0]:
            conn.ori_stroke_width = conn.stroke_width

        def update_choice(chain_choice):
            connections, dots = chain_choice
            alpha = chain_dot.get_center()[1] - chain.get_start()[1]
            alpha /= chain.get_end()[1] - chain.get_start()[1]
            if alpha <= 0: index = len(dots)
            else:
                index = int(np.log(alpha) / np.log(0.9))
                if index < 0: index = 0

            dots.set_fill(opacity = 0)
            VGroup(dots[:index+1]).set_fill(opacity = 1)
            for i, conn in enumerate(connections):
                if i < index: conn.set_stroke(width = conn.ori_stroke_width)
                else: conn.set_stroke(width = 0)

        self.revert_to_original_skipping_status()
        self.play(ShowCreation(chain))
        update_choice(chain_choice)
        chain_obj.save_state()
        chain_obj.shift(chain.get_end() - chain_dot.get_center())
        chain_preview.highlight(BLACK)
        self.play(chain_obj.restore)
        self.dither()
        for _ in range(2):
            self.play(
                chain_obj.shift, UP,
                UpdateFromFunc(chain_choice, update_choice),
            )
            self.dither(0.5)

        union_l = TextMobject("Sjednocení").next_to(chain_preview, UP)
        union_l.highlight(YELLOW)
        union_l.set_fill(opacity = 0)
        chain_obj.add(union_l)
        chain_obj.save_state()
        chain_obj.shift(chain.get_start() - chain_dot.get_center())
        chain_dot.highlight(YELLOW)
        union_l.set_fill(opacity = 1)
        self.play(
            MoveFromSaved(chain_obj),
            UpdateFromFunc(chain_choice, update_choice),
            run_time = 1.5,
        )
        self.dither()

    def make_choice(self, lines, dotq = 0.3):

        p0 = 2*lines[0].get_center() - lines[1].get_center()
        dots, connections = [], []
        for line in lines:
            p1 = interpolate(line.get_start(), line.get_end(), np.random.random())
            connections.append(Line(
                p0, p1,
                color = YELLOW,
                stroke_width = line.stroke_width
            ))
            dots.append(
                Dot(p1, color = YELLOW).scale_in_place(line.get_width()*dotq)
            )
            p0 = p1

        return VGroup(connections, dots)

class WellOrderingPrinciple(Scene):

    def construct(self):

        AC_title = TextMobject("Axiom výběru")
        zorn_title = TextMobject("Zornovo lemma")
        WOP_title = TextMobject("Princip dobrého uspořádání")
        equivalents = VGroup(WOP_title, zorn_title)
        equivalents.arrange_submobjects(DOWN, buff = 1.5, aligned_edge = LEFT)
        VGroup(AC_title, equivalents).arrange_submobjects(buff = 2)
        arrow_zorn = DoubleArrow(AC_title, zorn_title)
        arrow_WOP = DoubleArrow(AC_title, WOP_title)

        AC_title.save_state()
        AC_title.to_corner(UP+LEFT)
        self.add(zorn_title)
        self.play(AC_title.restore)

        self.play(ShowCreation(arrow_zorn))
        self.dither()
        self.play(
            ShowCreation(arrow_WOP),
            Write(WOP_title),
        )
        self.dither()

        WOP_title.save_state()
        WOP_title.center()
        WOP_title.scale(1.2)
        WOP_title.to_edge(UP)

        self.play(
            MoveFromSaved(WOP_title),
            FadeOut(VGroup(
                AC_title, zorn_title,
                arrow_WOP, arrow_zorn,
            ))
        )
        self.dither()

        reals = NumberLine()
        self.play(ShowCreation(reals))

        ordinals = OrdinalClass(x0 = -6, x1 = 6).to_edge(DOWN)
        self.play(
            ordinals.creation_anim()
        )

        ori_bars = ordinals[1].family_members_with_points()
        bars = VGroup(ori_bars).copy().highlight(BLUE).submobjects

        ordinal_line_cut = 0.9

        start = ordinals[0].get_start()
        end = ordinals[0].get_end()
        end = interpolate(start, end, ordinal_line_cut)
        dest_line = GradientLine(
            start, end,
            BLACK, BLUE,
        )
        gradient_segments = dest_line.family_members_with_points()

        reals.remove(reals.main_line)
        self.remove(reals.main_line)
        reals.main_line = GradientLine(
            reals.main_line.get_start(), reals.main_line.get_end(),
            reals.color, reals.color,
            segment_num = len(bars)+len(gradient_segments) - len(reals.tick_marks)
        )
        reals.add_to_back(reals.main_line)
        self.add(reals.main_line)

        for bar in bars: bar.priority = 100
        for segment in gradient_segments: segment.priority = 0

        ordinal_points = sorted(bars+gradient_segments, key = lambda mob: mob.get_center()[0])
        real_points = reals.family_members_with_points()
        random.shuffle(real_points)

        begin = 3
        for real_point, ordinal_point in zip(real_points[:begin], ordinal_points[:begin]):
            self.play(Transform(real_point, ordinal_point))

        for real_point, dest in zip(real_points, ordinal_points):
            real_point.priority = dest.priority + np.sum(dest.stroke_rgb)
        for bar in ori_bars:
            bar.priority = 50

        def order_f(mob):
            if hasattr(mob, "priority"):
                return mob.priority
            return -1

        to_fade_line = VGroup([
            line
            for line in ordinals[0]
            if line.get_end()[0] <= dest_line.get_end()[0]
        ])
        self.play(
            Animation(VGroup(ori_bars)),
            Animation(VGroup(bars[:begin])),
            Transform(
                VGroup(real_points[begin:]),
                VGroup(ordinal_points[begin:]),
                run_time = 3,
                submobject_mode = "lagged_start",
            ),
            order_f = order_f,
        )
        self.dither()

        well_ordered = BraceText(real_points, "Dobře uspořádané", UP)
        self.play(well_ordered.creation_anim())

        self.dither()
        self.play(FadeOut(well_ordered))

        comparability = TextMobject("Porovnatelnost množin")
        VGroup(comparability, AC_title).arrange_submobjects(buff = 2.5).shift(UP)

        arrow_comp = Arrow(
            WOP_title.get_corner(LEFT+DOWN),
            comparability.get_corner(LEFT+UP)
        ).shift(comparability.get_width()/2 * RIGHT)

        arrow_AC = Arrow(
            WOP_title.get_corner(RIGHT+DOWN),
            AC_title.get_corner(RIGHT+UP)
        ).shift(AC_title.get_width()/2 * LEFT)

        self.play(ShowCreation(arrow_comp), FadeIn(comparability))
        self.dither()
        self.play(ShowCreation(arrow_AC), FadeIn(AC_title))
        
        hint_comp = TextMobject("(Kapitola 5)").next_to(comparability, DOWN)
        self.play(FadeIn(hint_comp, submobject_mode = "lagged_start"))

        omega2 = OrdinalFiniteProd(OrdinalOmega, 2, x0 = -2, x1 = 2, height = 0.7)
        omega2.next_to(AC_title, DOWN)
        omega2.highlight(DARK_GREY)
        
        self.play(FadeIn(omega2))
        index_first = 3
        for bar in omega2[1][index_first+1:]:
            if np.random.random() < 0.4: bar.highlight(WHITE)

        bar = omega2[1][index_first]
        bar.highlight(WHITE)
        bar = bar.copy().highlight(YELLOW)

        pointer = TrianglePointer().scale(-1)
        pointer.highlight(YELLOW)
        pointer.next_to(bar, DOWN)
        pointer.save_state()
        pointer.next_to(omega2[0][0], DOWN)
        pointer.set_fill(opacity = 0)
        self.play(
            ShowCreation(bar),
            pointer.restore,
        )

        self.dither()
        self.remove(bar)
        omega2.highlight(DARK_GREY)
        
        index_first = 6
        for bar in omega2[0][index_first+1:]:
            if np.random.random() < 0.4: bar.highlight(WHITE)
        for bar in omega2[1]:
            if np.random.random() < 0.4: bar.highlight(WHITE)

        bar = omega2[0][index_first]
        bar.highlight(WHITE)
        bar = bar.copy().highlight(YELLOW)

        self.play(
            pointer.next_to, omega2[0][index_first], DOWN,
            ShowCreation(bar),
        )
        self.dither()

