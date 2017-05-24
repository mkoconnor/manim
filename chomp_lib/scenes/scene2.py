from scene import Scene
from .. import *

from animation.transform import *
from animation.simple_animations import *

def copy_and_move_down(new_mobj,by,num_copies):
    c = new_mobj()
    copies = [c]
    anims = []
    for i in xrange(num_copies):
        d = new_mobj()
        d.shift(c.get_center() - d.get_center())
        d.shift(by(i))
        copies.append(d)
        anims.append(Transform(c,d,rate_func=None))
        c = d
    return (copies, anims)

class Scene2(Scene):
    def construct(self):
        p = Players()
        player1 = p.player1
        player2 = p.player2
        self.add(player1,player2)
        self.dither()
        bites = [
            ((1,1),(1,3)),
            ((1,2),(2,2)),
            ((2,1),(4,2)),
            ((2,2),(3,2)),
            ((1,3),(2,4)),
            ((3,1),(3,2)),
            ((2,3),(4,4)),
            ((3,2),(4,4))
        ]
        num_copies = len(bites)
        x_width = 2
        shift = (-x_width,-1,0)
        moved_player1 = player1.copy().shift(shift)
        (player1s,player1_anims) = copy_and_move_down(
            (lambda : moved_player1.copy()),
            (lambda i: (0,-1,0)),
            num_copies=num_copies
        )
        player1_anims.insert(0,Transform(player1,moved_player1))
        def get_chocolate_bar():
            p = player1s[0]
            c = ChocolateBar().scale_to_fit_width(x_width * 0.9)
            c.next_to(p)
            return c
        (bars,bar_anims) = copy_and_move_down(
            get_chocolate_bar,
            (lambda i: (0,-1,0)),
            num_copies = num_copies - 1
        )
        first_bar = get_chocolate_bar()
        bar_anims.insert(0,ShowCreation(first_bar))
        bars.insert(0,first_bar)
        for (anim1,anim2) in zip(player1_anims,bar_anims):
            self.play(anim1,anim2)
        def get_anims(bars,bites,player):
            def get_anims(bar,(b1,b2)):
                return bar.bite_anims(b1,b2,player=player,highlight_player=True)
            anims = map(get_anims,bars[:len(bites)],bites)
            anims = zip(*anims)
            import itertools
            return map(lambda l: itertools.chain(*l), anims)
        for l in get_anims(bars,map(lambda (x,y): x, bites),player=player1):
            self.play(*l)
        moved_player2 = player2.copy().shift((0,-1,0))
        (player2s,player2_anims) = copy_and_move_down(
            (lambda : moved_player2.copy()),
            (lambda i: (0,-1,0)),
            num_copies=num_copies+1
        )
        player2_anims.insert(0,Transform(player2,moved_player2))
        player2s.insert(0,moved_player2)
        for a in player2_anims:
            self.play(a)
        player2_bars = [bar.copy() for bar in bars]
        orig_player2_bar_center = player2_bars[0].get_center()
        self.play(*(
            Transform(bar,bar.copy().next_to(p2))
            for (bar,p2) in zip(player2_bars,player2s)
        ))
        new_player2_bar_center = player2_bars[0].get_center()
        shift = new_player2_bar_center - orig_player2_bar_center
        for b in player2_bars:
            if b.permanent_rectangles is not None:
                for l in b.permanent_rectangles:
                    for x in l:
                        x.shift(shift)
        for l in get_anims(
                player2_bars,
                map(lambda (x,y): y, bites),
                player=player2
                ):
            self.play(*l)
        self.dither()
