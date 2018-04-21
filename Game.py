from Fireworks import State as FWState
from Fireworks import Fireworks
from Deck import Deck
from Player import Player


player_names = [
    'Anna', 'Bob', 'Chance', 'Dexter', 'Eric', 'Frank'
]


class State:
    CONTINUE = 0
    GAMEOVER = 1
    WIN = 2


class Game(object):
    def __init__(self, config):
        super(Game, self).__init__()
        self.config = config
        self.players = []
        self.deck = None
        self.fireworks = None
        self.hints = None
        self.lives = None
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
        self.hints = self.config.n_hints
        self.lives = self.config.n_lives
        self.turn = 0
        self.turns = 0
        self.turns_without_drawing = 0

        return self

    def consume_fw_state(self, fw_state):
        if fw_state == FWState.INVALID:
            self.lives -= 1
            game_state = State.GAMEOVER if self.lives < 0 else State.CONTINUE
        elif fw_state == FWState.VALID:
            game_state = State.CONTINUE
        elif fw_state == FWState.MOST:
            self.hints = min(self.hints + 1, self.config.n_hints)
            game_state = State.CONTINUE
        elif fw_state == FWState.WIN:
            game_state = State.WIN
        else:
            raise ValueError("Does not support Fireworks.State == {}".format(fw_state))
        return game_state

    def draw_card(self, player):
        if len(self.deck.cards) > 0:
            player.give(self.deck.draw())
            return State.CONTINUE
        
        if self.turns_without_drawing == len(self.players) - 1:
            return State.GAMEOVER

        self.turns_without_drawing += 1

        return State.CONTINUE

    def increment_turn(self):
        self.turn = (self.turn + 1) % len(self.players)
        self.turns += 1

    def play_turn(self):
        player = self.players[self.turn]
        card = player.play(player.decide())
        fw_state = self.fireworks.update(card)
        game_state = self.consume_fw_state(fw_state)

        if game_state is State.CONTINUE:
            game_state = self.draw_card(player)

        if game_state is State.CONTINUE:
            self.increment_turn()

        self.game_state = game_state

        return self.game_state

