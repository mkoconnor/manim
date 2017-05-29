#!/usr/bin/env python

from helpers import *
from scene import Scene

import eost.ordinal
from eost.ordinal import *

def color_interpolate(color1, color2, alpha):
    color1 = color_to_rgb(color1)
    color2 = color_to_rgb(color2)
    return rgb_to_color(interpolate(color1, color2, alpha))

class OrdinalPowerScene(Scene):

    def construct(self):

        eost.ordinal.pixel_size = SPACE_WIDTH*2 / self.camera.pixel_shape[1]
        self.max_pow = 5

        self.init_scene(1)
        self.dither()

        while(self.power < 10):
            self.power_inc()
            self.dither()

        self.dither(10)

    def init_scene(self, power):
        self.power = power
        self.construct_ord()
        self.add(self.ordinal)
        self.add(self.ordinal2)
        for l in self.layers: self.add(*l)
        for l in self.layers2: self.add(*l)
        self.brace, self.description = self.make_description(self.power, self.ordinal)
        self.play(GrowFromCenter(self.brace), Write(self.description))

    def power_inc(self):
        self.power += 1
        ori_ord = self.ordinal
        ori_ord2 = self.ordinal2
        self.construct_ord()
        target_brace, target_desc = self.make_description(self.power-1, self.ordinal[0])

        src_power = self.ordinal2.copy()
        src_power2 = self.ordinal2.copy()
        src_power.next_to(ori_ord2)
        src_power2.next_to(src_power)
        src_power.add_to_back(ori_ord, ori_ord2)

        dest_power = self.ordinal.copy()
        dest_power[0].make_deeper()
        dest_power[1].make_deeper()
        #dest_power.debug()

        def order_f(o):
            if not hasattr(o, 'pow_layer'): return 0
            return o.pow_layer
        self.play(
            Transform(src_power, dest_power, prepare_families = True),
            ReplacementTransform(src_power2, self.ordinal2, prepare_families = True),
            Transform(self.brace, target_brace),
            Transform(self.description, target_desc),
            order_f = order_f,
        )
        self.remove(src_power, ori_ord, ori_ord2)
        self.add(self.ordinal)
        for l in self.layers: self.add(*l)
        for l in self.layers2: self.add(*l)
        self.dither()
        target_brace, target_desc = self.make_description(self.power, self.ordinal)
        self.play(
            Transform(self.brace, target_brace),
            Transform(self.description, target_desc),
        )

    def make_description(self, power, ordinal):
        brace = Brace(ordinal, DOWN)
        if power == 1: text = "\\omega"
        else: text = "\\omega^{%d}" % power
        description = TexMobject(text)
        brace.put_at_tip(description)
        return brace, description

    def construct_ord(self):
        if self.power == 1: q = (0.9, 0.95, 0.95)
        elif self.power == 2: q = (0.8, 0.9, 0.9)
        else: q = (0.7, 0.84, 0.84)

        self.ordinal = make_ordinal_power(min(self.power, self.max_pow), q=q)

        self.layers = extract_ordinal_subpowers(self.ordinal)
        for i, layer in reversed(list(enumerate(self.layers))):
            for mob in layer:
                mob.pow_layer = self.power-i
                color = self.power_color(mob.pow_layer)
                color = color_interpolate(color, BLACK, float(max(i-1, 0))/(self.max_pow))
                mob.set_color(color)
        self.layers = self.layers[:-1]

        self.layers2, self.ordinal2 = copy.deepcopy((self.layers, self.ordinal))
        self.ordinal2.next_to(self.ordinal)

        self.layers[-1][0].set_color(WHITE)

    def power_color(self, power):
        if power == 0: return WHITE
        else: return [GREEN, YELLOW, ORANGE, RED, PURPLE, BLUE][(power-1) % 6]

class OrdinalPowerScene2(OrdinalPowerScene):
    pass

class OrdinalPowerTest(OrdinalPowerScene):
    def construct(self):

        eost.ordinal.pixel_size = SPACE_WIDTH*2 / self.camera.pixel_shape[1]
        self.max_pow = 5

        self.init_scene(5)
        self.dither()
        #self.power_inc()
        #self.dither()
        #self.power_inc()
        #self.dither()


class OrdinalAsIndex(Scene):

    def construct(self):

        o1 = OrdinalOmega()
        o2 = OrdinalOmega(x0 = 4, x1 = 12)
        o = o1.copy()

        o.set_color(WHITE)
        VGroup(o1, o2).highlight(DARK_GREY)

        steps = o.to_steps()
        steps.shift(UP)
        self.add(o1, o2, o)
        self.dither()
        #self.play(o2.shift, UP)     
        self.play(Transform(o, steps,
                            submobject_mode = "one_at_a_time",
                            run_time = 2*DEFAULT_ANIMATION_RUN_TIME,
                            rate_func = rush_into,
        ))
        o2[0].highlight(YELLOW)
        self.dither(3)


class OmegaShowcase(Scene):

    def construct(self):

        o = OrdinalOmega()
        o_even = LimitSubOrdinal(o.submobjects[::2])
        o_odd = LimitSubOrdinal(o.submobjects[1::2])

        o_odd_target = o_odd.copy()
        o_odd_target.highlight(BLACK)
        o_odd_target.shift(UP)

        self.add(o)
        self.dither()
        self.play(Transform(o_odd, o_odd_target))
        self.dither()
        self.play(Transform(o_even, OrdinalOmega()))
        self.dither()
