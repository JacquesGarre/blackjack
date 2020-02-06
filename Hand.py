from Card import Card

class Hand:

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def is_blackjack(self):
        aces = self.__get_cards_split_by_aces()[0]
        return len(aces) == 2 and self.score() == 21

    def score(self):
        score = 0
        aces, others = self.__get_cards_split_by_aces()
        for card in others:
            if not card.hidden:
                score += card.score()
        aces_score = 0
        for ace in aces:
            if not ace.hidden:
                aces_score += 11
            else:
                aces.remove(ace)
        while score + aces_score > 21 and len(aces) != 0:
            aces_score -= 10
            aces.pop()
        return score + aces_score

    def to_string(self):
        string = ""
        for card in self.cards:
            if card.hidden:
                string += "carte cachée, "
            else:
                string += str(card.value) + ", "
        return string

    def __get_cards_split_by_aces(self):
        aces = []
        others = []
        for card in self.cards:
            if card.value is Card.ACE:
                aces.append(card)
            else:
                others.append(card)
        return aces, others

    def unhide(self):
        for card in self.cards:
            card.hidden = False