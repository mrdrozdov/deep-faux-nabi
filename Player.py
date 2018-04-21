import random

from Move import Move
from Hint import Hint


class Player(object):
    def __init__(self, name):
        super(Player, self).__init__()
        self.name = name
        self.cards = []

    def give(self, card):
        self.cards.append(card)

    def play(self, game_view):
        index = random.randint(0, len(self.cards) - 1)
        card = self.cards.pop(index)
        move = Move(card=card)
        return move
