from mobject import Mobject, Group
from mobject.tex_mobject import TexMobject
from scene import Scene
from animation.simple_animations import *
from .widgets import *
import numpy as np
import helpers
from helpers import *
from animation.transform import *
from topics.geometry import *
from .matching import get_matching, MatchingAnimations

import random
random.seed(489903318756316287)
np.random.seed(2442432778)

def permute(l):
    ret = l[:]
    random.shuffle(ret)
    return ret

def permute_animations(mobj,move):
    mobjs = mobj.submobjects
    permuted_indices = np.random.permutation(len(mobjs))
    def path_along_arc(old_index,new_index):
        if ( (old_index < new_index and move == "down")
             or (new_index < old_index and move == "up")
             ):
            return helpers.path_along_arc(np.pi/4)
        else:
            return helpers.path_along_arc(-np.pi/4)
    return [
        Transform(mobjs[i],mobjs[i].copy().replace(mobjs[j]),
                  path_func=path_along_arc(i,j)
        )
        for (i,j) in enumerate(permuted_indices)
    ]

class GrowFromCenterGeneral(Transform):
    def __init__(self, mobject, **kwargs):
        target = mobject.copy()
        mobject.scale_in_place(0)
        Transform.__init__(self, mobject, target, **kwargs)

def random_small_angle():
    return random.uniform(-np.pi/40,np.pi/40)

def apple_pile():
    bottom_row = [Apple(i).rotate(random_small_angle()) for i in xrange(3)]
    top_row = [Apple(3).rotate(-np.pi/20),Apple(4).rotate(np.pi/20)]
    Group(*bottom_row).arrange_submobjects(buff=0.1)
    Group(*top_row).arrange_submobjects(buff=0.1)
    Group(*top_row).next_to(Group(*bottom_row),direction=UP,buff=0)
    return Group(*(bottom_row + top_row))

def pear_pile():
    bottom_two = [Pear(i).rotate(random_small_angle()) for i in xrange(2)]
    Group(*bottom_two).arrange_submobjects(buff=0.1)
    third_on_bottom = Pear(2).next_to(Group(*bottom_two),buff=0.1)
    top = (Pear(3)).rotate(-np.pi/20).next_to(Group(*bottom_two),direction=UP,buff=0)
    return Group(*(bottom_two + [third_on_bottom, top]))

class CountTransform():
    CONFIG = {
        'rate_func' : None
    }

    def __init__(self, mobject, target, direction):
        numbers=[]
        def transform(mobj,tgt,i):
            number = TextMobject(str(i+1)).next_to(tgt,direction=direction)
            numbers.append(number)
            return AnimationGroup(
                Write(number),
                Transform(mobj,tgt),
            )
        transforms = [
            transform(mobj,tgt,i)
            for (i,(mobj,tgt))
            in enumerate(zip(mobject.submobjects,target.submobjects))
        ]
        self.numbers = numbers
        self.transforms = transforms

    def play(self,scene):
        for transform in self.transforms:
            scene.play(transform)

    def summarize(self):
        central_number = self.numbers[-1].copy()
        central_number.shift(
            Group(*self.numbers).get_center()
            - central_number.get_center()
        )
        return AnimationGroup(*(
            [FadeOut(i) for i in self.numbers[:-1]]
            + [Transform(self.numbers[-1],central_number)]
        ))

class Scene1(Scene):
    def construct(self):
        apples = apple_pile().center()
        pears = pear_pile().center().next_to(apples,direction=DOWN)
        Group(apples,pears).center()
        # Display the two lines of apples and pears
        self.play(Succession(*map(GrowFromCenterGeneral, apples.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        self.play(Succession(*map(GrowFromCenterGeneral, pears.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        self.dither()
        counted_apples = [Apple(i) for i in xrange(5)]
        counted_pears = [Pear(i) for i in xrange(4)]
        counted_apple_group = Group(*counted_apples).arrange_submobjects().to_edge(UP)
        counted_pear_group = Group(*counted_pears).arrange_submobjects().to_edge(DOWN)
        apple_count = CountTransform(apples,counted_apple_group,direction=DOWN)
        apple_count.play(self)
        pear_count = CountTransform(pears,counted_pear_group,direction=UP)
        pear_count.play(self)
        self.play(apple_count.summarize(),pear_count.summarize())
        inequality = TexMobject(
            apple_count.numbers[-1].args[0],
            ">",
            pear_count.numbers[-1].args[0]
        ).center()
        self.play(
            Transform(
                apple_count.numbers[-1],
                inequality.get_part_by_tex(apple_count.numbers[-1].args[0])
            ),
            Write(inequality.get_part_by_tex(">")),
            Transform(
                pear_count.numbers[-1],
                inequality.get_part_by_tex(pear_count.numbers[-1].args[0])
            )
        )
        self.dither()
        self.play(*map(FadeOut,[
            apple_count.numbers[-1],
            inequality,
            pear_count.numbers[-1]
        ]))
        # Show a matching
        matching = MatchingAnimations(Group(*apples),Group(*pears))
        for anims in matching.match_animations:
            self.play(anims)
        self.play(Transform(apples[-1],apples[-1].copy().center().to_edge(UP)))
        self.emphasize(apples[-1]) # Above, I pretended like this function
                                   # was generic over the number of apples
                                   # pears.  But here, and in the emphasis
                                   # below, it isn't.
        self.play(Transform(apples[-1],apples[-1].copy().next_to(
            apples[-2], buff = matching.buff
        )))
        self.play(matching.remove_match_animation)
        self.dither()
        # Permute them
        apple_permutations=permute_animations(apples,move="up")
        pear_permutations=permute_animations(pears,move="down")
        self.play(*(apple_permutations + pear_permutations))
        # Show a different matching
        permuted_apples = permute(apples)
        permuted_pears = permute(pears)
        # matching = MatchingAnimations(Group(*apples),Group(*pears))
        # for anims in matching.match_animations:
        #     self.play(anims)
        matching = get_matching(Group(*permuted_apples),Group(*permuted_pears))
        self.play(ShowCreation(matching))
        self.dither()
        self.play(Transform(permuted_apples[-1],permuted_apples[-1].copy().center().to_edge(UP)))
        self.emphasize(permuted_apples[-1]) # See comment above. This [-1] is
                                            # kind of a cheat
        self.play(Uncreate(matching))
        self.dither()

    # Emphasize an apple mobj by making it slightly bigger and white
    def emphasize(self,apple):
        orig = apple.copy()
        emphasized = Apple(color=WHITE)
        emphasized.shift(orig.get_center() - emphasized.get_center())
        emphasized.scale_in_place(1.1)
        self.play(Transform(apple,emphasized))
        self.play(Transform(apple,orig))
