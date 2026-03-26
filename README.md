# Blackjack - Projet de Séminaire

Un jeu de Blackjack développé en Python avec Pygame pour un séminaire de jeu vidéo.

## 🎮 Structure du jeu

Le projet est organisé selon une architecture modulaire :

```
blackjack_seminaire_jv_efficom/
├── src/                    # Code source principal
│   ├── classes/           # Classes métier (Joueur, Croupier, etc.)
│   ├── components/        # Composants UI (boutons, cartes, etc.)
│   ├── database/          # Gestion de la base de données SQLite
│   ├── game.py           # Logique principale du jeu
│   ├── main.py           Point d'entrée de l'application
│   ├── settings.py       # Configuration et constantes
│   └── plot_metrics.py   # Visualisation des statistiques
├── assets/               # Ressources graphiques (images)
├── charts/               # Graphiques générés
├── requirements.txt      # Dépendances Python
└── blackjack.db          # Base de données SQLite
```

### Architecture logicielle

- **Game** : Classe principale orchestrant le déroulement du jeu
- **Player** : Gère le joueur (solde, mise, main)
- **Croupier** : Gère le croupier (main, règles de tirage)
- **Card** : Représente une carte avec sa valeur et son affichage
- **Database** : Persistance des parties et statistiques
- **UI Components** : Boutons interactifs et interface utilisateur

## 🚀 Installation et lancement

### Prérequis

- Python 3.14
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/adrienfdupont/blackjack_seminaire_jv_efficom.git
   cd blackjack_seminaire_jv_efficom
   ```

2. **Créer un environnement virtuel**

   ```bash
   python3 -m venv .venv
   ```

3. **Activer l'environnement virtuel**
   - Sur macOS/Linux :
     ```bash
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```bash
     .venv\Scripts\activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

### Lancement du jeu

**Méthode 1 : Via le point d'entrée principal**

```bash
python src/main.py
```

**Méthode 2 : Directement via le module game**

```bash
python src/game.py
```

**Méthode 3 : Exécutable (si disponible)**

```bash
# Dans le dossier dist/ après build
./blackjack
```

## 🎯 Règles du jeu

### Objectif

Battre le croupier sans dépasser 21 points.

### Valeur des cartes

- **Cartes 2 à 10** : Valeur faciale
- **Figures (Valet, Dame, Roi)** : 10 points
- **As** : 11 points (version simplifiée)

### Déroulement d'une partie

1. Le joueur place une mise
2. Distribution des cartes :
   - Joueur : 2 cartes face visible
   - Croupier : 1 carte face visible, 1 carte face cachée
3. Tour du joueur :
   - **Tirer (Hit)** : Prendre une carte supplémentaire
   - **Rester (Stand)** : Garder sa main actuelle
4. Tour du croupier :
   - Retourne sa carte cachée
   - Tire des cartes tant que son total ≤ 16
   - S'arrête à partir de 17
5. Détermination du gagnant

### Contrôles

- **Souris** : Cliquer sur les boutons d'action
- **Clavier** : R pour rejouer une manche, ← pour rester et → pour tirer
- **Interface** : Menus interactifs avec boutons cliquables

## 📊 Fonctionnalités

### Implémentées

- ✅ Interface graphique avec Pygame
- ✅ Logique basique du Blackjack
- ✅ Base de données pour les statistiques
- ✅ Visualisation des performances

### À venir (si temps)

- Gestion dynamique de l'As (1 ou 11)
- Système de mise et solde
- Doubler la mise
- Split (séparation des mains)
- Assurance
- Gestion des parties multiples
- Interface plus avancée

## 🛠️ Développement

### Structure de la base de données

La base SQLite (`blackjack.db`) stocke :

- Historique des parties
- Actions des joueurs
- Résultats et statistiques
- Performances par session

### Tests

```bash
# Tester la base de données
python src/test_db.py

# Générer des graphiques de statistiques
python src/plot_metrics.py
```

## 📈 Statistiques

Le jeu enregistre automatiquement :

- Taux de victoire
- Mise moyenne
- Durée des parties
- Décisions du joueur

Les graphiques sont générés dans le dossier `charts/`.

## 🤝 Contribution

Ce projet a été développé dans le cadre d'un séminaire de jeu vidéo.

- @Adrienfdupont
- @ATAGBA310
- @OkHandTone

## 📄 Licence

Projet éducatif - Libre d'utilisation et de modification.
