from Fireworks import Fireworks, fwMESSAGES
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
        self.turn = None

    def reset(self):
        n_players = self.config.n_players
        players = []

        for i in range(n_players):
            players.append(Player(player_names[i]))

        self.fireworks = Fireworks(self.config)
        self.deck = Deck(self.config)
        self.players = players
        self.turn = 0

    def turn(self):
        player = self.players[self.turn]
        card = player.play(player.decide())
        state = self.fireworks.update(card)
        player.give(self.deck.draw())
