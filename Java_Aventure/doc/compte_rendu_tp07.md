# Compte Rendu - Programmation Orientée Objet - TP07 (Aventure)

Ce document synthétise le travail de conception et d'implémentation réalisé durant le TP07 pour le projet "Aventure". L'objectif principal de ce TP était d'introduire la gestion des entrées/sorties, allant du chargement d'un scénario via description texte, jusqu'à la sauvegarde et le chargement de mondes sérialisés via flux binaires.

## 1. Interaction et Ordres : La classe `JoueurHumain`

La classe `JoueurHumain` a été complétée pour permettre à l'utilisateur d'interagir avec l'univers du jeu :
* **Stockage de l'ordre :** Un attribut `ordre` de type `String` a été ajouté, avec ses accesseurs `getOrdre()` et son mutateur `setOrdre(String)`.
* **Prise en charge des commandes :** Cinq méthodes privées ont été implémentées pour décomposer les actions possibles d'un joueur. Chacune est reliée à de nombreuses exceptions de notre architecture (exemple: `ObjetAbsentDeLaPieceException`, `PorteFermeException`, etc.) :
  * `commandePrendre(String nomObjet)`
  * `commandePoser(String nomObjet)`
  * `commandeFranchir(String nomPorte)`
  * `commandeOuvrirPorte(String nomPorte)`
  * `commandeOuvrirPorte(String nomPorte, String nomObjet)` (pour l'ouverture avec une clé)
* La méthode `executer()` a été définie (laissée vide pour le moment en attente du futur analyseur syntaxique du prochain TP).

## 2. Abstraction des flux : `Lecteur` & `Enregistreur`

Afin d'isoler la logique d'obtention et de persistance du `Monde`, deux interfaces de base ont été créées dans le paquet `fr.insarouen.iti.prog.aventure.data` :
* **`Lecteur`** : Contient simplement la méthode `Monde getMonde()`.
* **`Enregistreur`** : Contient la méthode d'écriture `void enregistrer(Monde monde)`.

## 3. Mise en place d'un Parseur : `LecteurDescription`

Pour instancier directement les éléments du monde à partir d'un fichier texte formaté (comme les `.aa`), la classe `LecteurDescription` (implémentant `Lecteur`) a été conçue.
* Elle utilise la classe `java.util.Scanner` de façon robuste dans un bloc *try-with-resources* englobant un `Reader` (ex: un `FileReader`).
* Un `switch...case` interprète le premier mot de la ligne (`Monde`, `Piece`, `PorteSerrure`, etc.).
* Des méthodes constructrices privées (`createPiece`, `placeCle`, etc.) sont chargées d'alimenter correctement le `Monde` à l'aide des jetons récupérés. 

## 4. Persistance des Instances : La Sérialisation

Afin de pouvoir sauvegarder et reprendre une partie exactement là où on l'a laissée :
* **`EnregistreurSerialisation` (implémente `Enregistreur`) :** Reçoit un `ObjectOutputStream` dans son constructeur. Sa méthode `enregistrer` utilise la méthode standard `writeObject(monde)` de l'API de Sérialisation Java pour envoyer l'univers dans un flux abstrait.
* **`LecteurSerialisation` (implémente `Lecteur`) :** Reçoit un `ObjectInputStream` et emploie sa méthode `readObject()`. Il effectue ensuite la désérialisation du scénario avec un _cast_ explicite `(Monde)`.
Les classes gèrent ou propagent avec précautions la vérification des `IOException` et `ClassNotFoundException`.

## 5. Le coeur du jeu : La classe `Main`

Pour relier l'ensemble du projet de manière interactive pour l'utilisateur, un point d'entrée unique `Main` a été mis en œuvre. 
Le programme repose sur une interface console manipulée avec `Scanner(System.in)`. L'utilisateur se voit présenter la boucle de menu de base :

```
--- Menu ---
1/ jouer
2/ charger un fichier de description
3/ sauver la partie actuelle
4/ charger une partie
5/ quitter
```

Le flux interne des choix orchestre les instanciations de classes créées pendant le TP :
* **L'option 2** branche le constructeur d'un `FileReader` dans un `LecteurDescription` pour récupérer l'univers du fichier texte.
* **L'option 3** crée un `FileOutputStream` greffé à un `EnregistreurSerialisation` pour écrire un `.sav` via `writeObject`. 
* **L'option 4** récupère un fichier `.sav` par un `FileInputStream` et son pont `LecteurSerialisation` pour recharger la référence du "mondeCourant". 

## 6. Automatisation locale

Pour faciliter la vie de l'utilisateur, et afin d'encapsuler la longue chaîne du classpath, une cible `run-main` a finalement été déclarée dans le `Makefile`. L'exécution de `make run-main` démarre instantanément la machine virtuelle Java sur la classe principale récemment implémentée.
