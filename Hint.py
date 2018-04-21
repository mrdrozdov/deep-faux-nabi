class Hint(object):
    def __init__(self, player, color=None, value=None):
        self.player = player
        self.color = color
        self.value = value

        if self.color is None and self.value is None:
            raise ValueError('Hint must have value or color.')
        if self.color is not None and self.value is not None:
            raise ValueError('Hint can not have value and color.')

    def has_color(self):
        return self.color is not None

    def has_value(self):
        return self.value is not None
        