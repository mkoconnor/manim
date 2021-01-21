#!/usr/bin/env python
# coding: utf-8

from scene import Scene
from eost.ordinal import *
from topics.runners import *
from topics.icons import *
from topics.common_scenes import OpeningTitle, OpeningQuote
from topics.objects import BraceDesc, Counter

class Chapter6OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 6\\\\ Ordinální aritmetika",
    }
class Chapter6OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Želva si byla vědoma své pomalosti,\\\\ale bez ustání běžela.",
        ],
        "author" : "Ezop",
    }

class Chapter5Recap(Scene):

    def construct(self):

        ordinal = OrdinalFiniteProd(OrdinalOmega, 2, x1 = 12)
        VGroup(*ordinal[1][3:]).highlight(DARK_GREY)
        ordinal.shift(2*LEFT + DOWN)
        self.play(FadeIn(ordinal))
        self.wait_to(4)

        brace_desc = TexMobject("\\omega+3")
        brace = Brace(VGroup(ordinal[0][0], ordinal[1][2]), DOWN)
        brace.put_at_tip(brace_desc)

        self.play(GrowFromCenter(brace), FadeIn(brace_desc))
        self.wait_to(8)

        bar = ordinal[1][3].copy().highlight(YELLOW)
        pointer = TrianglePointer(color = YELLOW).next_to(bar, UP)
        pointer_desc = brace_desc.copy().next_to(pointer, UP)
        self.play(ShowCreation(bar),
                  ShowCreation(pointer),
                  FadeIn(pointer_desc))
        self.wait_to(16)

        cur_topics = VGroup(
            TextMobject("Sčítání:", "$\\alpha+\\beta$"),
            TextMobject("Násobení:", "$\\alpha\\cdot\\beta$"),
        )
        cur_topics.arrange_submobjects(DOWN, aligned_edge=LEFT)
        cur_topics.to_corner(UP+LEFT)

        last_topics = VGroup(
            TextMobject("Následník:", "$\\alpha+1$"),
            TextMobject("Supremum:", "$\\sup_{i\in I}(\\alpha_i)$"),
        )
        last_topics.arrange_submobjects(DOWN, aligned_edge=LEFT)
        last_topics.to_corner(UP+RIGHT)

        for topic in cur_topics.submobjects + last_topics.submobjects:
            topic[1].highlight(BLUE)

        self.play(FadeIn(cur_topics,
                         submobject_mode = "lagged_start"),
                  run_time = 3)
        self.wait_to(21)
        self.play(FadeIn(last_topics,
                         submobject_mode = "lagged_start"),
                  run_time = 3)
        self.wait_to(42.5)

        for i in range(1,4):
            pointer_dest = pointer.copy()
            pointer_dest.next_to(ordinal[1][i], UP)
            pointer_desc_dest = TexMobject("\\omega+"+str(i))
            pointer_desc_dest.next_to(pointer_dest, UP)
            self.play(Transform(pointer, pointer_dest),
                      Transform(pointer_desc, pointer_desc_dest))
            self.dither()
        

class Addition(Scene):
    def construct(self):

        #self.force_skipping()
        omega = OrdinalOmega(x1 = 2).shift(UP+LEFT)
        omega_desc = TexMobject("\\omega").next_to(omega, UP)
        three = OrdinalFinite(3, x0 = 2).shift(UP+RIGHT)
        three_desc = TexMobject("3").next_to(three, UP)
        omega_g = VGroup(omega, omega_desc)
        three_g = VGroup(three, three_desc)

        three_g.highlight(GREEN)
        plus = TexMobject('+')
        plus.move_to((omega.get_edge_center(RIGHT) + three.get_edge_center(LEFT))/2)

        ord_sum = OrdinalSum(OrdinalOmega, 0.75,
                             lambda **kwargs: OrdinalFinite(3, **kwargs))
        ord_sum.shift(2.5*DOWN)
        ord_sum_desc = TexMobject("\\omega+3").next_to(ord_sum, UP)
        ord_sum[1].highlight(GREEN)

        self.play(FadeIn(omega), FadeIn(omega_desc))
        self.play(FadeIn(three), FadeIn(three_desc))
        self.play(Write(plus))
        self.wait_to(5.5)

        self.play(ReplacementTransform(omega.copy(), ord_sum[0]),
                  ReplacementTransform(three.copy(), ord_sum[1]))
        self.play(Write(ord_sum_desc),
                  ord_sum[1].highlight, WHITE)

        self.wait_to(29.5)

        self.play(FadeOut(VGroup(ord_sum, ord_sum_desc)))

        # ------------------------ Reversed order ------------------------
        #self.revert_to_original_skipping_status()

        omega_g_dest = omega_g.copy().shift(three.get_edge_center(RIGHT)
                                            - omega.get_edge_center(RIGHT))
        three_g_dest = three_g.copy().shift(omega.get_edge_center(LEFT)
                                            - three.get_edge_center(LEFT))
        omega_g_dest.highlight(GREEN)
        three_g_dest.highlight(WHITE)

        plus_dest = plus.copy()
        plus_dest.move_to((three_g_dest[0].get_edge_center(RIGHT)
                           + omega_g_dest[0].get_edge_center(LEFT))/2)
        self.play(Transform(plus, plus_dest, path_arc = -np.pi*0.5),
                  Transform(omega_g, omega_g_dest, path_arc = -np.pi*0.6),
                  Transform(three_g, three_g_dest, path_arc = -np.pi*0.8),
        )
        self.wait_to(33.5)

        ord_sum = OrdinalSum(lambda **kwargs: OrdinalFinite(3, **kwargs),
                             0.25, OrdinalOmega)
        ord_sum.shift(2.5*DOWN)
        ord_sum_desc = TexMobject("3+\\omega", "=\\omega").next_to(ord_sum, UP)
        ord_sum[1].highlight(GREEN)

        self.play(ReplacementTransform(omega.copy(), ord_sum[1]),
                  ReplacementTransform(three.copy(), ord_sum[0]))
        self.play(Write(ord_sum_desc[0]))
        self.wait_to(36)

        omega2 = OrdinalOmega()
        ord_sum_dest = VGroup(
            VGroup(*omega2[:3]).copy(),
            LimitSubOrdinal(omega2[3:]).copy(),
        )
        ord_sum_dest.move_to(ord_sum)
        ord_sum_dest.highlight(WHITE)

        self.play(Transform(ord_sum, ord_sum_dest),
                  Write(ord_sum_desc[1]))
        self.wait_to(47.5)

class RunnerScene(Scene):

    def make_short_desc(self, corner, color):
        result = TextMobject(':', '$0$')
        model = result[1].copy()
        model.to_corner(corner)

        result.shift(model.get_center() - result[1].get_center())
        result.set_color(color)
        result[0].set_fill(color = BLACK, opacity = 0)
        return result

    def transformed_desc(self, mobj, new_str):
        next_desc = TextMobject(":", "$"+new_str+"$")
        next_desc.shift(mobj[0][-1].get_center()
                        - next_desc[0].get_center())
        next_desc.set_color(mobj.color)
        return next_desc[1]

    def transform_desc(self, mobj, new_str):
        ori_desc = mobj[1]
        mobj.submobjects[1] = self.transformed_desc(mobj, new_str)
        return ReplacementTransform(ori_desc, mobj[1])

    def change_desc(self, mobj, new_str):
        self.remove(mobj[1])
        mobj.submobjects[1] = self.transformed_desc(mobj, new_str)
        self.add(mobj[1])

    def runner_step(self, runner, desc, index, bar = None, omega_index = 0, new_str = None):
        if bar is None: bar = self.ordinal[omega_index][index]

        if new_str is None:
            new_str = str(index)
            if omega_index > 0:
                if omega_index == 1: new_str = "\\omega+"+new_str
                else: new_str = "\\omega\\cdot"+str(omega_index)+"+"+new_str
                if index == 0: new_str = new_str[:-2]

        return AnimationGroup(
            runner.step_to(bar),
            self.transform_desc(desc, new_str),
        )

    def highlight_bar(self, bar, desc):
        bar_copy = bar.copy()
        self.play(FocusOn2(bar_copy))
        bar_desc = desc[1].copy()
        bar_desc.set_fill(opacity = 0)
        self.play(Transform(bar_copy, bar_desc))
        self.remove(bar_copy)

class TurtlesRace(RunnerScene):
    def introduce_turtles(self, animated = True, ord_copies = 2, wait_time = 0):
        self.ordinal = OrdinalFiniteProd(OrdinalOmega, ord_copies,
                                         x0 = -4.2,
                                         x1 = -4.2+8*ord_copies)

        self.gordon = Turtle()
        self.steve = Turtle(pointer_pos = UP)
        self.gordon_desc = TextMobject("Gordon:", '0').to_corner(LEFT+UP)
        self.steve_desc = TextMobject("Steve:", '0').to_corner(LEFT+DOWN)
        self.steve.set_color(YELLOW)

        self.gordon_desc.set_color(self.gordon.color)
        self.steve_desc.set_color(self.steve.color)

        self.gordon.move_to(self.ordinal[0][0])
        self.steve.move_to(self.ordinal[0][0])

        self.add(self.ordinal)
        self.steve_index = self.gordon_index = 0
        if animated:
            self.wait_to(wait_time)
            self.play(self.gordon.run_in(), self.steve.run_in(),
                      FadeIn(self.gordon_desc), FadeIn(self.steve_desc))
        else: self.add(self.gordon, self.steve, self.gordon_desc, self.steve_desc)

    def construct(self):

        #self.force_skipping()
        self.introduce_turtles()
        self.wait_to(9.5)

        self.play(self.steve_step(3))
        self.wait_to(12)

        self.play(self.steve_step(next_index = "3+1",
                                  bar = self.ordinal[0][4]),
                  self.gordon_step())

        self.wait_to(13.4)
        #self.highlight_bar(self.ordinal[0][0], self.gordon_desc)
        self.play(FocusOn2(self.gordon_desc[1]))
        self.wait_to(15)
        self.play(FocusOn2(self.steve_desc[1]))
        self.wait_to(18.1)
        self.play(self.transform_desc(self.steve_desc, "4"))
        self.wait_to(19.5)
        self.steve_index = 4

        for _ in range(31):
            self.play(self.steve_step(), self.gordon_step(), run_time = 0.5)
        #self.dither()
        # 41

        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0, omega_index = 1))
        self.wait_to(39)
        self.play(self.transform_desc(self.steve_desc, "3+\\omega"))
        self.wait_to(45.5)

        #self.revert_to_original_skipping_status()
        for _ in range(8):
            self.play(self.gordon_step(omega_index = 1),
                      self.steve_step(next_index = "3+\\omega+"+str(self.gordon_index),
                                      bar = self.ordinal[1][self.gordon_index]),
                      run_time = 0.5)
        # 49.5

        steve_desc_dest = self.transformed_desc(self.steve_desc, "3+\\alpha")
        steve_desc_dest.add(
            steve_desc_dest[-1].copy(),
            steve_desc_dest[-1].copy(),
        )
        self.play(
            Transform(self.steve_desc[1], steve_desc_dest),
            self.transform_desc(self.gordon_desc, "\\alpha"),
        )
        formulas = VGroup(
            TexMobject("\\alpha","=","3+\\alpha\\quad", "\\hbox{pro nekonečná $\\alpha$}"),
            TexMobject("\\alpha","<","\\alpha+3"),
        )
        formulas.to_edge(UP)
        formulas.shift(RIGHT)
        formulas[0][0].set_color(GREEN)
        formulas[0][2].set_color(YELLOW)

        self.play(Write(formulas[0]))

        self.wait_to(54)
        self.play(FadeOut(VGroup(self.steve_desc, self.gordon_desc)))

    def steve_step(self, next_index = None, **kwargs):
        if next_index is not None: self.steve_index = next_index
        else: self.steve_index += 1
        return self.runner_step(self.steve, self.steve_desc, self.steve_index, **kwargs)

    def gordon_step(self, next_index = None, **kwargs):
        if next_index is not None: self.gordon_index = next_index
        else: self.gordon_index += 1
        return self.runner_step(self.gordon, self.gordon_desc, self.gordon_index, **kwargs)

class TurtlesRace2(TurtlesRace):

    def make_question(self):
        question = TexMobject("\\alpha","=","\\omega+\\alpha", "?")
        question[0].set_color(GREEN)
        question[2].set_color(YELLOW)
        question.to_edge(UP)

        return question

    def construct(self):
        #self.force_skipping()
        formulas = VGroup(
            TexMobject("\\alpha","=","3+\\alpha\\quad", "\\hbox{pro nekonečná $\\alpha$}"),
            TexMobject("\\alpha","<","\\alpha+3"),
        )
        formulas2 = VGroup(
            TexMobject("\\alpha","=","10+\\alpha\\quad", "\\hbox{pro nekonečná $\\alpha$}"),
            TexMobject("\\alpha","<","\\alpha+10"),
        )
        question = self.make_question()
        for fs in [formulas, formulas2]:
            for formula in fs:
                formula[0].set_color(GREEN)
                formula[2].set_color(YELLOW)
            fs.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = 0.3)

        formulas.to_edge(UP)
        formulas.shift(RIGHT)
        formulas2.shift(formulas[0][0].get_center() - formulas2[0][0].get_center())

        self.add(formulas[0])

        self.introduce_turtles(wait_time = 4)
        #self.dither()
        for _ in range(9):
            self.play(self.steve_step(), self.gordon_step(), run_time = 0.5)

        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0, omega_index = 1))
        #self.dither()
        for _ in range(3):
            self.play(self.steve_step(omega_index = 1))
        self.wait_to(26)

        self.play(Write(formulas[1]))

        self.wait_to(37.5)
        formulas[0][2].add_to_back(formulas[0][2][0].copy())
        formulas[1][2].add(formulas[1][2][-1].copy())
        self.play(ReplacementTransform(formulas, formulas2))
        self.wait_to(42)
        formulas_dest = question.copy()
        formulas_dest[2].add_to_back(formulas_dest[2][0].copy())
        self.play(Transform(formulas2[0], formulas_dest),
                  FadeOut(formulas2[1]))
        self.remove(formulas2)
        self.add(question)

        self.gordon.cur_phase = 1
        self.steve.cur_phase = 1
        self.play(self.steve_step(next_index = 0, omega_index = 1),
                  self.gordon_step(next_index = 0)) # 43
        self.dither() # 44
        for _ in range(4):
            self.play(self.steve_step(omega_index = 1),
                      self.gordon_step(), run_time = 0.5) # 46
        #self.revert_to_original_skipping_status()

        self.play(self.steve_step(next_index = "\\omega+\\omega", bar = self.ordinal[1][-1]),
                  self.gordon_step(next_index = 0, omega_index = 1), run_time = 0.5)

def light_key(mobj):
    if hasattr(mobj, "darken"): return -mobj.darken
    return 0

class TurtlesRace3(TurtlesRace2):

    def construct(self):
        #self.force_skipping()
        self.introduce_turtles(animated = False, ord_copies = 6)
        question = self.make_question()
        self.add(question)
        ordinal_dest = OrdinalFiniteProd(OrdinalOmega, 6,
                                         q = (0.8, 0.9, 0.9),
                                         x0 = self.ordinal.x0,
                                         x1 = 8)
        ordinal_dest.highlight(GREY)
        VGroup(*extract_ordinal_subpowers(ordinal_dest)[1]).highlight(YELLOW)

        self.change_desc(self.gordon_desc, "\\omega")
        self.change_desc(self.steve_desc, "\\omega+\\omega")
        self.gordon.move_to(self.ordinal[1])
        self.steve.move_to(self.ordinal[2])

        self.gordon_index = 1
        self.steve_index = 2
        self.wait_to(2)
        self.play(
            ReplacementTransform(self.ordinal, ordinal_dest),
            self.gordon.move_to, ordinal_dest[self.gordon_index],
            self.steve.move_to, ordinal_dest[self.steve_index],
        )
        self.ordinal = ordinal_dest
        self.wait_to(3.8)
        self.play(self.transform_desc(self.steve_desc, "\\omega\cdot2"))
        self.wait_to(8.5)

        self.play(self.gordon_step(), self.steve_step())
        self.wait_to(23)
        counter = Counter()
        counter.count_from(5, self)
        self.wait_to(30.5)

        ordinal_dest = make_ordinal_power(2, q = (0.8, 0.9, 0.9),
                                          x0 = self.ordinal.x0,
                                          x1 = 4.5)
        subpowers = extract_ordinal_subpowers(ordinal_dest)
        for bar in subpowers[2]:
            bar.highlight(GREY)
            bar.darken = 0.5
        for bar in subpowers[1]:
            bar.highlight(YELLOW)
            bar.darken = 0

        tail = ordinal_dest.copy()
        tail.shift(RIGHT*(self.ordinal.x1 - tail.x0))
        self.ordinal.add(*tail.submobjects)
        ordinal2 = tail.deepcopy()
        ordinal2[0][0].highlight(ORANGE)
        ordinal2.shift(RIGHT*(ordinal2.x1 - ordinal2.x0))
        ordinal2_dest = ordinal2.copy()
        ordinal2_dest.shift(RIGHT*(ordinal_dest.x1
            - ordinal2_dest[0][0].get_center()[0]))

        #self.revert_to_original_skipping_status()
        self.play(
            ReplacementTransform(self.ordinal, ordinal_dest, prepare_families = True),
            ReplacementTransform(ordinal2, ordinal2_dest, prepare_families = True),
            self.gordon.move_to, ordinal_dest[self.gordon_index],
            self.steve.move_to, ordinal_dest[self.steve_index],
            order_f = light_key,
        )
        self.wait_to(40)
        for _ in range(8):
            self.play(self.gordon_step(), self.steve_step(), run_time = 0.5) # 44
        self.play(
            self.gordon_step(index = "\\omega\\cdot\\omega", bar = ordinal2),
            self.steve_step(index = "\\omega\\cdot\\omega", bar = ordinal2),
            run_time = 1) # 45
        self.wait_to(47)
        answer = TexMobject("\\omega\\cdot\\omega", '=',
                            "\\omega+\\omega\cdot\\omega", '?')
        answer.to_edge(UP)
        answer.shift(RIGHT)
        question[2].add(question[2][-1].copy(), question[2][-1].copy())
        answer[0].highlight(GREEN)
        answer[2].highlight(YELLOW)
        answer[3].highlight(BLACK)
        self.play(Transform(question, answer))
        self.wait_to(60 + 0.5)

    def gordon_step(self, index = None, **kwargs):
        if index is None:
            self.gordon_index += 1
            return self.runner_step(self.gordon, self.gordon_desc, 0,
                                    omega_index = self.gordon_index, **kwargs)
        else: return self.runner_step(self.gordon, self.gordon_desc, index, **kwargs)

    def steve_step(self, index = None, **kwargs):
        if index is None:
            self.steve_index += 1
            return self.runner_step(self.steve, self.steve_desc, 0,
                                    omega_index = self.steve_index, **kwargs)
        else: return self.runner_step(self.steve, self.steve_desc, index, **kwargs)

class Multiplication(Scene):
    def construct(self):

        #self.force_skipping()

        omega = OrdinalOmega(x1 = 2).shift(1.5*UP+LEFT)
        omega_desc = TexMobject("\\omega").next_to(omega, UP)
        two = OrdinalFinite(2, x0 = 2).shift(1.5*UP+RIGHT)
        two_desc = TexMobject("2").next_to(two, UP)
        omega_g = VGroup(omega, omega_desc)
        two_g = VGroup(two, two_desc)

        two_g.highlight(GREEN)
        omega[0].highlight(GREEN)
        times = TexMobject('\\cdot').scale(2)
        times.move_to((omega.get_edge_center(RIGHT) + two.get_edge_center(LEFT))/2)

        ord_prod = OrdinalFiniteProd(OrdinalOmega, 2)
        ord_prod.shift(1.5*DOWN)
        ord_prod_desc = TexMobject("\\omega\\cdot 2").next_to(ord_prod, UP)
        green_part = VGroup(ord_prod[0][0], ord_prod[1][0])
        white_part = VGroup(*[
            LimitSubOrdinal(subord[1:])
            for subord in ord_prod
        ])
        green_part.highlight(GREEN)

        self.play(FadeIn(omega), FadeIn(omega_desc))
        self.play(FadeIn(two), FadeIn(two_desc))
        self.wait_to(6)
        self.play(Write(times))
        self.wait_to(7.2)

        self.play(ReplacementTransform(omega.copy(), ord_prod[0]))
        self.wait_to(10)
        self.play(ReplacementTransform(ord_prod[0].copy(), ord_prod[1]),
                  Write(ord_prod_desc))
        self.wait_to(17)
        self.add_foreground_mobjects(green_part)
        self.play(FadeOut(white_part))
        self.wait_to(21.5)

        white_part_dest = white_part.copy()
        for subgreen, subwhite in zip(green_part, white_part):
            subwhite.stretch_about_point(0,0, subgreen.get_center())
        self.play(DelayedAnimGroup(
            Transform(white_part[0], white_part_dest[0]),
            Transform(white_part[1], white_part_dest[1]),
        ))
        self.wait_to(33.4)

        self.play(FadeOut(white_part), FadeOut(green_part), FadeOut(ord_prod_desc))
        self.remove(ord_prod)
        
        # ------------------------ Reversed order ------------------------

        omega_g_dest = omega_g.copy().shift(two.get_edge_center(RIGHT)
                                            - omega.get_edge_center(RIGHT))
        two_g_dest = two_g.copy().shift(omega.get_edge_center(LEFT)
                                        - two.get_edge_center(LEFT))
        omega_g_dest.highlight(GREEN)
        two_g_dest.highlight(WHITE)
        two_g_dest[0][0].highlight(GREEN)

        times_dest = times.copy()
        times_dest.move_to((two_g_dest[0].get_edge_center(RIGHT)
                            + omega_g_dest[0].get_edge_center(LEFT))/2)
        self.play(Transform(times, times_dest, path_arc = -np.pi*0.5),
                  Transform(omega_g, omega_g_dest, path_arc = -np.pi*0.6),
                  Transform(two_g, two_g_dest, path_arc = -np.pi*0.8),
        )
        self.wait_to(36)

        q = (0.93, 0.96, 0.96)
        ord_prod_standardized = OrdinalOmega(q = q).shift(1.5*DOWN)
        ord_prod = ord_prod_standardized.copy()
        green_part = LimitSubOrdinal(ord_prod[0::2])
        white_part = LimitSubOrdinal(ord_prod[1::2])
        white_part_hidden = white_part.copy()
        green_part.highlight(GREEN)
        for green_bar, white_bar, white_bar_hidden in zip(green_part, white_part, white_part_hidden):
            white_bar.scale_in_place(1/q[1])
            white_bar.move_to(0.2*green_bar.get_center() + 0.8*white_bar.get_center())
            white_bar_hidden.scale_in_place(1/q[1])
            white_bar_hidden.move_to(green_bar)

        ord_prod_desc = TexMobject("2\\cdot\\omega", "=\\omega").next_to(ord_prod, UP)

        self.wait_to(39)
        self.play(ReplacementTransform(omega.copy(), green_part))
        self.add_foreground_mobjects(green_part)
        self.wait_to(42.2)
        self.play(ReplacementTransform(white_part_hidden, white_part),
                  Write(ord_prod_desc[0]))
        #self.revert_to_original_skipping_status()
        self.dither()
        self.play(
            Write(ord_prod_desc[1]),
            ReplacementTransform(ord_prod, ord_prod_standardized, run_time = 0.4),
        )
        self.wait_to(53.5)

def make_achiles_ordinal1():
    ordinal = OrdinalFiniteProd(OrdinalOmega, 3, q = (0.8, 0.9, 0.9), x1 = SPACE_WIDTH+2)
    ordinal.set_color(GREY)
    VGroup(*extract_ordinal_subpowers(ordinal)[1]).highlight(YELLOW)
    return ordinal

def make_achiles_question():
    question = TexMobject('\\alpha', '=', '\\omega\\cdot\\alpha', '?')
    question[0].set_color(GREEN)
    question[2].set_color(ORANGE)
    question.to_corner(UP+RIGHT)
    return question

class TurtleRabbitRace(RunnerScene):

    def construct(self):

        #self.force_skipping()
        
        self.ordinal = OrdinalFiniteProd(OrdinalOmega, 3, x1 = 24)
        self.turtle = Turtle().move_to(self.ordinal[0])
        self.rabbit = Rabbit(pointer_pos = UP).move_to(self.ordinal[0])

        self.turtle_desc = self.make_short_desc(LEFT+UP, self.turtle.color)
        self.rabbit_desc = self.make_short_desc(LEFT+DOWN, self.rabbit.color)

        self.add(self.ordinal)
        self.play(self.turtle.run_in(), self.rabbit.run_in(),
                  FadeIn(self.turtle_desc), FadeIn(self.rabbit_desc))
        self.wait_to(6.5)
        self.turtle_index = self.rabbit_index = 0

        self.omega_index = 0
        self.play(self.global_step(expand_rabbit = True))
        self.wait_to(21.3)
        self.play(FocusOn2(self.turtle_desc[1]))
        self.wait_to(22.8)
        self.play(FocusOn2(self.rabbit_desc[1]))
        self.wait_to(24.8)
        self.play(self.global_step(expand_rabbit = True, step_num = 2))
        self.wait_to(26.5)
        self.play(FocusOn2(self.turtle_desc[1]))
        self.wait_to(28)
        self.play(self.transform_desc(self.rabbit_desc, '6'))
        self.wait_to(29.9)
        for _ in range(11):
            self.play(self.global_step()) # 45.9 
        self.play(self.global_step(limit = True, expand_rabbit = True))
        self.wait_to(43.5)
        formula = TexMobject("\\omega","=","2\\cdot\\omega\\quad")
        formula[0].set_color(self.turtle.color)
        formula[2].set_color(self.rabbit.color)
        formula.to_edge(UP)
        #self.revert_to_original_skipping_status()
        self.play(Write(formula))
        self.wait_to(52.8)
        self.play(VGroup(self.rabbit, self.turtle, self.ordinal).shift, 9*LEFT) # 58.8
        self.play(self.global_step())
        self.wait_to(58.5)
        for _ in range(6):
            self.play(self.global_step())
        self.play(self.global_step(limit = True))
        self.wait_to(60 + 7.7)
        formula2 = TexMobject("\\alpha","=","2\\cdot\\alpha\\quad","\hbox{pro limitní $\\alpha$}")
        formula2[0].set_color(self.turtle.color)
        formula2[2].set_color(self.rabbit.color)
        formula2.shift(formula[0].get_center() - formula2[0].get_center())
        self.play(Transform(formula, VGroup(*formula2[:3])),
                  Write(formula2[3]))
        self.remove(formula)
        self.add(formula2)
        self.wait_to(60 + 32)
        ordinal2 = make_achiles_ordinal1()
        self.play(FadeOut(VGroup(self.turtle, self.rabbit, self.turtle_desc, self.rabbit_desc, formula2)),
                  ReplacementTransform(self.ordinal, ordinal2))
        self.wait_to(60 + 37)

    def global_step(self, limit = False, step_num = 1, expand_rabbit = False):

        if limit:
            self.omega_index += step_num
            self.rabbit_index = self.turtle_index = 0
        else:
            self.rabbit_index += 2*step_num
            self.turtle_index += 1*step_num

        turtle_anim = self.runner_step(self.turtle, self.turtle_desc, self.turtle_index,
                                       omega_index = self.omega_index)
        new_str = None
        if expand_rabbit:
            new_str = self.turtle_desc[1].tex_string[1:-1]
            if self.turtle_index > 0 and self.omega_index > 0:
                new_str = "("+new_str+")"
            new_str = "2\\cdot"+new_str

        rabbit_anim = self.runner_step(self.rabbit, self.rabbit_desc, self.rabbit_index,
                                       omega_index = self.omega_index, new_str = new_str)

        return AnimationGroup(turtle_anim, rabbit_anim)

class AchilesScene(Scene):

    def construct(self):

        self.ordinal = make_achiles_ordinal1()
        achiles = Achiles(pointer_pos = UP).move_to(self.ordinal)
        self.add(self.ordinal)
        omega_mul = [
            TexMobject("\\omega\\cdot "+str(i)).next_to(subord[0], UP)
            for i,subord in enumerate(self.ordinal)
        ]

        self.play(achiles.run_in())
        self.wait_to(5)
        self.play(Write(omega_mul[0]))
        self.wait_to(7.5)
        self.play(achiles.step_to(self.ordinal[1]))
        self.play(Write(omega_mul[1]))
        self.wait_to(11)
        self.play(achiles.step_to(self.ordinal[2]))
        self.play(Write(omega_mul[2]))
        self.wait_to(20)
        self.play(FadeOut(VGroup(*omega_mul)),
                  achiles.move_to, self.ordinal)

class TurtleAchilesRace(RunnerScene):

    def construct(self):

        #self.force_skipping()
        self.ordinal = make_achiles_ordinal1()
        self.achiles = Achiles(pointer_pos = UP).move_to(self.ordinal)
        self.turtle = Turtle().move_to(self.ordinal)
        self.achiles_desc = self.make_short_desc(LEFT+DOWN, self.achiles.color)
        self.turtle_desc = self.make_short_desc(LEFT+UP, self.turtle.color)

        self.add(self.ordinal, self.achiles)
        self.play(FadeIn(self.achiles_desc), FadeIn(self.turtle_desc), self.turtle.run_in())
        self.wait_to(7)

        question = make_achiles_question()
        self.play(Write(question))
        self.wait_to(15)

        self.play(self.global_step('1', self.ordinal[0][1],
                                   '\\omega', self.ordinal[1]))
        self.wait_to(16.3)
        self.play(FocusOn2(self.turtle_desc))
        self.wait_to(18.3)
        self.play(FocusOn2(self.achiles_desc))
        self.wait_to(20.5)
        for i in range(2, 10):
            if i < len(self.ordinal): achiles_bar = self.ordinal[i]
            else: achiles_bar = self.ordinal[-1][-1]
            self.play(self.global_step(str(i), self.ordinal[0][i],
                                       '\\omega\\cdot'+str(i), achiles_bar),
                      run_time = 0.5) # 24.5
        self.play(self.global_step("\\omega", self.ordinal[1][0],
                                   '\\omega\\cdot\\omega', achiles_bar)) # 25.5
        self.wait_to(25.8)
        q = (0.7, 0.8, 0.8)
        omega_squared = make_ordinal_power(2, q=q)
        omega_squared.highlight(GREY)
        VGroup(*extract_ordinal_subpowers(omega_squared)[1]).highlight(YELLOW)
        omega_squared0 = omega_squared.copy()
        omega_squared0.shift(RIGHT*(self.ordinal.x1 - omega_squared0.x0))
        omega_squared1 = omega_squared0.copy()
        omega_squared1[0][0].highlight(ORANGE)
        omega_squared1.shift(RIGHT*(omega_squared0.x1 - omega_squared1.x0))
        self.achiles.move_to(omega_squared1)

        moving = VGroup(self.ordinal, self.achiles, self.turtle, omega_squared0, omega_squared1)
        self.play(moving.shift, omega_squared.get_center() - omega_squared0.get_center())
        self.wait_to(29.1)

        self.play(FocusOn2(self.achiles_desc[1]))
        self.wait_to(32.6)
        self.play(self.transform_desc(self.achiles_desc, "\\omega^2"))
        self.wait_to(35)

        omega_squared2 = omega_squared1.copy()
        omega_squared2.shift(RIGHT*(omega_squared1.x1 - omega_squared2.x0))
        moving.add(omega_squared2)
        self.play(moving.shift, omega_squared.get_center() - omega_squared1.get_center())
        self.wait_to(39.5)

        self.turtle.dist = self.achiles.dist = 0.6

        turtle_up_shift = 0.6
        turtle_ord = OrdinalFiniteProd(OrdinalOmega, 3, x0 = -12, x1 = 12, q=q, height = 0.5)
        turtle_ord.shift(UP*turtle_up_shift)
        turtle_ord.highlight(GREY)
        for subord in turtle_ord:
            subord[0].highlight(YELLOW)

        turtle_ord_ori = turtle_ord.copy()
        turtle_ord_ori.shift(UP*SPACE_HEIGHT - turtle_ord_ori.get_edge_center(DOWN))
        self.turtle.move_to(turtle_ord_ori[1])

        achiles_down_shift = 1
        achiles_ord = VGroup(omega_squared0, omega_squared1, omega_squared2)
        omega_squared[0][0].highlight(ORANGE)
        achiles_ord_dest = VGroup(omega_squared.copy(), omega_squared.copy(), omega_squared.copy())
        achiles_ord_dest.stretch(0.5, 1)
        achiles_ord_dest[0].shift(8*LEFT)
        achiles_ord_dest[2].shift(8*RIGHT)
        achiles_ord_dest.shift(DOWN*achiles_down_shift)

        self.play(Transform(achiles_ord, achiles_ord_dest),
                  ReplacementTransform(turtle_ord_ori, turtle_ord),
                  self.turtle.move_to, turtle_ord[1],
                  self.achiles.move_to, achiles_ord_dest[1],
        )
        self.revert_to_original_skipping_status()
        self.wait_to(41.5)
        for i in range(1, 4):
            self.play(self.global_step('\\omega+'+str(i), turtle_ord[1][i],
                                       '\\omega^2+\\omega\\cdot'+str(i), achiles_ord[1][i]),
                      run_time = 0.9) # 44.2
        self.play(self.global_step("\\omega\\cdot2", turtle_ord[2],
                                   '\\omega^2\\cdot2', achiles_ord[2]))

        self.play(FocusOn2(self.turtle_desc[1]))
        self.wait_to(47.8)
        self.play(FocusOn2(self.achiles_desc[1]))
        self.wait_to(59)

        counter = Counter()
        counter.scale(0.8)
        counter.center()
        counter.to_edge(UP)
        counter.count_from(5, self)

    def global_step(self, turtle_str, turtle_bar, achiles_str, achiles_bar):
        return AnimationGroup(
            self.turtle.step_to(turtle_bar),
            self.achiles.step_to(achiles_bar),
            self.transform_desc(self.turtle_desc, turtle_str),
            self.transform_desc(self.achiles_desc, achiles_str),
        )

CIRCLE_DECREASE = 0.5

def to_spiral(mob):

    x = mob.points[:,0]
    y = mob.points[:,1]
    complex_points = 1j * x \
                     + 1.5 + 0.2*y - CIRCLE_DECREASE*x/(2*np.pi)
    complex_transformed = np.exp(complex_points)
    mob.points = np.stack([
        complex_transformed.imag,
        complex_transformed.real,
        np.zeros([len(complex_points)]),
    ], axis = 1)

def power_color(power):
    if power == 0: return WHITE
    else: return [YELLOW, ORANGE, RED, PURPLE, BLUE, GREEN][(power-1) % 6]

def assign_ordinal_powers(ordinal, exponent):
    subpowers = extract_ordinal_subpowers(ordinal)
    for i,subord in reversed(list(enumerate(subpowers))):
        for mob in subord:
            mob[0].power = exponent-i

    subpowers[0][0].power = exponent-1

def assign_color_to_bar(bar):
    bar.set_color(color_interpolate(power_color(bar.power), BLACK, bar.darken))

def make_spiral():

    ordinal = []
    i = 0
    #for _ in range(3):
    while True:
        size = np.exp(i*CIRCLE_DECREASE)
        min_size = (size, size, 0.1)
        thickness = DEFAULT_POINT_THICKNESS / np.sqrt(size)
        if 1 / size < pixel_size or thickness < 0.1: break

        power = i+1
        if power > 5: power = max(3, 2*5-power)

        q = (0.7, 0.7, 0.8)

        cur_ordinal = make_ordinal_power(
            power,
            x0 = i*2*np.pi, x1 = (i+1)*2*np.pi,
            q = q,
            min_size = min_size,
            thickness = thickness,
        )
        assign_ordinal_powers(cur_ordinal, i+1)
        ordinal.append(cur_ordinal)
        i += 1

    ordinal = VGroup(*ordinal)
    for mob in ordinal.family_members_with_points():
        mob.darken = (mob.get_center()[0] / (2*np.pi) - mob.power)/5
        assign_color_to_bar(mob)

    return ordinal

class SpiralPointer(TrianglePointer):

    def to_pos(self, pos):
        new_pointer = TrianglePointer()
        bar = Line(0.8*UP, 0.8*DOWN)
        bar.shift(RIGHT*pos)
        to_spiral(bar)
        new_pointer.to_bar(bar)
        self.points = new_pointer.points
        self.pos = pos

        return self

    def anim_to_pos(self, pos):
        start_pos = self.pos
        def update(mob, alpha):
            mob.to_pos(interpolate(start_pos, pos, alpha))

        return UpdateFromAlphaFunc(self, update)

    def anim_to_ord(self, index):
        return self.anim_to_pos(self.ord_to_pos(index))

    def ord_to_pos(self, index):
        size = np.pi*2
        pos = np.pi*2*index[0]
        for i in index[1:]:
            pos += size*(1-0.7**i)
            size *= 0.3*0.7**i

        return pos

    def to_ord(self, index):
        return self.to_pos(self.ord_to_pos(index))

class ToSpiralScene(RunnerScene):
    def construct(self):

        q = (0.7, 0.8, 0.8)
        turtle_up_shift = 0.6

        behind_turtle = make_ordinal_power(1, q=q, x0=-12, x1 = -4, height = 0.5).shift(turtle_up_shift*UP)

        ahead_turtle = make_ordinal_power(1, q=q, x0=4, x1 = 12, height = 0.5).shift(turtle_up_shift*UP)
        behind_achiles = make_ordinal_power(2, q=q, x0=-12, x1 = -4, height = 0.5).shift(DOWN)
        ahead_achiles = make_ordinal_power(2, q=q, x0=4, x1 = 12, height = 0.5).shift(DOWN)

        #for mob in behind_turtle.family_members_with_points():
        #    if abs(mob.get_center()[0]) > SPACE_WIDTH+1:
        #        to_spiral(mob)
        for mob in VGroup(*behind_achiles[:2]).family_members_with_points():
                mob.stretch(0.7, 0)
                mob.shift(UP + 2.5*LEFT)
                to_spiral(mob)

        max_x = ahead_turtle[-1].get_center()[0] - SPACE_WIDTH
        for mob in ahead_turtle.family_members_with_points():
            alpha = mob.get_center()[0]
            alpha -= SPACE_WIDTH
            if alpha < 0: continue
            alpha /= max_x
            mob.rotate_in_place(-alpha*np.pi/2)
            mob.move_to(interpolate(turtle_up_shift*UP + SPACE_WIDTH*RIGHT,
                                    behind_achiles[0][0].get_center(),
                                    alpha))

        turtle_ord = make_ordinal_power(1, q=q, height = 0.5).shift(turtle_up_shift*UP)
        achiles_ord = make_ordinal_power(2, q=q, height = 0.5).shift(DOWN)
        turtle = Turtle()
        achiles = Achiles(pointer_pos = UP)
        turtle.dist = achiles.dist = 0.6
        turtle.move_to(ahead_turtle[0])
        achiles.move_to(ahead_achiles[0][0])

        turtle_desc = self.make_short_desc(LEFT+UP, turtle.color)
        achiles_desc = self.make_short_desc(LEFT+DOWN, achiles.color)
        self.change_desc(turtle_desc, "\\omega\\cdot2")
        self.change_desc(achiles_desc, "\\omega^2\\cdot2")
        question = make_achiles_question()
        self.add(turtle_desc, achiles_desc, question)

        rect = Rectangle(width = 2*SPACE_WIDTH, height = 2*SPACE_HEIGHT)

        spiral = make_spiral()

        straight_spiral = spiral.copy()
        spiral.apply_to_family(to_spiral)
        behind_turtle_swirled = VGroup(*spiral[0][:3]).copy()
        behind_turtle_swirled.scale(3)
        behind_turtle.add_to_back(*behind_turtle_swirled.submobjects)
        #turtle_dest = TrianglePointer(color = GREEN).to_bar(spiral[1][1])
        #achiles_dest = TrianglePointer(color = ORANGE).to_bar(spiral[2][1])
        turtle_dest = SpiralPointer(color = GREEN).to_ord([1,1])
        achiles_dest = SpiralPointer(color = ORANGE).to_ord([2,1])
        straight_spiral.stretch(0.5, 1)
        straight_spiral.shift(ahead_achiles.get_edge_center(RIGHT)
                              - straight_spiral[2][2].get_edge_center(LEFT))

        straight_spiral.submobjects[0] = behind_turtle
        behind_achiles.add_to_back(turtle_ord, ahead_turtle)
        straight_spiral.submobjects[1] = behind_achiles
        straight_spiral[2].submobjects[0] = achiles_ord
        straight_spiral[2].submobjects[1] = ahead_achiles

        spiral.align_data(straight_spiral)
        for src, dest in zip(straight_spiral.family_members_with_points(),
                             spiral.family_members_with_points()):
            src.highlight(dest.color)

        behind_turtle.highlight(GREY)
        for omega_squared in [behind_achiles, achiles_ord, ahead_achiles]:
            omega_squared.highlight(GREY)
            VGroup(*extract_ordinal_subpowers(omega_squared)[1]).highlight(YELLOW)
            omega_squared[0][0].highlight(ORANGE)
        behind_achiles[0][0].highlight(YELLOW)

        self.add(straight_spiral, turtle, achiles)
        #return

        #animation = AnimationGroup(
        #    ReplacementTransform(straight_spiral, spiral,
        #                         prepare_family = True),
        #    Transform(straight_spiral[0][2], spiral[0][2], path_arc = np.pi*0.6),
        #    Transform(straight_spiral[0][3], spiral[0][3], path_arc = np.pi*0.6),
        #)
        #animation.update_mobject(0.0)

        #self.add(rect)
        #for mob in self.mobjects:
        #    mob.points *= 0.25
        #return

        self.wait_to(4.7)

        self.play(ReplacementTransform(straight_spiral, spiral,
                                       prepare_family = True),
                  Transform(straight_spiral[0][2], spiral[0][2], path_arc = np.pi*0.6),
                  Transform(straight_spiral[0][3], spiral[0][3], path_arc = np.pi*0.6),
                  ReplacementTransform(turtle, turtle_dest),
                  ReplacementTransform(achiles, achiles_dest),
                  order_f = light_key,
                  run_time = 3)

        self.remove(straight_spiral[0][2], straight_spiral[0][3])
        self.wait_to(9)

class SpiralScene(RunnerScene):

    def construct(self):
        #self.force_skipping()
        spiral = make_spiral()
        spiral.apply_to_family(to_spiral)

        self.add(spiral)
        self.update_frame()
        self.set_camera_background(self.get_frame())
        self.remove(spiral)

        self.turtle = SpiralPointer(color = GREEN)
        self.achiles = SpiralPointer(color = ORANGE)

        self.turtle_desc = self.make_short_desc(LEFT+UP, self.turtle.color)
        self.achiles_desc = self.make_short_desc(LEFT+DOWN, self.achiles.color)
        question = make_achiles_question()

        self.global_set_ord(1,1)
        self.add(self.turtle_desc, self.achiles_desc, question,
                 self.turtle, self.achiles)

        self.wait_to(0.2)
        self.play(self.global_step(1,1,1))
        self.highlight_bar(spiral[1][1][1], self.turtle_desc)
        self.wait_to(4.2)
        self.highlight_bar(spiral[2][1][1][0], self.achiles_desc)
        self.wait_to(8.8)

        self.play(self.global_step(1,2))
        self.wait_to(10.3)
        self.highlight_bar(spiral[1][2][0], self.turtle_desc)
        self.wait_to(13.1)
        self.highlight_bar(spiral[2][2][0][0], self.achiles_desc)
        self.wait_to(18.8)

        self.play(self.global_step(2))
        self.highlight_bar(spiral[2][0][0][0], self.turtle_desc)
        self.wait_to(22.6)
        self.highlight_bar(spiral[3][0][0][0][0], self.achiles_desc)
        self.wait_to(27)

        #self.play(FocusOn2(self.turtle_desc[1]))
        #self.dither()
        #self.play(FocusOn2(self.achiles_desc[1]))
        #self.dither()
        self.wait_to(28.5)
        self.play(self.global_step(3))
        self.wait_to(30.3)
        self.highlight_bar(spiral[3][0][0][0][0], self.turtle_desc)
        #self.play(FocusOn2(self.turtle_desc[1]))
        #self.dither()
        self.highlight_bar(spiral[4][0][0][0][0][0], self.achiles_desc)
        self.play(FocusOn2(self.achiles_desc[1]))
        self.wait_to(36.5)
        for i in range(4,7):
            self.play(self.global_step(i))

        self.wait_to(43.5)

        brace = Brace(VGroup(spiral[0][4], Line((SPACE_HEIGHT-0.1)*UP, (SPACE_HEIGHT-0.1)*DOWN)), LEFT)
        arrow = Arrow(brace.get_tip()+0.3*LEFT, ORIGIN)
        dot = Dot(color = YELLOW, radius = 0.03)
        spiral_desc = TexMobject("\\omega^\\omega")
        spiral_desc.set_color(YELLOW)
        brace.put_at_tip(spiral_desc)
        
        #self.revert_to_original_skipping_status()
        self.play(ShowCreation(arrow),
                  ShowCreation(dot))
        self.wait_to(47.5)
        self.play(Write(spiral_desc))
        self.wait_to(50.6)
        self.play(
            self.turtle.anim_to_pos(24*np.pi),
            self.achiles.anim_to_pos(25*np.pi),
            self.transform_desc(self.turtle_desc, '\\omega^\\omega'),
            self.transform_desc(self.achiles_desc, '\\omega^\\omega'),
            run_time = 2,
        )
        answer = TexMobject('\\omega^\\omega', '=', '\\omega\\cdot\\omega^\\omega', '?')
        answer[0].set_color(GREEN)
        answer[2].set_color(ORANGE)
        answer[3].set_color(BLACK)
        answer.to_corner(UP+RIGHT)
        answer.shift(RIGHT*(answer[3].get_edge_center(RIGHT) - answer[2].get_edge_center(RIGHT)))
        question[2].add(question[2][-1].copy(), question[2][-1].copy())
        self.wait_to(53.5)
        self.play(ReplacementTransform(question, answer))
        self.wait_to(58.5)
        self.play(FadeOut(VGroup(arrow, dot, self.turtle, self.achiles,
                                 self.turtle_desc, self.achiles_desc)))
        self.wait_to(60 + 3.5)
        self.play(GrowFromCenter(brace))
        self.wait_to(60 + 29.5)

    def ord_to_str(self, index):
        degree = index[0]
        poly = index[1:degree+2]
        poly += list(0 for _ in range(degree+1-len(poly)))
        poly[0] += 1
        result = ""
        for coef, power in zip(poly, reversed(range(degree+1))):
            if coef == 0: continue
            result += '+'
            if power > 0:
                result += '\\omega'
                if power > 1: result += '^'+str(power)
                if coef > 1: result += '\\cdot'+str(coef)
            else: result += str(coef)

        return result[1:]

    def global_set_ord(self, *turtle_index):
        self.turtle_index = list(turtle_index)
        self.achiles_index = list(turtle_index)
        self.achiles_index[0] += 1

        self.change_desc(self.turtle_desc, self.ord_to_str(self.turtle_index))
        self.change_desc(self.achiles_desc, self.ord_to_str(self.achiles_index))
        self.turtle.to_ord(self.turtle_index)
        self.achiles.to_ord(self.achiles_index)

    def global_step(self, *turtle_index):
        self.turtle_index = list(turtle_index)
        self.achiles_index = list(turtle_index)
        self.achiles_index[0] += 1

        return AnimationGroup(
            self.transform_desc(self.turtle_desc, self.ord_to_str(self.turtle_index)),
            self.transform_desc(self.achiles_desc, self.ord_to_str(self.achiles_index)),
            self.turtle.anim_to_ord(self.turtle_index),
            self.achiles.anim_to_ord(self.achiles_index),
        )

class TransfinitePowers(Scene):

    def construct(self):
        equations = [
            ["\\omega^0", '=', "1"],
            ["\\omega^1", '=', "\\omega"],
            ["\\omega^2", '=', "\\omega\\cdot\\omega"],
            ['\\vdots'],
            ["\\omega^\\omega", '=', "\\hbox{Supremum všech předchozích}"],
            ["\\omega^{\\omega+1}", '=', "\\omega^\\omega","\\cdot\\omega"],
        ]
        equations = VGroup(*[TexMobject(*eq) for eq in equations])
        for eq in equations:
            eq.shift(-eq[1].get_center())
        equations.arrange_submobjects(DOWN, coor_mask = UP)
        equations[-1][-1].highlight(YELLOW)
        equations.to_corner(UP+LEFT)
        self.play(FadeIn(VGroup(*equations[:-1]), submobject_mode = "lagged_start"),
                  run_time = 3)

        limit_step_title = TextMobject("Limitní krok").highlight(YELLOW)
        arrow_end = equations[-2][-1].get_edge_center(UP)
        arrow = Arrow(arrow_end+1.5*UP, arrow_end)
        limit_step_title.next_to(arrow, UP)

        self.wait_to(5.5)
        self.play(ShowCreation(arrow),
                  FadeIn(limit_step_title))
        self.wait_to(7.5)

        self.play(Write(equations[-1]))
        self.wait_to(13)

        demonstration = TexMobject("\\omega\cdot","\\omega^\\omega", "\\cdot\\omega")
        demonstration.shift(2*DOWN)
        demonstration[0].set_color(YELLOW)
        demonstration[2].set_color(YELLOW)
        self.play(FadeIn(demonstration[1]))
        dest = demonstration[1][0].copy()
        for _ in range(3):
            cur_mul = demonstration[0].copy()
            self.play(Write(cur_mul))
            self.dither()
            self.play(Transform(cur_mul, dest))
            self.remove(cur_mul)
            #self.dither()

        self.wait_to(23)

        last = None
        for _ in range(2):
            cur_mul = demonstration[2].copy()
            if last is not None:
                cur_mul.next_to(last, coor_mask = RIGHT)
            self.play(Write(cur_mul))
            #self.dither()
            self.play(cur_mul.highlight, WHITE)
            self.dither()
            last = cur_mul

        # 19

class CountabilityScene(Scene):

    def construct(self):

        #self.force_skipping()

        self.darken_coef = 0.2
        fin_powers = self.make_fin_powers(1)

        title = TextMobject("Mohutnost").to_edge(UP)
        self.play(Write(title), *map(FadeIn, fin_powers))

        ord_brace = BraceDesc(fin_powers[0], "\\omega", DOWN)
        card_brace = BraceDesc(fin_powers[0], "\\aleph_0", UP)

        self.wait_to(6.5)
        self.play(ord_brace.creation_anim())
        self.play(card_brace.creation_anim())

        for exponent in range(2,4):
            next_fin_powers = self.make_fin_powers(exponent)
            ori_fin_powers = self.prepare_to_fin_transform(*fin_powers+next_fin_powers)
            transforms = [
                ReplacementTransform(ori_fin_power, next_fin_power, prepare_families = True)
                for ori_fin_power, next_fin_power in zip(ori_fin_powers, next_fin_powers)
            ]
            for transform in transforms: self.fix_transform(transform)

            #if exponent == 2: self.wait_to(8.5)
            if exponent == 3: self.wait_to(16.8)
            self.play(
                ord_brace.shift_brace, next_fin_powers[0][0],
                card_brace.shift_brace, next_fin_powers[0][0],
                *transforms,
                order_f = light_key
            )
            fin_powers = next_fin_powers
            self.play(
                ord_brace.change_brace_desc, fin_powers[0], "\\omega^"+str(exponent)
            )
            if exponent == 2: self.wait_to(10.8)
            elif exponent == 3: self.wait_to(19.5)
            self.play(
                card_brace.change_brace_desc, fin_powers[0], "\\aleph_0\\cdot\\aleph_0"
            )

            if exponent == 2: self.wait_to(12.8)
            if exponent == 3: self.wait_to(21)
            next_aleph0 = TexMobject("\\aleph_0")
            card_brace.brace.put_at_tip(next_aleph0)
            self.play(
                FadeOut(card_brace.desc[2]),
                Transform(VGroup(*card_brace.desc[:2]), next_aleph0.copy()),
                Transform(VGroup(*card_brace.desc[3:]), next_aleph0.copy()),
            )
            self.remove(*self.mobjects_from_last_animation)
            card_brace.change_desc("\\aleph_0")
            self.add(card_brace)

        # 26

        inf_power = self.make_inf_power()
        inf_power_ori = self.prepare_to_inf_transform(
            fin_powers[0], fin_powers[1], exponent, inf_power
        )
        #self.dither()
        transform = ReplacementTransform(inf_power_ori, inf_power, prepare_families = True)
        self.fix_transform(transform)

        brace_obj = VGroup(*inf_power[:exponent])
        card_brace_dest = card_brace.copy()
        card_brace_dest.shift_brace(brace_obj)
        card_brace_dest.highlight(BLACK)

        self.play(transform,
                  ord_brace.shift_brace, brace_obj,
                  Transform(card_brace, card_brace_dest),
                  run_time = 2, order_f = light_key) # 27
        self.remove(card_brace)

        self.revert_to_original_skipping_status()

        descriptions = self.make_descriptions(inf_power)
        self.play(FadeIn(VGroup(*descriptions[1:])),
                  submobject_mode = "lagged_start",
                  run_time = 2) # 29
        #self.dither()
        self.play(
            ord_brace.change_brace_desc, inf_power, "\\omega^\\omega",
        ) # 30
        self.wait_to(36)

        power_countable = TexMobject("|","\\omega^\\omega","| = \\aleph_0")
        power_countable.shift(ord_brace.desc.get_center()
                              - power_countable[1].get_center())
        power_countable.remove(power_countable[1])
        self.play(Write(power_countable))
        self.wait_to(60 + 4)

    def fix_transform(self, transform):
        families = transform.get_all_families_zipped()
        for submob, start, end in families[1:]:
            if end.power != start.power:
                end.darken += (end.power-start.power+1)*self.darken_coef
                end.power = start.power
                assign_color_to_bar(end)
        
    def make_fin_powers(self, exponent):
        if exponent == 1: q = (0.9, 0.95, 0.95)
        elif exponent == 2: q = (0.8, 0.9, 0.9)
        else: q = (0.7, 0.84, 0.84)
        ordinal0 = make_ordinal_power(exponent, q = q)

        assign_ordinal_powers(ordinal0, exponent)
        family = ordinal0.family_members_with_points()
        family[0].power = exponent
        for mob in family:
            mob.darken = (exponent-mob.power)*self.darken_coef
            assign_color_to_bar(mob)

        ordinal1 = ordinal0.copy().next_to(ordinal0)
        family[0].set_color(WHITE)

        return ordinal0, ordinal1

    def make_descriptions(self, inf_power):
        main_bars = []
        for subord in inf_power:
            while isinstance(subord, LimitOrdinal): subord = subord[0]
            main_bars.append(subord)
        main_bars = LimitSubOrdinal(main_bars)
        main_bars.fix_x1()

        def make_desc(n):
            if n == 0: return TexMobject('0')
            elif n == 1: return TexMobject('\\omega')
            else: return TexMobject('\\omega^'+str(n))
        descriptions = main_bars.add_descriptions(make_desc)
        for desc in descriptions[2:]:
            desc.shift(RIGHT*desc[1].get_width()/2)
        for desc, bar in zip(descriptions, main_bars):
            desc.highlight(bar[0].color)
        return descriptions

    def make_inf_power(self):
        def aux_fin_power(order = 0, x0 = -4, x1 = 4, **kwargs):
            power = min(3, order+1)
            ordinal = make_ordinal_power(power, x0=x0, x1=x1, **kwargs)
            assign_ordinal_powers(ordinal, order+1)
            for mob in ordinal.family_members_with_points():
                mob.darken = ((mob.get_center()[0]-x0) / (x1-x0) + order - mob.power)*self.darken_coef
                assign_color_to_bar(mob)
            return ordinal

        return LimitOrdinal(aux_fin_power, q = (0.7, 0.8, 0.8), x0 = -5, x1 = 5)

    def prepare_to_inf_transform(self, fin_ord0, fin_ord1, exponent, inf_ord):
        tail = LimitSubOrdinal(inf_ord[exponent:]).copy()
        tail.next_to(fin_ord1, buff = 0)
        tail[0].add_to_back(fin_ord1)
        head = fin_ord0
        for _ in range(exponent-1):
            tail.add_to_back(LimitSubOrdinal(head[1:]))
            head = head[0]
        tail.add_to_back(head)

        return tail

    def prepare_to_fin_transform(self, fin_ord0, fin_ord1, next_fin_ord0, next_fin_ord1):
        tail = VGroup(*next_fin_ord0[2:]).copy().next_to(fin_ord1, buff = 0)
        tail.add_to_back(fin_ord0, fin_ord1)
        return tail, next_fin_ord1.copy().next_to(tail)
