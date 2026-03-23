import random

import pygame

couleurs = ["Coeur", "Carreau", "Trèfle", "Pique"]
rangs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi", "As"]

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
    "Valet": 10,
    "Dame": 10,
    "Roi": 10,
    "As": 11,
}


paquet = [(couleur, rang) for couleur in couleurs for rang in rangs]
random.shuffle(paquet)
print(paquet)
