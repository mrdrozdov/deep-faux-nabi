import random

from Card import Card


class Deck(object):
    def __init__(self, config):
        super(Deck, self).__init__()
        self.config = config
        self.cards = []
        self.discarded = []

    def reset(self):
        n_colors = self.config.n_colors
        n_numbers = self.config.n_numbers
        cards = []

        for c in range(n_colors):
            for i, n in enumerate(n_numbers):
                for _ in range(n):
                    cards.append(Card(color=c, value=i+1))

        random.shuffle(cards)

        self.cards = cards
        self.discarded = []

    def draw(self):
        return self.cards.pop()

    def discard(self, card):
        self.discarded.append(card)
        