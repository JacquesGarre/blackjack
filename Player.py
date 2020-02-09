from Hand import Hand

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def show_hand(self):
        print("La main de {} contient les cartes suivantes: {}\nIl totalise un score de {} points. {}".format(
            self.name,
            self.hand.to_string(),
            self.hand.score(),
            "BLACKJACK!" if self.hand.is_blackjack() else ""
        ))
