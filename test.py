import unittest
import random

from Card import Card
from Deck import Deck
from Fireworks import fwINVALID, fwVALID, fwMOST, fwWIN
from Fireworks import Fireworks
from GameConfig import GameConfig


class TestDeck(unittest.TestCase):
    def setUp(self):
        random.seed(11)
        self.config = GameConfig()

    def test_reset_card_count(self):
        deck = Deck(self.config)
        deck.reset()
        expected = self.config.n_colors * sum(self.config.n_numbers)
        self.assertEqual(len(deck.cards), expected)

    def test_reset_discarded_count(self):
        deck = Deck(self.config)
        deck.reset()
        expected = 0
        self.assertEqual(len(deck.discarded), expected)

    def test_values(self):
        deck = Deck(self.config)
        deck.reset()
        values = [card.value for card in deck.cards]
        self.assertEqual(min(values), 1)
        self.assertEqual(max(values), len(self.config.n_numbers))

    def test_draw(self):
        deck = Deck(self.config)
        deck.reset()
        expected_card_count = len(deck.cards) - 1
        expected = deck.cards[-1]
        actual = deck.draw()
        self.assertEqual(len(deck.cards), expected_card_count)
        self.assertEqual(actual.color, expected.color)
        self.assertEqual(actual.value, expected.value)

    def test_discard(self):
        deck = Deck(self.config)
        deck.reset()
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
        fw = Fireworks(self.config)
        fw.reset()
        self.assertEqual(fw.complete, 0)

    def test_reset_state(self):
        fw = Fireworks(self.config)
        fw.reset()
        self.assertEqual(len(fw.state), self.config.n_colors)
        for c in range(self.config.n_colors):
            self.assertEqual(fw.state[c], 0)

    def test_update_invalid(self):
        fw = Fireworks(self.config)
        fw.reset()
        card = Card(color=0, value=2)
        response = fw.update(card)
        self.assertEqual(response, fwINVALID)

    def test_update_valid(self):
        fw = Fireworks(self.config)
        fw.reset()
        card = Card(color=0, value=1)
        response = fw.update(card)
        self.assertEqual(response, fwVALID)

    def test_update_most(self):
        fw = Fireworks(self.config)
        fw.reset()
        fw.state[0] = len(self.config.n_numbers) - 1
        card = Card(color=0, value=len(self.config.n_numbers))
        response = fw.update(card)
        self.assertEqual(response, fwMOST)

    def test_update_win(self):
        fw = Fireworks(self.config)
        fw.reset()
        fw.state = {i: len(self.config.n_numbers) for i in range(self.config.n_colors)}
        fw.state[0] -= 1
        fw.complete = self.config.n_colors - 1
        card = Card(color=0, value=len(self.config.n_numbers))
        response = fw.update(card)
        self.assertEqual(response, fwWIN)


if __name__ == '__main__':
    unittest.main()