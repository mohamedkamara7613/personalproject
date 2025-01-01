

---

# Jeu du Pendu (Hangman Game)

Ce projet est une implémentation simple et interactive du jeu du pendu en JavaScript. L'objectif est de deviner un mot caché, lettre par lettre, en évitant les mauvaises tentatives.

## Fonctionnalités
- **Chargement dynamique des mots :** Les mots sont chargés à partir d'un fichier texte (`liste.txt`) via une requête `fetch`.
- **Choix aléatoire :** Un mot est sélectionné de manière aléatoire dans la liste après filtrage des lignes vides.
- **Interface utilisateur interactive :** 
  - Affichage du mot sous forme de tirets (`_`) représentant les lettres à deviner.
  - Saisie d'une lettre via un champ de texte avec validation immédiate.
  - Retour d'information pour chaque tentative :
    - "Bonne lettre !"
    - "Mauvaise lettre !"
    - "Entrer une seule lettre !"
  - Affichage d'un message de victoire lorsque le mot est complété.
- **Gestion des erreurs :** Un message d'erreur est affiché en cas de problème lors du chargement des mots.

## Technologies utilisées
- **HTML** pour la structure de la page.
- **CSS** (non inclus ici) pour le style.
- **JavaScript** pour la logique du jeu et l'interactivité.

## Comment ça fonctionne ?
### 1. Chargement des mots
Les mots sont stockés dans un fichier `liste.txt`. 
```javascript
fetch("liste.txt")
    .then(response => response.text())
    .then(data => {
        var wordList = data.split("\n").filter(word => word.trim() !== "");
    });
```
- Le fichier est lu ligne par ligne, et les mots sont nettoyés à l'aide de `trim()` pour supprimer les espaces superflus.

### 2. Sélection aléatoire
Un mot est choisi aléatoirement dans la liste à l'aide de :
```javascript
var randomIndex = Math.floor(Math.random() * wordList.length);
const wordToGuess = wordList[randomIndex].toLowerCase();
```
- **`Math.random()`** génère un nombre aléatoire entre 0 et 1.
- **`Math.floor()`** arrondit à l'entier inférieur.

### 3. Jeu interactif
- L'utilisateur propose une lettre via un champ de saisie.
- La lettre est vérifiée dans le mot choisi :
  - Si elle est correcte, elle remplace le `_` correspondant.
  - Sinon, un message d'erreur est affiché.
- Le jeu s'arrête lorsque toutes les lettres sont correctement devinées.

### 4. Gestion des événements
- **Clic sur le bouton "submit" :** Déclenche la fonction principale.
- **Appui sur "Enter" :** Permet également de valider la tentative.

### 5. Résultat final
- Si l'utilisateur devine le mot :
  - Le message "Bravo !" s'affiche.
  - Les champs de saisie et le bouton sont masqués.
  - Un bouton de restart est affiché.


## Points d'amélioration
- Ajouter un compteur d'essais pour limiter le nombre de tentatives.
- Ajouter des animations pour rendre le jeu plus attractif.


---