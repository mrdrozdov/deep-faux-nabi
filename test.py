import unittest
import random

from Card import Card
from Deck import Deck
from Fireworks import State as FWState
from Fireworks import Fireworks
from Game import Game
from GameConfig import GameConfig


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
        game.play_turn()
        self.assertEqual(game.turn, 1)
        self.assertEqual(game.turns, 1)

    def test_increment_turn_twice(self):
        game = Game(self.config).reset()
        game.play_turn().play_turn()
        self.assertEqual(game.turn, 0)
        self.assertEqual(game.turns, 2)


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