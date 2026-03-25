class Player:
    point_values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
    }

    def __init__(self, name="Player"):
        self.name = name
        self.hand = []

    def add_card(self, card_data):
        self.hand.append(card_data)

    def calculate_score(self):
        return sum(self.point_values[rank] for rank, suit in self.hand)

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand} (Score: {self.calculate_score()})")
