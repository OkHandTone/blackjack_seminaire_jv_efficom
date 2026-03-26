class Hit:
    def __init__(self, player, paquet):
        self.player = player
        self.paquet = paquet

    def hit(self):
        self.player.ajouter_carte(self.paquet.pop(0))
