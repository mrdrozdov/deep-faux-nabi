class Choice:
    CARD = 0
    DISCARD = 1
    HINT = 2


class Move(object):
    def __init__(self, choice, card=None, hint=None):
        self.choice = choice
        self.card = card
        self.hint = hint

        if self.card is None and self.hint is None:
            raise ValueError('Move must have hint or card.')
        if self.card is not None and self.hint is not None:
            raise ValueError('Move can not have hint and card.')

    def has_card(self):
        return self.card is not None

    def has_hint(self):
        return self.hint is not None
