from mobject import *
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from .crossbones import *

__all__ = ['ChocolateBar']

class ChocolateBar(Mobject):
    def crossbones(self):
        lower_left_square = self.rectangles[-1][0]
        c = Crossbones().scale_to_fit_height(
            lower_left_square.get_height()*0.8
        )
        c.shift(lower_left_square.get_center()-c.get_center())
        return c

    def bite_anims(self,r,s,player,highlight_player=True):
        if self.permanent_rectangles is None:
            self.permanent_rectangles = [
                [x.copy() for x in y] for y in self.rectangles
            ]
        def from_rects(rects):
            return [ x for y in rects[:r] for z in y[-s:] for x in z]
        mobjs = from_rects(self.rectangles)
        all_rects = Mobject(*(from_rects(self.permanent_rectangles)[::-1]))
        outer = Rectangle(height=all_rects.get_height(),width=all_rects.get_width(),color=player.color)
        outer.shift(all_rects.get_center() - outer.get_center())
        anims = []
        if highlight_player:
            anims.append([ShowCreation(outer),player.scale_up()])
        else:
            anims.append([ShowCreation(outer)])
        anims.append([Uncreate(outer)])
        if highlight_player:
            anims.append([Uncreate(Group(*mobjs)),player.scale_down()])
        else:
            anims.append([Uncreate(Group(*mobjs))])
        return anims

    def play_bite(self,scene,*args,**kwargs):
        anims = self.bite_anims(*args,**kwargs)
        for l in anims:
            scene.play(*l)

    def __init__(self,n=3,m=5,height=3*1.2,width=5*1.2):
        stroke_width = DEFAULT_POINT_THICKNESS # * 2
        buff = 0
        rect = Rectangle(height=height/m,width=width/n,stroke_width=stroke_width,color=WHITE)
        rectangles = [[]]
        for i in xrange(n):
            for j in xrange(m):
                this_rect = rect.copy()
                if i == 0 and j == 0:
                    rectangles[0].append(this_rect)
                elif j == 0:
                    last_rect = rectangles[-1][0]
                    this_rect.next_to(last_rect,direction=DOWN,buff=buff)
                    rectangles.append([this_rect])
                else:
                    last_rect = rectangles[-1][-1]
                    this_rect.next_to(last_rect,direction=RIGHT,buff=buff)
                    rectangles[-1].append(this_rect)
        self.rectangles = rectangles
       # Initialized in play_bite, so that we get it after any moves have
       # happened
        self.permanent_rectangles = None
        Mobject.__init__(self,*[r for l in rectangles for r in l])

    def copy(self):
        c = Mobject.copy(self)
        def copy_rects(rects):
            return [[x.copy() for x in y] for y in rects]
        if self.permanent_rectangles is not None:
            c.permanent_rectangles = copy_rects(self.permanent_rectangles)
        c.rectangles = copy_rects(self.rectangles)
        return c
