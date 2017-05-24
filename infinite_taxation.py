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

def gen_coin(fill_color):
    return SVGMobject(file_name='/Users/michaeloconnor/Downloads/coin.svg',
                      initial_scale_factor=0.01,
                      fill_color=fill_color,
                      fill_opacity=1,
                      stroke_color=GRAY,
                      propogate_style_to_family=True)
coin = gen_coin(fill_color=YELLOW)

train = SVGMobject(file_name='/Users/michaeloconnor/Downloads/businessman.svg',
                   initial_scale_factor=0.0030,
                   fill_color=WHITE,
                   propogate_style_to_family=True)
trainBackground = Rectangle(color=BLACK,height=train.get_height(),width=2)
train.add_to_back(trainBackground)

class CoinStack(Mobject):
    def __init__(self,num_coins):
        self.coin_list=[coin.copy()]
        for i in xrange(num_coins):
            new_coin=self.coin_list[-1].copy()
            # new_coin.scale(0.9)
            new_coin.next_to(self.coin_list[-1],direction=UP)
            self.coin_list.append(new_coin)
        dots = TexMobject("\cdots")
        dots.rotate_in_place(np.pi/2)
        dots.next_to(self.coin_list[-1],direction=UP)
        all_mobjs = self.coin_list[:]
        all_mobjs.append(dots)
        Mobject.__init__(self,*all_mobjs)

class NumberLineComponent:
    def __init__(self,dot=None,tex=None,line=None):
        self.dot = dot
        self.tex = tex
        self.line = line

    def mobjs(self):
        return [x for x in [self.dot, self.tex, self.line] if x is not None]

class NumberLine(Mobject):
    def __init__(self,n,first_mobj,label=lambda n:str(n)):
        self.components=[]
        for i in xrange(n):
            dot = Dot()
            tex = TexMobject(label(i))
            if i > 0:
                prev_center = self.components[i-1].dot.get_center()
                new_center=(prev_center[0]+first_mobj.get_width(),prev_center[1],prev_center[2])
                if i == n - 1:
                    dot = TexMobject("\\cdots")
                dot.shift(new_center-dot.get_center())
                tex.next_to(dot,direction=DOWN)
                line = Line(prev_center,new_center)
                if i == n - 1:
                    new_component = NumberLineComponent(dot)
                else:
                    new_component = NumberLineComponent(dot,tex,line)
            else:
                tex.next_to(first_mobj,direction=UP)
                dot.next_to(tex,direction=UP)
                new_component = NumberLineComponent(dot,tex)
            self.components.append(new_component)
        Mobject.__init__(self,*[x for y in self.components for x in y.mobjs()])

class EntranceFees:
    def __init__(self,next = lambda : None):
        self.last_mobj = None
        self.next = next
        self.stacks = []

    def get_animation(self):
        current = self.next()
        if current is None:
            # Empty animation
            return Animation(Mobject())
        else:
            if len(self.stacks) <= 1 or len(self.stacks[0]) <= 1:
                point = self.stacks[current[0]][current[1]].get_center()
            else:
                x_diff = self.stacks[1][0].get_center() - self.stacks[0][0].get_center()
                y_diff = self.stacks[0][1].get_center() - self.stacks[0][0].get_center()
                point = self.stacks[0][0].get_center() + current[0]*x_diff + current[1]*y_diff
            dot = Dot(point,color=RED)
            if self.last_mobj is None:
                self.last_mobj = dot
                return ShowCreation(dot)
            line = Line(self.last_mobj.get_center(),point,color=RED)
            self.last_mobj = dot
            return ShowCreation(Mobject(line,dot),
                                subobject_mode="one_at_a_time")

    def add_stack(self,stack):
        self.stacks.append(stack)
        return self.get_animation()

class SceneWithNumberLine(Scene):
    def __init__(self,*args,**kwargs):
        self.num_stops = 5
        Scene.__init__(self,*args,**kwargs)

class SalesmanScene(SceneWithNumberLine):
    CONFIG = {
        "show_intro" : True,
        "entrance_fees" : EntranceFees(),
        "num_extra_segments" : 10
    }

    def construct(self):
        bigTrain = train.copy()
        bigTrain.center()
        bigTrain.scale_to_fit_height(SPACE_HEIGHT)
        train.to_corner()
        bigTrainToTrain = Transform(bigTrain,train)
        num_stops = self.num_stops
        n = NumberLine(num_stops,train)
        if self.show_intro:
            self.play(ShowCreation(bigTrain))
            self.dither()
            self.play(bigTrainToTrain)
            self.dither()
            self.play(ShowCreation(n))
        else:
            bigTrainToTrain.update(1)
            self.play(ShowCreation(bigTrain),ShowCreation(n))
        for i in xrange(num_stops - 1):
            self.dither()
            coinstack = CoinStack(num_coins=3)
            coinstack.next_to(n.components[i].dot,direction=UP)
            self.play(self.entrance_fees.add_stack(coinstack.coin_list))
            self.play(ShowCreation(coinstack))
            self.dither()
            if i < num_stops - 2:
                train2 = bigTrain.copy()
                train2.shift((bigTrain.get_width(),0,0))
                self.play(Transform(bigTrain,train2))
        self.dither()
        train2 = bigTrain.copy()
        train2.move_to((RIGHT_SIDE[0]+train2.get_width(),train2.get_center()[1],train2.get_center()[2]))
        self.play(Transform(bigTrain,train2))
        for i in xrange(self.num_extra_segments):
            self.play(self.entrance_fees.get_animation(),run_time=DEFAULT_ANIMATION_RUN_TIME / 3.0)

class Scene1(SalesmanScene):
    def __init__(self,**kwargs):
        SalesmanScene.__init__(self,show_intro=True,**kwargs)

class Scene2(Scene):
    def construct(self):
        title=TexMobject("\\underline{\\text{Entrance Fee Rules}}")
        title.to_edge(UP)
        self.play(Write(title))
        self.dither()
        line1 = TexMobject("\\text{Upon \\textit{entering} a city:}")
        line1.next_to(title,DOWN)
        self.play(Write(line1))
        line2 = TexMobject("\\text{If you have \\textit{no} dollars, none will be taken}")
        line2.next_to(line1,DOWN)
        self.play(Write(line2))
        line3 = TexMobject("\\text{If you have at least one dollar, one will be taken}")
        line3.next_to(line2,DOWN)
        self.play(Write(line3))
        self.dither()

class Scene3(SalesmanScene):
    def __init__(self,**kwargs):
        class Next:
            def __init__(self):
                self.num_calls = 0
                self.prev_return = None

            def __call__(self):
                num_calls = self.num_calls
                self.num_calls = num_calls + 1
                if num_calls == 0:
                    self.prev_return = None
                elif num_calls == 1:
                    self.prev_return = (0,0)
                else:
                    self.prev_return = (self.prev_return[0]+1,self.prev_return[1])
                return self.prev_return
        next = Next()
        entrance_fees=EntranceFees(next=next)
        SalesmanScene.__init__(self,
                               show_intro=False,
                               entrance_fees=entrance_fees,
                               **kwargs)

class Scene4(SalesmanScene):
    def __init__(self,**kwargs):
        class Next:
            def __init__(self):
                self.num_calls = 0
                self.moving = None

            def __call__(self):
                num_calls = self.num_calls
                self.num_calls = self.num_calls + 1
                if num_calls == 0:
                    return None
                elif num_calls == 1:
                    self.prev_return = (0,0)
                elif self.prev_return[1] == 0 and (self.moving is None or self.moving == "down-right"):
                    self.moving = "up-left"
                    self.prev_return = (self.prev_return[0] + 1,0)
                elif self.prev_return[0] == 0 and (self.moving is None or self.moving == "up-left"):
                    self.moving = "down-right"
                    self.prev_return = (0, self.prev_return[1]+1)
                elif self.moving == "up-left":
                    self.prev_return = (self.prev_return[0]-1,self.prev_return[1]+1)
                elif self.moving == "down-right":
                    self.prev_return = (self.prev_return[0]+1,self.prev_return[1]-1)
                return self.prev_return
        next = Next()
        entrance_fees=EntranceFees(next=next)
        SalesmanScene.__init__(self,
                               show_intro=False,
                               entrance_fees=entrance_fees,
                               num_extra_segments=100,
                               **kwargs)


class LabeledDot(Mobject):
    def __init__(self,dot,label):
        self.dot = dot
        self.label = label
        Mobject.__init__(self,dot,label)

class CountableNumberLine(Mobject):
    def __init__(self):
        unfilledDot = Circle(radius=0.2,color=WHITE)
        zero = Dot(radius=0.01)
        zero.to_edge(LEFT)
        unfilledDot.to_edge(RIGHT)
        ending_ordinal = TexMobject("\\omega_1").next_to(unfilledDot,DOWN)
        line = Line(zero.get_center(),unfilledDot.get_left())
        self.line = line
        # brace = Brace(Mobject(zero,line))
        # text = TextMobject(smaller_ordinal_label)
        # text.next_to(brace,direction=DOWN)
        return Mobject.__init__(self,zero,line,unfilledDot,ending_ordinal)

    def make_label(self,tex,s,color):
        dot_location = self.line.get_left()*(1-s) + self.line.get_right()*s
        dot = Dot(dot_location,color=color)
        tex = TexMobject(tex,fill_color=color).next_to(dot,direction=DOWN)
        return LabeledDot(dot,tex)

class Scene5(Scene):
    def construct(self):
        n = CountableNumberLine()
        n.to_edge(DOWN)
        self.play(ShowCreation(n))
        self.dither()
        lemma1 = TextMobject("Lemma:")
        lemma2 = TextMobject("For any", "$\\alpha$", ",")
        lemma3 = TextMobject("there is an", "$f(\\alpha)", "{} > \\alpha")
        lemma4 = TextMobject("such that you have \\$0 when arriving at $f(\\alpha)")

        alpha_color = YELLOW
        f_alpha_color = BLUE
        lemma2.highlight_by_tex("alpha",alpha_color)
        lemma3.highlight_by_tex("f(",f_alpha_color)
        lemma1.to_edge(UP)
        lemma2.next_to(lemma1,DOWN)
        lemma3.next_to(lemma2,DOWN)
        lemma4.next_to(lemma3,DOWN)
        self.play(Write(lemma1))
        self.dither()
        alpha = n.make_label("\\alpha",0.4,color=alpha_color)
        self.play(Write(lemma2), ShowCreation(alpha))
        self.dither()
        f_alpha = n.make_label("f(\\alpha)",0.7,color=f_alpha_color)
        self.play(Write(lemma3), ShowCreation(f_alpha))
        self.dither()
        self.play(Write(lemma4))
        self.dither()

class Scene6(Scene):
    def construct(self):
        given_lemma = TextMobject("\\textit{Given} the lemma:")
        given_lemma.to_edge(UP)

        class Suppose(Mobject):
            def __init__(self):
                self.start = TextMobject("Suppose you had a ")
                self.coin = coin.copy().next_to(self.start,RIGHT)
                self.end = TextMobject(" at the end").next_to(self.coin,RIGHT)
                return Mobject.__init__(self,self.start,self.coin,self.end)

        suppose=Suppose()
        suppose.next_to(given_lemma,direction=DOWN)

        must_have_acquired = TextMobject("You must have acquired it at some", "$\\alpha$").highlight_by_tex("alpha",YELLOW).next_to(suppose,DOWN)
        must_have_lost = TextMobject("But then you must have lost it by", "$f(\\alpha)").highlight_by_tex("f(",BLUE).next_to(must_have_acquired,DOWN)

        n = CountableNumberLine()
        n.to_edge(DOWN)

        self.play(ShowCreation(n))
        self.play(Write(given_lemma))
        self.play(Write(suppose))
        self.play(Write(must_have_acquired))
        alpha = n.make_label("\\alpha",0.4,YELLOW)
        alpha_coin = suppose.coin.copy()
        alpha_coin.next_to(alpha,direction=UP)
        self.play(ShowCreation(alpha),
                  Transform(suppose.coin.copy(),alpha_coin),
                  Transform(
                      must_have_acquired.get_part_by_tex("alpha").copy(),
                      alpha.label
                      )
                  )
        self.play(Write(must_have_lost))
        f_alpha = n.make_label("f(\\alpha)",0.7,BLUE)
        self.play(ShowCreation(f_alpha),Transform(
            must_have_lost.get_part_by_tex("f(").copy(),
            f_alpha.label
        ))
        self.dither()

def_of_f = TextMobject("Definition of $f$:")
def_of_f.to_edge(UP)

class Scene7(Scene):
    def construct(self):

        coin_taken_away = gen_coin(GREEN)

        class CoinConvention(Mobject):
            def __init__(self):
                coin = coin_taken_away.copy().to_edge(LEFT)
                equals = TextMobject("${}={}$ a coin taken away at some stop").next_to(coin)
                Mobject.__init__(self,coin,equals)

        coin_convention=CoinConvention().next_to(def_of_f,DOWN)

        class G_def(Mobject):
            def __init__(self):
                given_a = TextMobject("Given a ").to_edge(LEFT)
                coin1 = coin_taken_away.copy().next_to(given_a)
                g_def1 = TextMobject(", let $g($").next_to(coin1,buff=0)
                coin2 = coin_taken_away.copy().next_to(g_def1,buff=0)
                g_def2 = TextMobject("$)$ be the stop it was taken away at").next_to(coin2,buff=0)
                Mobject.__init__(self,given_a,coin1,g_def1,coin2,g_def2)

        g_def = G_def().next_to(coin_convention,DOWN,buff=MED_LARGE_BUFF)

        class H_def(Mobject):
            def __init__(self):
                line1 = TextMobject("Given an $\\alpha$, let $h(\\alpha)$ be")

                line2_part1 = TexMobject("\\sup\\lbrace g(")
                coin1 = coin_taken_away.copy().next_to(line2_part1,buff=0)
                line2_part2 = TexMobject(")\\rbrace").next_to(coin1,buff=0)
                line2 = Mobject(line2_part1,coin1,line2_part2).center()
                line2.next_to(line1,DOWN)

                line3_part1 = TextMobject("over all ")
                coin2 = coin_taken_away.copy().next_to(line3_part1)
                line3_part2 = TextMobject(" you had when you arrived at $\\alpha$").next_to(coin2)
                line3 = Mobject(line3_part1,coin2,line3_part2).center()
                line3.next_to(line2,DOWN)

                Mobject.__init__(self,line1,line2,line3)
        h_def = H_def().next_to(g_def,DOWN,buff=MED_LARGE_BUFF)

        self.play(Write(def_of_f))
        self.dither()
        self.play(Write(coin_convention))
        self.dither()
        self.play(Write(g_def))
        self.dither()
        self.play(Write(h_def))
        self.dither()

class Scene8(Scene):
    def construct(self):
        n = CountableNumberLine().to_edge(DOWN)
        self.play(Write(def_of_f),ShowCreation(n))
        self.dither()
        for_any_alpha = TextMobject("For any", "$\\alpha$",", we have: ").next_to(def_of_f,DOWN).to_edge(LEFT)
        for_any_alpha.highlight_by_tex("alpha",YELLOW)
        alpha = n.make_label("\\alpha",0.1,YELLOW)
        self.play(Write(for_any_alpha),ShowCreation(alpha))
        h_alpha_tex = TextMobject("$h(\\alpha),").next_to(for_any_alpha,DOWN).to_edge(LEFT)
        h_alpha = n.make_label("h(\\alpha)", 0.25, WHITE)
        self.play(Write(h_alpha_tex), ShowCreation(h_alpha))
        h2_alpha_tex = TextMobject("$h(h(\\alpha))=h^{(2)}(\\alpha)$,").next_to(h_alpha_tex)
        h2_alpha = n.make_label("h^{(2)}(\\alpha)",0.45,WHITE)
        self.play(Write(h2_alpha_tex), ShowCreation(h2_alpha))
        h3_alpha_tex = TextMobject("$h^{(3)}(\\alpha)$,").next_to(h2_alpha_tex)
        h3_alpha = n.make_label("h^{(3)}(\\alpha)",0.6,WHITE)
        self.play(Write(h3_alpha_tex), ShowCreation(h3_alpha))

        ellipsis = TexMobject("\\ldots").next_to(h3_alpha_tex)
        other_dots=[n.make_label("{}",0.9-(0.5**i)*0.3,WHITE) for i in xrange(10)]
        self.play(*([Write(ellipsis)]+[ShowCreation(x) for x in other_dots]))

        f_alpha_tex=TexMobject("f(\\alpha)","=\\sup_n h^{(n)}(\\alpha)").next_to(ellipsis,DOWN,buff=MED_LARGE_BUFF).to_edge(LEFT)
        f_alpha_tex.highlight_by_tex("f(",BLUE)
        f_alpha = n.make_label("f(\\alpha)",0.9,BLUE)
        self.play(Write(f_alpha_tex), ShowCreation(f_alpha))
        self.dither()

        self.play(*[Uncreate(x) for x in [for_any_alpha,h_alpha_tex,h2_alpha_tex,h3_alpha_tex,ellipsis,f_alpha_tex]])
        self.dither()

        beta = n.make_label("\\beta",0.35,WHITE)
        beta_coin = coin.copy().next_to(beta,UP)
        self.play(ShowCreation(beta),ShowCreation(beta_coin))
        self.dither()
        h3_alpha_green = n.make_label("h^{(3)}(\\alpha)",0.6,GREEN)
        self.play(Transform(h3_alpha.copy(),h3_alpha_green))
        self.dither()
        self.play(ShowCreation(h3_alpha))

class Scene9(Scene):
    def construct(self):
        self.play(Write(TextMobject("Many, many thanks to 3blue1brown!")))

