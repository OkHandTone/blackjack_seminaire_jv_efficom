from settings import POINT_VALUE


class Player:
    point_values = POINT_VALUE

    def __init__(self, name="Player"):
        self.name = name
        self.hand = []

    def add_card(self, card_data):
        self.hand.append(card_data)

    def calculate_score(self):
        return sum(self.point_values[rank] for rank, suit in self.hand)

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand} (Score: {self.calculate_score()})")
