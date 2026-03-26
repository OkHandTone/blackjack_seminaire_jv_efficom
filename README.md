pour lancer le projet

git clone https://github.com/adrienfdupont/blackjack_seminaire_jv_efficom.git .
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/game.py


règle : 

Règles du Blackjack – Version synthétique

Objectif

Battre le croupier sans dépasser 21.

Valeur des cartes

Les cartes de 2 à 10 valent leur valeur faciale. Les figures (Valet, Dame, Roi) valent 10. L'As vaut 11 uniquement dans cette version initiale ; la gestion dynamique de l'As (1 ou 11) sera implémentée ultérieurement si le temps le permet.

Déroulement d'une main

Le joueur place une mise. Le croupier distribue deux cartes face visible au joueur, une carte face visible et une carte face cachée pour lui-même.

Le joueur peut ensuite choisir de tirer une carte (hit) ou de rester (stand). S'il dépasse 21, il perd immédiatement.

Une fois le joueur satisfait, le croupier retourne sa carte cachée. Il tire tant que son total est inférieur ou égal à 16, et reste à partir de 17.

Gains

Le système de gains (détermination des vainqueurs, calcul des paiements, gestion des mises et du solde) sera implémenté ultérieurement si le temps le permet.

Fonctionnalités avancées (version ultérieure)

Le doublement de la mise après les deux premières cartes, le split (séparer deux cartes de même valeur en deux mains distinctes), l'assurance (mise complémentaire lorsque le croupier montre un As) et la gestion dynamique de l'As seront ajoutés dans une version future.
