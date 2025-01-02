
---

# **README - game.py (détaillé)**

## **Description globale**
Le fichier `game.py` est le cœur du gameplay de Mario Sokoban v2.0.  
Il s'occupe de l'**exécution de la logique principale du jeu**, gère les interactions utilisateur (clavier), contrôle les déplacements du joueur et des caisses, et vérifie les conditions de victoire.

Il est structuré autour de trois fonctions principales :
1. `play()` : La boucle principale du jeu.
2. `deplacer_joueur()` : Gestion des mouvements du joueur.
3. `deplacer_caisse()` : Gestion des déplacements des caisses.

---

## **Fonctions principales**

### **1. Fonction `play(window_surface)`**
La fonction `play` est le point d’entrée pour lancer une partie complète du jeu.

#### **a) Initialisation**
- **Activation des répétitions des touches :**
  - Permet de maintenir une touche enfoncée pour répéter l’action associée.  
    ```python
    pygame.key.set_repeat(200, 200)
    ```

- **Chargement des ressources :**
  - Sons (`pygame.mixer.Sound`) : Joués en fonction des événements (victoire, mouvement, etc.).
  - Sprites (`pygame.image.load`) : Images des murs, caisses, objectifs, etc.
  - Polices (`pygame.font.Font`) : Utilisées pour afficher du texte (niveau actuel).
  
- **Initialisation du joueur et du niveau :**
  - Le joueur est sélectionné via le module `personnage`.
  - La grille est remplie par le niveau en cours, chargé depuis `gestion_file`.

#### **b) Affichage des instructions**
Avant de commencer le jeu, un écran d’instructions est affiché :
- Série d’images expliquant les commandes et le gameplay.
- Une boucle attend que l’utilisateur appuie sur une touche pour continuer.

#### **c) Boucle principale du jeu**
La boucle principale gère :
1. **Les événements utilisateur :**
   - Fermeture de la fenêtre : `pygame.QUIT`.
   - Changement de niveau : `PAGEUP` et `PAGEDOWN`.
   - Redémarrage du niveau : `R`.
   - Déplacement du joueur : Flèches directionnelles (`K_UP`, `K_DOWN`, etc.).

2. **Mise à jour de l’état du jeu :**
   - Le joueur se déplace en fonction des règles.
   - Les caisses sont déplacées si elles peuvent être poussées.
   - Si toutes les caisses sont placées sur les objectifs, le niveau suivant est chargé.

3. **Rendu graphique :**
   - Efface l’écran (couleur de fond).
   - Affiche les éléments de la grille :
     - Murs, caisses, objectifs, joueur.
   - Affiche les informations, comme le niveau actuel.

4. **Vérification des conditions de victoire :**
   - Si tous les objectifs sont remplis (`objectif_restant == False`), un écran de victoire est affiché et le niveau suivant est chargé.

#### **d) Gestion de la fin de jeu**
Si le joueur termine le dernier niveau :
- Un message final s’affiche.
- Le jeu joue un son spécifique (`Ralenti.wav`) et se termine.

---

### **2. Fonction `deplacer_joueur(direction_deplacement, grille)`**
Gère les déplacements du joueur dans une direction donnée (haut, bas, gauche, droite).

#### **a) Vérifications avant déplacement**
1. **Bord de la fenêtre :**
   - Le joueur ne peut pas sortir des limites de la grille.

2. **Obstacle devant le joueur :**
   - Si le joueur tente de passer à travers un mur (`items["MUR"]`), le mouvement est annulé.
   - Si une caisse bloque le chemin, vérifie si la caisse peut être déplacée.

3. **Conditions pour déplacer une caisse :**
   - Une caisse peut être poussée uniquement si la case suivante est libre ou un objectif.

#### **b) Déplacement**
- Si les conditions sont remplies :
  - Déplace la caisse en appelant `deplacer_caisse`.
  - Met à jour la position du joueur.
  - Joue un son de mouvement (`move.wav`).

---

### **3. Fonction `deplacer_caisse(direction_deplacement, position_joueur)`**
Gère le déplacement des caisses poussées par le joueur.

#### **a) Vérifications**
1. **Type de caisse :**
   - Vérifie si la case devant contient une caisse (`items["CAISSE"]` ou `items["CAISSE_OK"]`).

2. **Destination de la caisse :**
   - Si la case suivante est un objectif, transforme la caisse en "caisse OK" (`items["CAISSE_OK"]`).
   - Sinon, la caisse reste une caisse classique.

3. **Mise à jour de la grille :**
   - La position actuelle de la caisse devient vide (`items["VIDE"]` ou `items["OBJECTIF"]` si la caisse était sur un objectif).

#### **b) Effets**
- Les caisses qui atteignent les objectifs changent d’état pour indiquer qu’elles sont bien placées.

---

## **Gestion des niveaux**
- Les niveaux sont chargés dynamiquement via le module `gestion_file`.
- Chaque niveau est représenté par une grille bidimensionnelle où chaque cellule correspond à un type d’objet (mur, vide, caisse, etc.).
- Navigation entre niveaux :
  - `PAGEUP` : Passe au niveau suivant.
  - `PAGEDOWN` : Revient au niveau précédent.
  - `R` : Recharge le niveau actuel.

---

## **Exemple de déroulement d’une partie**
1. L’utilisateur lance `play(window_surface)`.
2. Le jeu affiche les instructions.
3. Une fois les instructions validées, le premier niveau est chargé.
4. L’utilisateur contrôle le joueur pour pousser les caisses sur les objectifs.
5. Lorsque toutes les caisses sont bien placées, le jeu passe au niveau suivant.
6. Si le dernier niveau est terminé, un message final s’affiche.

---

## **Détails techniques importants**

1. **Rendu graphique :**
   - Les éléments sont affichés dans une boucle continue, utilisant `pygame.Surface` pour les sprites.

2. **Sons :**
   - Les sons d’événements sont associés à des actions précises :
     - Mouvement réussi : `move.wav`.
     - Mouvement impossible : `impossible.wav`.
     - Victoire : `bingo.ogg`, `tasty.ogg`.

3. **Grille de jeu :**
   - Représentée par une liste bidimensionnelle. Chaque cellule contient un entier correspondant à un type d’objet.

4. **Boucle principale :**
   - Limite à 60 images par seconde (`clock.tick(60)`) pour des performances uniformes sur différents appareils.

5. **Gestion des conditions de victoire :**
   - Vérifie après chaque mouvement si toutes les caisses sont sur des objectifs.

---

## **Prochaines étapes**
`gestion_file.py`, `personnage.py`

