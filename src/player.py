class Player:
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

    def __init__(self, nom="Joueur"):
        self.nom = nom
        self.main = []

    def hit(self, carte):
        self.main.append(carte)

    def stand(self):
        self.main.append(None)

    def calcul_score(self):
        return sum(self.valeurs_point[rang] for _, rang in self.main)

    def show_hand(self):
        print(f"Main de {self.nom} : {self.main} (Score : {self.calcul_score()})")
