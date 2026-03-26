import pygame


class FontManager:
    """Manages font initialization and provides font instances"""

    def __init__(self):
        """Initialize the font manager and load fonts"""
        pygame.font.init()
        self.fonts = {}
        self.load_default_fonts()

    def load_default_fonts(self):
        """Load default fonts used in the game"""
        self.fonts["game_over"] = pygame.font.SysFont("Arial", 40, bold=True)
        self.fonts["score"] = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonts["small"] = pygame.font.SysFont("Arial", 25, bold=True)

    def get_font(self, font_name):
        """
        Get a font by name

        Args:
            font_name: Name of the font to retrieve

        Returns:
            Pygame font object

        Raises:
            KeyError: If font_name is not found
        """
        return self.fonts[font_name]

    def create_font(self, name, size, bold=False, italic=False):
        """
        Create and store a new font

        Args:
            name: Font name (e.g., "Arial")
            size: Font size
            bold: Whether font is bold
            italic: Whether font is italic

        Returns:
            Created pygame font object
        """
        font = pygame.font.SysFont(name, size, bold, italic)
        self.fonts[name] = font
        return font

    def add_font(self, name, font):
        """
        Add an existing font to the manager

        Args:
            name: Name to store the font under
            font: Pygame font object
        """
        self.fonts[name] = font

    def get_game_over_font(self):
        """Get the font for game over messages"""
        return self.get_font("game_over")

    def get_score_font(self):
        """Get the font for score display"""
        return self.get_font("score")

    def get_small_font(self):
        """Get the small font for secondary text"""
        return self.get_font("small")

    def clear_fonts(self):
        """Clear all stored fonts"""
        self.fonts.clear()
        self.load_default_fonts()
