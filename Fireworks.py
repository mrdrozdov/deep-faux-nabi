fwINVALID = 0
fwVALID = 1
fwMOST = 2
fwWIN = 3


fwMESSAGES = {
    0: 'Player played an invalid card and it was discarded.',
    1: 'Player played a valid card.',
    2: 'Player played a valid card and it completed a stack.',
    3: 'Player played the winning card!'
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

    def update(self, card):
        success = self.state[card.color] == card.value - 1

        if success:
            self.state[card.color] = card.value
        else:
            return fwINVALID

        if self.state[card.color] == len(self.config.n_numbers):
            self.complete += 1

            if self.complete == self.config.n_colors:
                return fwWIN
            else:
                return fwMOST

        return fwVALID
