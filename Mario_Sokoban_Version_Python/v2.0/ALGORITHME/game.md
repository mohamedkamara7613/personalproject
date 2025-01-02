
---

# **README - game.py**

## **Description du fichier**
Le fichier `game.py` gère l'exécution d'une partie complète du jeu Mario Sokoban.  
Il contient :
1. Les mécanismes de gestion de la boucle de jeu principale.
2. La gestion des mouvements du joueur et des caisses.
3. Le chargement et l'affichage des niveaux.
4. La vérification des conditions de victoire.

---

## **Fonctionnalités principales**

### **1. Initialisation d'une partie**
- La fonction principale `play(window_surface)` initialise les ressources nécessaires pour une partie :
  - Activation de la répétition des touches avec `pygame.key.set_repeat`.
  - Chargement des sons, images (sprites), et polices utilisés dans le jeu.
  - Initialisation du joueur (via le module `personnage`) et du niveau.

---

### **2. Gestion de la boucle de jeu principale**
La boucle principale :
1. **Écoute des événements utilisateur** (clavier, fermeture de la fenêtre).
2. **Met à jour l'état du jeu** en fonction des interactions (mouvements, changement de niveau).
3. **Dessine les éléments du jeu à l'écran** :
   - Effacement de l'écran.
   - Affichage des murs, caisses, objectifs, et joueur.
   - Affichage des informations du jeu (ex. niveau actuel).
4. **Vérifie les conditions de victoire** :
   - Si tous les objectifs sont remplis, passe au niveau suivant.

---

### **3. Mécanismes des mouvements**
#### **Déplacement du joueur : `deplacer_joueur(direction_deplacement, grille)`**
- Vérifie si le joueur peut se déplacer dans la direction souhaitée.
- Si une caisse est dans la direction choisie, appelle `deplacer_caisse` pour la déplacer.
- Joue des sons spécifiques en cas de mouvement ou d’impossibilité (mur, bord de la fenêtre, etc.).

#### **Déplacement des caisses : `deplacer_caisse(direction_deplacement, position_joueur)`**
- Si une caisse est poussée :
  - Vérifie si la position cible est valide (pas de mur, autre caisse, etc.).
  - Met à jour la grille en transformant la caisse en "caisse OK" si elle est sur un objectif.

---

### **4. Gestion des niveaux**
- **Chargement des niveaux** : 
  Utilise le module `gestion_file` pour charger un niveau en fonction de l'indice actuel. Les niveaux sont représentés comme des grilles de jeu.
- **Navigation entre niveaux** :
  - `PAGEUP` : Passe au niveau suivant.
  - `PAGEDOWN` : Revient au niveau précédent.
  - `R` : Recharge le niveau actuel.
- **Recherche de la position initiale du joueur** :
  - Après le chargement d'un niveau, recherche la position du joueur dans la grille et la met à jour.

---

### **5. Affichage**
- **Sprites des objets** :
  - Les murs, caisses, objectifs et caisses "OK" sont dessinés à l'aide de sprites chargés depuis `doc/src_img/`.
- **Interface utilisateur** :
  - Affiche le niveau actuel en haut à droite de l'écran.
  - Utilise une police chargée depuis `doc/police.ttf`.
- **Instructions** :
  - Avant le début de la partie, affiche des instructions à l'utilisateur via une série d'images.

---

### **6. Gestion sonore**
- **Sons pendant la partie** :
  - Joue des sons en fonction des événements :
    - Mouvement valide : `move.wav`.
    - Mouvement impossible : `impossible.wav`.
    - Victoire : `bingo.ogg` et `tasty.ogg`.
- **Son de fin de jeu** :
  - Joue un son spécifique (`Ralenti.wav`) lorsque le dernier niveau est terminé.

---

## **Technologies et techniques utilisées**

1. **Pygame** :
   - Gestion des événements (clavier, fermeture de fenêtre).
   - Gestion graphique : `pygame.Surface` pour le rendu des sprites.
   - Gestion sonore : `pygame.mixer.Sound`.

2. **Structure modulaire** :
   - Le fichier utilise d'autres modules (`data`, `gestion_file`, `personnage`) pour maintenir une organisation claire.

3. **Boucle de jeu optimisée** :
   - Limite les images par seconde à 60 avec `clock.tick(60)` pour garantir une vitesse constante.

4. **Manipulation de grilles** :
   - Les objets du jeu sont représentés dans une grille bidimensionnelle, ce qui simplifie la gestion des déplacements et des vérifications.

---

## **Points importants pour une transcription ou un recodage**

1. **Mécanismes de déplacement** :
   - Gardez la logique de déplacement du joueur et des caisses séparée pour faciliter les adaptations.

2. **Rendu graphique** :
   - Les sprites actuels sont affichés avec `pygame.Surface`. Si vous passez à une autre technologie (ex. HTML5 Canvas), adaptez cette logique.

3. **Sons** :
   - Les formats `.wav` et `.ogg` sont utilisés pour les sons. Assurez-vous que le nouvel environnement supporte ces formats.

4. **Niveaux et grilles** :
   - Les niveaux sont chargés dynamiquement depuis un fichier. Assurez-vous que cette logique est bien transcrite pour éviter de hardcoder les niveaux.

5. **Modularité** :
   - La structure actuelle sépare clairement les responsabilités (mécaniques dans `game.py`, données dans `data.py`, etc.). Conservez cette modularité.

---

## **Prochaines étapes**
`gestion_file.py`, `personnage.py`