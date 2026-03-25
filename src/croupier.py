from player import Player


class Croupier(Player):
    def __init__(self):
        super().__init__(name="Croupier")

    def show_initial_hand(self):
        visible_card = self.hand[0]
        rank = visible_card[0]
        score_visible = self.point_values[rank]

        # 3. On affiche la main avec le score visible
        print(
            f"Croupier's initial hand: [{visible_card}, ('?', '?')] (Score visible : {score_visible})"
        )

        # 4. [ASTUCE DEV] On affiche le vrai score total pour toi dans la console
        print(
            f"[DEBUG Backend] Vrai score total du croupier : {self.calculate_score()}"
        )
