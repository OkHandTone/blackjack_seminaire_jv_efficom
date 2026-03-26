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
from font_manager import FontManager
from game_over_renderer import GameOverRenderer
from player import Player
from score_renderer import ScoreRenderer
from settings import (
    BUTTON_HIT,
    BUTTON_STAND,
    CARD_HEIGHT,
    DISPLAY_CAPTION,
    RANK_CARD,
    SUIT_CARD,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Game:
    def __init__(self):
        # 1. Pygame initialization
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # 2. UI components initialization
        HitButton(self.player_hit)
        StandButton(self.player_stand)

        # 3. Database initialization
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

        # 4. Game entities initialization
        self.player1 = Player(name=username)
        self.dealer = Croupier()

        # 5. Rendering system initialization
        self.font_manager = FontManager()
        self.score_renderer = ScoreRenderer(self.screen, self.font_manager.get_score_font())
        self.game_over_renderer = GameOverRenderer(self.screen, self.font_manager)

        # 6. Game state initialization
        self._initialize_game_state()
        self.deal_initial_cards()
        self.total_score_players()

    def deal_initial_cards(self):
        """Deal initial cards to both player and dealer"""
        # Deal cards to dealer
        for i in range(2):
            self._deal_card_to_dealer(i, is_first_card=(i == 0))

        # Deal cards to player
        for i in range(2):
            self._deal_card_to_player(i)

        self.player1.show_hand()
        self.dealer.show_initial_hand()

        if self.player1.has_blackjack():
            for sprite_card in Card.instances:
                if sprite_card.player == self.dealer.player_number and sprite_card.cards == 1:
                    sprite_card.show()
            self.check_winner()

    def total_score_players(self):
        """Get current scores of both players"""
        return self.player1.calculate_score(), self.dealer.calculate_score()

    def player_hit(self):
        """Handle player hitting"""
        if self.player1.hit(self.deck):
            self.player1.show_hand()
            self._reveal_dealer_second_card()

            if self.player1.should_stand():
                self.check_winner()

    def player_stand(self):
        """Handle player standing and dealer's turn"""
        self._reveal_dealer_second_card()
        self.dealer.show_hand()
        self.dealer.play_dealer_turn(self.deck)
        self.check_winner()

    def check_winner(self):
        """Determine the winner based on scores"""
        player_score = self.player1.calculate_score()
        dealer_score = self.dealer.calculate_score()

        if self.player1.is_busted():
            self.end_game("Le Croupier gagne.")
        elif self.dealer.is_busted():
            self.end_game("Le Croupier a sauté ! Vous gagnez.")
        elif player_score > dealer_score:
            self.end_game("Vous gagnez !")
        elif dealer_score > player_score:
            self.end_game("Le Croupier gagne.")
        else:
            self.end_game("Égalité (Push).")

    def end_game(self, message):
        """End the game with a message"""
        self.game_over = True
        self.end_message = message

    def draw_scores(self):
        """Draw player and dealer scores on screen"""
        self.score_renderer.draw_scores(self.player1, self.dealer, self.game_over)

    def reset_game(self):
        """Reset the game for a new round"""
        self.player1.clear_hand()
        self.dealer.clear_hand()

        Card.instances.empty()

        # Reset game state
        self._initialize_game_state()

        self.deal_initial_cards()

    def _initialize_deck(self):
        """Initialize and shuffle a new deck of cards"""
        suits = SUIT_CARD
        ranks = RANK_CARD
        self.deck = [(r, s) for s in suits for r in ranks]
        random.shuffle(self.deck)

    def _initialize_game_state(self):
        """Initialize or reset the game state"""
        self.game_over = False
        self.end_message = ""
        self._initialize_deck()

    def _deal_card_to_dealer(self, card_index, is_first_card=False):
        """
        Deal a card to the dealer

        Args:
            card_index: Index of the card in dealer's hand
            is_first_card: Whether this is the dealer's first card (face down)
        """
        rank, suit = self.deck.pop()
        self.dealer.add_card((rank, suit))
        is_flipped = not is_first_card  # First card is face down
        Card(rank, suit, card_index, self.dealer.player_number, is_flipped)

    def _deal_card_to_player(self, card_index):
        """
        Deal a card to the player

        Args:
            card_index: Index of the card in player's hand
        """
        rank, suit = self.deck.pop()
        self.player1.add_card((rank, suit))
        Card(rank, suit, card_index, self.player1.player_number, True)

    def _reveal_dealer_second_card(self):
        """Reveal the dealer's second card (face down card)"""
        for sprite_card in Card.instances:
            if sprite_card.player == self.dealer.player_number and sprite_card.cards == 1:
                sprite_card.show()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            if not self._handle_events():
                running = False
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            Button.instances.update(event)
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self._handle_keydown_event(event)

        return True

    def _handle_keydown_event(self, event):
        """Handle keydown events"""
        if not self.game_over:
            self._handle_gameplay_keys(event)
        else:
            self._handle_game_over_keys(event)

    def _handle_gameplay_keys(self, event):
        """Handle gameplay key presses"""
        if event.key == BUTTON_HIT:
            self.player_hit()
            if self.player1.should_stand():
                self.check_winner()
        elif event.key == BUTTON_STAND:
            self.player_stand()

    def _handle_game_over_keys(self, event):
        """Handle game over key presses"""
        if event.key == pygame.K_r:
            self.reset_game()

    def render(self):
        """Render the game screen"""
        self.screen.fill((34, 139, 34))
        Card.instances.draw(self.screen)
        Button.instances.draw(self.screen)
        self.draw_scores()

        # Render game over message if game is over
        self.game_over_renderer.render(self.game_over, self.end_message)

        pygame.display.flip()
