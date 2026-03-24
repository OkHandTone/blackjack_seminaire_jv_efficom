import random
from unittest.main import main

import pygame

couleurs = ["♥", "♦", "♣", "♠"]
rangs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

valeurs_point = {
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

paquet = [(couleur, rang) for couleur in couleurs for rang in rangs]
random.shuffle(paquet)

main_joueur = []
main_croupier = []

main_joueur.append(paquet.pop(0))
main_croupier.append(paquet.pop(0))
main_joueur.append(paquet.pop(0))
main_croupier.append(paquet.pop(0))

total_main_joueur = sum(valeurs_point[rang] for _, rang in main_joueur)
total_main_croupier = sum(valeurs_point[rang] for _, rang in main_croupier)

print("main_joueur:", total_main_joueur)
print("main_croupier:", total_main_croupier)

# print("point joueur:", sum(valeurs_point[rang] for _, rang in main_joueur))
# print("point croupier:", sum(valeurs_point[rang] for _, rang in main_croupier))
