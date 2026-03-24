from player import Player


class Croupier(Player):
    def __init__(self):
        super().__init__(nom="Croupier")

    def show_card(self):
        carte_visible = self.main[0]
        print(f"Main initiale du Croupier : [{carte_visible}, ('?', '?')]")
