import numpy as np
from src.helper_functions import *

# from trick import Trick



STARTING_BID = 70


class BriscolaChiamata:
    num_tricks_per_round = 8

    values_en = ['A', '3', 'K', 'H', 'I', '7', '6', '5', '4', '2']
    points = {'A': 11, '3': 10, 'K': 4, 'H': 3, 'I': 2, '7': 0, '6': 0, '5': 0, '4': 0, '2': 0}
    suits = ['Gold', 'Bat', 'Coin', 'Sword']

    cards = [Card(value, suit) for value in values_en for suit in suits]

    def __init__(self, players):
        self.players = players
        self.rounds = []
        self.dealer = None

    def play(self):
        while True:
            self.next_dealer()
            round = Round(self.players, self.dealer)
            round.play()
            self.rounds.append(round)

        self.players = sorted(self.players, key=lambda x: x.score)
        print(f'Final scores: {player.id_ + ": " + player.score for player in self.players}; ')

    def next_dealer(self):
        self.dealer = self.players[len(self.rounds) % len(self.players)]


class Round:
    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        self.tricks = []

        self.briscola = None
        self.bid_winner = None
        self.partner = None
        self.bid_value = None

    def play(self):
        self.reset_roles()
        for player in self.players:
            player.reset_won_cards()

        self.deal()
        self.bid_winner, self.bid_value = self.bidding(self.dealer)
        self.bid_winner.set_role('BID_WINNER')

        starting_player = self.dealer
        for i in range(BriscolaChiamata.num_tricks_per_round):
            trick = Trick(starting_player, self.players)
            trick_winner = trick.play(self)
            starting_player = trick_winner

        points_per_card = BriscolaChiamata.points
        points_won = self.bid_winner.count_points(points_per_card) + self.partner.count_points(points_per_card)

        if points_won >= self.bid_value:
            sign = 1
        else:
            sign = -1

        self.bid_winner.score += sign * 2
        self.partner += sign * 1
        for player in self.players:
            if player.role == 'Regular':
                player.score -= sign * 1


    def count_points(self):


    def reset_roles(self):
        for player in self.players:
            player.set_role(None)

    def bidding(self, starting_player):
        """Start the bidding process to determine the amount to be scored, and the bid winner. The bidding process
        takes turns, clockwise, starting from the dealer."""
        self.player_order = self.players[starting_player.id_:] + self.players[:starting_player.id_]
        players_in_bidding = {player.id_: True for player in self.players}

        i = 0
        current_highest_player = self.player_order[0]
        current_highest_bid = max(STARTING_BID, self.player_order[0].make_bid())
        while np.sum(list(players_in_bidding.values())) != 0:
            count = i // len(self.player_order)
            player = self.player_order[count]

            if players_in_bidding[player.id_] is False:
                i += 1
                continue

            if player.id_ == current_highest_player.id_:
                break

            bid = player.make_bid()
            if bid < current_highest_bid:
                players_in_bidding[player.id_] = False
                i += 1
                continue

            current_highest_player, current_highest_bid = player, bid
            i += 1

        current_highest_player.set_role('Bid Winner')
        return current_highest_player, current_highest_bid

    def deal(self):
        """Give every player 8 unique cards."""
        cards = BriscolaChiamata.cards.copy()
        cards = np.random.shuffle(cards)
        num_players = len(self.players)
        num_cards_per_player = num_players // BriscolaChiamata.num_tricks_per_round
        for i, player in enumerate(self.players):
            k = i * num_cards_per_player
            player.get_cards_dealt(cards[k: k + num_cards_per_player])

    def set_briscola(self):
        """Determine the Briscola"""
        self.briscola = self.bid_winner.choose_briscola(BriscolaChiamata.cards)
        for player in self.players:
            if self.briscola in player.dealt_cards:
                self.partner = player
                self.partner.set_role('Partner')
                break
        for player in self.players:
            if player.role is None:
                player.set_role('Regular')


class Trick:
    def __init__(self, starting_player, players):
        self.starting_player = starting_player
        
        # maybe this can be done neater
        self.player_order = players[starting_player.id_:] + players[:starting_player.id_]
    
    def play(self, round):
        """Every player plays one card in clockwise order."""
        played_cards = []
        
        for player in self.player_order:
            played_cards.append(player.play_card())
            
        if round.briscola.suit is None:
            round.set_briscola()

        winner = self.determine_winner(played_cards, round.briscola.suit, BriscolaChiamata.values_en)
        winner.win_trick(played_cards)
        return winner
            
    def determine_winner(self, played_cards, briscola_suit, card_values):
        """The winner of a round is the player who played the best card. Priorities are: 1) Briscola suit, 2) starting
        suit 3) card value"""
        if any([card.suit == briscola_suit for card in played_cards]):
            briscola_cards_played = [card for card in played_cards if card.suit == briscola_suit]
            winning_card = max(briscola_cards_played, card_values)
        else:
            first_suit = played_cards[0].suit
            first_suit_cards_played = [card for card in played_cards if card.suit == first_suit]
            winning_card = max(first_suit_cards_played, card_values)

        player_index = played_cards.index(winning_card)    
        winner = self.player_order[player_index]
        return winner
