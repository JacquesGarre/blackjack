from Card import Card
import random

class Deck:

    def __init__(self):
        self.cards = self.generate_cards()

    def generate_cards(self):
        cards = []
        values = [card for card in range(2,11)] + Card.FACES + [Card.ACE]
        for color in Card.COLORS:
            for value in values:
                cards.append(Card(color, value))
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    
    
