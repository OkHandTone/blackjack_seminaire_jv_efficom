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

    def deal_initial_cards(self):
        """Distribue 2 cartes au joueur et 2 au croupier au début de la partie."""

        for i in range(2):
            rank, suit = self.deck.pop()
            self.player1.add_card((rank, suit))
            Card(rank, suit, i, 1, True)

        # 2. Distribution au Croupier (Player = 2)
        for i in range(2):
            rank, suit = self.deck.pop()
            self.dealer.add_card((rank, suit))
            is_flipped = True if i == 0 else False
            Card(rank, suit, i, 2, is_flipped)

        self.player1.show_hand()
        self.dealer.show_initial_hand()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def render(self):
        self.screen.fill((34, 139, 34))
        Card.instances.draw(self.screen)
        pygame.display.flip()
