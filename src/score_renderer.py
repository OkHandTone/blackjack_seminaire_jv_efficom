import pygame

from settings import D_Y, P_Y, WINDOW_WIDTH


class ScoreRenderer:
    """Handles rendering of player and dealer scores"""

    def __init__(self, screen, score_font):
        """
        Initialize the score renderer

        Args:
            screen: Pygame screen surface
            score_font: Pygame font for score display
        """
        self.screen = screen
        self.score_font = score_font

    def draw_player_score(self, player, y_position=P_Y):
        """
        Draw player's score on screen

        Args:
            player: Player object with calculate_score() method
            y_position: Y position for score display
        """
        score = player.calculate_score()
        score_text = self.score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, y_position))
        self.screen.blit(score_text, score_rect)

    def draw_dealer_score(self, dealer, game_over=False, y_position=D_Y):
        """
        Draw dealer's score on screen

        Args:
            dealer: Dealer object with calculate_score() and get_visible_score() methods
            game_over: Whether the game is over (shows total score if True)
            y_position: Y position for score display
        """
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
        """
        Draw both player and dealer scores

        Args:
            player: Player object
            dealer: Dealer object
            game_over: Whether the game is over
        """
        self.draw_player_score(player)
        self.draw_dealer_score(dealer, game_over)
