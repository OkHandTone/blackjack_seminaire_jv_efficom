import pygame

from components.card import Card
from settings import POINT_VALUE


class Player:
    point_values = POINT_VALUE

    def __init__(self, name="Player", player_number=2):
        self.name = name
        self.hand = []
        self.player_number = player_number

    def add_card(self, card_data):
        self.hand.append(card_data)

    def calculate_score(self):
        return sum(self.point_values[rank] for rank, suit in self.hand)

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand} (Score: {self.calculate_score()})")

    def hit(self, deck):
        if len(deck) > 0:
            rank, suit = deck.pop()
            self.add_card((rank, suit))
            card_index = len(self.hand) - 1
            Card(rank, suit, card_index, self.player_number, True)
            return True
        return False

    def should_stand(self):
        score = self.calculate_score()
        return score >= 21

    def is_busted(self):
        return self.calculate_score() > 21

    def has_blackjack(self):
        return self.calculate_score() == 21 and len(self.hand) == 2

    def clear_hand(self):
        self.hand = []
