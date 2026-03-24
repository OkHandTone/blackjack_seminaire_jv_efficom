import random

from croupier import Croupier
from player import Player


class Game:
    def __init__(self):
        self.couleurs = ["♥", "♦", "♣", "♠"]
        self.rangs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.paquet = [
            (couleur, rang) for couleur in self.couleurs for rang in self.rangs
        ]
        random.shuffle(self.paquet)

        self.player = Player("Martin")
        self.dealer = Croupier()

    def run(self):
        """Lance le déroulement de la partie (la distribution et les tours)."""
        print("=== BIENVENUE AU BLACKJACK ===\n")

        for _ in range(2):
            self.player.ajouter_carte(self.paquet.pop(0))
            self.dealer.ajouter_carte(self.paquet.pop(0))

        print("--- DISTRIBUTION ---")
        self.player.afficher_main()
        self.dealer.afficher_main_initiale()

        print("\n--- À VOTRE TOUR ---")

        while True:
            choix = input("Voulez-vous Tirer (t) ou Rester (r) ? ").lower()

            if choix == "t":
                nouvelle_carte = self.paquet.pop(0)
                self.player.ajouter_carte(nouvelle_carte)

                print(f"\nVous avez tiré : {nouvelle_carte[1]} de {nouvelle_carte[0]}")
                self.player.afficher_main()

                if self.player.calculer_score() > 21:
                    print("Vous avez dépassé 21 ! Vous avez perdu.")
                    return

            elif choix == "r":
                print("\nVous avez choisi de rester.")
                print(f"Votre score final est de {self.player.calculer_score()}.")
                break

            else:
                print(
                    "Choix invalide. Veuillez taper 't' pour Tirer ou 'r' pour Rester."
                )

        print("\n--- TOUR DU CROUPIER ---")

        self.dealer.afficher_main()

        while self.dealer.calculer_score() < 17:
            print("Le croupier pioche une carte...")
            nouvelle_carte = self.paquet.pop(0)
            self.dealer.ajouter_carte(nouvelle_carte)
            self.dealer.afficher_main()

        print("\n--- RÉSULTAT FINAL ---")
        score_joueur = self.player.calculer_score()
        score_croupier = self.dealer.calculer_score()

        if score_croupier > 21:
            print(f" Le croupier a {score_croupier}. Il a sauté ! VOUS GAGNEZ ! ")

        elif score_croupier > score_joueur:
            print(f" Le croupier gagne avec {score_croupier} contre {score_joueur}.")

        elif score_joueur > score_croupier:
            print(f" VOUS GAGNEZ avec {score_joueur} contre {score_croupier} ! ")

        else:
            print(
                f" ÉGALITÉ ! Vous avez tous les deux {score_joueur}. Vous récupérez votre mise."
            )
