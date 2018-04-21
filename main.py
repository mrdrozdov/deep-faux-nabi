import random

from Card import Card
from Deck import Deck
from Fireworks import State as FWState
from Fireworks import Fireworks
from Game import State as GameState
from Game import Game
from GameConfig import GameConfig


if __name__ == '__main__':
    random.seed(11)

    config = GameConfig()
    game = Game(config).reset()

    while game.play_turn() == GameState.CONTINUE:
        print(game.message)
