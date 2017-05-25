from mobject import Mobject, Group
from scene import Scene
from animation.simple_animations import *
from .widgets import *
import numpy as np
import helpers
from helpers import *
from animation.transform import *
from topics.geometry import *

def in_a_row(mobj,n):
    mobjs = []
    last_mobj = None
    for _ in xrange(n):
        this_mobj = mobj.copy()
        if last_mobj is not None:
            this_mobj.next_to(last_mobj)
        last_mobj = this_mobj
        mobjs.append(this_mobj)
    return mobjs

def line(from_,to):
    return Line(from_.get_center(),to.get_center())

def permute(l):
    import random
    ret = l[:]
    random.shuffle(ret)
    return ret

def permute_animations(mobjs,move):
    permuted_indices = np.random.permutation(len(mobjs))
    def path_along_arc(old_index,new_index):
        if ( (old_index < new_index and move == "down")
             or (new_index < old_index and move == "up")
             ):
            return counterclockwise_path()
        else:
            return clockwise_path()
    return [
        Transform(mobjs[i],mobjs[j].copy(),path_func=path_along_arc(i,j))
        for (i,j) in enumerate(permuted_indices)
    ]

class Scene1(Scene):
    def construct(self):
        num_apples = 5
        num_pears = 4
        min_fruit = min(num_apples,num_pears)
        apples = in_a_row(Apple(),num_apples)
        pears = in_a_row(Pear(),num_pears)
        apple_group = Group(*apples).center().to_edge(UP)
        pear_group = Group(*pears).center().to_edge(DOWN)
        # Display the two lines of apples and pears
        self.play(ShowCreation(apple_group))
        self.play(ShowCreation(pear_group))
        self.dither()
        # Show a matching
        matching = Group(*map(line,apples[:min_fruit],pears[:min_fruit]))
        self.play(ShowCreation(matching))
        self.dither()
        self.play(Uncreate(matching))
        # Permute them
        apple_permutations=permute_animations(apple_group,move="down")
        pear_permutations=permute_animations(pear_group,move="up")
        self.play(*(apple_permutations + pear_permutations))
        # Show a different matching
        matching = Group(*map(
            line,
            permute(apples)[:min_fruit],
            permute(pears)[:min_fruit]
        ))
        self.play(ShowCreation(matching))
        self.dither()
        self.play(Uncreate(matching))
        self.dither()
