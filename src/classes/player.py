import numpy as np
from src.helper_functions import *


class Player:
    id_count = 0

    def __init__(self):
        self.id_ = Player.id_count
        Player.id_count += 1

        self.dealt_cards = []
        self.cards_in_hand = []

        self.won_cards = []

        self.role = None

        self.score = 0  # overall score of the game

    def count_points(self, points_per_card_value):
        """Counts the amount of won points"""
        total_points = 0
        for card in self.won_cards:
            total_points += points_per_card_value[card.value]
        return total_points

    def reset_won_cards(self):
        self.won_cards = []

    def win_round(self, cards):
        self.won_cards.extend(cards)

    def get_cards_dealt(self, cards):
        self.dealt_cards = cards.copy()
        self.cards_in_hand = cards.copy()

    def play_card(self):
        """Play a card when it's your turn."""
        answer = input(f'Play a card. The cards in your hand are {self.cards_in_hand}')
        while not check_if_string_is_card(answer, self.cards_in_hand):
            answer = input(f'This is not a valid card in your hand. Please choose again.')
        answer = answer.split()
        card = Card(answer[0], answer[1])

        self.cards_in_hand.remove(card)
        return card

    def choose_briscola(self, cards):
        """Choose the briscola card, i.e. your partner card, if you won the bidding."""
        answer = input(f'Choose a card to be the Briscola. Give your answer as "suit value". The cards you can choose'
                       f'from are {cards}')
        while not check_if_string_is_card(answer, cards):
            answer = input('That is not a valid card, choose again.')
        answer = answer.split()
        return Card(answer[0], answer[1])

    def set_role(self, role):
        self.role = role

    def make_bid(self):
        """return a number or pass. Passing is done by giving a number lower than the previous bid"""
        bid = input('Make a bid')
        while (not bid.isnumeric()) or (int(bid) < 0):
            bid = input('That is not a valid bid. A bid must be an integer. Please try again.')
        return int(bid)
