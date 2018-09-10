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
from topics.chat_bubbles import Conversation, ChatBubble

import random
from eost.ordinal import *
from topics.number_line import NumberLine
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.icons import MirekOlsakLogo, TrianglePointer, IconYes, IconNo
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic

import importlib

class Chapter9OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 9\\\\Axiomy",
    }

class Chapter9OpeningQuote(Scene):
    def construct(self):
        quote = [
            "Na počátku bylo","slovo,\\\\",
            "a to slovo bylo od","Matematika,\\\\",
            "a to slovo bylo:","\\uv{množina}.",
        ]
        quote = TextMobject(
            *quote,
            alignment="\\raggedright"
        )
        quote.to_edge(UP)
        quote[1].highlight(GREEN)
        quote[3].highlight(GREEN)
        quote[5].highlight(YELLOW)
        for i in range(3):
            self.play(FadeIn(
                VGroup(quote[2*i:2*(i+1)]),
                run_time = 2,
                rate_func = None,
                submobject_mode = "lagged_start",
            ))
            self.dither()

        self.dither(2)

def dot_r_comp(*args, **kwargs):
    dot = Dot(*args, **kwargs)
    dot.stretch_in_place(-1, 0)
    dot.rotate_in_place(-np.pi/4)
    return dot

def hide_arrows(arrows):
    arrows.save_state()
    for arrow in arrows:
        arrow.set_stroke(width = 0)
        arrow.scale_about_point(0, np.array(arrow.get_start()))

class ReminderScene(Scene):
    def construct(self):

        title = TextMobject("Formální svět množin").to_edge(UP)
        edge_buff = DEFAULT_MOBJECT_TO_EDGE_BUFFER
        title_buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        width = 2*(SPACE_WIDTH-edge_buff)
        rect_top = title.get_edge_center(DOWN) + title_buff*DOWN
        rect_bot = SPACE_HEIGHT*DOWN + edge_buff*UP
        height = (rect_top - rect_bot)[1]
        world_rect = Rectangle(width = width, height = height)
        world_rect.move_to((rect_top+rect_bot)/2)

        self.play(ShowCreation(world_rect))
        self.play(FadeIn(title, submobject_mode = "lagged_start"))

        squares = VGroup([Square(side_length = 0.3) for _ in range(3)])
        squares.arrange_submobjects(buff = 1)
        set_rect = SurroundingRectangle(squares, buff = 0.5)

        self.dither()
        self.play(ShowCreation(set_rect))
        self.play(ShowCreation(squares))

        self.dither()

        dashed_rect = Rectangle(width = width - 0.3, height = height - 0.3)
        dashed_rect.move_to(world_rect)
        dashed_label = TextMobject("Třída všech množin")
        dashed_label.shift(
            dashed_rect.get_corner(RIGHT+DOWN)
            - dashed_label.get_corner(RIGHT+DOWN)
            + 0.2*(UP+LEFT)
        )
        dashed_rect = VGroup([
            DashedLine(start, end, color = ORANGE)
            for start, end in zip(dashed_rect.get_anchors(),
                                  dashed_rect.get_anchors()[1:])
        ])

        self.play(
            ShowCreation(dashed_rect),
            FadeIn(dashed_label),
        )

        self.dither()
        self.play(FadeOut(VGroup(dashed_rect, dashed_label)))

        elements = VGroup([dot_r_comp(sq.get_center()) for sq in squares])
        container = dot_r_comp(set_rect.get_center(), color = YELLOW)
        shift = 0.7
        elements.shift(shift*UP)
        container.shift(shift*DOWN)
        arrows = VGroup([
            Arrow(el, container, color = BLUE)
            for el in elements
        ])

        self.dither()
        hide_arrows(arrows)
        arrows.shift(shift*DOWN)

        self.play(
            arrows.restore,
            ReplacementTransform(squares, elements),
            ReplacementTransform(set_rect, container),
        )
        self.dither()

        el_or_set_label = TextMobject("prvky","/","množiny")
        el_or_set_label.next_to(container, DOWN)
        for sublab, col in zip(el_or_set_label, (WHITE, GRAY, YELLOW)):
            sublab.highlight(col)
        self.play(FadeIn(
            el_or_set_label,
            submobject_mode = "lagged_start",
            run_time = 2,
        ))
        self.dither()

        self.play(
            title.behind_edge, UP,
            Transform(
                world_rect,
                Rectangle(width = 2.1*SPACE_WIDTH, height = 2.1*SPACE_HEIGHT)
            ),
            FadeOut(VGroup(arrows, elements, container, el_or_set_label)),
        )

axiom_data = [
    ("existence", "Existuje prázdná množina."),
    ("extensionality", "Množina je určena pouze svými prvky."),
    ("dvojice", "Pro libovolné prvky $x$, $y$\\\\existuje množina obsahující přesně je."),
    ("sjednocení", "Můžeme sjednotit všechny prvky dané množiny."),
    ("vydělení", "Z množiny můžeme vydělit podmnožinu jakýmkoli pravidlem."),
    ("nekonečna", "Existuje množina přirozených čísel."),
    ("potenční množiny", "K libovolné množině najdeme její potenční množinu."),
    ("nahrazení", "Můžeme nahradit prvky\\\\v množině za jiné pomocí daného pravidla."),
    ("výběru", "Můžeme provést\\\\nekonečně mnoho nahodilých výběrů najednou."),
    ("fundovanosti", "Neexistují \\uv{divné} množiny."),
]

class AxiomShortMobject(TextMobject):
    CONFIG = {
        "fill_color" : GREEN,
    }
    def __init__(self, n, **kwargs):
        name = axiom_data[n][0]
        TextMobject.__init__(self, "{}) Axiom {}".format(n, name), **kwargs)

class AxiomMobject(VMobject):
    CONFIG = {
        "newline" : True,
    }
    def __init__(self, n, **kwargs):
        VMobject.__init__(self, **kwargs)
        if self.newline: newline = "\\\\"
        else: newline = ""
        name, description = axiom_data[n]
        tex = TextMobject(
            "{}) Axiom {}:{}".format(n, name, newline),
            description,
            alignment = "\\raggedright",
        )
        tex[0].highlight(GREEN)
        self.submobjects = tex.submobjects

    def creation_anim(self):
        return AnimationGroup(
            Write(self[0], run_time = 2),
            FadeIn(self[1], submobject_mode = "lagged_start", run_time = 2),
        )

class FirstAxioms(Scene):
    def construct(self):

        axiom0 = AxiomMobject(0, newline = False)
        axiom0.to_corner(UP+LEFT)

        self.play(axiom0.creation_anim())

        emptyset = Square(side_length = 0.5)
        self.play(ShowCreation(emptyset))
        emptyset.save_state()
        self.play(Transform(emptyset, dot_r_comp(emptyset.get_center())))

        arrow_in = Arrow(1.5*UP, emptyset, color = DARK_GREY)
        cross = Cross(color = RED).move_to(arrow_in)
        tmp_rect = Rectangle(width = 3.7, height = 1.6)
        arrows_out = VGroup(
            Arrow(emptyset, dest, color = BLUE)
            for dest in tmp_rect.get_anchors()[:-1]
        )
        
        self.play(ShowCreation(arrow_in))
        self.play(ShowCreation(cross))

        self.dither()
        self.play(ShowCreation(arrows_out))

        self.play(
            FadeOut(VGroup(
                arrow_in, arrows_out, cross,
            )),
            emptyset.restore,
        )
        emptyset.mark_paths_closed = True
        emptyset2 = emptyset.copy().highlight(BLUE).shift(0.7*LEFT)
        emptyset_ori = emptyset.copy()
        self.play(ReplacementTransform(emptyset.copy(), emptyset2))
        emptyset.save_state()
        emptyset.shift(0.7*RIGHT).highlight(RED)
        self.play(MoveFromSaved(emptyset))
        neq = TexMobject("\\neq")
        neq.move_to(VGroup(emptyset, emptyset2))
        self.play(Write(neq))
        self.dither()

        self.play(
            FadeOut(neq),
            Transform(emptyset, emptyset_ori),
            Transform(emptyset2, emptyset_ori, remover = True),
        )
        axiom1 = AxiomMobject(1).next_to(axiom0, DOWN, aligned_edge = LEFT)
        self.play(axiom1.creation_anim())
        self.dither()

        self.play(FadeOut(emptyset))
        elements = VGroup(Dot() for _ in range(3))
        elements.arrange_submobjects(buff = 1.2)
        set1 = SurroundingRectangle(elements, buff = 0.5, color = GREEN)
        set2 = SurroundingRectangle(elements, buff = 0.5, color = PURPLE)
        set1.shift(0.1*(DOWN+LEFT))
        set2.shift(0.1*(UP+RIGHT))

        self.play(ShowCreation(set1), FadeIn(elements))
        self.dither()
        self.play(ShowCreation(set2))

        dot1 = dot_r_comp(1.3*DOWN+0.8*LEFT, color = GREEN)
        dot2 = dot_r_comp(1.3*DOWN+0.8*RIGHT, color = PURPLE)
        arrows = VGroup(
            Arrow(el, dest, color = BLUE)
            for dest in (dot1, dot2)
            for el in elements
        )
        hide_arrows(arrows)        
        self.play(
            arrows.restore,
            ReplacementTransform(set1, dot1),
            ReplacementTransform(set2, dot2),
        )

        dot_dest = Dot((dot1.get_center() + dot2.get_center())/2, color = YELLOW)
        arrows_dest = VGroup(
            Arrow(el, dot_dest, color = BLUE)
            for el in elements
        )
        self.play(
            Transform(VGroup(arrows[:3]), arrows_dest),
            Transform(VGroup(arrows[3:]), arrows_dest),
            Transform(dot1, dot_dest),
            Transform(dot2, dot_dest),
        )
        self.remove(dot1, dot2, arrows)
        self.add(dot_dest, arrows_dest)

        self.dither()

        additional_arrows = []
        for hdir, dot in ((LEFT, elements[0]), (RIGHT, elements[-1])):
            additional_arrows += [
                Arrow(
                    dot.get_center() + 1.6*hdir + 0.8*vdir,
                    dot,
                    color = BLUE
                )
                for vdir in (UP, DOWN)
            ]

        additional_arrows = VGroup(additional_arrows)
        self.play(ShowCreation(additional_arrows))

        self.dither()
        self.play(FadeOut(additional_arrows))

        axioms01 = VGroup(axiom0, axiom1)
        self.play(
            axioms01.behind_edge, UP,
            dot_dest.highlight, WHITE,
        )
        self.remove(axioms01)

        axiom_proposal = TextMobject("Každá konečná třída je množinou").to_corner(UP+LEFT)
        self.play(FadeIn(axiom_proposal, submobject_mode = "lagged_start", run_time = 2))

        sel_dots = VGroup(elements[1:] + [dot_dest])
        rings = VGroup(
            Circle(color = GREEN, radius = 0.2).shift(dot.get_center())
            for dot in sel_dots
        )
        self.play(ShowCreation(rings))
        rect = SurroundingRectangle(rings)
        self.play(ShowCreation(rect))

        rect_dot = dot_r_comp(
            elements[-1].get_center()*X_MASK + dot_dest.get_center()*Y_MASK,
            color = YELLOW,
        )
        arrows2 = VGroup(
            Arrow(dot, rect_dot, color = BLUE)
            for dot in sel_dots
        )
        hide_arrows(arrows2)            
        self.play(
            FadeOut(rings),
            arrows2.restore,
            ReplacementTransform(rect, rect_dot)
        )
        self.dither()

        picture = VGroup(axiom_proposal, elements, dot_dest, rect_dot, arrows_dest, arrows2)
        self.play(FadeOut(picture))

def dot_triple(angle = RIGHT, radius = 0.8):
    if angle == "random":
        angle = rotate_vector(RIGHT, random.random()*2*np.pi)
    points = compass_directions(3, angle)*radius
    return VGroup(Dot(p) for p in points)

class SingletonsAndUnions(Scene):

    def prepare_ax_prop(self):
        ax_prop = VGroup(
            TextMobject("Jednoprvkové množiny"),
            TextMobject("Sjednocení dvojic"),
        )
        ax_prop.arrange_submobjects(DOWN, aligned_edge = LEFT)
        ax_prop.to_corner(UP+LEFT)
        return ax_prop

    def show_set_pair(self, shift = DOWN):

        elements1 = dot_triple(LEFT)
        elements2 = dot_triple(RIGHT)
        rect1 = SurroundingRectangle(elements1, buff = 0.5)
        rect2 = SurroundingRectangle(elements2, buff = 0.5)
        set1 = VGroup(rect1, elements1)
        set2 = VGroup(rect2, elements2)
        VGroup(set1, set2).arrange_submobjects(RIGHT, buff = 0.5).shift(shift)
        self.play(ShowCreation(rect1), FadeIn(elements1))
        self.play(ShowCreation(rect2), FadeIn(elements2))

        return VGroup(set1, set2)

    def construct(self):

        ax_prop = self.prepare_ax_prop()
        self.play(FadeIn(ax_prop[0], run_time = 2, submobject_mode = "lagged_start"))

        dot = Dot()
        rect = SurroundingRectangle(dot, buff = 0.5)
        self.play(ShowCreation(dot))
        self.play(ShowCreation(rect))

        self.play(
            FadeOut(VGroup(dot, rect)),
            FadeIn(ax_prop[1], run_time = 2, submobject_mode = "lagged_start"),
        )

        set1, set2 = self.show_set_pair()
        self.dither()
        set_u = self.play_union(set1, set2)
        self.dither()
        self.play(FadeOut(set_u))

        dots = VGroup(Dot() for _ in range(4)).arrange_submobjects(buff = 1.3)
        self.play(ShowCreation(dots))
        self.dither()
        rects = VGroup(SurroundingRectangle(dot, buff = 0.5) for dot in dots)
        self.play(ShowCreation(rects))
        self.dither()
        sets = VGroup(zip(rects, dots))
        cur_set = sets[0]
        for s in sets[1:]:
            cur_set = self.play_union(cur_set, s)
        self.dither()

        self.play(
            FadeOut(cur_set),
            ax_prop[0].behind_edge, UP,
            ax_prop[1].to_corner, UP+LEFT,
        )

    def play_union(self, set1, set2):

        rect1, elements1 = set1
        rect2, elements2 = set2

        shift = rect2.get_edge_center(LEFT) - rect1.get_edge_center(RIGHT)
        shift /= 2
        self.play(set1.shift, shift, set2.shift, -shift)

        color = rgb_to_color(rect1.stroke_rgb)
        rect = SurroundingRectangle(VGroup(rect1, rect2), buff = 0, color = color)
        separator = Line(
            rect1.get_corner(UP+RIGHT),
            rect1.get_corner(DOWN+RIGHT),
            color = color
        )
        self.remove(rect1, rect2)
        self.add(rect)
        self.play(Uncreate(separator))

        return VGroup(
            rect,
            elements1.family_members_with_points()
            + elements2.family_members_with_points()
        )

class PairsAndUnions(SingletonsAndUnions):
    def construct(self):

        ax_prop = self.prepare_ax_prop()
        ax_prop[1].to_corner(UP+LEFT)
        self.add(ax_prop[1])

        sets = self.show_set_pair(shift = 2*DOWN)
        superset = SurroundingRectangle(sets, color = ORANGE, buff = 0.3)

        axiom2 = AxiomMobject(2, newline = False)
        axiom2.next_to(ax_prop[1], DOWN, aligned_edge = LEFT)
        self.play(axiom2.creation_anim())

        self.play(ShowCreation(superset))

        axiom3 = AxiomMobject(3)
        axiom3.next_to(axiom2, DOWN, aligned_edge = LEFT)
        self.play(axiom3.creation_anim())

        rects = VGroup(s[0] for s in sets)
        rects.save_state()
        for rect in rects:
            rect.highlight(BLACK)
            rect.scale_in_place(1.1)
        self.play(MoveFromSaved(rects, remover = True))
        self.dither()

        axiom2.save_state()
        axiom3.save_state()
        axiom2.to_corner(UP+LEFT)
        axiom3.next_to(axiom2, DOWN, aligned_edge = LEFT).highlight(BLACK)

        self.play(
            FadeOut(VGroup(
                [s[1] for s in sets],
                superset,
            )),
            ax_prop.behind_edge, UP,
            MoveFromSaved(axiom2),
            MoveFromSaved(axiom3),
        )
        self.remove(ax_prop, axiom3)

        dot = dot_r_comp()
        dot_l = TexMobject('x').next_to(dot, UP)
        x_g = VGroup(dot, dot_l)
        self.play(FadeIn(x_g))

        x_copy = x_g.copy().shift(1.5*RIGHT)
        rect = SurroundingRectangle(VGroup(x_g, x_copy), buff = 0.5)

        self.play(ReplacementTransform(x_g.copy(), x_copy))
        self.play(ShowCreation(rect))

        result = dot.copy().highlight(YELLOW).shift(1.3*DOWN)

        arrows = VGroup(
            Arrow(src, result, color = BLUE)
            for src in (dot, x_copy[0])
        )
        hide_arrows(arrows)
        self.play(
            ReplacementTransform(rect, result),
            arrows.restore,
        )

        self.dither()
        self.play(
            Transform(
                VGroup(arrows[1], x_copy),
                VGroup(arrows[0], x_g),
                remover = True,
            )
        )
        self.dither()
        rect = SurroundingRectangle(x_g, buff = 0.5)
        arrows = VGroup(arrows[0])
        hide_arrows(arrows)
        self.play(
            MoveFromSaved(arrows, remover = True),
            ReplacementTransform(result, rect),
        )
        self.dither()
        self.play(FadeOut(VGroup(rect, x_g)))

class AxiomOfSelection(Scene):
    def construct(self):

        axiom2 = AxiomMobject(2, newline = False).to_corner(UP+LEFT)
        axiom4 = AxiomMobject(4).to_corner(UP+LEFT)

        axiom2.save_state()
        axiom4.save_state()
        axiom4.next_to(axiom2, DOWN, aligned_edge = LEFT).highlight(BLACK)
        axiom2.next_to(axiom2, UP, aligned_edge = LEFT).highlight(BLACK)
        self.play(
            MoveFromSaved(axiom2, remover = True),
            axiom4.restore,
        )

        numbers = [2,3,4,5,7,8]
        numbers_mob = TexMobject(*[str(n) for n in numbers])
        numbers_mob.arrange_submobjects(buff = 1, coor_mask = X_MASK)
        numbers_mob.shift(0.3*DOWN)
        rect = SurroundingRectangle(numbers_mob, buff = 0.3)
        rect.stretch_in_place(1.1, 0)
        label = TexMobject('A').highlight(YELLOW).next_to(rect, LEFT, buff = 0.3)
        self.play(
            FadeIn(numbers_mob),
        )
        self.play(
            ShowCreation(rect),
            FadeIn(label),
        )
        shift = 2*DOWN
        rule = TextMobject("Lichá čísla")
        rule.move_to(label).shift(shift)
        self.play(Write(rule))

        icons = []
        sat_numbers = []
        sat_icons = []

        for n,mob in zip(numbers, numbers_mob):
            satisfied = n % 2 == 1
            if satisfied: icon = IconYes()
            else: icon = IconNo()
            icon.scale(0.8)
            icon.move_to(mob)
            if satisfied:
                icon.shift(0.1*RIGHT)
                sat_numbers.append(mob)
                sat_icons.append(icon)
            icons.append(icon)

        icons = VGroup(icons).next_to(rect, UP, coor_mask = Y_MASK)
        sat_numbers = VGroup(sat_numbers).copy()
        sat_icons = VGroup(sat_icons).copy()
            
        self.dither()
        for icon in icons:
            self.play(ShowCreation(icon, run_time = 0.5))

        self.dither()

        satisfied = VGroup(sat_numbers, sat_icons)
        self.play(satisfied.shift, shift)

        rect2 = SurroundingRectangle(sat_numbers, buff = 0.3)
        self.play(ShowCreation(rect2))

        dots = VGroup(Dot() for _ in range(7))
        dots.arrange_submobjects(buff = 1)

        self.revert_to_original_skipping_status()
        
        dots.move_to(numbers_mob, coor_mask = Y_MASK)
        A_dots = VGroup(dots[:5])
        A_rect = SurroundingRectangle(A_dots, buff = 0.5).shift(0.1*UP)
        A_label = TexMobject('A').highlight(YELLOW).next_to(A_rect, LEFT)
        B_rect = SurroundingRectangle(
            VGroup(dots[2:]), buff = 0.5, color = ORANGE,
        ).shift(0.1*DOWN)
        B_label = TexMobject('B').highlight(ORANGE).next_to(B_rect, RIGHT)
        
        self.play(
            FadeOut(VGroup(
                rule, rect2, numbers_mob[-1], satisfied, icons,
            )),
            ReplacementTransform(label, A_label),
            ReplacementTransform(rect, A_rect),
            ReplacementTransform(VGroup(numbers_mob[:-1]), A_dots),
        )
        self.play(
            FadeIn(B_label),
            FadeIn(VGroup(dots[5:])),
            ShowCreation(B_rect),
        )

        rule = TextMobject("prvky","B")
        rule[-1].highlight(ORANGE)

        shift = 2.2*DOWN
        rule.move_to(A_label).shift(shift+0.1*DOWN)
        self.play(Write(rule))

        icons = VGroup([IconNo() for _ in range(2)]+[IconYes() for _ in range(3)])
        for dot, icon in zip(A_dots, icons):
            icon.scale(0.8).move_to(dot)
        icons.next_to(A_rect, UP, coor_mask = Y_MASK)

        for icon in icons:
            self.play(ShowCreation(icon, run_time = 0.5))

        self.dither()
        intersection = VGroup(dots[2:5], icons[2:]).copy()
        self.play(
            intersection[0].shift, shift,
            intersection[1].shift, shift+0.15*DOWN,
        )
        i_rect = SurroundingRectangle(intersection[0], buff = 0.5)
        self.play(ShowCreation(i_rect))
        self.dither()
        
        axiom4.save_state()
        axioms = VGroup(AxiomShortMobject(n) for n in (0,2,3))
        axioms.arrange_submobjects(DOWN, aligned_edge = LEFT).to_corner(UP+LEFT)
        axiom4.next_to(axioms[-1], DOWN, aligned_edge = LEFT)
        axiom4[1].set_fill(opacity = 0)
        axiom4[0][-1].set_fill(opacity = 0)
        axioms.save_state()
        axioms.highlight(BLACK)
        axioms.next_to(axioms, UP, coor_mask = Y_MASK)

        self.play(
            FadeOut(VGroup(
                intersection, i_rect, rule,
                A_rect, A_label, B_rect, B_label,
                dots, icons,
            )),
            axioms.restore,
            MoveFromSaved(axiom4),
        )

class InfiniteWorld(Scene):
    def construct(self):

        axioms = VGroup(AxiomShortMobject(n) for n in (0,2,3,4))
        axioms.arrange_submobjects(DOWN, aligned_edge = LEFT).to_corner(UP+LEFT)

        self.add(axioms)

        unit = 1.5
        dots = [Dot()]
        dots.append(Dot(dots[0].get_center() + unit*DOWN))
        arrows = [Arrow(dots[0], dots[1], color = BLUE)]
        self.play(FadeIn(VGroup(dots)), ShowCreation(arrows[0]), run_time = 0.5)

        for i in range(12):
            if i%2 == 0:
                src = dots[-2], dots[-1]
                next_dot = sum([dot.get_center() for dot in src])/2
                next_dot = Dot(next_dot + unit*np.sqrt(3)/2*RIGHT)
            else:
                src = dots[-3], dots[-1]
                if i%4 == 1: next_dot = Dot(dots[-1].get_center() + unit*UP)
                else: next_dot = Dot(dots[-1].get_center() + unit*DOWN)

            next_arrows = [Arrow(dot, next_dot, color = BLUE) for dot in src]
            self.play(
                FadeIn(next_dot),
                *map(ShowCreation, next_arrows),
                run_time = 0.5,
                rate_func = None
            )

            dots.append(next_dot)
            arrows += next_arrows

        dots = VGroup(dots)
        arrows = VGroup(arrows)
        self.dither()

        rect = SurroundingRectangle(VGroup(dots[::4]), buff = 0.3)
        self.play(ShowCreation(rect))
        self.dither(3)

        axioms.save_state()
        axioms.shift(DOWN)
        axioms.set_fill(opacity = 0)
        series = VideoSeries(num_videos = 16).to_edge(UP)
        active = series[3]
        active.remove(active[1])
        active.add(TexMobject('4').replace(active, 1).scale_in_place(0.6))
        active.highlight(YELLOW)
        series.save_state()
        series.behind_edge(UP)

        self.play(
            FadeOut(VGroup(dots, arrows, rect)),
            MoveFromSaved(axioms, remover = True),
            series.restore,
        )

chapter4 = importlib.import_module('eost.04-well-ordering')

class LargeConstructionReminder(Scene):
    def construct(self):
        
        series = VideoSeries(num_videos = 16).to_edge(UP)
        active = series[3]
        active.remove(active[1])
        active.add(TexMobject('4').replace(active, 1).scale_in_place(0.6))
        active.highlight(YELLOW)
        self.add(series)

        omega = OrdinalOmega(q=(0.8, 0.9, 0.9))
        omega[0].highlight(GREEN)

        p_powers = omega.add_descriptions(chapter4.make_p_power,
                                          direction = UP)
        for i,label in enumerate(p_powers):
            label[-i-1].highlight(GREEN)

        self.play(Write(p_powers[0]), ShowCreation(omega[0]))
        self.dither()
        self.play(ReplacementTransform(p_powers[0][0].copy(), p_powers[1][-2]))
        self.play(
            Write(VGroup(p_powers[1][:-2], p_powers[1][-1])),
            ShowCreation(omega[1]),
        )
        self.dither()

        for i in range(2,4):
            self.play(
                ShowCreation(omega[i]),
                FadeIn(VGroup(p_powers[i][:2], p_powers[i][-1])),
                ReplacementTransform(p_powers[i-1].copy(), VGroup(p_powers[i][2:-1])),
            )

        self.play(
            ShowCreation(VGroup(omega[i+1:])),
            ShowCreation(VGroup(p_powers[i+1:])),
        )
        self.dither()

        union_bar = omega[0].copy().highlight(YELLOW).next_to(omega)
        union_label = TextMobject("Sjednocení").highlight(YELLOW).next_to(union_bar, UP)

        self.play(
            ShowCreation(union_bar),
            ReplacementTransform(
                p_powers.copy(), VGroup(union_label),
            )
        )
        self.dither()

        self.play(
            series.behind_edge, UP,
            FadeOut(VGroup(
                omega, p_powers, union_bar, union_label,
            ))
        )

class LargeConstructionAxioms(Scene):
    def construct(self):

        omega = OrdinalOmega(q=(0.8, 0.9, 0.9))
        omega.shift(1.5*DOWN)
        omega[0].highlight(GREEN)

        p_powers = omega.add_descriptions(chapter4.make_p_power,
                                          direction = UP)
        for i,label in enumerate(p_powers):
            label[-i-1].highlight(GREEN)

        self.play(Write(p_powers[0]), ShowCreation(omega[0]))

        numbers = TexMobject(*[str(n) for n in range(13)])
        numbers.arrange_submobjects(buff = 0.5)
        numbers.next_to(p_powers[0])
        numbers.next_to(p_powers[1], coor_mask = X_MASK, buff = 0.8)
        numbers_rect = SurroundingRectangle(numbers, color = GREEN)
        line1 = Line(*numbers_rect.get_anchors()[:2], color = GREEN)
        line2 = PolyLine(*reversed(numbers_rect.get_anchors()[2:]), color = GREEN)
        self.play(
            ShowCreation(line1),
            ShowCreation(line2),
            FadeIn(numbers, submobject_mode = "lagged_start"),
        )
        self.remove(line1, line2)
        self.add(numbers_rect)

        axiom5 = AxiomMobject(5).to_corner(UP+LEFT)
        self.play(axiom5.creation_anim())

        series = VideoSeries(num_videos = 16).to_edge(UP)
        active = series[10]
        active.remove(active[1])
        active.add(TexMobject('11').replace(active, 1).scale_in_place(0.6))
        series = VGroup(series[6:])
        series.gradient_highlight(BLACK, BLUE)
        active.highlight(YELLOW)
        series.save_state()
        series.behind_edge(UP)

        self.play(
            series.restore,
            Animation(axiom5),
        )
        self.dither()
        self.play(
            series.behind_edge, UP,
            Animation(axiom5),
        )
        self.remove(series)

        self.play(ReplacementTransform(p_powers[0][0].copy(), p_powers[1][-2]))
        self.play(
            Write(VGroup(p_powers[1][:-2], p_powers[1][-1])),
            ShowCreation(omega[1]),
        )
        numbers_g = VGroup(numbers, numbers_rect)
        subsets = VGroup(numbers_g.copy() for _ in range(5))
        subsets.arrange_submobjects(DOWN).next_to(numbers_g, DOWN)
        for subset in subsets:
            for num in subset[0]:
                if random.random() < 0.5: num.set_fill(opacity = 0)
        subset_rect = SurroundingRectangle(VGroup(numbers_g, subsets))

        self.play(
            FadeIn(subset_rect),
            ReplacementTransform(VGroup(numbers_g).copy(), subsets),
        )

        axiom6 = AxiomMobject(6).next_to(axiom5, DOWN, aligned_edge = LEFT)
        self.play(axiom6.creation_anim())

        self.dither()

        self.play(FadeOut(VGroup(
            subsets, numbers_g, subset_rect
        )))

        for i in range(2,4):
            self.play(
                ShowCreation(omega[i]),
                FadeIn(VGroup(p_powers[i][:2], p_powers[i][-1])),
                ReplacementTransform(p_powers[i-1].copy(), VGroup(p_powers[i][2:-1])),
            )
        self.play(
            ShowCreation(VGroup(omega[i+1:])),
            ShowCreation(VGroup(p_powers[i+1:])),
        )
        self.dither()

        self.play(FadeOut(VGroup(axiom5, axiom6)))
        axiom3 = AxiomMobject(3).to_corner(UP+LEFT)
        axiom3.save_state()
        axiom3.behind_edge(UP)
        self.play(axiom3.restore)

        self.dither()

        buff = 0.2
        corner_ul = p_powers.get_corner(UP+LEFT)+buff*(UP+LEFT)
        corner_dr = omega.get_edge_center(RIGHT) + buff*RIGHT
        p_powers_rect = Rectangle(
            width = corner_dr[0] - corner_ul[0],
            height = corner_ul[1] - corner_dr[1],
            color = YELLOW,
        ).move_to((corner_ul+corner_dr)/2)
        dashed_rect = VGroup([
            DashedLine(start, end, color = YELLOW)
            for start, end in zip(p_powers_rect.get_anchors(),
                                  p_powers_rect.get_anchors()[1:])
        ])
        self.play(ShowCreation(dashed_rect))

        axiom7 = AxiomMobject(7, newline = False).next_to(axiom3, DOWN, aligned_edge = LEFT)
        self.play(axiom7.creation_anim())

        self.play(FadeOut(dashed_rect))

        numbers = omega.add_descriptions(lambda n: TexMobject(str(n)),
                                        direction = DOWN)
        self.play(ShowCreation(numbers))

        corner_dl = numbers.get_corner(DOWN+LEFT)+buff*(DOWN+LEFT)
        corner_ur = omega.get_edge_center(RIGHT) + buff*RIGHT
        numbers_rect = Rectangle(
            width = corner_ur[0] - corner_dl[0],
            height = corner_ur[1] - corner_dl[1],
            color = YELLOW,
        ).move_to((corner_dl+corner_ur)/2)
        self.play(ShowCreation(numbers_rect))

        self.dither()

        rule = VGroup(
            TexMobject("n").next_to(omega[0], DOWN),
            TexMobject("\\mathcal P^n(\\omega)").next_to(omega[0], UP),
        )
        rule[1].shift((p_powers[0].get_center() - rule[1][-1].get_center())*Y_MASK)
        rule.add(Arrow(*rule))
        col = BLUE
        rule[0].highlight(col)
        rule[1][1].highlight(col)
        rule.to_edge(LEFT)

        self.play(FadeIn(rule[0]))
        self.play(
            ShowCreation(rule[2]),
            FadeIn(rule[1]),
        )

        arrows = VGroup(
            Arrow(
                bar.get_edge_center(DOWN),
                bar.get_edge_center(UP)+0.1*bar.height*DOWN,
                buff = 0.0,
                thickness = bar.thickness,
                tip_length = 0.25*bar.height,
            )
            for bar in omega
        )
        for arrow in arrows[20:]:
            arrow.remove(arrow.tip)
        for i in range(2):
            self.remove(omega[i])
            self.play(ShowCreation(arrows[i]))

        i += 1
        self.dither()
        self.remove(omega[i])
        self.play(
            FadeOut(VGroup(omega[i+1:]), submobject_mode = "one_at_a_time"),
            ShowCreation(VGroup(arrows[i:])),
            run_time = 2,
        )
        self.dither()

        rect = numbers_rect
        numbers_rect = rect.copy()
        self.play(Transform(rect, p_powers_rect))

        self.dither()

        self.play(FocusOn2(axiom3[0], scale = 1.1))

        union_bar = omega[0].copy().highlight(YELLOW).next_to(omega)
        union_label = TextMobject("Sjednocení").highlight(YELLOW).next_to(union_bar, UP)

        self.play(
            Transform(
                rect,
                SurroundingRectangle(union_label, stroke_width = 0),
                remover = True,
            ),
            ReplacementTransform(
                p_powers.copy(), VGroup(union_label),
            ),
        )
        self.play(
            ShowCreation(union_bar),
        )
        self.dither()

        self.play(
            FadeOut(VGroup(union_bar, union_label)),
            axiom3.behind_edge, UP,
        )
        axiom1 = AxiomMobject(1)
        axiom1.to_corner(LEFT+UP)
        self.play(UnapplyMethod(axiom1.behind_edge, UP))

        rect = numbers_rect.copy()
        self.play(FadeIn(rect))
        self.play(Transform(rect, p_powers_rect))
        self.dither()
        self.play(FadeOut(rect))

        rule.save_state()
        rule.move_to(ORIGIN, coor_mask = X_MASK)
        self.play(
            FadeOut(VGroup(
                arrows, p_powers, numbers,
            )),
            MoveFromSaved(rule),
        )

        number = rule[0]
        power = rule[1]
        arrow = rule[2]
        self.play(FocusOn2(number))
        self.play(FocusOn2(power))
        self.dither()

        cancel_line = VGroup(
            Line(row.get_edge_center(LEFT), row.get_edge_center(RIGHT), color = RED)
            for row in axiom1
        )
        self.play(
            axiom1.set_fill, None, 0.2,
            ShowCreation(cancel_line),
        )
        
        powers = VGroup(power.copy().highlight(color) for color in (PURPLE, ORANGE))
        powers[0].shift(1.6*LEFT+0.5*DOWN)
        powers[1].shift(1.6*RIGHT+0.5*DOWN)
        arrows = VGroup(
            Arrow(number, p)
            for p in powers
        )
        for power2 in powers: self.play(FadeIn(power2))
        self.play(ShowCreation(arrows))

        self.play(
            Uncreate(cancel_line),
            axiom1.set_fill, None, 1,
        )
        self.play(
            Transform(arrows, VGroup(arrow), remover = True),
            Transform(powers, VGroup(power), remover = True),
        )
        self.dither()

        self.play(
            VGroup(axiom1, axiom7).behind_edge, UP,
            FadeOut(rule),
        )

class AxiomOfChoice(Scene):
    def construct(self):

        series = VideoSeries(num_videos = 16).to_edge(UP)
        active = series[12]
        active.remove(active[1])
        active.add(TexMobject('13').replace(active, 1).scale_in_place(0.6))
        active.highlight(YELLOW)

        axiom8 = AxiomMobject(8, newline = False)
        axiom8.next_to(series, DOWN, aligned_edge = LEFT)
        self.play(axiom8.creation_anim())

        self.dither()

        self.play(
            UnapplyMethod(series.behind_edge, UP),
            Animation(axiom8),
        )
        self.dither()

        colors = [ORANGE, PURPLE, RED, BLUE]

        sets = VGroup(
            VGroup(
                Square(),
                dot_triple(
                    angle = "random",
                    radius = 0.6,
                ),
            ).highlight(color)
            for color in colors
        )
        VGroup(
            VGroup(sets[:2]).arrange_submobjects(RIGHT),
            VGroup(sets[2:]).arrange_submobjects(LEFT),
        ).arrange_submobjects(DOWN)

        sets_rect = SurroundingRectangle(sets, color = WHITE, buff = 0.2)
        sets_g = VGroup(sets, sets_rect)
        sets_g.to_corner(DOWN+LEFT)

        for sq in sets:
            sq.save_state()
            sq.highlight(BLACK)

        self.play(
            ShowCreation(sets_rect),
            Succession(*[
                ApplyMethod(sq.restore, rate_func = None)
                for sq in sets
            ], run_time = 1),
        )
        self.dither()

        chosen = VGroup(sq[1][0] for sq in sets)
        chosen_circ = VGroup(
            Circle(color = GREEN, radius = 0.2).shift(dot.get_center())
            for dot in chosen
        )
        self.play(ShowCreation(chosen_circ))
        chosen = VGroup(zip(chosen, chosen_circ)).copy()
        chosen.save_state()

        VGroup(
            VGroup(chosen[:2]).arrange_submobjects(RIGHT),
            VGroup(chosen[2:]).arrange_submobjects(LEFT),
        ).arrange_submobjects(DOWN)
        chosen_rect = SurroundingRectangle(chosen)
        chosen_g = VGroup(chosen, chosen_rect)
        chosen_g.move_to(sets_rect.get_edge_center(RIGHT))
        chosen_g.move_to(SPACE_WIDTH*RIGHT, coor_mask = X_MASK*0.5)

        self.play(MoveFromSaved(chosen))
        self.dither()
        chosen.save_state()
        for dot, circ in chosen:
            circ.highlight(BLACK)
        self.play(
            ShowCreation(chosen_rect),
            MoveFromSaved(chosen),
        )
        self.dither()
        self.play(
            FadeOut(VGroup(
                chosen_g, sets_g, chosen_circ,
            )),
            VGroup(
                series, axiom8,
            ).behind_edge, UP,
        )

class AxiomOfFoundation(Scene):
    def construct(self):

        axiom9 = AxiomMobject(9, newline = False).to_edge(UP)
        self.play(axiom9.creation_anim())
        self.dither()

        sq_out = Square(color = YELLOW).shift(2*LEFT)
        arrow = Arc(angle = -np.pi*1.5, start_angle = np.pi, color = BLUE)
        arrow.shift(sq_out.get_corner(UP+RIGHT))
        path_g = VGroup(
            Line(sq_out.get_center(), arrow.get_anchors()[0]),
            arrow.copy(),
            Line(arrow.get_anchors()[-1], sq_out.get_center()),
        )
        path = VMobject()
        path.points = np.concatenate(
            [mob.points[:-1] for mob in path_g] + [path_g[-1].points[-1:]],
            0,
        )
        arrow.add_tip()
        sq_in = sq_out.copy()
        sq_in.save_state()
        sq_in.highlight(WHITE)
        sq_in.scale_in_place(0.8)
        path.scale_about_point(0.7, sq_out.get_center())

        self.play(ShowCreation(sq_out))
        self.dither()
        self.play(
            ShowCreation(arrow),
            MoveFromSaved(sq_in),
            MoveAlongPath(sq_in, path),
        )
        self.dither()

        colors = [YELLOW, GREEN, BLUE, PURPLE, RED, ORANGE]
        tunnel = [Square(color = colors[0])]
        ci = 1
        while tunnel[-1].stroke_width > 0.2:
            next_set = tunnel[-1].copy()
            next_set.scale_in_place(0.8)
            next_set.stroke_width *= 0.9
            next_set.color = colors[ci]
            next_set.highlight(next_set.color)
            tunnel.append(next_set)

            ci += 1
            if ci == len(colors): ci = 0

        tunnel = VGroup(tunnel)
        tunnel.shift(2*RIGHT)
        for sq in tunnel:
            darkness = 1 - (sq.get_width() / tunnel[0].get_width())
            sq.fade(darkness)

        for i in range(3):
            self.play(ShowCreation(tunnel[i]))
        i += 1
        self.play(FadeIn(VGroup(tunnel[i:]), submobject_mode = "one_at_a_time"))

        self.dither()

        self.play(FadeOut(VGroup(tunnel, sq_out, arrow, sq_in)))

        dots1 = VGroup(dot_r_comp() for _ in range(5)).arrange_submobjects(buff = 1)
        dots1.shift(1.5*UP)
        rect1 = SurroundingRectangle(dots1, buff = 0.5, color = YELLOW)
        self.play(FadeIn(dots1), ShowCreation(rect1))

        dot = dots1[1]
        pointer = TrianglePointer().next_to(rect1, UP)
        pointer.highlight(BLACK)
        pointer.save_state()
        pointer.move_to(dot, coor_mask = X_MASK)
        pointer.highlight(YELLOW)
        self.play(MoveFromSaved(pointer))

        rect2 = rect1.copy().highlight(WHITE)
        dots2 = dots1.copy().highlight(GREEN)
        VGroup(rect2, dots2).next_to(rect1, DOWN, buff = 0.5)

        self.play(
            ReplacementTransform(dot.copy(), rect2),
            FadeIn(dots2),
        )
        self.dither()

        tunnel_backup = tunnel.copy()
        tunnel.to_corner(DOWN+LEFT)
        self.play(FadeIn(tunnel))

        dots = []
        arrows = []
        shift = 2*RIGHT
        for _ in range(10):
            rect = tunnel[0]
            tunnel = VGroup(tunnel[1:])
            dot = dot_r_comp(rect.get_center(), color = rect.color)
            if len(arrows) > 0:
                longer_arrow = Arrow(dot, dots[-1], color = BLUE)
                animations = [Transform(arrows[-1], longer_arrow)]
            else: animations = []

            tunnel.save_state()
            tunnel.shift(shift)
            arrow = Arrow(tunnel, dot, color = BLUE)
            arrow.save_state()
            arrow.set_stroke(width = 0)
            arrow.scale_about_point(0, np.array(arrow.get_end()))
            animations += [
                MoveFromSaved(tunnel),
                ReplacementTransform(rect, dot),
                arrow.restore,
            ]
            rate_func = None
            run_time = 0.7                
            self.play(*animations, rate_func = rate_func, run_time = run_time)
            dots.append(dot)
            arrows.append(arrow)

        self.remove(tunnel)

        dots = VGroup(dots)
        arrows = VGroup(arrows)
        rect = SurroundingRectangle(dots, buff = 0.5)
        self.play(ShowCreation(rect))

        index = 3
        pointer2 = pointer.copy().scale(-1).next_to(rect, DOWN)
        pointer2.move_to(dots[index], coor_mask = X_MASK)

        pointer2.save_state()
        pointer2.shift(2*LEFT).highlight(BLACK)
        self.play(pointer2.restore)

        square = SurroundingRectangle(
            dots[index+1],
            color = dots[index].color,
            buff = 0.4,
        )
        self.play(ReplacementTransform(dots[index].copy(), square))

        self.dither()
        self.play(FadeOut(VGroup(pointer2, square)))
        cancel_line = Line(
            rect.get_edge_center(LEFT) + 0.1*UP,
            rect.get_edge_center(RIGHT) + 0.1*DOWN,
            color = RED,
        )
        self.play(
            VGroup(rect, dots, arrows).fade, 0.8,
            ShowCreation(cancel_line),
        )
        tunnel = tunnel_backup
        tunnel.next_to(rect, UP, aligned_edge = LEFT, buff = 0.3)
        tunnel.fade(0.5)
        cross = Cross(color = RED).replace(tunnel).scale_in_place(1.1)
        self.play(FadeIn(tunnel))
        self.play(ShowCreation(cross))

        self.dither()

        self.play(FadeOut(VGroup(
            pointer, rect1, dots1, rect2, dots2,
            tunnel, cross,
            rect, dots, arrows, cancel_line,
        )))

class VonNeumannUniverse(Scene):
    def construct(self):

        axiom9 = AxiomMobject(9, newline = False).to_edge(UP)
        self.add(axiom9)

        ordinals = OrdinalClass(x1 = SPACE_WIDTH-0.5)
        end_height = SPACE_HEIGHT - 1

        lines = VGroup(
            Line(
                ordinals.get_corner(d+LEFT) + 0.2*d,
                ordinals.line.get_end() + end_height*d,
            )
            for d in (UP, DOWN)
        )
        universe = VGroup(ordinals, lines)
        universe.to_edge(DOWN)

        line_points = [
            [
                interpolate(line.get_start(), line.get_end(), alpha)
                for alpha in np.linspace(0,1,100)
            ]
            for line in lines
        ]

        trapezoid = VGroup(
            Polygon(
                p0,p1,p2,p3,
                stroke_width = 0,
                color = BLUE,
                fill_opacity = 0.3,
            )
            for p0,p1,p2,p3 in zip(
                line_points[0],
                line_points[0][1:],
                line_points[1][1:],
                line_points[1],
            )
        )
        trapezoid.gradient_highlight(GREEN, BLUE, average_color(PURPLE, BLACK))

        all_sets_label = TextMobject("Všechny množiny")
        all_sets_label.next_to(ordinals.line, UP, aligned_edge = RIGHT)
        all_sets_label.shift(0.5*UP + 0.3*LEFT)
        universe.add(trapezoid, all_sets_label)

        self.play(
            ordinals.creation_anim(),
            ShowCreation(lines, submobject_mode = "all_at_once"),
            FadeIn(trapezoid, submobject_mode = "lagged_start"),
            FadeIn(all_sets_label),
        )
        references = VGroup(
            TextMobject("Von Neumann universe"),
            TextMobject("Fundované jádro"),
        )
        references.highlight(BLUE)
        references.arrange_submobjects(DOWN, aligned_edge = LEFT)
        references.next_to(axiom9, DOWN, buff = 0.5, aligned_edge = LEFT)

        self.play(Write(references[0]))
        self.play(FadeIn(references[1], submobject_mode = "lagged_start"))

        self.dither()
        self.play(
            FadeOut(axiom9[0][-1]),
            FadeOut(axiom9[1]),
            FadeOut(VGroup(universe, references)),
        )

class AxiomsReminder(Scene):
    def construct(self):

        axioms = VGroup(
            TextMobject("{}) Axiom {}".format(i,name))
            for i, (name, description) in enumerate(axiom_data)
        )
        axioms.highlight(GREEN)
        axioms.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = 0.1)
        axioms.to_edge(LEFT)
        axioms.save_state()
        axioms[-1].to_corner(UP+LEFT)
        VGroup(axioms[:-1]).behind_edge(UP)

        self.play(axioms.restore)
        self.dither()

        for i in (1,3,5,6,7,8):
            self.play(
                axioms[i].highlight, YELLOW,
                submobject_mode = "lagged_start",
            )

        self.dither()

class NextChapter(Scene):
    def construct(self):

        pair = [0,2]
        triple = [1,4,3]

        x_to_y = [0 for _ in range(5)]
        y_to_x = [0 for _ in range(5)]
        for cycle in (pair, triple):
            for x,y in zip(cycle, cycle[1:]+[cycle[0]]):
                x_to_y[x] = y
                y_to_x[y] = x

        unit = 1
        h_numbers = VGroup(TexMobject(str(n)) for n in range(5))
        v_numbers = h_numbers.copy()
        for i,mob in enumerate(h_numbers):
            mob.move_to(unit*(DOWN + i*RIGHT))
        for i,mob in enumerate(v_numbers):
            mob.move_to(unit*(LEFT + i*UP))
        h_line = Line(1.5*LEFT, 4.5*RIGHT).shift(0.5*DOWN).scale(unit)
        v_line = Line(1.5*DOWN, 4.5*UP).shift(0.5*LEFT).scale(unit)

        VGroup(h_line, v_line, h_numbers, v_numbers).highlight(BLUE)

        graph_points = np.array([
            (float(x), float(x_to_y[x]), 0)
            for x in range(5)
        ])
        graph_points *= unit
        dots = VGroup(Dot(p) for p in graph_points).highlight(YELLOW)
        graph_line = PolyLine(*graph_points).highlight(GREEN)

        graph = VGroup(
            h_numbers, v_numbers, h_line, v_line,
            graph_line, dots,
        ).center()

        self.play(ShowCreation(h_line), FadeIn(h_numbers, submobject_mode = "lagged_start"))
        self.play(ShowCreation(v_line), FadeIn(v_numbers, submobject_mode = "lagged_start"))

        self.play(
            ShowCreation(graph_line),
            FadeIn(dots, submobject_mode = "one_at_a_time"),
        )
        self.dither()

        v_connections = VGroup(
            Line(
                v_numbers[x_to_y[x]].get_edge_center(RIGHT) + RIGHT*0.2,
                dots[x].get_center(),
            )
            for x in range(5)
        )
        h_connections = VGroup(
            Line(
                h_numbers[x].get_edge_center(UP) + UP*0.2,
                dots[x].get_center(),
            )
            for x in range(5)
        )
        connections = VGroup(zip(h_connections, v_connections))
        self.play(
            FadeOut(VGroup(
                h_line, v_line, graph_line,
            )),
            ShowCreation(connections, submobject_mode = "all_at_once"),
            Animation(dots),
        )

        bot_numbers = h_numbers.copy()
        for i,mob in enumerate(bot_numbers):
            mob.move_to(i*RIGHT*1.6)

        bot_numbers.center()
        top_numbers = bot_numbers.copy()
        shift = 2
        bot_numbers.shift(shift*DOWN)
        top_numbers.shift(shift*UP)

        arrows = VGroup(
            Arrow(
                bot_numbers[x].get_edge_center(UP),
                top_numbers[x_to_y[x]].get_edge_center(DOWN),
            )
            for x in range(5)
        ).highlight(WHITE)

        connections_dest = []
        dots.save_state()
        for dot, arrow in zip(dots, arrows):
            start = arrow.get_start()
            end = arrow.get_end()
            mid = (start+end)/2
            connections_dest.append([
                Line(start, mid), Line(end, mid)
            ])
            dot.scale(0)
            dot.move_to(mid)
        connections_dest = VGroup(connections_dest)

        self.play(
            MoveFromSaved(dots, remover = True),
            Transform(connections, connections_dest),
            ReplacementTransform(h_numbers, bot_numbers),
            ReplacementTransform(v_numbers, top_numbers),
        )
        self.dither()

        self.play(ShowCreation(VGroup(arrows[y_to_x[y]].tip for y in range(5))))
        self.remove(connections)
        self.add(arrows)

        numbers = bot_numbers.copy()
        numbers[pair[0]].move_to(top_numbers[0])
        numbers[pair[1]].move_to(bot_numbers[0])

        numbers[triple[0]].move_to(ORIGIN)
        numbers[triple[1]].move_to(top_numbers[-1])
        numbers[triple[2]].move_to(bot_numbers[-1])

        arrows_cycles = VGroup(
            [
                Arrow(numbers[x], numbers[y])
                for x,y in zip(cycle, cycle[1:]+[cycle[0]])
            ]
            for cycle in (pair, triple)
        ).highlight(WHITE)
        for arrow, d in zip(arrows_cycles[0], (LEFT, RIGHT)):
            arrow.shift(0.15*d)

        arrows_cycles_src = VGroup(
            [
                arrows[x]
                for x in cycle
            ]
            for cycle in (pair, triple)
        )
        self.play(
            ReplacementTransform(arrows_cycles_src, arrows_cycles),
            Transform(top_numbers, numbers),
            Transform(bot_numbers, numbers),
        )
        self.remove(top_numbers, bot_numbers)
        self.add(numbers)
        self.dither(2)
