import pygame

from font_manager import FontManager
from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class GameOverRenderer:
    """Handles rendering of game over messages and restart prompts"""

    def __init__(self, screen, font_manager):
        """
        Initialize the game over renderer

        Args:
            screen: Pygame screen surface
            font_manager: FontManager instance for accessing fonts
        """
        self.screen = screen
        self.font_manager = font_manager
        self.font = font_manager.get_game_over_font()
        self.small_font = font_manager.get_small_font()

    def render_game_over(self, message):
        """
        Render the game over screen with message and restart prompt

        Args:
            message: The game over message to display
        """
        # Render game over message
        result_text = self.font.render(message, True, (255, 215, 0))
        result_rect = result_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        )

        # Render restart prompt
        restart_text = self.small_font.render(
            "Press R pour relancer", True, (255, 255, 255)
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        )

        # Create background box
        box_width = max(result_rect.width, restart_rect.width) + 40
        box_height = result_rect.height + restart_rect.height + 40
        background = pygame.Surface((box_width, box_height))
        background.set_alpha(200)
        background.fill((0, 0, 0))
        background_rect = background.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )

        # Draw everything to screen
        self.screen.blit(background, background_rect)
        self.screen.blit(result_text, result_rect)
        self.screen.blit(restart_text, restart_rect)

    def render(self, game_over, message):
        """
        Conditional rendering of game over screen

        Args:
            game_over: Boolean indicating if game is over
            message: Game over message to display if game is over
        """
        if game_over:
            self.render_game_over(message)
