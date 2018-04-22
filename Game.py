from Fireworks import State as FWState
from Fireworks import Fireworks
from Deck import Deck
from GameView import GameView
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
            players.append(Player(player_names[i], i))

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

    def consume_hint(self, hint):
        player_index = hint.player_index
        cards = self.players[player_index].cards
        if hint.has_color():
            for c in cards:
                if c.color == hint.color:
                    c.color_revealed = True
        else:
            for c in cards:
                if c.value == hint.value:
                    c.value_revealed = True
        self.hints -= 1

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

    @staticmethod
    def build_message(player, move, fw_state, game_state):
        if move.has_card():
            move_message = 'Card=[color={}, value={}]'.format(
                move.card.color, move.card.value)
        else:
            move_message = 'Hint=[player={}, color={}, value={}]'.format(
                move.hint.player_index, move.hint.color, move.hint.value)
        return 'Player={} {} FWState={} GameState={}'.format(
            player.name, move_message, fw_state, game_state)

    def get_view_for_player(self, player_index):
        return GameView.build(self, player_index)

    def play_turn(self):
        player = self.players[self.turn]
        game_view = self.get_view_for_player(self.turn)
        move = player.play(game_view)

        if move.has_card():
            card = move.card
            fw_state = self.fireworks.update(card)
            game_state = self.consume_fw_state(fw_state)

            if game_state is State.CONTINUE:
                game_state = self.draw_card(player)
        else:
            self.consume_hint(move.hint)
            fw_state = None
            game_state = State.CONTINUE

        if game_state is State.CONTINUE:
            self.increment_turn()

        self.message = Game.build_message(player, move, fw_state, game_state)
        self.game_state = game_state

        return self.game_state

