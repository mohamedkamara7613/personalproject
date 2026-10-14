# 🔴🟡 IA Puissance 4 — Algorithmes Minimax & Élagage Alpha-Bêta

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Game AI](https://img.shields.io/badge/Game_AI-Minimax_%7C_Alpha--Beta-brightgreen?style=for-the-badge)](#)
[![GUI](https://img.shields.io/badge/UI-Tkinter_%7C_Pygame-informational?style=for-the-badge)](#)

Implémentation d'une Intelligence Artificielle avancée pour le jeu classique de **Puissance 4** (grille 6×7), combinant la théorie des jeux à somme nulle et des techniques d'exploration arborescente optimisée.

---

## 🧠 Architecture de l'Intelligence Artificielle

### 1. Théorème du Minimax & Arbre de Jeu
Le jeu est modélisé sous la forme d'un arbre d'états où :
- Le joueur IA cherche à **maximiser** le score de la position finale (**MAX**).
- Le joueur adverse cherche à **minimiser** le score de l'IA (**MIN**).

$$V(s) = \begin{cases} 
\text{Score terminal} & \text{si } s \text{ est terminal ou prof. max atteinte} \\
\max_{a \in A(s)} V(s') & \text{si } \text{tour de MAX} \\
\min_{a \in A(s)} V(s') & \text{si } \text{tour de MIN}
\end{cases}$$

### 2. Élagage Alpha-Bêta ($\alpha-\beta$ Pruning)
Pour explorer des profondeurs plus importantes sans explosion combinatoire, l'élagage alpha-bêta coupe les branches de jeu mathématiquement prouvées comme sous-optimales :
- $\alpha$ : Le score minimal garanti pour le joueur MAX.
- $\beta$ : Le score maximal garanti pour le joueur MIN.
- Dès que $\beta \le \alpha$, la branche courante est élaguée.

### 3. Fonction d'Évaluation Heuristique
Lorsque la profondeur maximale est atteinte avant l'état terminal, la grille est évaluée selon :
- **Occupation du centre :** Les colonnes centrales (colonne 3) offrent statistiquement plus d'opportunités d'alignement.
- **Comptage des fenêtres de 4 pions :**
  - 4 pions alignés : $+100\,000$ points (victoire immédiate).
  - 3 pions + 1 case vide : $+50$ points (menace directe).
  - 2 pions + 2 cases vides : $+10$ points (construction).
  - 3 pions adverses bloqués : défense prioritaire.

---

## 📁 Structure du Projet

```
IA_puissance4/
├── avec_ia/            # Moteurs IA (ia_perso_v0, ia_perso_v1, ia_engine)
├── sans_ia.py          # Version 2 joueurs humains en local
├── a partger/          # Versions packagées pour distribution
├── Conseils Puissance4.pdf # Guide d'analyse stratégique
├── feuille de route.txt
└── tests/              # Scripts de test et validation de l'IA
```

---

## 🚀 Exécution

### 1. Lancer le mode 2 joueurs (sans IA)
```bash
python3 sans_ia.py
```

### 2. Lancer le mode avec IA (Minimax / Alpha-Bêta)
```bash
python3 avec_ia/moi/ia_perso_v1.py
```

---

## 📑 Documents & Stratégie
- 📄 [Consulter les Conseils Stratégiques de Puissance 4 (PDF)](./Conseils%20Puissance4.pdf)
