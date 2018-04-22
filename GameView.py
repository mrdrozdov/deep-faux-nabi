from Card import Card
from Hint import Hint


class GameView(object):
    def __init__(self, players, player_index, hints, lives):
        view = {}

        for i, p in enumerate(players):
            view[i] = p.cards

        def card_view(card):
            return Card(
                color=card.color if card.color_revealed else None,
                value=card.value if card.value_revealed else None,
                color_revealed=card.color_revealed,
                value_revealed=card.value_revealed
                )

        view[player_index] = map(card_view, players[player_index].cards)

        self.player_index = player_index
        self.hints = hints
        self.lives = lives
        self.view = view

    def has_hints(self):
        return self.lives > 0

    def possible_hints(self):
        # TODO: Ideally this should have amortized constant time lookup.

        hints = []

        for player_index in self.view.keys():
            if player_index == self.player_index:
                continue
            colors = set(c.color for c in self.view[player_index] if not c.color_revealed)
            hints += [Hint(player_index, color=c) for c in colors]
            values = set(c.value for c in self.view[player_index] if not c.value_revealed)
            hints += [Hint(player_index, value=v) for v in values]

        return hints

    @staticmethod
    def build(game, player_index):
        return GameView(game.players, player_index, game.hints, game.lives)
