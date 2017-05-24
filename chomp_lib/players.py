__all__ = ['Players']

from .smileyguy import *
from constants import *
from mobject import Mobject, Group


class Players:
    def __init__(self):
        player1 = SmileyGuy(color=GREEN)
        player2 = SmileyGuy(color=PURPLE).next_to(player1,buff=0.5)
        Group(player1,player2).center().to_edge(UP)
        self.player1 = player1
        self.player2 = player2
