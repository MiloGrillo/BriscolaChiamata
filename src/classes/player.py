import numpy as np


class Player:
    id_count = 0

    def __init__(self):
        self.id_ = Player.id_count
        Player.id_count += 1

        self.dealt_cards = []
        self.cards_in_hand = []

        self.won_cards = []

        self.role = None

    def win_round(self, cards):
        self.won_cards.extend(cards)

    def get_cards_dealt(self, cards):
        self.dealt_cards = cards.copy()
        self.cards_in_hand = cards.copy()

    def play_card(self):
        card = np.random.choice(self.cards_in_hand)
        self.cards_in_hand.remove(card)
        return card

    def choose_briscola(self, cards):
        return np.random.choice(cards)

    def set_role(self, role):
        self.role = role

    def make_bid(self):
        """return a number or pass"""
        return []
