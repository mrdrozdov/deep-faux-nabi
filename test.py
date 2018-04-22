import unittest
import mock
import random

from Card import Card
from Deck import Deck
from Fireworks import State as FWState
from Fireworks import Fireworks
from Game import State as GameState
from Game import Game
from GameConfig import GameConfig
from Move import Choice
from Player import Player


def force_choice(game, choice):
    player = game.players[game.turn]
    player.choose = mock.MagicMock(return_value=choice)

class TestGame(unittest.TestCase):
    def setUp(self):
        random.seed(11)
        self.config = GameConfig()

    def test_reset_game(self):
        game = Game(self.config).reset()
        self.assertTrue(game.deck is not None)
        self.assertTrue(game.fireworks is not None)
        self.assertTrue(game.turn is 0)
        self.assertEqual(len(game.players), self.config.n_players)

    def test_cards_drawn(self):
        game = Game(self.config).reset()
        n_cards = self.config.n_colors * sum(self.config.n_numbers)
        n_cards_drawn = len(game.players) * self.config.n_cards_per_hand
        for p in game.players:
            self.assertEqual(len(p.cards), self.config.n_cards_per_hand)
        self.assertEqual(len(game.deck.cards), n_cards - n_cards_drawn)

    def test_increment_turn(self):
        game = Game(self.config).reset()
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.turn, 1)
        self.assertEqual(game.turns, 1)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_increment_turn_twice(self):
        game = Game(self.config).reset()
        force_choice(game, Choice.CARD)
        game.play_turn()
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.turn, 0)
        self.assertEqual(game.turns, 2)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_fw_state_invalid(self):
        game = Game(self.config).reset()
        self.assertEqual(game.lives, 3)
        game.fireworks.update = mock.MagicMock(return_value=FWState.INVALID)
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.lives, 2)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_fw_state_valid(self):
        game = Game(self.config).reset()
        self.assertEqual(game.lives, 3)
        game.fireworks.update = mock.MagicMock(return_value=FWState.VALID)
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.lives, 3)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_fw_state_most(self):
        game = Game(self.config).reset()
        game.hints -= 1
        self.assertEqual(game.hints, 7)
        game.fireworks.update = mock.MagicMock(return_value=FWState.MOST)
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.hints, 8)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_fw_state_win(self):
        game = Game(self.config).reset()
        game.fireworks.update = mock.MagicMock(return_value=FWState.WIN)
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game_state, GameState.WIN)

    def test_gameover_nolives(self):
        game = Game(self.config).reset()
        game.lives = 0
        self.assertEqual(game.lives, 0)
        game.fireworks.update = mock.MagicMock(return_value=FWState.INVALID)
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game.lives, -1)
        self.assertEqual(game_state, GameState.GAMEOVER)

    def test_gameover_nocards(self):
        game = Game(self.config).reset()
        game.turns_without_drawing = 1
        game.deck.cards = []
        force_choice(game, Choice.CARD)
        game_state = game.play_turn()
        self.assertEqual(game_state, GameState.GAMEOVER)

    def test_give_hint(self):
        game = Game(self.config).reset()
        n_cards = len(game.deck.cards)
        n_hints = game.hints
        force_choice(game, Choice.HINT)
        game_state = game.play_turn()
        self.assertEqual(len(game.deck.cards), n_cards)
        self.assertEqual(game.hints, n_hints-1)
        self.assertEqual(game_state, GameState.CONTINUE)

    def test_possible_hints(self):
        game = Game(self.config).reset()
        turn = game.turn
        n_initial_hints = len(game.get_view_for_player(turn).possible_hints())
        force_choice(game, Choice.HINT)
        game.play_turn()
        n_remaining_hints = len(game.get_view_for_player(turn).possible_hints())
        self.assertTrue(n_remaining_hints < n_initial_hints)

    def test_discard(self):
        game = Game(self.config).reset()
        game.hints -= 1
        n_cards = len(game.deck.cards)
        n_hints = game.hints
        player = game.players[game.turn]
        force_choice(game, Choice.DISCARD)
        game_state = game.play_turn()
        self.assertEqual(len(game.deck.cards), n_cards-1)
        self.assertEqual(game.hints, n_hints+1)
        self.assertEqual(game_state, GameState.CONTINUE)
        self.assertEqual(len(player.cards), self.config.n_cards_per_hand)

    def test_discard_max_hints(self):
        game = Game(self.config).reset()
        n_cards = len(game.deck.cards)
        n_hints = game.hints
        player = game.players[game.turn]
        force_choice(game, Choice.DISCARD)
        game_state = game.play_turn()
        self.assertEqual(len(game.deck.cards), n_cards-1)
        self.assertEqual(game.hints, n_hints)
        self.assertEqual(game_state, GameState.CONTINUE)
        self.assertEqual(len(player.cards), self.config.n_cards_per_hand)

    def test_discard_empty_deck(self):
        game = Game(self.config).reset()
        game.deck.cards = []
        n_hints = game.hints
        player = game.players[game.turn]
        force_choice(game, Choice.DISCARD)
        game_state = game.play_turn()
        self.assertEqual(len(game.deck.cards), 0)
        self.assertEqual(game.hints, n_hints)
        self.assertEqual(game_state, GameState.CONTINUE)
        self.assertEqual(len(player.cards), self.config.n_cards_per_hand-1)

    def test_discard_empty_deck_gameover(self):
        game = Game(self.config).reset()
        game.turns_without_drawing = 1
        game.deck.cards = []
        n_hints = game.hints
        player = game.players[game.turn]
        force_choice(game, Choice.DISCARD)
        game_state = game.play_turn()
        self.assertEqual(game_state, GameState.GAMEOVER)

    def test_play_til_end(self):
        game = Game(self.config).reset()
        while game.play_turn() == GameState.CONTINUE:
            pass
        self.assertNotEqual(game.game_state, GameState.CONTINUE)


class TestDeck(unittest.TestCase):
    def setUp(self):
        random.seed(11)
        self.config = GameConfig()

    def test_reset_card_count(self):
        deck = Deck(self.config).reset()
        expected = self.config.n_colors * sum(self.config.n_numbers)
        self.assertEqual(len(deck.cards), expected)

    def test_reset_discarded_count(self):
        deck = Deck(self.config).reset()
        expected = 0
        self.assertEqual(len(deck.discarded), expected)

    def test_values(self):
        deck = Deck(self.config).reset()
        values = [card.value for card in deck.cards]
        self.assertEqual(min(values), 1)
        self.assertEqual(max(values), len(self.config.n_numbers))

    def test_draw(self):
        deck = Deck(self.config).reset()
        expected_card_count = len(deck.cards) - 1
        expected = deck.cards[-1]
        actual = deck.draw()
        self.assertEqual(len(deck.cards), expected_card_count)
        self.assertEqual(actual.color, expected.color)
        self.assertEqual(actual.value, expected.value)

    def test_discard(self):
        deck = Deck(self.config).reset()
        card = deck.draw()
        expected = len(deck.discarded) + 1
        deck.discard(card)
        discarded = deck.discarded[-1]
        self.assertEqual(len(deck.discarded), expected)
        self.assertEqual(card.color, discarded.color)
        self.assertEqual(card.value, discarded.value)


class TestFireworks(unittest.TestCase):
    def setUp(self):
        random.seed(11)
        self.config = GameConfig()

    def test_reset_complete(self):
        fw = Fireworks(self.config).reset()
        self.assertEqual(fw.complete, 0)

    def test_reset_state(self):
        fw = Fireworks(self.config).reset()
        self.assertEqual(len(fw.state), self.config.n_colors)
        for c in range(self.config.n_colors):
            self.assertEqual(fw.state[c], 0)

    def test_update_invalid(self):
        fw = Fireworks(self.config).reset()
        card = Card(color=0, value=2)
        response = fw.update(card)
        self.assertEqual(response, FWState.INVALID)

    def test_update_valid(self):
        fw = Fireworks(self.config).reset()
        card = Card(color=0, value=1)
        response = fw.update(card)
        self.assertEqual(response, FWState.VALID)

    def test_update_most(self):
        fw = Fireworks(self.config).reset()
        fw.state[0] = len(self.config.n_numbers) - 1
        card = Card(color=0, value=len(self.config.n_numbers))
        response = fw.update(card)
        self.assertEqual(response, FWState.MOST)

    def test_update_win(self):
        fw = Fireworks(self.config).reset()
        fw.state = {i: len(self.config.n_numbers) for i in range(self.config.n_colors)}
        fw.state[0] -= 1
        fw.complete = self.config.n_colors - 1
        card = Card(color=0, value=len(self.config.n_numbers))
        response = fw.update(card)
        self.assertEqual(response, FWState.WIN)


if __name__ == '__main__':
    unittest.main()