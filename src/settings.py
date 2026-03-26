import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
DISPLAY_CAPTION = "Blackjack"
CARD_WIDTH = 125
CARD_HEIGHT = 182

BUTTON_WIDTH = 86
BUTTON_HEIGHT = 86
BUTTON_HIT = pygame.K_RIGHT
BUTTON_STAND = pygame.K_LEFT
BUTTON_RESET = pygame.K_r
BUTTON_CLOSE = pygame.K_ESCAPE

POINT_VALUE = {
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
SUIT_CARD = ["C", "D", "H", "S"]
RANK_CARD = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

P_Y = WINDOW_HEIGHT - CARD_HEIGHT - 50
D_Y = 10 + CARD_HEIGHT + 10

GAME_BACKGROUND = (34, 139, 34)
