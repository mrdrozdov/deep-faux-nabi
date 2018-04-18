import random


class Player(object):
    def __init__(self, name):
        super(Player, self).__init__()
        self.name = name
        self.cards = []

    def give(self, card):
        self.cards.append(card)

    def play(self, index):
        return self.cards.pop(index)

    def decide(self):
        return random.randint(0, len(self.cards) - 1)
