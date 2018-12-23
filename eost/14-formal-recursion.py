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
from topics.icons import MirekOlsakLogo, TrianglePointer, IconYes, IconNo
from topics.objects import BraceDesc, BraceText, Counter
import eost.deterministic

class Chapter14OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Essence of Set Theory",
        "chapter_str" : "Chapter 14\\\\ Formal Recursion",
    }

class Chapter14OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "If you already know what","recursion","is, just remember the answer. Otherwise, find someone who is standing closer to Douglas Hofstadter than you are; then ask him or her what","recursion","is."
        ],
        "highlighted_quote_terms" : {
            "recursion" : GREEN,
        },
        "author" : "Andrew Plotkin"
    }

class Intro(Scene):
    def construct(self):

        ordinal = OrdinalSum(OrdinalOmega, 0.7,
                             lambda **kwargs: OrdinalFinite(3, **kwargs),
                             x0 = -6, x1 = 7)
        ordinal.shift(DOWN)
        ordinal_fg = ordinal
        ordinal_bg = ordinal_fg.copy()
        ordinal_bg.highlight(DARK_GREY)

        self.play(ShowCreation(ordinal_bg))
        #self.wait_to(4.5)
        ordinal_fg[0][0].highlight(GREEN)
        ordinal_fg[1][0].highlight(YELLOW)

        for i in range(4):
            self.play(ShowCreation(ordinal_fg[0][i]), run_time = 0.5)
        self.play(ShowCreation(VGroup(ordinal_fg[0][i+1:])))
        self.play(ShowCreation(ordinal_fg[1]))
        self.remove(ordinal_bg)

        #self.wait_to(9.5)

        def make_nat_index(n):
            return TexMobject(str(n))
        def make_omega_index(n):
            if n == 0: return TexMobject("\\omega")
            return TexMobject("\\omega+"+str(n))
        
        indices0 = ordinal[0].add_descriptions(
            make_nat_index,
            direction = UP, size = 0.5,
        )
        indices1 = VGroup([
            bar.add_description(
                make_omega_index(i),
                direction = UP, size = 0.7,
            )
            for i, bar in enumerate(ordinal[1])
        ])
        indices = VGroup(indices0, indices1)

        def make_p_power_tex_string(n, start):
            return ("\\mathcal P("*n) + start + (")"*n)

        def make_omega_power(n):
            result = TexMobject(make_p_power_tex_string(n, "\\omega"))
            result[-(n+1)].highlight(GREEN)
            return result

        def make_U_power(n):
            result = TexMobject(make_p_power_tex_string(n, "U"))
            result[-(n+1)].highlight(YELLOW)
            return result

        p_powers0 = ordinal[0].add_descriptions(
            make_omega_power,
            direction = DOWN,
        )
        p_powers1 = VGroup([
            bar.add_description(
                make_U_power(i),
                direction = DOWN, size = 0.7,
            )
            for i, bar in enumerate(ordinal[1])
        ])
        p_powers = VGroup(p_powers0, p_powers1)

        self.play(ShowCreation(indices0))
        self.play(ShowCreation(indices1))
        self.play(ShowCreation(p_powers0))
        self.play(ShowCreation(p_powers1))

        #self.wait_to(21.5)

        series = VideoSeries(num_videos = 16).to_edge(UP)
        series.save_state()
        series.behind_edge(UP)
        self.play(
            series.restore,
            VGroup(ordinal, indices, p_powers).shift, DOWN,
        )

        brace_infinity = BraceText(series[:7], "Theory of\\\\Infinity")
        brace_formal = BraceText(series[7:14], "Foundations\\\\of mathematics")
        self.play(
            brace_infinity.creation_anim(),
            brace_formal.creation_anim(),
        )
        #self.wait_to(26)

        p0 = brace_infinity.desc.get_edge_center(RIGHT)
        p1 = brace_formal.desc.get_edge_center(LEFT)
        arrow_right = Arrow(p0, p1).shift(0.2*UP)
        arrow_left = Arrow(p1, p0).shift(0.2*DOWN)
        self.play(ShowCreation(arrow_left))
        self.play(ShowCreation(arrow_right))

        #self.wait_to(33.5)
        self.play(
            VGroup(series[14:16]).highlight, YELLOW
        )
        self.dither()
        #self.wait_to(62)

dec_seq_color = ORANGE

def make_jumps(start_x, end_x, q = 0.8):

    t = DEFAULT_POINT_THICKNESS
    x = start_x - end_x
    buff = 0.02
    jumps = []

    while True:
        next_x = x*q
        t *= q**0.5
        if x-next_x < pixel_size: break

        jumps.append(
            StepCurve(start = (end_x+x)*RIGHT,
                      end = (end_x+next_x)*RIGHT,
                      stroke_width = t)
        )
        x = next_x

    jumps = VGroup(*jumps)
    jumps.set_color(dec_seq_color)

    return jumps

class NaiveProof(Scene):
    def construct(self):
        global pixel_size
        pixel_size = SPACE_WIDTH*2 / self.camera.pixel_shape[1]

        line = Line(6*LEFT, 4*RIGHT, color=BLUE)
        line_l = TextMobject("Ordered set")
        line_l.shift(1.5*UP)

        self.play(
            ShowCreation(line),
            FadeIn(line_l, submobject_mode = "lagged_start"),
        )
        #self.wait_to(3)

        line.put_start_and_end_on(4*LEFT, 4*RIGHT)
        line_beg = Line(6*LEFT, 4*LEFT, color = BLUE)
        fadeout = FadeOut(line_beg)
        fadeout.target_mobject.shift(2*DOWN)

        self.play(fadeout)
        #self.wait_to(6.5)

        pointer_o = TrianglePointer(color = YELLOW).scale(-1)
        pointer_l = TextMobject("Not minimal")
        pointer = VGroup(pointer_o, pointer_l)
        pointer.arrange_submobjects(DOWN)
        pointer.next_to(line,DOWN, buff=0)

        self.play(FadeIn(pointer))

        self.play(pointer.shift, 2*LEFT)
        self.play(pointer.shift, 1*LEFT)

        #self.wait_to(12)
        fadeout = FadeOut(pointer)
        fadeout.target_mobject.shift(1*LEFT)
        self.play(fadeout)

        jumps = make_jumps(3,-4)
        self.play(ShowCreation(jumps), run_time = 1.5)

        #self.wait_to(18)
        self.dither()
        self.play(FadeOut(jumps))
        #self.wait_to(21)

        pointer.move_to(jumps[0].get_anchors()[0], coor_mask = X_MASK)
        pointer_o.save_state()

        pointer_o.shift(0.5*DOWN)
        pointer_o.set_fill(YELLOW, opacity = 0)
        self.play(pointer_o.restore)
        #self.wait_to(25)
        self.play(FadeIn(pointer_l, submobject_mode = "lagged_start"))

        #self.wait_to(27)
        self.play(ShowCreation(jumps[0]))

        pointer_dest = pointer.copy()
        pointer_dest.move_to(jumps[0].get_anchors()[1], coor_mask = X_MASK)

        #self.wait_to(28.5)
        self.play(Transform(pointer, pointer_dest))
        #self.wait_to(30.5)
        self.play(ShowCreation(jumps[1]))
        for i in range(2,4):
            pointer_dest = pointer.copy()
            pointer_dest.move_to(jumps[i].get_anchors()[0], coor_mask = X_MASK)
            self.play(
                ShowCreation(jumps[i]),
                Transform(pointer, pointer_dest),
                run_time = 0.9,
            )

        fadeout = FadeOut(pointer)
        fadeout.target_mobject.move_to(line.get_anchors()[0], coor_mask = X_MASK)
        self.play(
            fadeout,
            ShowCreation(VGroup(jumps[4:])),
        )

        #self.wait_to(41)
        conversation = Conversation(self, start_answer = True)
        conversation.add_bubble("Proof cannot have infinite number of steps")
        self.dither(2)
        #self.wait_to(54)
        conversation.add_bubble("What? We are doing it all the time.")

        #self.wait_to(59.5)
        self.dither(2)
        self.play(FadeOut(VGroup(
            line,
            line_l,
            jumps,
            conversation.dialog,
        )))

import importlib
chapter2 = importlib.import_module('eost.02-size-comparison-countable-cz')

class CantorTheorem(chapter2.CantorDiagonal):
    def construct(self):

        self.zero = TexMobject('0')
        self.one = TexMobject('1')
        self.h_shift = 0.6*RIGHT
        self.v_shift = 0.8*DOWN
        self.diag_dir = self.h_shift + self.v_shift

        column = VGroup(*[
            TexMobject(str(n)) for n in range(10)
        ])
        for i, num in enumerate(column):
            num.move_to(i*self.v_shift)

        column.to_corner(UP+LEFT)
        column.shift(DOWN)
        column.highlight(GREEN)

        self.matching_l_buff = 0.2
        self.matching_r_buff = 0.7
        self.play(ShowCreation(column))

        matching = []
        for num in column:
            start = num.get_edge_center(RIGHT)+self.matching_l_buff*RIGHT
            end = copy.copy(start)
            end[0] = -SPACE_WIDTH+2.5
            matching.append(Line(start, end))

        self.sequences = VGroup()
        for line in matching:
            seq = self.make_seq()
            self.seq_to_match_line(seq, line)
            self.sequences.submobjects.append(seq)

        #self.wait_to(3.8)
        for line, seq in zip(matching, self.sequences)[:3]:
            self.play(ShowCreation(line), FadeIn(VGroup(seq), submobject_mode = "lagged_start"))

        self.play(
            ShowCreation(VGroup(matching[3:]), submobject_mode = "all_at_once"),
            FadeIn(VGroup(zip(*self.sequences[3:])), submobject_mode = "all_at_once"),
        )

        #self.wait_to(14.3)
        missing_seq = self.apply_diag_argument(times = [18, 23])
        #self.wait_to(41)
        self.dither()

class Riddle(Scene):
    def construct(self):

        line = Line(4*LEFT, 4*RIGHT, color=BLUE).shift(DOWN)
        jumps = make_jumps(3,-4)
        arrow = Arrow(DOWN, UP).shift(3.5*RIGHT)
        arrow.save_state()
        arrow_l = TextMobject("???").next_to(arrow)
        arrow.scale_about_point(0, arrow.get_start())
        jumps_dest = jumps.copy()
        jumps_dest.shift(UP)
        jumps.shift(DOWN)
        jumps_base = jumps.copy()
        jumps.highlight(BLACK)

        self.add(line)
        self.play(
            arrow.restore,
            Transform(jumps, jumps_dest),
            Animation(line),
        )
        #self.wait_to(3)
        self.play(Write(arrow_l))

        #self.wait_to(8.5)

        for jump in jumps_base[:3]:
            self.play(ShowCreation(jump))

        self.play(ShowCreation(VGroup(jumps_base[3:])))

        #self.wait_to(23.5)

        conversation = Conversation(self, start_answer = True)
        conversation.add_bubble("Hint: Use induction instead of recursion")
        #self.wait_to(25.5)

        self.dither(2)
        self.play(FadeOut(VGroup(jumps_base, arrow, arrow_l, jumps)))
        jumps = jumps_base

        first_step = TextMobject("Holds for","$n=0$")
        ind_step = TextMobject("Holds for","$n \Rightarrow n+1$")
        result = TextMobject("Holds for","all $n$")

        VGroup(
            first_step[1][0],
            ind_step[1][0],
            ind_step[1][2:],
            result[1][-1],
        ).highlight(YELLOW)
        first_step.to_corner(UP+LEFT)
        ind_step.to_corner(UP+LEFT).shift(0.8*DOWN)
        result.to_corner(UP+RIGHT)

        #self.wait_to(30)
        self.play(Write(first_step))
        #self.wait_to(33.5)
        self.play(Write(ind_step))
        #self.wait_to(40)
        self.play(
            Transform(first_step.copy(), result),
            Transform(ind_step.copy(), result),
        )
        self.remove(*self.mobjects_from_last_animation)
        self.add(result)

        #self.wait_to(44.5)

        ind_statement = TextMobject("There is a decreasing sequence of size","$n$")
        ind_statement.highlight(ORANGE)
        ind_statement[1].highlight(YELLOW)
        ind_statement.to_corner(UP+LEFT)
        ind_statement.shift(2*DOWN)

        self.play(
            Write(ind_statement),
            VGroup(
                first_step, ind_step, result
            ).set_fill, None, 0.3
        )
        #self.wait_to(52)

        first_tick = IconYes().next_to(first_step, buff = 0.5)
        self.play(first_step.set_fill, None, 1)
        #self.wait_to(54)
        self.play(ShowCreation(first_tick))

        pointer = TrianglePointer(color = YELLOW).scale(-1)
        pointer.next_to(line.get_end(),DOWN, buff=0)
        pointer_dest = pointer.copy()
        pointer.set_fill(opacity=0)
        pointer_dest.next_to(jumps[0].get_anchors()[0], DOWN, buff=0)
        #self.wait_to(56)
        self.play(Transform(pointer, pointer_dest))

        #self.wait_to(58.5)

        jumps_l = TexMobject("n").highlight(YELLOW)
        jumps_l.move_to(VGroup(jumps[:5])).shift(UP)
        self.play(
            first_step.set_fill, None, 0.3,
            ind_step.set_fill, None, 1,
            FadeIn(VGroup(jumps[:5], jumps_l)),
            first_tick.fade, 0.3,
        )

        #self.wait_to(60+1)
        self.play(pointer.next_to, jumps[5].get_anchors()[0], DOWN, 0)
        #self.wait_to(60+3.5)
        self.play(ShowCreation(jumps[5]))
        jumps_l_dest = TexMobject("n+1").highlight(YELLOW)
        jumps_l_dest.move_to(VGroup(jumps[:6])).shift(UP)
        #self.wait_to(60+4.7)
        self.play(Transform(jumps_l, jumps_l_dest))
        #self.wait_to(60+6.5)

        ind_tick = IconYes().next_to(ind_step, buff = 0.5)
        self.play(ShowCreation(ind_tick))

        result_tick = IconYes().next_to(result, LEFT, buff = 0.5)
        #self.wait_to(60+9.2)
        self.play(
            Transform(first_tick, result_tick),
            Transform(ind_tick, result_tick),
            ind_step.set_fill, None, 0.3,
            result.set_fill, None, 1,
        )
        self.remove(first_tick, ind_tick)
        self.add(result_tick)
        #self.wait_to(60+17.5)
        self.dither()

        bubble_anim = conversation.add_bubble_anim("How that helped?")
        self.dither()
        self.play(
            FadeOut(VGroup(line, jumps[:6], jumps_l, pointer)),
            bubble_anim,
        )

        infinite_proof = VGroup([
            TexMobject(str(i), "\\Rightarrow", str(i+1))
            for i in range(11)
        ])
        for i,x in enumerate(infinite_proof):
            VGroup(x[0], x[2]).highlight(YELLOW)
            if i>0:
                x.shift(infinite_proof[i-1][-1].get_center()-x[0].get_center())
                x.remove(x[0])

        infinite_proof.next_to(ind_statement, DOWN, aligned_edge = LEFT)

        #self.wait_to(60+20)
        self.play(Write(infinite_proof[0]))
        #self.wait_to(60+25)
        self.play(Write(infinite_proof[1]))

        #self.wait_to(60+27)
        self.play(
            FadeIn(VGroup(infinite_proof[2:]),
                   submobject_mode = "lagged_start",
                   run_time = 2,
        ))
        #self.wait_to(60+30)
        conversation.add_bubble("Induction is a proof by contradiction")
        #self.wait_to(60+39.5)
        self.dither(2)

class Contradiction(Scene):
    def construct(self):

        seq = self.make_swift_seq()
        rect = SurroundingRectangle(seq, color = YELLOW, buff = 0.25)
        rect_l = TexMobject("\\omega").highlight(YELLOW).next_to(rect, LEFT)
        seq_g = VGroup(seq, rect, rect_l)
        seq_g.to_corner(UP+LEFT)
        self.play(FadeIn(seq_g))
        #self.wait_to(8.5)

        ticks = VGroup([
            IconYes().move_to(obj)
            for obj in seq[0]
        ])
        ticks_fade = VGroup([
            IconYes().move_to(obj)
            for obj in seq[1][1]
        ])
        ticks_fade.gradient_highlight(GREEN, BLACK)
        cross = IconNo().move_to(seq[-1][-8])

        VGroup(ticks, ticks_fade, cross).shift(DOWN)

        conversation = Conversation(self, start_answer = True)
        conversation.add_bubble("Is there a decreasing sequence of your length?")
        self.dither(3)

        #self.wait_to(22.5)
        self.play(ReplacementTransform(seq[0].copy(), ticks))
        #self.wait_to(30)
        seq_g.add(ticks, ticks_fade, cross)

        self.play(seq_g.to_edge, RIGHT, -1.2, run_time = 1.5)
        #self.wait_to(47)

        crosses = VGroup([
            IconNo().move_to(obj)
            for obj in seq[-1][-7:]
        ]).shift(DOWN)
        self.play(ShowCreation(crosses))
        #self.wait_to(52)
        self.play(FadeOut(seq))

        self.remove(ticks, ticks_fade)
        rect_g = VGroup(rect_l, rect)
        rect_dest = Rectangle(height = rect.get_height(), width = 12, color = YELLOW)
        rect_l_dest = rect_l.copy()
        rect_g_dest = VGroup(rect_l_dest, rect_dest).arrange_submobjects()
        rect_g_dest.move_to(rect)
        rect_g_dest.to_edge(LEFT)
        corner_l = rect_dest.get_corner(LEFT+DOWN)
        corner_r = rect_dest.get_corner(RIGHT+DOWN)
        mid = interpolate(corner_l, corner_r, 0.4)

        crosses.add(cross)
        cross = VGroup(cross.copy())
        cross_br = Brace(Line(mid, corner_r), DOWN).highlight(RED)
        cross_br.put_at_tip(cross)
        rect_g.move_to(ORIGIN, coor_mask = X_MASK)

        corner_l_ori = rect_g.get_corner(LEFT+DOWN)
        corner_r_ori = rect_g.get_corner(RIGHT+DOWN)
        mid_ori = interpolate(corner_l_ori, corner_r_ori, 0.1)
        cross_br_ori = Brace(Line(mid_ori, corner_r_ori), DOWN).set_fill(RED,0)

        self.play(
            Transform(rect_g, rect_g_dest),
            ReplacementTransform(cross_br_ori, cross_br),
            ReplacementTransform(crosses, cross)
        )
        #self.wait_to(56)

        tick_br = Brace(Line(corner_l, mid), DOWN).highlight(GREEN)
        tick = IconYes()
        tick_br.put_at_tip(tick)
        self.play(
            FadeIn(tick),
            GrowFromCenter(tick_br),
        )

        split = TexMobject("n-1","n").move_to(rect)
        split[0].highlight(GREEN).next_to(cross_br, LEFT, coor_mask = X_MASK)
        split[1].highlight(RED).next_to(tick_br, RIGHT, coor_mask = X_MASK)

        #self.wait_to(60+5.5)
        self.play(Write(split[1]))
        #self.wait_to(60+11)
        self.play(FadeIn(split[0]))

        split_impl = TexMobject("n-1", "\\Rightarrow", "n")
        VGroup(split_impl[0], split_impl[2]).highlight(GREEN)
        contr_l = TextMobject("Contradiction!").highlight(YELLOW)
        contr = VGroup(split_impl, contr_l).arrange_submobjects(buff = 0.5)

        #self.wait_to(60+16)
        self.play(Write(VGroup(split_impl, contr_l)))
        #self.wait_to(60+30)

        tick_br_dest = Brace(Line(corner_l, corner_r), DOWN).highlight(GREEN)
        tick_dest = tick.copy()
        tick_br_dest.put_at_tip(tick_dest)

        cross_dest = cross.copy()
        cross_dest.move_to(corner_r, coor_mask = X_MASK)
        cross_dest.highlight(BLACK)
        self.play(
            cross_br.stretch_about_point, 0,0,corner_r,
            Transform(cross, cross_dest),
            Transform(tick_br, tick_br_dest),
            Transform(tick, tick_dest),
            FadeOut(split)
        )
        #self.wait_to(60+38.5)
        self.play(FadeOut(conversation.dialog))
        conversation1 = Conversation(self)
        conversation2 = Conversation(self, start_answer = True)
        conversation1.add_bubble("Done?")
        #self.wait_to(60+43)
        self.dither()
        conversation2.add_bubble("Not by far")
        #self.wait_to(60+52)
        self.dither(2)

    def make_swift_seq(self,
                       dist1 = 1,
                       dist2 = 1.2,
                       no_blur = 13,
                       grad = 20,
                       blur_len = 10,
                       next_start = 653,
                       blur_col = DARK_GRAY):

        ini_segment = [
            TexMobject(str(i)).shift(i*dist1*RIGHT)
            for i in range(no_blur+grad)
        ]
        blur_h = ini_segment[0].get_height()
        ini_no_blur_segment = VGroup(ini_segment[:no_blur])
        ini_gradient = VGroup([
            Rectangle(
                width = dist1,
                height = blur_h,
                stroke_width = 0,
                fill_opacity = 1,
            ).shift(i*RIGHT*dist1)
            for i in range(no_blur, no_blur+grad)
        ])
        ini_gradient.gradient_highlight(BLACK, blur_col)
        ini_blur_segment = VGroup(ini_segment[no_blur:])
        for opacity,obj in zip(np.linspace(1,0,grad), ini_blur_segment):
            obj.set_fill(opacity = opacity)

        mid_blur = Rectangle(
            width = blur_len,
            height = blur_h,
            fill_opacity = 1,
            color = blur_col,
            stroke_width = 0,
        )

        term_segment = VGroup([
            TexMobject(str(i+next_start)).shift(i*dist2*RIGHT)
            for i in range(grad+no_blur)
        ])
        term_gradient = VGroup([
            Rectangle(
                width = dist2,
                height = blur_h,
                stroke_width = 0,
                fill_opacity = 1,
            ).shift(i*RIGHT*dist2)
            for i in range(0, grad)
        ])
        term_gradient.gradient_highlight(blur_col, BLACK)
        term_blur_segment = VGroup(term_segment[:grad])
        term_no_blur_segment = VGroup(term_segment[grad:])

        for opacity,obj in zip(np.linspace(0,1,grad), term_blur_segment):
            obj.set_fill(opacity = opacity)

        mid_blur.next_to(ini_gradient, buff = 0)
        VGroup(term_gradient, term_segment).next_to(mid_blur,buff = 0)

        return VGroup(
            ini_no_blur_segment,
            [ini_gradient, ini_blur_segment],
            mid_blur,
            [term_gradient, term_blur_segment],
            term_no_blur_segment
        )

class Crisis(Scene):
    def construct(self):

        numbers = VGroup([
            TexMobject(str(i))
            for i in range(9)
        ]).arrange_submobjects(DOWN, buff = 0.5)
        num_rect = SurroundingRectangle(numbers, buff = 0.3)

        VGroup(numbers, num_rect).to_corner(UP+RIGHT)

        self.play(FadeIn(numbers, submobject_mode = "lagged_start"))
        jumps = make_jumps(3,-4)
        jumps[0].insert_n_anchor_points(1)

        subjumps = VGroup([
            VGroup(jumps[:i]).copy().next_to(numbers[i], LEFT, buff = 1)
            for i in range(1,len(numbers))
        ])

        #self.wait_to(5)
        self.play(
            *map(ShowCreation, subjumps)
        )

        #self.wait_to(19.5)

        base_rect = SurroundingRectangle(subjumps[-1], color = GREEN)
        self.x1 = subjumps[-1].get_corner(LEFT+DOWN)[0]
        self.x2 = subjumps[-1].get_corner(RIGHT+DOWN)[0]

        sets = VGroup([
            base_rect.copy().move_to(number, coor_mask = Y_MASK)
            for number in numbers
        ])

        cur_set = sets[4]
        self.play(ShowCreation(cur_set))

        ##self.wait_to(24)
        for _ in range(3):
            cur_jumps = subjumps[3]
            jumps_dest = self.random_jumps(cur_jumps.copy())
            self.play(Transform(cur_jumps, jumps_dest))

        reg_jumps = subjumps.copy()
        for i,jumps in enumerate(reg_jumps):
            jumps.highlight(BLUE)
            self.stretch_jumps(jumps, np.linspace(self.x1, self.x2, i+4)[1:-1])

        self.play(Transform(cur_jumps, reg_jumps[3]))

        #self.wait_to(28)
        self.play(
            FadeIn(VGroup(sets[:4], sets[5:])),
            Transform(subjumps, reg_jumps),
        )

        axioms = VGroup(
            TextMobject("Replacement"),
            TextMobject("Choice"),
        )
        axioms.arrange_submobjects(DOWN, aligned_edge = LEFT)
        axioms.to_corner(UP+LEFT)

        #self.wait_to(39.5)
        self.play(Write(axioms[0]))
        
        #self.wait_to(42)
        self.play(FadeIn(num_rect))

        #self.wait_to(44.5)
        sets_rect = SurroundingRectangle(sets, buff = 0.2)
        self.play(ReplacementTransform(num_rect, sets_rect))

        #self.wait_to(51.5)
        self.play(
            axioms[0].highlight, DARK_GREY,
            Write(axioms[1]),
        )
        #self.wait_to(56)
        self.play(
            FadeOut(sets),
            subjumps.highlight, ORANGE,
            submobject_mode = "lagged_start",
        )
        #self.wait_to(60+10)

        jumps = subjumps
        jumps_dest = jumps.copy()
        for seq in jumps_dest: seq.move_to(ORIGIN, coor_mask = Y_MASK)
        #jumps.save_state()

        #self.play(Transform(jumps, jumps_dest))

        #self.wait_to(60+16.4)
        #self.play(jumps.restore)
        self.play(FadeOut(axioms))

        ordinal = OrdinalOmega(x0 = -6.5, x1 = -2)
        ordinal = VGroup([bar[0] for bar in ordinal])
        #self.wait_to(60+26.5)
        self.play(ShowCreation(ordinal))
        one = ordinal[0].copy().next_to(ordinal)
        self.play(ShowCreation(one), run_time = 0.5)
        ordinal.add(one)
        self.ordinal = ordinal

        #self.wait_to(60+30.5)
        self.last_seq = None
        self.show_ordinal_jumps(1)

        #self.wait_to(60+33.3)
        self.show_ordinal_jumps(5)
        self.show_ordinal_jumps(10)
        #self.wait_to(60+39.5)
        self.show_ordinal_jumps(20, 1)

        conversation = Conversation(self)
        #self.wait_to(60+44.5)
        conversation.add_bubble("So we have lost :-(")
        self.dither(2)
        #self.wait_to(60+55.5)
        self.play(
            FadeOut(VGroup(self.ordinal, self.last_seq)),
            conversation.add_bubble_anim("Blame the ambiguity"),
        )
        #self.wait_to(2*60+7)
        self.play(Transform(jumps, jumps_dest), Animation(conversation.dialog))

        self.dither(2)
        #self.wait_to(2*60+17)
        self.play(FadeOut(VGroup(
            numbers,
            sets_rect,
            num_rect,
            jumps,
            conversation.dialog,
        )))

    def show_ordinal_jumps(self, n, first_step_wait = None):
        seq_bars = VGroup([self.ordinal[-1]]+list(reversed(self.ordinal[:n]))).copy()
        seq_jumps = seq_to_jumps(seq_bars, color = dec_seq_color)
        seq_bars.highlight(dec_seq_color)
        if self.last_seq is not None:
            fadeout = [FadeOut(self.last_seq)]
        else:
            fadeout = []

        if first_step_wait is None:
            self.play(*fadeout+[
                ShowCreation(seq_bars),
                ShowCreation(seq_jumps),
            ])
        else:
            self.play(*fadeout+[
                ShowCreation(VGroup(seq_bars[:2])),
                ShowCreation(seq_jumps[0]),
            ])
            self.play(
                ShowCreation(VGroup(seq_bars[2:])),
                ShowCreation(VGroup(seq_jumps[1:])),
            )

        self.last_seq = VGroup(seq_bars, seq_jumps)

    def random_jumps(self, jumps, min_len = 0.4):
        n = len(jumps)+1
        x_seq = np.random.random(n)
        x_seq.sort()
        x_seq *= (self.x2-self.x1) - min_len*(n-1)
        x_seq = [
            self.x1 + x + min_len*i
            for i,x in enumerate(x_seq)
        ]
        self.stretch_jumps(jumps, x_seq)

        return jumps

    def stretch_jumps(self, jumps, x_seq):
        for x1,x2,jump in zip(x_seq[:-1], x_seq[1:], reversed(jumps)):
            jump.stretch_to_fit_width(x2-x1)
            jump.move_to((x1+x2)/2, coor_mask = X_MASK)

class RealExample(Scene):
    def construct(self):

        line = NumberLine()
        line.add_numbers()
        line_shift = DOWN
        line.shift(line_shift)
        self.play(ShowCreation(line))
        #self.wait_to(3)

        rule_t = TextMobject("Rules").highlight(YELLOW)
        rule1 = TextMobject("Start: 4")
        rule2 = TexMobject("x\\to\\frac x2")
        VGroup(
            rule1[-1],
            rule2[0],
            rule2[-3:],
        ).highlight(ORANGE)
        rules = VGroup(rule_t, rule1, rule2).arrange_submobjects(DOWN, buff = 0.5)
        rule_rect = SurroundingRectangle(rules, buff = 0.2)
        rules.add(rule_rect)
        rules.to_corner(UP+LEFT)

        self.play(
            Write(rule_t),
            ShowCreation(rule_rect)
        )
        #self.wait_to(8)
        self.play(Write(rule1))
        self.play(Write(rule2))

        jumps = make_jumps(4,0,0.5)
        jumps[0].insert_n_anchor_points(1)
        jumps.shift(line_shift)

        numbers = VGroup([
            TexMobject(str(i))
            for i in range(1,7)
        ]).arrange_submobjects(DOWN, buff = 1)
        VGroup(numbers).to_corner(UP+RIGHT, buff = 1)

        subjumps = VGroup([
            VGroup(jumps[:i+1]).copy().move_to(numbers[i], coor_mask = Y_MASK)
            for i,num in enumerate(numbers)
        ])

        #self.wait_to(15)
        for i in range(2):
            cur_jumps = VGroup(jumps[:i+1]).copy()

            #if i == 1: self.wait_to(23)
            for jump in cur_jumps:
                self.play(ShowCreation(jump))

            #if i == 0: self.wait_to(20)
            self.play(
                ReplacementTransform(cur_jumps, subjumps[i]),
                FadeIn(numbers[i]),
            )

        self.play(
            line.behind_edge, DOWN,
            FadeIn(VGroup(subjumps[2:], submobject_mode = "lagged_start")),
            FadeIn(VGroup(numbers[2:], submobject_mode = "lagged_start")),
        )

        jumps_rect = SurroundingRectangle(subjumps, buff = 0.5)
        jumps.next_to(subjumps, DOWN, aligned_edge = RIGHT)
        subjumps.add(jumps)
        #self.wait_to(29)
        self.play(ShowCreation(jumps_rect))
        #self.wait_to(36)

        jumps_dest = subjumps.copy()
        for seq in jumps_dest:
            seq.move_to(ORIGIN, coor_mask = Y_MASK)

        omega = VGroup(TexMobject("\\omega"))
        omega.move_to(numbers, coor_mask = X_MASK)
        self.play(
            Transform(subjumps, jumps_dest),
            ReplacementTransform(numbers, omega),
        )
        self.remove(subjumps)
        self.add(jumps)

        #self.wait_to(42.5)

        conversation = Conversation(self)
        conversation.add_bubble("What to do in the general case?")
        self.dither(2)

        #self.wait_to(57)
        conversation.add_bubble("Use the Axiom of Choice.")
        self.dither(2)
        #self.wait_to(60+6)

class AxiomOfChoice(Scene):
    def construct(self):

        self.line_start_x = -4
        self.line_end_x = 4
        self.line_len = self.line_end_x - self.line_start_x
        self.point_num = 29
        self.point_dist = float(self.line_len)/(self.point_num+1)
        #self.jump_dist = self.point_dist/2
        self.jump_dist = self.point_dist

        line = Line(self.line_start_x*RIGHT, self.line_end_x*RIGHT, color = BLUE)
        self.play(ShowCreation(line))

        dot = Dot(2*RIGHT, color = BLUE)
        #self.wait_to(3.5)
        self.play(dot.shift, UP)

        dec_jumps = self.make_jumps_from(dot)
        self.add_foreground_mobjects(dot)
        #self.wait_to(5)
        self.play(ShowCreation(dec_jumps, submobject_mode = "all_at_once"))
        for jump in dec_jumps:
            jump.points = jump.points[::-1]

        ini_line = Line(self.line_start_x*RIGHT,
                        dot.get_center()*X_MASK,
                        color = dec_seq_color).move_to(dot, coor_mask = Y_MASK)
        self.play(
            Uncreate(dec_jumps, submobject_mode = "all_at_once"),
            FadeIn(ini_line),
        )
        self.play(FadeOut(VGroup(ini_line, dot)))

        points = np.linspace(line.get_start()[0], line.get_end()[0], self.point_num+2)
        points = points[1:-1]
        y = line.get_center()[1]
        points = np.array([
            [x, y, 0] for x in points
        ])
        dots = VGroup([ Dot(p, color = BLUE) for p in points ])

        #self.wait_to(9.5)
        self.add_foreground_mobjects(dots)
        self.play(FadeOut(line))
        line.highlight(DARK_GREY)

        dots_dest = dots.copy()
        for i,dot in enumerate(dots_dest):
            dot.shift(UP*i)
        dots_dest.move_to(ORIGIN, coor_mask = Y_MASK)
        lines = VGroup([
            line.copy().move_to(dot, coor_mask = Y_MASK)
            for dot in dots_dest
        ])
        line.set_stroke(width = 0)
        #self.wait_to(11.5)
        self.play(
            ReplacementTransform(VGroup(line), lines),
            Transform(dots, dots_dest),
        )
        self.remove(lines[0], dots[0])
        lines.remove(lines[0])
        dots.remove(dots[0])

        dec_jumps = VGroup([
            self.make_jumps_from(dot)
            for dot in dots
        ])
        #self.wait_to(14)
        self.play(ShowCreation(dec_jumps, submobject_mode = "all_at_once"))

        ac_title = TextMobject("Axiom\\\\of Choice", alignment="\\raggedright")
        ac_title.to_corner(DOWN+LEFT)

        #for row in dec_jumps:
        #    print(len(row))
        sel_index = [
            np.random.randint(0, len(row))
            for row in dec_jumps
        ]

        #i = len(dots)-2
        #while i > 0:
        #    if sel_index[i] % 2 == 0:
        #        if sel_index[i] > 1: sel_index[i] -= 1
        #        else: sel_index[i] += 1
        #    i -= (sel_index[i]+1)/2
        i = len(dots)-2
        while i > 0:
            if sel_index[i] >= i/2:
                sel_index[i] = i//3
            i -= 1+sel_index[i]

        selected = VGroup([
            row[i]
            for row, i in zip(dec_jumps, sel_index)
        ])
        unselected = VGroup([
            [line]+row[:i]+row[i+1:]
            for line, row, i in zip(lines, dec_jumps, sel_index)
        ])
        #self.wait_to(19)
        self.play(
            Write(ac_title),
            unselected.highlight, DARK_GREY,
            selected.highlight, YELLOW,
        )

        rect = Rectangle(
            width = SPACE_WIDTH*2+0.5,
            height = dec_jumps.get_height()+1,
            color = GREEN,
        )
        rules_t = TextMobject("Rules").highlight(GREEN)
        rules_t.to_corner(UP+LEFT, buff = 0.5)
        dots_dest = dots.copy()
        selected_dest = selected.copy() # .highlight(ORANGE)
        unselected_dest = unselected.copy().highlight(BLACK)
        for jump in selected_dest:
            jump.insert_n_anchor_points(1)

        for dot, sel, unsel in zip(dots_dest, selected_dest, unselected_dest):
            shift = dot.get_center()*Y_MASK*(-0.97)
            VGroup(dot, sel, unsel).shift(shift)

        VGroup(dots_dest, selected_dest, unselected_dest).to_edge(UP, buff = 0.5)

        rec_start = TrianglePointer().scale(-1).highlight(YELLOW)
        rec_start.next_to(dots_dest[-2], DOWN, buff = 0.1)
        rec_start = VGroup([
            rec_start,
            TextMobject("Start").next_to(rec_start, aligned_edge = UP),
        ])

        rect_dest = SurroundingRectangle(VGroup(
            dots_dest, selected_dest, rules_t, rec_start,
        ), buff = 0.2, color = GREEN)
        #self.wait_to(25)
        self.play(
            FadeIn(rules_t),
            FadeOut(ac_title),
            Transform(unselected, unselected_dest),
            Transform(selected, selected_dest),
            Transform(dots, dots_dest),
            Transform(rect, rect_dest),
        )

        rec_start[0].save_state()
        rec_start[0].shift(0.5*DOWN)
        rec_start[0].set_fill(opacity = 0)

        #self.wait_to(29.5)
        self.play(
            rec_start[0].restore,
            FadeIn(rec_start[1]),
        )

        index = len(selected)-2
        dot = rec_start[0].copy()
        self.foreground_mobjects = []

        #self.wait_to(37)

        jumps = []
        play_jump = True
        for i in range(10):
            if play_jump:
                dot_dest = dots[index].copy().highlight(ORANGE)
                self.play(Transform(dot, dot_dest), rate_func = rush_into, run_time = 0.7)

            jump = selected[index].copy().highlight(ORANGE)
            jump.insert_n_anchor_points(1)
            jumps.append([jump])
            if play_jump:
                self.play(ShowCreation(jump), rate_func = rush_from, run_time = 0.7)
                self.remove(dot)
            shift = -jump.points[0]*Y_MASK

            if play_jump:
                self.play(jump.shift, shift)
            else:
                jump.shift(shift)
                jump.set_stroke(width = 0)

            if index == 0: break
            index -= 1+sel_index[index]
            if i == 3: play_jump = False
            if play_jump:
                dot = Dot(jump.points[-1])
                dot.set_fill(ORANGE, 0)

        jumps = VGroup(jumps)
        jumps_inf = jumps.copy()

        #self.wait_to(48)

        numbers = VGroup([
            TexMobject(str(i+1))
            for i in range(7)
        ]).arrange_submobjects(DOWN, buff = 0.5)
        
        numbers.next_to(rect, DOWN, buff = 0.5)
        numbers.next_to(jumps, buff = 1, coor_mask = X_MASK)

        jumps_dest = []
        for i,[jump] in enumerate(jumps):
            cur_numbers = numbers[i:]
            if len(cur_numbers) == 0: cur_numbers = [numbers[-1]]
            jump_dest = [
                jump.copy().next_to(num, coor_mask = Y_MASK, aligned_edge = DOWN)
                for num in cur_numbers
            ]
            jumps_dest.append(jump_dest)
        jumps_dest = VGroup(jumps_dest)
        jumps_dest.set_stroke(width = DEFAULT_POINT_THICKNESS)
        self.play(
            Transform(jumps, jumps_dest),
            FadeIn(numbers),
        )

        for _ in range(5):
            jump = jumps_inf[-1].copy().scale(0.5)
            jump.next_to(jumps_inf, LEFT, buff = 0, coor_mask = X_MASK)
            jumps_inf.add(jump)

        for jump in jumps_inf:
            stroke = min(4, np.sqrt(jump.get_width())*4)
            jump.set_stroke(width = stroke)
        jumps_inf.shift(DOWN)

        jumps_inf_src = jumps_inf.copy()
        jumps_inf_src.next_to(jumps, DOWN, coor_mask = Y_MASK)
        for [jump], jump_col in zip(jumps_inf_src, jumps):
            jump_col.add(jump)
        jumps.add(*jumps_inf_src[len(jumps):])

        jumps_rect = SurroundingRectangle(jumps, buff = 0.3)

        #self.wait_to(58)
        self.play(ShowCreation(jumps_rect))
        self.dither(2)

        omega = VGroup(TexMobject("\\omega")).move_to(numbers)
        omega.move_to(jumps_inf, coor_mask = Y_MASK)
        #self.wait_to(60+7.5)
        self.play(
            ReplacementTransform(numbers, omega),
            ReplacementTransform(jumps, jumps_inf),
        )
        self.dither(2)
        #self.wait_to(60+36)

    def make_jumps_from(self, obj):
        start = obj.get_center()
        start_x = start[0]
        line_y = start[1]
        jump_num = (start_x - self.line_start_x)/self.jump_dist
        jump_num = 1+int(jump_num+0.5)
        points_x = np.linspace(start_x, self.line_start_x,
                               jump_num)
        points_x = points_x[1:-1]
        points = np.array([
            [x, line_y, 0] for x in points_x
        ])
        lens = [
            start_x - x
            for x in points_x
        ]

        jumps = []
        for p,l in zip(points,lens):
            jump = StepCurve(start = start, end = p, y_handle = min(1.0/l, 0.25))
            jump.highlight(dec_seq_color)
            jumps.append(jump)

        return VGroup(jumps)

class Summary(Scene):
    def construct(self):

        title = TextMobject("Recursion").to_edge(UP).scale(1.2)
        title.to_edge(UP)
        self.add(title)

        seq = make_jumps(5, -5)
        seq[0].insert_n_anchor_points(1)
        seq.next_to(title, DOWN)
        self.play(ShowCreation(seq))

        ind_title = TextMobject("Induction")
        ind_subtitle = TextMobject("$=$ proof by contradiction")
        ind_ordinal = OrdinalOmega(x0 = -3, x1 = 3)
        ind_pointer = TrianglePointer().scale(-1).highlight(RED)
        ind_group = VGroup(ind_title, ind_subtitle, ind_ordinal, ind_pointer)
        ind_group.arrange_submobjects(DOWN)
        ind_rect = SurroundingRectangle(ind_group, color = WHITE)
        ind_rect.stretch_in_place(1.2,0)
        ind_group.add(ind_rect)
        ind_group.to_corner(DOWN+RIGHT)

        unique_rules = TextMobject("Unique\\\\instructions").to_corner(LEFT+DOWN)
        axiom_of_choice = TextMobject("Axiom\\\\of Choice")
        axiom_of_choice.next_to(unique_rules, UP, buff = 1.5)

        p0 = ind_title.get_edge_center(UP)
        p1 = seq.get_edge_center(DOWN)
        p1 = p0*X_MASK + p1*Y_MASK
        arrow_ind = Arrow(p0,p1)

        p0 = unique_rules.get_edge_center(RIGHT)
        p1 = ind_rect.get_edge_center(LEFT)
        p1 = p0*Y_MASK + p1*X_MASK
        arrow_uniq = Arrow(p0,p1)

        p0 = axiom_of_choice.get_edge_center(DOWN)
        p1 = unique_rules.get_edge_center(UP)
        arrow_ac = Arrow(p0,p1)

        #self.wait_to(5)
        self.play(
            FadeIn(ind_title),
            ShowCreation(arrow_ind),
        )
        self.remove(seq)
        seq_begin = 4
        for jump in seq[:seq_begin]:
            self.play(ShowCreation(jump))

        self.play(
            FadeIn(ind_subtitle),
            FadeIn(ind_ordinal),
            ShowCreation(ind_rect),
        )
        #self.wait_to(13.5)
        red_split = 10
        VGroup(ind_ordinal[:red_split]).highlight(GREEN)
        VGroup(ind_ordinal[red_split:]).highlight(RED)
        ind_pointer.move_to(ind_ordinal[red_split], coor_mask = X_MASK)
        ind_pointer.save_state()
        ind_pointer.move_to(ind_ordinal[-1], coor_mask = X_MASK)
        ind_pointer.set_fill(opacity = 0)
        #self.wait_to(16)
        self.play(ind_pointer.restore)

        ind_ordinal3 = OrdinalFiniteProd(OrdinalOmega, 3, x0 = -3, x1 = 3)
        ind_ordinal3.shift(
            ind_ordinal[0].get_center() - ind_ordinal3[0][0].get_center()
        )
        ind_ordinal3_src = VGroup(ind_ordinal3[1:]).copy()
        ind_ordinal3_src.scale_about_point(0, ind_ordinal3.get_edge_center(RIGHT))
        ind_ordinal3_src.add_to_back(ind_ordinal.copy())
        #self.wait_to(24.5)
        self.remove(ind_ordinal)
        self.play(
            ReplacementTransform(ind_ordinal3_src, ind_ordinal3)
        )

        red_split = 3
        VGroup(ind_ordinal3[0], ind_ordinal3[1][:red_split]).highlight(GREEN)
        VGroup(ind_ordinal3[2], ind_ordinal3[1][red_split:]).highlight(RED)
        pointer_dest = ind_pointer.copy()
        pointer_dest.move_to(ind_ordinal3_src[1][red_split], coor_mask = X_MASK)
        self.play(Transform(ind_pointer, pointer_dest))

        #self.wait_to(35.5)
        self.play(ShowCreation(VGroup(seq[seq_begin:])))

        last_bar = ind_ordinal[0].copy().next_to(ind_ordinal)
        ind_group.add(last_bar)
        last_bar.highlight(RED)
        ind_ordinal.highlight(GREEN)
        pointer_dest = ind_pointer.copy()
        pointer_dest.move_to(last_bar, coor_mask = X_MASK)

        #self.wait_to(38.5)
        self.play(
            ReplacementTransform(ind_ordinal3[0], ind_ordinal),
            ReplacementTransform(
                VGroup(ind_ordinal3[1:]),
                VGroup([[last_bar]]),
            ),
            Transform(ind_pointer, pointer_dest),
        )

        #self.wait_to(50)
        self.play(
            FadeIn(unique_rules),
            ShowCreation(arrow_uniq),
        )
        #self.wait_to(56)
        self.play(
            FadeIn(axiom_of_choice),
            ShowCreation(arrow_ac),
        )

        scale = 0.5
        rect = Rectangle(width = 2.1*SPACE_WIDTH, height = 2.1*SPACE_HEIGHT)
        rect.set_fill(BLACK, opacity = 0)

        picture = VGroup(
            seq, arrow_ind, ind_group,
            arrow_uniq, unique_rules,
            arrow_ac, axiom_of_choice,
        )
        rect_dest = rect.copy().scale(scale)
        rect_dest.set_fill(BLACK, 0.9)

        label = TextMobject("(transfinite)", "Recursion", "with choice")
        label.scale(1.2)
        label.arrange_submobjects(DOWN)
        label_src = VGroup(label[0].copy(), title, label[2].copy())
        label_src[0].set_fill(opacity = 0)
        label_src[0].next_to(title, UP)
        label_src[2].set_fill(opacity = 0)
        label_src[2].next_to(title, DOWN)

        #self.wait_to(60+4.5)
        self.dither(3)
        self.play(
            picture.scale, scale,
            Transform(rect, rect_dest),
            ReplacementTransform(label_src, label),
            run_time = 2,
        )
        self.dither()
        #self.wait_to(60+23)

class NextChapter(Scene):
    def construct(self):

        color_A, color_B = RED, BLUE
        
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

        labels = VGroup(label_A, label_B)
        self.add(box1)
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

        self.remove(labels)
        self.play(
            ReplacementTransform(lines_src, lines_boxes),
            ReplacementTransform(layers_boxes_src, layers_boxes),
            ReplacementTransform(boxes_mid, boxes_mid_dest),
            run_time = 2,
        )
        layers_boxes[2].submobjects = layer2_ori

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
            line = lines_boxes[line_index].copy()
            self.add(line)
            lines_boxes[line_index].highlight(WHITE)
            self.play(
                Transform(small_box, layers_boxes_light[layer_index][box_index]),
                ShowCreation(lines_boxes[line_index])
            )
            self.remove(line)

            last_code = layers_code[layer_index-1][last_box_index]
            code = layers_code[layer_index][box_index]
            mline_index = 0
            for c1,c2 in zip(last_code, code):
                if c2 == '-': continue
                if c1 == '-': break
                mline_index += 1

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


        VGroup(lines_dots, layers_dots).move_to(layers_boxes)
        self.play(
            ReplacementTransform(lines_boxes, lines_dots),
            ReplacementTransform(layers_boxes, layers_dots),
            run_time = 2,
        )
        poset = VGroup(layers_dots, lines_dots)
        self.play(poset.shift, 4*DOWN)

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

        shift = DOWN*ordinal.get_height()
        ordinal.shift(shift)
        picture = VGroup(
            poset, seq, first_bar, limit_dot
        )
        self.play(picture.shift, shift)
        self.remove(poset)
        picture.remove(poset)
        self.add_foreground_mobjects(limit_dot)
        self.play(
            ordinal.creation_anim()
        )
        maximum_dot = Dot(ordinal.get_edge_center(UP), color = GREEN)
        maximum_l = TextMobject("Maximum")
        maximum_l.next_to(maximum_dot, UP, aligned_edge = LEFT)
        self.play(
            GrowFromCenter(maximum_dot),
            FadeIn(maximum_l, submobject_mode = "lagged_start"),
        )
        self.dither(2)
        #self.wait_to(20)

    def make_matching(self, code, mikro = True):

        color_A, color_B = RED, BLUE

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
