

---

# **README - data.py**

## **Description du fichier**
Le fichier `data.py` définit les **constantes** et les **variables globales** utilisées dans le projet Mario Sokoban v2.0.  
Il agit comme une bibliothèque centralisée qui regroupe :
1. Les paramètres de base, tels que les dimensions de la fenêtre et la taille des blocs.
2. Les structures de données universelles, comme la grille de jeu et les niveaux.
3. Les configurations, telles que les couleurs et les objets du jeu.

---

## **Fonctionnalités principales**

### **1. Définition des dimensions du jeu**
- **Taille des blocs et de la grille** :
  - Chaque élément du jeu est représenté par un bloc carré de `34x34` pixels (`bloc_size`).
  - La grille de jeu a une dimension de `12x12` blocs.
- **Dimensions de la fenêtre** :
  - La fenêtre est calculée en multipliant la taille des blocs par le nombre de blocs en largeur et hauteur.
  - Résultat : `window_width = 408 px`, `window_height = 408 px`.
  ```python
  window_width = bloc_size * nb_bloc_width
  window_height = bloc_size * nb_bloc_height
  dimension_window = (window_width, window_height)
  ```

---

### **2. Définition des constantes**
- **Directions** :
  - Un dictionnaire nommé `directions` associe des clés (HAUT, BAS, GAUCHE, DROITE) à des entiers.
  - Utile pour le contrôle du joueur et les mouvements.
  ```python
  directions = {"HAUT": 0, "BAS": 1, "GAUCHE": 2, "DROITE": 3}
  ```

- **Types d'objets dans le jeu** :
  - Le dictionnaire `items` mappe des noms (VIDE, MUR, CAISSE, etc.) à des entiers.
  - Utilisé pour représenter les éléments de la grille.
  ```python
  items = {"VIDE": 0, "MUR": 1, "CAISSE": 2, "OBJECTIF": 3, "JOUEUR": 4, "CAISSE_OK": 5}
  ```

---

### **3. Structures de données**
- **Grille de jeu** :
  - `grille` est une liste bidimensionnelle de taille `12x12`, initialisée avec des `0` (VIDE).
  - Représente l'état courant du plateau de jeu.
  ```python
  grille = [[0] * cols for i in range(line)]
  ```
  
- **Position du joueur** :
  - `position_joueur` est une liste `[x, y]` qui indique la position actuelle du joueur sur la grille.
  ```python
  position_joueur = [0, 0]
  ```

- **Niveaux du jeu** :
  - Le dictionnaire `niveaux` contient deux niveaux prédéfinis.
  - Chaque niveau est codé sous forme d'une chaîne de caractères où chaque chiffre représente un type d'objet (selon `items`).
  ```python
  niveaux = {
      0: "000000000000...000",
      1: "000000000000...000"
  }
  ```

---

### **4. Variables de couleur**
- Définit des couleurs spécifiques pour les graphismes :
  - `color_blue` : Bleu, utilisé dans l'interface du jeu.
  - `black_color` : Noir, utilisé pour les éléments de fond.
  - `font` : Référence une couleur utilisée pour le texte ou d'autres éléments.
  ```python
  color_blue = (0, 75, 255)
  black_color = (0, 0, 0)
  font = color_blue
  ```

---

## **Technologies et techniques utilisées**

1. **Approche modulaire** :
   - Centralise les constantes et variables globales pour faciliter la maintenance et l'évolutivité.
   - Réduit les répétitions en utilisant des dictionnaires pour les objets et les directions.

2. **Encodage des niveaux** :
   - Les niveaux sont codés sous forme de chaînes de caractères compactes, chaque chiffre représentant un objet.
   - Cette méthode simplifie le stockage et la lecture des niveaux.

3. **Structure de grille** :
   - L'utilisation d'une liste bidimensionnelle permet une représentation claire du plateau de jeu, compatible avec les algorithmes de résolution et d'affichage.

---

## **Points importants pour une transcription ou un recodage**
1. **Représentation des objets** :
   - Lors de la transcription, conservez la logique des entiers pour représenter les types d'objets dans la grille. Par exemple, utilisez un énumérateur ou des constantes similaires dans d'autres langages.

2. **Encodage des niveaux** :
   - Si vous passez à un autre langage, adaptez la logique pour lire et convertir les chaînes de caractères en une grille bidimensionnelle.

3. **Couleurs** :
   - Les couleurs sont définies en format RGB (triplet de 0 à 255). Ce format est compatible avec de nombreux environnements graphiques (HTML/CSS, JavaScript Canvas, Unity, etc.).

4. **Évolutivité** :
   - Le fichier est conçu pour permettre l'ajout de nouveaux niveaux ou objets en modifiant uniquement les dictionnaires ou listes correspondants.

---

