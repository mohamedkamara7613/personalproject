# 📦 Mario Sokoban — Moteur de Jeu & Solveur d'Espace d'États

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Engine-Pygame-informational?style=for-the-badge&logo=python)](https://www.pygame.org/)
[![YouTube Demo](https://img.shields.io/badge/YouTube-Watch_Video_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/6K3uYd2GtoY)
[![AI Solver](https://img.shields.io/badge/Solver-BFS_%7C_A*-brightgreen?style=for-the-badge)](#)

Développement d'une version complète du célèbre jeu de réflexion **Mario Sokoban** avec éditeur de niveaux, moteur graphique sous Pygame et **solveur automatique d'états par algorithme A***.

---

## 🎬 Démonstration Vidéo

[![Voir la Démo sur YouTube](https://img.shields.io/badge/YouTube-Regarder_la_Démonstration_Vidéo-red?style=for-the-badge&logo=youtube)](https://youtu.be/6K3uYd2GtoY)

![Mario Sokoban Demo](./demo_sokoban.gif)
*Animation du solveur résolvant automatiquement les caisses jusqu'aux cibles sans blocage.*

---

## 🧠 Algorithme de Résolution A* & Détection de Deadlocks
L'espace d'états est modélisé par la position du joueur et l'ensemble ordonné des positions des caisses :
$$S = (p_{\text{mario}}, \{(x_1, y_1), (x_2, y_2), \dots, (x_k, y_k)\})$$

Pour éviter l'explosion combinatoire ($O(N^K)$), le solveur applique :
1. **Élagage de Deadlocks Statiques :** Toute configuration où une caisse est poussée dans un coin non-cible ou le long d'un mur sans cible est immédiatement éliminée.
2. **Heuristique de Manhattan Bipartite :** Distance minimale de chaque caisse vers sa cible la plus proche.

---

## 🚀 Lancement

```bash
# Lancer le jeu avec solveur automatique
cd Solveur/V2.0
python3 main.py

# Lancer le jeu classique
cd v2.0
python3 main.py
```
