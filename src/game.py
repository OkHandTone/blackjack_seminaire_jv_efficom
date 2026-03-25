import random

import pygame

from card import Card
from croupier import Croupier
from player import Player
from settings import DISPLAY_CAPTION, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player1 = Player(name="Joueur Principal")
        self.dealer = Croupier()

        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [(r, s) for s in suits for r in ranks]
        random.shuffle(self.deck)

        self.deal_initial_cards()
        self.total_score_players()

    def deal_initial_cards(self):

        for i in range(2):
            rank, suit = self.deck.pop()
            self.dealer.add_card((rank, suit))  # Sauvegarde backend
            is_flipped = True if i == 0 else False
            Card(rank, suit, i, 1, is_flipped)

        for i in range(2):
            rank, suit = self.deck.pop()
            self.player1.add_card((rank, suit))  # Sauvegarde backend
            Card(rank, suit, i, 2, True)

        self.player1.show_hand()
        self.dealer.show_initial_hand()

    def total_score_players(self):
        return self.player1.calculate_score(), self.dealer.calculate_score()

    def player_hit(self):
        """Action de tirer une nouvelle carte UNIQUEMENT pour le Joueur (ID 2)."""
        if len(self.deck) > 0:
            rank, suit = self.deck.pop()
            self.player1.add_card((rank, suit))
            card_index = len(self.player1.hand) - 1
            Card(rank, suit, card_index, 2, True)

            print("\n--- Le joueur (ID 2) a tiré une carte ! ---")
            self.player1.show_hand()
            for sprite_card in Card.instances:
                if sprite_card.player == 1 and sprite_card.cards == 1:
                    sprite_card.show()

    def player_stand(self):
        """Action de rester (Stand) pour le joueur. C'est au tour du croupier."""
        print("\n--- Le joueur reste. Au tour du croupier ! ---")

        for sprite_card in Card.instances:
            if sprite_card.player == 1 and sprite_card.cards == 1:
                sprite_card.show()
        self.dealer.show_hand()

        while self.dealer.calculate_score() < 17:
            if len(self.deck) > 0:
                rank, suit = self.deck.pop()
                self.dealer.add_card((rank, suit))  # Backend

                card_index = len(self.dealer.hand) - 1
                Card(rank, suit, card_index, 1, True)

                print("Le croupier tire une carte...")
                self.dealer.show_hand()

        self.check_winner()

    def check_winner(self):
        """Compare les scores et annonce le gagnant dans la console."""
        player_score = self.player1.calculate_score()
        dealer_score = self.dealer.calculate_score()

        print("\n=== RÉSULTATS DE LA MANCHE ===")
        print(f"Score final du Joueur   : {player_score}")
        print(f"Score final du Croupier : {dealer_score}")

        if player_score > 21:
            print("=> Le joueur a dépassé 21 (Bust). Le Croupier gagne !")
        elif dealer_score > 21:
            print("=> Le Croupier a dépassé 21 (Bust). Le Joueur gagne !")
        elif player_score > dealer_score:
            print("=> Le Joueur a un meilleur score. Le Joueur gagne !")
        elif dealer_score > player_score:
            print("=> Le Croupier a un meilleur score. Le Croupier gagne !")
        else:
            print("=> Égalité (Push) !")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Touche ESPACE = Tirer (Hit)
                    if event.key == pygame.K_SPACE:
                        self.player_hit()

                    # Touche ENTRÉE = Rester (Stand)
                    elif event.key == pygame.K_RETURN:
                        self.player_stand()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def render(self):
        self.screen.fill((34, 139, 34))
        Card.instances.draw(self.screen)
        pygame.display.flip()
