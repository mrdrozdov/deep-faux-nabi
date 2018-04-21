class State:
    INVALID = 0
    VALID = 1
    MOST = 2
    WIN = 3


MESSAGES = {
    State.INVALID: 'Player played an invalid card and it was discarded.',
    State.VALID: 'Player played a valid card.',
    State.MOST: 'Player played a valid card and it completed a stack.',
    State.WIN: 'Player played the winning card!'
}


class Fireworks(object):
    def __init__(self, config):
        super(Fireworks, self).__init__()
        self.config = config
        self.state = None
        self.complete = None

    def reset(self):
        n_colors = self.config.n_colors
        state = {i: 0 for i in range(n_colors)}

        self.state = state
        self.complete = 0

        return self

    def update(self, card):
        success = self.state[card.color] == card.value - 1

        if success:
            self.state[card.color] = card.value
        else:
            return State.INVALID

        if self.state[card.color] == len(self.config.n_numbers):
            self.complete += 1

            if self.complete == self.config.n_colors:
                return State.WIN
            else:
                return State.MOST

        return State.VALID
