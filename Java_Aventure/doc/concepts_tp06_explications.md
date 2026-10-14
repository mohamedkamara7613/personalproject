# Comprendre le TP06 : Concepts et Modifications récentes

Ce document a pour but d'éclaircir tout ce qui a été fait jusqu'à présent dans le TP06, ce que le TP06 introduit en termes de concepts Java et de gameplay, et pourquoi certaines modifications ont été ajoutées dans ton code pour faire passer les tests du prof.

---

## 1. La grande image : Qu'apporte le TP06 ?

Le TP06 vise à enrichir le gameplay de *Java Aventure* avec deux nouveautés majeures :
1. **Les Portes verrouillables** (via des serrures et des clés).
2. **Les Monstres** (qui se déplacent seuls, ouvrent des portes, et s'épuisent).

### Concept Java mis en avant : L'Encapsulation et la Délégation
Dans le TP05, on a créé une [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#20-122). Dans le TP06, on lui ajoute une [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92). 
Plutôt que de coder toute la logique de verrouillage dans [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#20-122), on **délègue** cette responsabilité à un nouvel objet : la [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92).
- **Encapsulation :** La clé ([Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#13-35)) est intimement liée à la [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92). Seule une serrure peut fabriquer sa propre clé. C'est pour cela que le constructeur de [Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#13-35) doit être *package-private* (sans `public`) : pour empêcher le reste du programme de forger de fausses clés !

---

## 2. Comment fonctionne l'activation d'une Porte désormais ?

Avant le TP06, une porte était soit [FERME](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81) soit [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81). 
Maintenant, avec une serrure, elle peut être `VERROUILLE`. Voici la cinématique complète :

1. **Création (`new Porte(..., serrure, ...)`):** La porte naît avec une serrure. Son état initial est obligatoirement `VERROUILLE`.
2. **Essayer d'ouvrir à mains nues ([activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#74-87)) :** La porte demande à sa serrure : "Es-tu verrouillée ?". Si oui, elle refuse de s'ouvrir (`ActivationImpossibleException`).
3. **Utiliser une clé ([activerAvec(cle)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#88-105)) :**
   - La porte passe la clé à la serrure.
   - La serrure reconnaît SA clé et passe en état `DEVERROUILLE`.
   - La porte voit que la serrure s'est déverrouillée, donc elle s'ouvre automatiquement (passe à [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81)).
4. **Utiliser un Pied de Biche ([activerAvec(piedDeBiche)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#88-105)) :**
   - La porte reconnaît l'outil miracle.
   - Elle **détruit la serrure** (`this.serrure = null;`) !
   - Elle s'ouvre de force (passe à [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81)).
   - *Désormais, cette porte se comportera pour toujours comme une porte sans serrure (plus besoin de clé).*

---

## 3. Explication des modifications de code récentes

Pour que ton code soit 100% compatible avec les tests stricts du professeur (les fameux `.class` dans le zip), j'ai dû ajuster quelques détails importants. Voici exactement ce qui a changé et **pourquoi**.

### Modification A) L'état initial de la Porte
- **Fichier :** [Porte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java)
- **Ce qui a changé :** Dans le constructeur avec serrure, j'ai ajouté `this.etat = Etat.VERROUILLE;`
- **Pourquoi :** Si on crée une porte avec une serrure, la logique du prof impose qu'elle soit de facto verrouillée, et non simplement "fermée". S'appuyer sur l'état de la serrure est la règle.

### Modification B) La réaction de la Porte après l'usage de la clé
- **Fichier :** [Porte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java) (méthode [activerAvec()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#88-105))
- **Ce qui a changé :** Une fois que la clé déverrouille la serrure, la porte change son propre état : `if (this.serrure.getEtat() == Etat.DEVERROUILLE) { this.etat = Etat.OUVERT; }`
- **Pourquoi :** Dans les tests du prof, l'action "utiliser la bonne clé" ne fait pas que déverrouiller la serrure : elle **ouvre** directement la porte dans la foulée. Avant cette modif, la porte restait [FERME](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81). 

### Modification C) La méthode manquante [getSerrure()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#49-52)
- **Fichier :** [Porte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java)
- **Ce qui a changé :** Ajout de la méthode `public Serrure getSerrure() { return this.serrure; }`
- **Pourquoi :** Les tests du prof s'en servent pour vérifier que le Pied de Biche a bien arraché la serrure (ils vérifient que [getSerrure()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#49-52) retourne `null` après le coup de pied de biche). Ton code ne l'avait pas, donc le test crashait.

### Modification D) La méthode manquante [getPorte(String)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#282-285)
- **Fichier :** [Piece.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java)
- **Ce qui a changé :** Ajout de `public Porte getPorte(String nomPorte)` (qui cherche la porte dans la `HashMap` par son nom).
- **Pourquoi :** Exactement comme [getSerrure()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#49-52), le test [TestPorte](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#18-158) du prof appelle `piece.getPorte("nomDeLaPorte")`. Comme cette méthode n'était pas écrite, le test crashait (`NoSuchMethodError`).

---

## 4. Bilan et Prochaine Étape : Le Monstre

Grâce à ces 4 petites corrections méticuleuses axées sur "ce qu'attend le prof", **tous les tests du prof pour les Portes et les Serrures sont désormais au vert**.

La **seule chose** qui manque dans tout ton projet TP06, c'est la classe `Monstre`. 
Le monstre est passionnant car il va illustrer deux concepts Java :
1. **L'héritage :** `Monstre` hérite de [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328).
2. **Les Streams Java 8 :** Le monstre doit trouver une porte parmi toutes les portes de la pièce en utilisant l'API Stream (`.stream().filter(...).findFirst()`). C'est un point de notation important du prof.

Dès que tu auras codé `Monstre` et sa méthode `executer()`, ton TP06 sera terminé à 100% !
