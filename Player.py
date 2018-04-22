import random

from Move import Move
from Hint import Hint


class Player(object):
    CHOOSE_CARD = 0
    CHOOSE_HINT = 1

    def __init__(self, name, index):
        super(Player, self).__init__()
        self.name = name
        self.index = index
        self.cards = []

    def give(self, card):
        self.cards.append(card)

    def choose(self):
        return random.randint(0, 1)

    def play(self, game_view):
        choice = self.choose()
        move = None

        if not game_view.has_hints():
            choice = Player.CHOOSE_CARD

        if choice == Player.CHOOSE_HINT:
            hints = game_view.possible_hints()
            if len(hints) > 0:
                index = random.randint(0, len(hints) - 1)
                move = Move(hint=hints[index])

        if choice == Player.CHOOSE_CARD or move is None:
            index = random.randint(0, len(self.cards) - 1)
            card = self.cards.pop(index)
            move = Move(card=card)

        if move is None:
            raise ValueError("Not valid move created for choice: {}".format(choice))

        return move
