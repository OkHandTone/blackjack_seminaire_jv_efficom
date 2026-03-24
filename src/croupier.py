from player import Player


class Croupier(Player):
    def __init__(self):
        super().__init__(name="Croupier")

    def show_initial_hand(self):
        visible_card = self.hand[0]
        print(f"Croupier's initial hand: [{visible_card}, ('?', '?')]")
