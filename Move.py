class Move(object):
    def __init__(self, card=None, hint=None):
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
