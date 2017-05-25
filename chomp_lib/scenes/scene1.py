from scene import Scene
from animation.simple_animations import *
from .. import *

class Scene1(Scene):
    def construct(self):
        p = Players()
        player1 = p.player1
        player2 = p.player2
        self.play(ShowCreation(player1))
        self.play(ShowCreation(player2))
        self.dither()
        chocolate_bar = ChocolateBar().center()
        self.play(ShowCreation(chocolate_bar))
        self.play(ShowCreation(chocolate_bar.crossbones()))
        chocolate_bar.play_bite(self,2,1,player1)
        self.dither()
        chocolate_bar.play_bite(self,1,4,player2)
        self.dither()
        chocolate_bar.play_bite(self,3,4,player1)
        self.dither()
        chocolate_bar.play_bite(self,2,5,player2)
        self.dither()
        self.play(player1.v_face(),player2.toothy_grin())
        self.dither()
