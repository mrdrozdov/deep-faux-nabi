import random

from Move import Choice
from Move import Move
from Hint import Hint


class Player(object):
    def __init__(self, name, index):
        super(Player, self).__init__()
        self.name = name
        self.index = index
        self.cards = []

    def give(self, card):
        self.cards.append(card)

    def choose(self, game_view):
        choices = [Choice.CARD, Choice.DISCARD]
        can_hint = game_view.has_hints()
        can_hint = can_hint or len(game_view.possible_hints()) > 0
        if can_hint:
            choices.append(Choice.HINT)
        return random.choice(choices)

    def play(self, game_view):
        choice = self.choose(game_view)

        if choice == Choice.HINT:
            hints = game_view.possible_hints()
            index = random.randint(0, len(hints) - 1)
            move = Move(choice, hint=hints[index])

        elif choice == Choice.CARD:
            index = random.randint(0, len(self.cards) - 1)
            card = self.cards.pop(index)
            move = Move(choice, card=card)

        elif choice == Choice.DISCARD:
            index = random.randint(0, len(self.cards) - 1)
            card = self.cards.pop(index)
            move = Move(choice, card=card)

        else:
            raise ValueError("Not valid move created for choice: {}".format(choice))

        return move
