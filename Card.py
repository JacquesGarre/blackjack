

class Card:

    FACES = ['J', 'Q', 'K']
    ACE = 'A'
    COLORS = ['spade', 'heart', 'diamond', 'club']

    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.hidden = False

    def score(self):
        score = self.value
        if self.value in self.FACES:
            score = 10
        return score

    def hide(self):
        self.hidden = True
