# ⚪⚫ Gomoku AI — Moteur de Jeu 5-en-Ligne en POO & Pygame

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Pygame-informational?style=for-the-badge&logo=python)](https://www.pygame.org/)
[![Design](https://img.shields.io/badge/Architecture-POO_Clean-blue?style=for-the-badge)](#)

Développement d'un jeu de **Gomoku** (Morpion 5-en-ligne sur plateau 15×15) avec moteur graphique sous **Pygame** et intelligence artificielle d'évaluation de positions.

---

## 🎮 Règles & Objectifs
Le Gomoku se joue sur une grille de type Go (15×15 cases). Le premier joueur qui aligne exactement ou au moins **5 pierres** de sa couleur horizontalement, verticalement ou en diagonale remporte la partie.

---

## 🧩 Architecture Logicielle (POO)
Le projet est conçu selon une architecture orientée objet propre :
- `Plateau` : Gestion matricielle de l'état du jeu, détection des coups légaux et vérification des alignements gagnants.
- `Joueur` : Classe abstraite dérivée en `JoueurHumain` et `JoueurIA`.
- `Evaluateur` : Fonction de scoring détectant les configurations tactiques clés :
  - **Quinte :** 5 pierres alignées (victoire).
  - **Quatre ouvert :** `_XXXX_` (victoire imparable au coup suivant).
  - **Trois ouvert :** `_XXX_` (menace créant une double attaque).
  - **Fourchette 3x3 ou 4x3 :** Combinaison offensive prioritaire.
- `GomokuGUI` : Boucle événementielle Pygame avec détection de clics sur les intersections, affichage dynamique et messages de fin de partie.

---

## 🚀 Exécution

### 1. Lancer la version avec interface graphique Pygame
```bash
python3 gomoku_pygame.py
```

### 2. Lancer la version orientée objet
```bash
python3 gomoku_POO.py
```

---

## 📁 Organisation des Fichiers
- `gomoku_pygame.py` : Version interactive avec rendu graphique Pygame.
- `gomoku_POO.py` : Implémentation purement orientée objet de la logique métier.
- `gomoku_all_V0.py` & `gomoku_all_V1.py` : Versions procédurales et itérations de développement.
- `documentation du code all V0.txt` : Documentation des fonctions internes.
