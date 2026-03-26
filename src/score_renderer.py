import pygame

from settings import D_Y, P_Y, WINDOW_WIDTH


class ScoreRenderer:
    def __init__(self, screen, score_font):
        self.screen = screen
        self.score_font = score_font

    def draw_player_score(self, player, y_position=P_Y):
        score = player.calculate_score()
        score_text = self.score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, y_position))
        self.screen.blit(score_text, score_rect)

    def draw_dealer_score(self, dealer, game_over=False, y_position=D_Y):
        if game_over:
            score = dealer.calculate_score()
            label = "Dealer (Total)"
        else:
            score = dealer.get_visible_score()
            label = "Dealer (Visible)"

        score_text = self.score_font.render(f"{label}: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, y_position))
        self.screen.blit(score_text, score_rect)

    def draw_scores(self, player, dealer, game_over=False):

        self.draw_player_score(player)
        self.draw_dealer_score(dealer, game_over)
