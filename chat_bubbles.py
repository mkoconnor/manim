#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *

class ChatBubble(VMobject):
    def __init__(self, text, answer_bubble = False, border = 0.3, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.answer_bubble = answer_bubble

        self.bubble = SVGMobject(file_name = "Chat_bubble.svg", initial_scale_factor = 0.02)[0]
        self.bubble.set_fill(BLACK, opacity = 0.9)

        if answer_bubble: self.bubble.set_stroke(YELLOW)
        else: self.bubble.set_stroke(BLUE)

        self.text = TextMobject(text, alignment="\\raggedright\\hsize = 0.7\\hsize")
        print(self.text.get_tex_string())
        self.tip_h = self.bubble.points[12,1] - self.bubble.points[15,1]
        self.text.move_to(self.bubble.get_corner(LEFT+DOWN)+np.array([border,self.tip_h+border,0]), aligned_edge = LEFT+DOWN)
        size_shift = self.text.get_corner(UP+RIGHT) - self.bubble.get_corner(UP+RIGHT) + border
        shift_w = size_shift[0]
        shift_h = size_shift[1]
        for p in self.bubble.points[19:31]: p[0] += shift_w
        for p in self.bubble.points[:4]: p[1] += shift_h
        for p in self.bubble.points[25:]: p[1] += shift_h
        self.add(self.bubble, self.text)

        if answer_bubble:
            self.center()
            self.bubble.scale([-1,1,1])
            self.to_corner(RIGHT+DOWN)
        else:
            self.to_corner(LEFT+DOWN)

def stretch_rate_func(f):
    f0 = f(0)
    f1 = f(1)
    def result(t):
        return (f(t)-f0)/(f1-f0)
    return result

class Conversation:
    def __init__(self, scene, start_answer = False):
        self.scene = scene
        self.dialog = VGroup()
        self.next_answer = start_answer

    def add_bubble(self, text, answer_bubble = False):
        bubble = ChatBubble(text, self.next_answer)
        self.next_answer = not self.next_answer

        height = bubble.get_height()
        shift = height - bubble.tip_h + 0.2
        dialog_target = self.dialog.copy()
        dialog_target.shift([0, shift, 0])

        bubble_target = bubble.copy()
        bubble.highlight(BLACK)
        bubble.scale([1, 0, 1], about_point = np.array([0, -SPACE_HEIGHT, 0]))

        def dialog_rate_func(t):
            bubble_rate = rush_from(t)
            bubble_rel_pos = (bubble_rate - 1) * height / shift + 1
            return np.exp(bubble_rel_pos-1)

        self.scene.play(Transform(self.dialog, dialog_target, rate_func = stretch_rate_func(dialog_rate_func)),
                        Transform(bubble, bubble_target, rate_func = rush_from))
        self.dialog.add(bubble)
