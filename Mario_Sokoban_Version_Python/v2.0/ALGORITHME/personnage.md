# README - personnage.py

## Description détaillée

Le fichier `personnage.py` constitue l'une des pierres angulaires de la gestion des personnages dans le jeu *Mario Sokoban v2.0*. Ce script est chargé de permettre à l'utilisateur de choisir son personnage parmi une liste prédéfinie de héros emblématiques, tout en gérant l'affichage des options de sélection et en adaptant les actions possibles de chaque personnage selon les choix effectués.

Lorsque le jeu est lancé, ce fichier prend en charge la gestion du menu de sélection des personnages. À l'aide de Pygame, il présente une interface interactive à l'utilisateur, lui permettant de visualiser les personnages disponibles sous forme d'images et de sélectionner celui qu'il souhaite incarner.

Le choix du personnage n'est pas seulement une question d'apparence : chaque personnage possède des comportements distincts, et ce fichier gère le chargement des images spécifiques pour chaque direction de déplacement du personnage (haut, bas, gauche, droite), garantissant que les animations sont correctement associées au personnage sélectionné.

Le processus de sélection des personnages est interactif, réactif et basé sur des entrées clavier. Dès qu'un joueur appuie sur une touche dédiée (de `1` à `5`), le personnage correspondant est sélectionné, et ses animations (images de déplacement dans les différentes directions) sont chargées et prêtes à être utilisées dans le jeu.

### Les principales étapes de la logique de ce fichier :

1. **Initialisation de l'interface et chargement des ressources**
   - Le fichier commence par charger les ressources nécessaires à l'affichage du menu de sélection des personnages, telles que les images des personnages et les polices de texte pour l'affichage.
   - Chaque personnage a des images représentant son état dans différentes directions, comme "haut", "bas", "gauche", et "droite".

2. **Affichage du menu de sélection des personnages**
   - L'interface de sélection est affichée sous la forme d'une liste d'images représentant les différents personnages.
   - Les images sont centrées à l'écran pour une présentation claire et cohérente.
   
3. **Gestion des entrées utilisateur**
   - Le fichier surveille les événements utilisateurs (appuis sur les touches du clavier) pour détecter quel personnage a été sélectionné.
   - Chaque touche (`1`, `2`, `3`, `4`, `5`) correspond à un personnage particulier (Mario, Ndeya, Shadow, Tail, Sonic).
   - Lorsqu'une touche est pressée, le fichier charge les images de direction correspondantes pour le personnage choisi et passe à l'étape suivante, où une confirmation du choix est affichée à l'écran.
   
4. **Confirmation du choix du personnage**
   - Une fois le personnage sélectionné, le jeu affiche un message confirmant le choix de l'utilisateur.
   - Le personnage est alors affiché avec son image de base (dans ce cas, l'image de la direction "bas").
   - Une courte pause est ajoutée pour que l'utilisateur puisse voir son choix avant de continuer.

5. **Transition vers le jeu**
   - Après la sélection et la confirmation du personnage, le fichier quitte la boucle de sélection et permet au jeu de continuer avec le personnage choisi, prêt à interagir avec l'environnement du jeu.

## Rôle dans le projet

Le fichier `personnage.py` joue un rôle essentiel dans la gestion de l'interactivité du jeu *Mario Sokoban v2.0*, en permettant à l'utilisateur de personnaliser son expérience de jeu dès le début. Il permet non seulement de choisir un personnage, mais aussi d'établir une dynamique visuelle et fonctionnelle autour de ce personnage pour la suite du jeu.

Ce fichier sert de point de départ pour l'initialisation des personnages, et il est conçu pour être facilement extensible. À l'avenir, d'autres personnages pourront être ajoutés sans modification importante de la logique existante.

## Fonctionnalités détaillées

### 1. **Sélection des personnages**
   - Le joueur peut choisir parmi cinq personnages distincts :
     - Mario (touche `1`)
     - Ndeya (touche `2`)
     - Shadow (touche `3`)
     - Tail (touche `4`)
     - Sonic (touche `5`)
   - Chaque personnage est représenté par une image dans le menu et possède des animations propres pour les quatre directions de déplacement.

### 2. **Gestion des animations des personnages**
   - Lorsqu'un personnage est sélectionné, des images spécifiques à chaque direction de déplacement (haut, bas, gauche, droite) sont chargées en mémoire.
   - Ces images sont ensuite utilisées dans le jeu pour animer le mouvement du personnage lorsque celui-ci interagit avec l'environnement.
   - Par exemple, pour Mario, les images `mario_haut.gif`, `mario_bas.gif`, `mario_gauche.gif`, et `mario_droite.gif` sont chargées, et une image spécifique est affichée en fonction de la direction choisie par le joueur.

### 3. **Affichage dynamique du menu**
   - Le menu de sélection est interactif et réactif. Lorsqu'une touche est pressée, le jeu réagit immédiatement, mettant à jour l'affichage pour montrer quel personnage a été choisi.
   - Un message est affiché pour informer l'utilisateur de sa sélection, accompagné de l'animation correspondante du personnage choisi (image de direction `bas`).

### 4. **Contrôle des événements utilisateur**
   - Les événements sont gérés en temps réel à l'aide de Pygame. Le fichier détecte les pressions de touches et les événements de fermeture de fenêtre pour ajuster l'état du jeu.
   - Le contrôle des entrées se fait principalement via les touches numériques du clavier, ce qui rend le processus de sélection fluide et simple pour l'utilisateur.

### 5. **Confirmation et transition**
   - Une fois le personnage choisi, le jeu affiche une confirmation du choix et passe à l'étape suivante, où le personnage pourra être utilisé dans le gameplay.

## Technologies utilisées

- **Pygame** : Cette bibliothèque est utilisée pour toutes les opérations liées à l'affichage graphique et à la gestion des événements dans le jeu. Elle permet de charger et d'afficher des images, de gérer les entrées clavier, et d'actualiser l'affichage en temps réel.
- **Python** : Le langage de programmation principal utilisé dans ce projet. La logique du jeu, la gestion des événements et le contrôle du flux de programme sont tous codés en Python.
  
## Conclusion

Le fichier `personnage.py` est un composant clé pour l'interactivité et la personnalisation du jeu *Mario Sokoban v2.0*. Il permet de sélectionner un personnage, de gérer les animations de mouvement associées à chaque personnage et d'afficher un menu dynamique et réactif. Ce fichier est conçu de manière modulaire et extensible, permettant l'ajout facile de nouveaux personnages dans le futur sans nécessiter de refonte majeure de la logique existante.
