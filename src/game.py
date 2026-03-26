import random
import sqlite3
import uuid
from datetime import datetime

import pygame

from components.ace_toggle import AceToggle
from components.button import Button
from components.card import Card
from components.hit_button import HitButton
from components.reset_button import ResetButton
from components.stand_button import StandButton
from croupier import Croupier
from database.db_manager import (
    init_db,
    insert_player,
    log_game_ended,
    log_game_started,
    log_initial_deal,
    log_player_action,
    log_round_ended,
    log_round_result,
    log_round_started,
)
from font_manager import FontManager
from game_over_renderer import GameOverRenderer
from player import Player
from score_renderer import ScoreRenderer
from settings import (
    BUTTON_CLOSE,
    BUTTON_HIT,
    BUTTON_RESET,
    BUTTON_STAND,
    DISPLAY_CAPTION,
    GAME_BACKGROUND,
    RANK_CARD,
    SUIT_CARD,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        HitButton(self.player_hit)
        StandButton(self.player_stand)
        ResetButton(self.reset_game)

        self.ace_value = 11
        AceToggle(self._on_ace_changed)

        init_db()
        self.player_id = str(uuid.uuid4())
        username = f"Player_{self.player_id[:8]}"

        try:
            insert_player(self.player_id, username)
        except sqlite3.IntegrityError:
            exit()

        self.game_id = str(uuid.uuid4())
        self.start_time = datetime.now().isoformat()

        self.player1 = Player(name=username)
        self.dealer = Croupier()

        self.font_manager = FontManager()
        self.score_renderer = ScoreRenderer(
            self.screen, self.font_manager.get_score_font()
        )
        self.game_over_renderer = GameOverRenderer(self.screen, self.font_manager)

        self._initialize_game_state()

        self.round_number = 1
        self.round_id = str(uuid.uuid4())
        self.action_order = 0

        log_game_started(self.game_id, self.start_time, 1)
        log_round_started(
            self.round_id, self.game_id, self.round_number, self.start_time
        )

        self.deal_initial_cards()
        self.total_score_players()

    def deal_initial_cards(self):

        dealer_first_card = None

        for i in range(2):
            card = self._deal_card_to_dealer(i, is_first_card=(i != 0))
            if i == 0:
                dealer_first_card = card

        for i in range(2):
            self._deal_card_to_player(i)

        self.player1.show_hand()
        self.dealer.show_initial_hand()

        if self.player1.has_blackjack():
            for sprite_card in Card.instances:
                if (
                    sprite_card.player == self.dealer.player_number
                    and sprite_card.cards == 1
                ):
                    sprite_card.show()
            self.check_winner()

        initial_hand_value = self.player1.calculate_score()
        dealer_card_str = (
            f"{dealer_first_card[0]}{dealer_first_card[1]}"
            if dealer_first_card
            else "Unknown"
        )
        deal_id = str(uuid.uuid4())

        log_initial_deal(
            deal_id, self.round_id, self.player_id, initial_hand_value, dealer_card_str
        )

    def total_score_players(self):
        return self.player1.calculate_score(), self.dealer.calculate_score()

    def _on_ace_changed(self, value):
        self.ace_value = value
        self.player1.set_ace_value(value)

    def player_hit(self):
        hand_value_before = self.player1.calculate_score()

        if self.player1.hit(self.deck):
            last_card = self.player1.hand[-1]
            drawn_card_str = f"{last_card[0]}{last_card[1]}"

            hand_value_after = self.player1.calculate_score()

            self.action_order += 1
            self._log_player_action(
                "hit", hand_value_before, hand_value_after, drawn_card_str
            )

            self.player1.show_hand()
            self._reveal_dealer_second_card()

            if self.player1.should_stand():
                self.check_winner()

    def player_stand(self):
        hand_value_before = self.player1.calculate_score()
        self.action_order += 1
        self._log_player_action("stand", hand_value_before, hand_value_before, None)

        self._reveal_dealer_second_card()
        self.dealer.show_hand()
        self.dealer.play_dealer_turn(self.deck)
        self.check_winner()

    def check_winner(self):
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
        self.game_over = True
        self.end_message = message

        player_final_value = self.player1.calculate_score()
        dealer_final_value = self.dealer.calculate_score()

        msg = message.lower()

        if "croupier gagne" in msg:
            result = "lose"
        elif "gagnez" in msg or ("gagne" in msg and "croupier" not in msg):
            result = "win"
        else:
            result = "push"

        has_blackjack = 1 if self.player1.has_blackjack() else 0
        has_bust = 1 if self.player1.is_busted() else 0

        bet_amount = 0.0
        gain_loss = 0.0

        if result == "win":
            if has_blackjack:
                gain_loss = bet_amount * 1.5
            else:
                gain_loss = bet_amount
        elif result == "lose":
            gain_loss = -bet_amount

        end_time = datetime.now().isoformat()
        self._log_round_result(
            player_final_value,
            dealer_final_value,
            result,
            has_blackjack,
            has_bust,
            bet_amount,
            gain_loss,
            end_time,
    )
        log_round_ended(self.round_id, end_time)

    def draw_scores(self):
        self.score_renderer.draw_scores(
            self.player1, self.dealer, self.game_over, self.dealer_second_card_revealed
        )

    def reset_game(self):
        self.player1.clear_hand()
        self.dealer.clear_hand()

        Card.instances.empty()

        self._initialize_game_state()

        self.round_number += 1
        self.round_id = str(uuid.uuid4())
        self.action_order = 0
        log_round_started(
            self.round_id, self.game_id, self.round_number, datetime.now().isoformat()
        )

        self.deal_initial_cards()

    def _initialize_deck(self):
        suits = SUIT_CARD
        ranks = RANK_CARD
        self.deck = [(r, s) for s in suits for r in ranks]
        random.shuffle(self.deck)

    def _initialize_game_state(self):
        self.game_over = False
        self.end_message = ""
        self.dealer_second_card_revealed = False
        self._initialize_deck()

    def _deal_card_to_dealer(self, card_index, is_first_card=True):
        rank, suit = self.deck.pop()
        self.dealer.add_card((rank, suit))
        is_flipped = not is_first_card
        Card(rank, suit, card_index, self.dealer.player_number, is_flipped)
        return (rank, suit)

    def _deal_card_to_player(self, card_index):
        rank, suit = self.deck.pop()
        self.player1.add_card((rank, suit))
        Card(rank, suit, card_index, self.player1.player_number, True)
        return (rank, suit)

    def _reveal_dealer_second_card(self):
        if not self.dealer_second_card_revealed:
            for sprite_card in Card.instances:
                if (
                    sprite_card.player == self.dealer.player_number
                    and sprite_card.cards == 1
                ):
                    sprite_card.show()
            self.dealer_second_card_revealed = True

    def run(self):
        running = True
        while running:
            if not self._handle_events():
                running = False
            self.render()
            self.clock.tick(60)

        end_time = datetime.now().isoformat()
        log_game_ended(self.game_id, end_time)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            Button.instances.update(event)
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self._handle_keydown_event(event)

        return True

    def _handle_keydown_event(self, event):
        if not self.game_over:
            self._handle_gameplay_keys(event)
        else:
            self._handle_game_over_keys(event)

    def _handle_gameplay_keys(self, event):
        if event.key == BUTTON_HIT:
            self.player_hit()
            if self.player1.should_stand():
                self.check_winner()
        elif event.key == BUTTON_STAND:
            self.player_stand()

    def _handle_game_over_keys(self, event):
        if event.key == BUTTON_RESET:
            self.reset_game()

        if event.key == BUTTON_CLOSE:
            pygame.quit()

    def render(self):
        self.screen.fill(GAME_BACKGROUND)
        Card.instances.draw(self.screen)
        Button.instances.draw(self.screen)
        self.draw_scores()

        self.game_over_renderer.render(self.game_over, self.end_message)

        pygame.display.flip()

    def _log_player_action(
        self, action_type, hand_value_before, hand_value_after, drawn_card
    ):
        action_id = str(uuid.uuid4())
        log_player_action(
            action_id=action_id,
            game_id=self.game_id,
            round_id=self.round_id,
            player_id=self.player_id,
            action_type=action_type,
            hand_value_before=hand_value_before,
            hand_value_after=hand_value_after,
            drawn_card=drawn_card,
            action_order=self.action_order,
            timestamp=datetime.now().isoformat(),
        )

    def _log_round_result(
        self,
        player_final_value,
        dealer_final_value,
        result,
        has_blackjack,
        has_bust,
        bet_amount,
        gain_loss,
        end_time,
    ):
        result_id = str(uuid.uuid4())
        log_round_result(
            result_id=result_id,
            round_id=self.round_id,
            player_id=self.player_id,
            final_hand_value=player_final_value,
            dealer_final_value=dealer_final_value,
            result=result,
            has_blackjack=has_blackjack,
            has_bust=has_bust,
            bet_amount=bet_amount,
            gain_loss=gain_loss,
            end_time=end_time,
        )