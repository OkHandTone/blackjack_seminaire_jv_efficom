import pygame

from components.card import Card

from .player import Player


class Croupier(Player):
    def __init__(self):
        super().__init__(name="Croupier", player_number=1)

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

    def play_dealer_turn(self, deck):
        """Play dealer's turn according to blackjack rules (hit until 17)"""
        while self.calculate_score() < 17:
            if len(deck) > 0:
                rank, suit = deck.pop()
                self.add_card((rank, suit))
                card_index = len(self.hand) - 1
                Card(rank, suit, card_index, self.player_number, True)
                self.show_hand()
            else:
                break
        return self.calculate_score()

    def hit(self, deck):
        if len(deck) > 0:
            rank, suit = deck.pop()
            self.add_card((rank, suit))
            card_index = len(self.hand) - 1
            Card(rank, suit, card_index, self.player_number, True)
            return True
        return False

    def should_hit(self):
        return self.calculate_score() < 17

    def is_busted(self):
        """Check if dealer's score exceeds 21"""
        return self.calculate_score() > 21

    def clear_hand(self):
        """Clear dealer's hand for new game"""
        self.hand = []

    def get_visible_score(self):
        """Get the visible score (first card only) for display"""
        if len(self.hand) > 0:
            visible_card = self.hand[0]
            rank = visible_card[0]
            return self.point_values.get(rank, 0)
        return 0
