import random
import sqlite3
import uuid
from datetime import datetime

import pygame

from components.button import Button
from components.card import Card
from components.hit_button import HitButton
from components.stand_button import StandButton
from croupier import Croupier
from database.db_manager import init_db, insert_player, log_game_started
from player import Player
from settings import (
    BUTTON_HIT,
    BUTTON_STAND,
    CARD_HEIGHT,
    DISPLAY_CAPTION,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)

        HitButton(self.player_hit)
        StandButton(self.player_stand)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        init_db()
        self.player_id = str(uuid.uuid4())
        username = f"Player_{self.player_id[:8]}"

        try:
            insert_player(self.player_id, username)
        except sqlite3.IntegrityError:
            exit()

        self.game_id = str(uuid.uuid4())
        self.start_time = datetime.now().isoformat()

        log_game_started(self.game_id, self.start_time, 1)

        self.player1 = Player(name=username)
        self.dealer = Croupier()

        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [(r, s) for s in suits for r in ranks]
        random.shuffle(self.deck)

        self.game_over = False
        self.end_message = ""
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.score_font = pygame.font.SysFont("Arial", 28, bold=True)

        self.deal_initial_cards()
        self.total_score_players()

    def deal_initial_cards(self):

        for i in range(2):
            rank, suit = self.deck.pop()
            self.dealer.add_card((rank, suit))
            is_flipped = True if i == 0 else False
            Card(rank, suit, i, 1, is_flipped)

        for i in range(2):
            rank, suit = self.deck.pop()
            self.player1.add_card((rank, suit))
            Card(rank, suit, i, 2, True)

        self.player1.show_hand()
        self.dealer.show_initial_hand()

        # bonus
        if self.player1.calculate_score() == 21:
            print("BLACKJACK INITIAL !")
            for sprite_card in Card.instances:
                if sprite_card.player == 1 and sprite_card.cards == 1:
                    sprite_card.show()
            self.check_winner()  # On lance la comparaison des scores

    def total_score_players(self):
        return self.player1.calculate_score(), self.dealer.calculate_score()

    def player_hit(self):
        if len(self.deck) > 0:
            rank, suit = self.deck.pop()
            self.player1.add_card((rank, suit))
            card_index = len(self.player1.hand) - 1  # cal nbr carte packet
            Card(rank, suit, card_index, 2, True)

            self.player1.show_hand()
            for sprite_card in Card.instances:
                if sprite_card.player == 1 and sprite_card.cards == 1:
                    # Afficher la 2e carte du croupier et ajoute sa somme a son score
                    sprite_card.show()

    def player_stand(self):

        for sprite_card in Card.instances:
            if sprite_card.player == 1 and sprite_card.cards == 1:
                sprite_card.show()

        self.dealer.show_hand()

        while self.dealer.calculate_score() < 17:
            if len(self.deck) > 0:
                rank, suit = self.deck.pop()
                self.dealer.add_card((rank, suit))

                card_index = len(self.dealer.hand) - 1
                Card(rank, suit, card_index, 1, True)
                self.dealer.show_hand()

        self.check_winner()

    def check_winner(self):

        player_score = self.player1.calculate_score()
        dealer_score = self.dealer.calculate_score()

        if player_score > 21:
            self.end_game("Le Croupier gagne.")
        elif dealer_score > 21:
            self.end_game("Le Croupier a sauté ! Vous gagnez.")
        elif player_score > dealer_score:
            self.end_game("Vous gagnez !")
        elif dealer_score > player_score:
            self.end_game("Le Croupier gagne.")
        else:
            self.end_game("Égalité (Push).")

    def end_game(self, message):
        self.game_over = True
        self.end_message = message

    def draw_scores(self):

        p_score = self.player1.calculate_score()
        p_text = self.score_font.render(f"Score: {p_score}", True, (255, 255, 255))

        p_y = WINDOW_HEIGHT - CARD_HEIGHT - 50
        p_rect = p_text.get_rect(center=(WINDOW_WIDTH // 2, p_y))
        self.screen.blit(p_text, p_rect)

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

        if self.game_over:
            d_score = self.dealer.calculate_score()
            d_label = "Dealer (Total)"
        else:
            visible_card = self.dealer.hand[0]
            rank = visible_card[0]
            d_score = point_values.get(rank, 0)
            d_label = "Dealer (Visible)"

        d_text = self.score_font.render(f"{d_label}: {d_score}", True, (255, 255, 255))

        d_y = 10 + CARD_HEIGHT + 10
        d_rect = d_text.get_rect(center=(WINDOW_WIDTH // 2, d_y))
        self.screen.blit(d_text, d_rect)

    def reset_game(self):
        self.player1.hand = []
        self.dealer.hand = []

        Card.instances.empty()
        self.game_over = False
        self.end_message = ""

        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [(r, s) for s in suits for r in ranks]
        random.shuffle(self.deck)

        self.deal_initial_cards()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                Button.instances.update(event)
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == BUTTON_HIT:
                            self.player_hit()

                            score_actuel = self.player1.calculate_score()

                            if score_actuel > 21:
                                self.check_winner()
                            elif score_actuel == 21:
                                print("21 atteint ! Tour automatique du croupier.")
                                self.player_stand()

                        elif event.key == BUTTON_STAND:
                            self.player_stand()

                    else:
                        if event.key == pygame.K_r:
                            self.reset_game()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def render(self):
        self.screen.fill((34, 139, 34))
        Card.instances.draw(self.screen)
        Button.instances.draw(self.screen)
        self.draw_scores()

        if self.game_over:
            texte_resultat = self.font.render(self.end_message, True, (255, 215, 0))
            rect_resultat = texte_resultat.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
            )
            font_small = pygame.font.SysFont("Arial", 25, bold=True)
            texte_restart = font_small.render(
                "Press R pour relancer", True, (255, 255, 255)
            )
            rect_restart = texte_restart.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
            )

            largeur_box = max(rect_resultat.width, rect_restart.width) + 40
            hauteur_box = rect_resultat.height + rect_restart.height + 40
            fond = pygame.Surface((largeur_box, hauteur_box))
            fond.set_alpha(200)
            fond.fill((0, 0, 0))
            rect_fond = fond.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

            self.screen.blit(fond, rect_fond)
            self.screen.blit(texte_resultat, rect_resultat)
            self.screen.blit(texte_restart, rect_restart)

        pygame.display.flip()
