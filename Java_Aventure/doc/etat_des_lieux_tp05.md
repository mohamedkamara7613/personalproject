# État des lieux - TP 05 "ASI Aventure"

J'ai analysé les consignes du TP (fichier PDF) et le code du répertoire `codes`. Voici où vous en êtes dans l'ordre du TP :

## L'avancement actuel

### 1 et 2. Passage aux collections & retours de tableaux 
**Statut : En cours, mais avec des erreurs**
* **Fait** : Les entités internes ont bien été transformées en collections (`Map<String, Objet>`, `Map<String, Vivant>`, etc.) dans les classes [Monde](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#12-145), [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#21-261) et [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#19-231).
* **Fait** : Les méthodes de type « getter » ont été mises à jour pour retourner des `Collection<Type>`.
* **Problème** : **Les tests échouent.** La contrainte *« Tant que AllTests ne passe pas, on ne passe pas à la suite »* n'est pas remplie. 

**Explication des 4 erreurs de tests actuelles (`make run-tests`) :**
1. **`NullPointerException` lors du retrait d'un objet absent (`Piece.retirer(String)` et `Vivant.prendre(String)`)** :
   En passant d'un tableau à une `Map`, vous avez gardé un bloc `catch (ArrayIndexOutOfBoundsException)`. Or, la méthode [get()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#42-50) ou `remove()` d'une `Map` ne lève pas cette exception si l'élément n'existe pas, elle renvoie `null`. Vous essayez d'appeler `.estDeplacable()` sur un objet `null`, ce qui fait planter le code.
2. **AssertionError dans `TestPiece.test_retirer_Objet_Absent`** :
   Même problème, la méthode ne déclenche plus l'exception attendue `ObjetAbsentDeLaPieceException`.
3. **Erreur d'assertion dans `TestPiece.test_getVivants`** :
   La méthode a été changée pour retourner une `Collection`, mais le test unitaire attend peut-être encore un certain format précis ou a besoin d'être adapté (l'étape 2 du TP autorise à modifier les tests pour s'adapter aux collections).

### 3. La classe `Porte`
**Statut : Non commencé**
La classe n'a pas encore été créée dans les sources.

### 4 et 5. Gestion des portes dans [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#19-231) et [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#21-261)
**Statut : Non commencé**

---

## Prochaines étapes suggérées

Pour respecter l'ordre du TP, il faut d'abord **corriger les 4 erreurs de tests unitaires** avant de toucher aux portes. Voulez-vous que je procède à la correction de la classe [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#19-231) (et des tests `TestPiece`) pour que `AllTests` soit valide à nouveau ?
