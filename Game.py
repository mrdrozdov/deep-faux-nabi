from Fireworks import Fireworks
from Deck import Deck
from Player import Player


player_names = [
    'Anna', 'Bob', 'Cara', 'Dexter', 'Eric', 'Frank'
]


class Game(object):
    def __init__(self, config):
        super(Game, self).__init__()
        self.config = config
        self.players = []
        self.deck = None
        self.fireworks = None
        self.turn = None
        self.turns = None

    def reset(self):
        n_players = self.config.n_players
        n_cards_per_hand = self.config.n_cards_per_hand

        deck = Deck(self.config).reset()
        fireworks = Fireworks(self.config).reset()
        players = []

        for i in range(n_players):
            players.append(Player(player_names[i]))

        for _ in range(n_cards_per_hand):
            for p in players:
                p.give(deck.draw())

        self.deck = deck
        self.fireworks = fireworks
        self.players = players
        self.turn = 0
        self.turns = 0

        return self

    def play_turn(self):
        player = self.players[self.turn]
        card = player.play(player.decide())
        state = self.fireworks.update(card)
        player.give(self.deck.draw())
        self.turn = (self.turn + 1) % len(self.players)
        self.turns += 1
        return self
