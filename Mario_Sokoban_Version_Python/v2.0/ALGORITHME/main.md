

---

# **README - main.py**

## **Description du fichier**
Le fichier `main.py` est le point d'entrée principal du projet Mario Sokoban v2.0.  
Son rôle est de :
1. Initialiser les paramètres globaux du jeu, tels que l'affichage et les ressources (images, sons).
2. Fournir un menu interactif permettant de naviguer vers différentes sections du jeu (jouer, éditeur, quitter).
3. Gérer les événements principaux (clavier, fermeture de la fenêtre) via une boucle principale.

---

## **Fonctionnalités principales**

### **1. Initialisation de l'environnement**
- **Modules et bibliothèques** :
  - Importe les modules internes `data` et `game` pour la gestion des données et des mécanismes du jeu.
  - Utilise `pygame` pour gérer l'interface graphique, les événements, et le son.
- **Configuration graphique** :
  - Charge et définit une icône pour la fenêtre (`doc/src_img/icone.png`).
  - Configure une fenêtre de jeu avec des dimensions prédéfinies (`dimension_window`) en utilisant `pygame.display.set_mode`.
  - Définit le titre de la fenêtre avec `pygame.display.set_caption`.

### **2. Chargement des ressources**
- **Images** :  
  Le menu du jeu utilise une série d'images stockées dans `doc/src_img/menu/`. Les images sont positionnées dynamiquement à l'écran en fonction des dimensions de la fenêtre.
  - Images principales : `1.png`, `2.png`, `3.png`, `4.png`, `5.png`.
  - Signature : `signature.png`.
- **Son** :  
  Charge un fond sonore (`font_soung.ogg`) qui est joué en boucle avec un volume ajusté à 90%.

### **3. Menu principal interactif**
Le menu affiche des options interactives permettant :
- De lancer une partie en appuyant sur `K_KP1` (touche pavé numérique 1).
- D'accéder à un éditeur (non implémenté dans ce fichier, mais prévu sur la touche `K_KP2`).
- De quitter le jeu en appuyant sur `K_ESCAPE` ou en fermant la fenêtre.

### **4. Gestion des événements**
- La boucle principale écoute les événements utilisateurs avec `pygame.event.get()` :
  - **Fermeture** : Quitte proprement en cas d'appui sur `ESCAPE` ou fermeture de la fenêtre.
  - **Navigation** : Permet de naviguer dans les options via les touches du clavier.

### **5. Rendu graphique**
- Le menu est redessiné en continu :
  - Efface l'écran avec une couleur de fond.
  - Blitte (affiche) chaque élément graphique (images de menu, signature).
  - Met à jour l'affichage avec `pygame.display.flip()`.

---

## **Technologies et techniques utilisées**

### **1. Pygame**
- **Affichage** :
  - Utilise `pygame.Surface` pour dessiner et afficher les éléments graphiques.
  - Gère les dimensions et positions dynamiques des images du menu.
- **Événements** :
  - Écoute les événements clavier (`pygame.KEYDOWN`) pour déclencher des actions.
  - Gère proprement la fermeture via `pygame.QUIT`.
- **Son** :
  - Charge et joue une musique de fond en boucle avec `pygame.mixer.Sound`.

### **2. Architecture modulaire**
- Le fichier délègue certaines responsabilités à d'autres modules :
  - `game` : Gestion des mécanismes du jeu (non détaillé ici).
  - `data` : Données et configurations partagées (probablement les dimensions, couleurs, etc.).

---

## **Points importants pour une transcription ou un recodage**
1. **Gestion des ressources** :
   - Le chemin des ressources (images, sons) est relatif. Assurez-vous de bien gérer ces chemins dans d'autres environnements.
   - Format des ressources (PNG, OGG) : Privilégier des formats compatibles avec l'environnement cible.

2. **Interface utilisateur** :
   - L'algorithme du menu repose sur la gestion dynamique des positions des images. Cela pourrait nécessiter des adaptations si l'interface est transcrite dans une technologie différente (ex. HTML/CSS/JS).

3. **Événements clavier** :
   - Les actions du menu sont liées à des touches spécifiques (`K_KP1`, `K_ESCAPE`). Adaptez-les selon les conventions du nouveau langage.

4. **Sons et performances** :
   - Le son de fond est joué en boucle avec un volume fixe. Si vous transcrivez dans un navigateur ou une application mobile, considérez les performances audio et la compatibilité.

5. **Gestion de la boucle principale** :
   - La boucle principale (`while True`) gère à la fois les événements et le rendu graphique. Veillez à adapter ce modèle dans des environnements asynchrones (comme JavaScript ou frameworks modernes).

---

## **Prochaines étapes**
`data.py`, `game.py`
