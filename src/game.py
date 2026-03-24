import random

import pygame

from card import Card
from croupier import Croupier
from player import Player
from settings import DISPLAY_CAPTION


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        Card(0, 0, 10, "10.bmp")

        # logique Martin
        # ---------------------------------
        # rank (2, 3, 4, etc)
        # suit (K, Q, etc)
        # cards (nombre de cartes dont le joueur dispose)
        # player (1 ou 2)
        # flipped (carte retournée ou non)
        # format : Card(2, "C", 2, 2, true)

        self.suit = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.rank = ["H", "D", "C", "S"]
        self.cards = 2
        self.player = Player("Player")
        self.croupier = Croupier()
        self.flipped = True

        self.pack_joueur = [
            (couleur, rang, 1, f"{rang}.bmp", self.flipped)
            for couleur in self.rank
            for rang in self.suit
        ]

        self.pack_croupier = [
            (couleur, rang, 2, f"{rang}.bmp", self.flipped)
            for couleur in self.rank
            for rang in self.suit
        ]

        random.shuffle(self.pack_joueur)
        random.shuffle(self.pack_croupier)

        # ---------------------------------

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def update(self):

        for _ in range(2):
            self.player.hit(self.pack_joueur.pop(0))
            self.croupier.hit(self.pack_croupier.pop(0))

        self.player.show_hand()
        self.croupier.show_card()

    def flip_card(self):
        self.croupier.main[1] = self.pack.pop(0)
        self.croupier.show_hand()
        if self.croupier.calcul_score() > 21:
            print("Le croupier a dépassé 21 ! Vous avez gagné.")
        return

    def hit_card(self):
        nouvelle_carte = self.pack.pop(0)
        self.player.hit(nouvelle_carte)
        print(f"\nVous avez tiré : {nouvelle_carte[1]} de {nouvelle_carte[0]}")
        self.player.show_hand()
        if self.player.calcul_score() > 21:
            print("Vous avez dépassé 21 ! Vous avez perdu.")
            return

    def stand_card(self):
        self.player.stand()
        print("\nVous avez choisi de rester.")
        print(f"Votre score final est de {self.player.calcul_score()}.")
        return

    def score_player(self):
        return self.player.calcul_score()

    def score_croupier(self):
        return self.croupier.calcul_score()

    def render(self):
        self.screen.fill((0, 0, 0))
        Card.instances.draw(self.screen)
        pygame.display.flip()
