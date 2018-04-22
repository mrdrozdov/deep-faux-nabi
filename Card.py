class Card(object):
    def __init__(self, color, value, color_revealed=False, value_revealed=False):
        super(Card, self).__init__()
        self.color = color
        self.value = value
        self.color_revealed = color_revealed
        self.value_revealed = value_revealed

    def reveal_color(self):
        self.color_revealed = True

    def reveal_value(self):
        self.value_revealed = True
        