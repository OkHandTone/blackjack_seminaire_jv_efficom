from player import Player


class Croupier(Player):
    def __init__(self):
        super().__init__(nom="Croupier")

    def afficher_main_initiale(self):
        carte_visible = self.main[0]
        print(f"Main initiale du Croupier : [{carte_visible}, ('?', '?')]")
