# 🐍 Snake AI — Deep Q-Learning & Safe A* Pathfinding

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep_RL-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)

Moteur de jeu Snake intégrant trois modes d'intelligence artificielle autonomes :
1. **Safe A* Pathfinding :** Algorithme heuristique temps réel avec détection d'impasse et mécanisme de repli (*fallback*) vers la queue du serpent.
2. **Deep Q-Learning (DQN) :** Réseau de neurones profond sous **PyTorch** entraîné par apprentissage par renforcement avec mémoire de relecture (*Experience Replay*) et décroissance exponentielle d'$\\varepsilon$.
3. **BFS Solver :** Exploration en largeur pour la garantie du plus court chemin.

---

## 🎬 Démonstration du Solveur Safe A*

![Snake AI Demo](./demo_snake_astar.gif)

---

## 🧮 Formulation Mathématique du DQN

- **Espace des États (11 booléens) :** Danger tout droit, à gauche, à droite ; direction actuelle (N, S, E, W) ; position relative de la nourriture (haut, bas, gauche, droite).
- **Espace des Actions (3 discrètes) :** $[\text{Continuer}, \text{Tourner Droite}, \text{Tourner Gauche}]$.
- **Fonction de Récompense (Reward Shaping) :**
  - Manger une pomme : $+10$
  - Collision (Game Over) : $-10$
  - Se rapprocher de la pomme : $+0.1$
- **Équation de Bellman :**
  $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

---

## 🚀 Lancer la démonstration
```bash
python3 game.py
```
