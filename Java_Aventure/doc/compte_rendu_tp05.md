# Compte-rendu TP05 — ASI Aventure

Ce document résume les modifications apportées aux classes [Monde](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java), [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java) et [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java), ainsi que la création de [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java), les erreurs rencontrées et corrigées.

---

## 0. Concepts clés utilisés dans ce TP

### `Map<K, V>` (interface Java Collections)
Une `Map` associe une **clé** (`K`) à une **valeur** (`V`). On a utilisé `HashMap<String, T>` où la clé est le **nom** de l'entité, ce qui permet une recherche en O(1) au lieu de O(n) avec un tableau.

| Méthode Map | Rôle |
|---|---|
| `put(clé, valeur)` | Ajouter/mettre à jour un élément |
| [get(clé)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Entite.java#83-91) | Récupérer un élément par clé (`null` si absent) |
| `remove(clé)` | Supprimer et retourner l'élément |
| `containsKey(clé)` | Teste si la clé existe |
| `containsValue(val)` | Teste si la valeur existe (**O(n)** — parcours linéaire) |
| `values()` | Retourne une **vue live** des valeurs |
| `keySet()` | Retourne l'ensemble des clés |

### Copie défensive sur `Collection`
Lorsqu'une méthode retourne `map.values()`, elle expose une **vue live** de la structure interne : toute modification externe pourrait corrompre l'état de l'objet. La bonne pratique est de retourner une **copie** :

```java
// ❌ Dangereux : expose l'état interne directement
return this.tabObjet.values();

// ✅ Correct : copie défensive — l'appelant ne peut pas modifier l'interne
return new ArrayList<>(this.tabObjet.values());
```

### Interface [Activable](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#7-16)
Toute entité pouvant être activée (comme [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81)) implémente cette interface :
```java
public interface Activable {
    boolean activableAvec(Objet obj);
    void activer() throws ActivationException;
    void activerAvec(Objet obj) throws ActivationException;
}
```

### Enum [Etat](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#31-34)
L'état d'une porte (ou tout élément activable) est représenté par l'enum [Etat](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#31-34) :
[FERME](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81), [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81), `VERROUILLE`, `DEVERROUILLE`, `CASSE`.

> [!IMPORTANT]
> Comparer des enums avec `.equals()` ou `==` fonctionne tous les deux, mais `==` est préféré pour les enums car il est plus lisible et évite les NullPointerException.

---

## 1. Modifications structurelles — Passage aux Collections

L'objectif était de remplacer la gestion manuelle de tableaux par des `HashMap<String, T>`.

### Classe [Monde](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#14-161)
- **Attribut** : `Entite[] entites` → `Map<String, Entite> entites`
- **Méthodes modifiées** :
  - [getEntites()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#37-47) : retourne `Collection<Entite>` via `new ArrayList<>(this.entites.values())`
  - [getEntite(String nom)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#59-85) : utilise une boucle sur `keySet()` pour trouver l'entité (*refactoring possible* : un simple `return this.entites.get(nom)` suffirait)
  - [ajouter(Entite)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#127-160) : utilise `this.entites.put()` au lieu d'élargir un tableau dynamiquement
  - [toString()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#239-262) : parcours des clés via `entites.keySet()`

### Classe [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328)
- **Attribut** : `TableauDynamique objets` → `Map<String, Objet> objets`
- **Méthodes modifiées** :
  - Le constructeur peuple la `Map` via une boucle sur le varargs `Objet... objets`
  - [getObjets()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#131-141) : retourne `Collection<Objet>` avec copie défensive
  - [possede(Objet)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#172-183) / [possede(String)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#172-183) : `containsValue()` / `containsKey()`
  - [prendre()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#196-207), [deposer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#220-235) : utilisent `put()` et `remove()` avec vérifications préalables

### Classe [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#20-282)
- **Attributs** : `Map<String, Objet> tabObjet`, `Map<String, Vivant> tabVivant`, `Map<String, Porte> tabPorte`
- **Méthodes modifiées** :
  - [getObjets()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#131-141) / [getVivants()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#228-238) / [getPortes()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#278-281) : copie défensive via `new ArrayList<>(...values())`
  - [contientObjet(...)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#51-63) / [contientVivant(...)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#155-167) : `containsKey()` / `containsValue()`
  - [entrer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#205-227) / [sortir()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#168-191) / [deposer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#220-235) / [retirer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#108-130) : `put()` et `remove()`

---

## 2. Erreurs rencontrées — Passage aux Collections

### Erreur 1 — `NullPointerException` dans [retirer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#108-130) et [prendre()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#196-207)
- **Cause** : Avec les tableaux, chercher un élément absent levait `ArrayIndexOutOfBoundsException`. Avec une `Map`, [get()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Entite.java#83-91) ou `remove()` sur une clé absente retourne **`null`** silencieusement. L'appel suivant `obj.estDeplacable()` sur `null` déclenchait une NPE.
- **Solution** : Ajouter une vérification préalable explicite :

```java
// ✅ Après : vérification avant d'utiliser l'objet
if (!this.contientObjet(obj)) {
    throw new ObjetAbsentDeLaPieceException("L'objet " + obj.getNom() + " n'est pas dans la pièce");
}
return (Objet) this.tabObjet.remove(obj.getNom());
```

### Erreur 2 — `AssertionError` sur les exceptions métier
- **Cause** : Les tests attendaient `ObjetAbsentDeLaPieceException` ou `VivantAbsentDeLaPieceException`. Ces exceptions n'étaient plus levées car le `catch (ArrayIndexOutOfBoundsException)` n'était jamais atteint avec les `Map`.
- **Solution** : Remplacer le pattern try/catch par une vérification conditionnelle préalable (`if (!contient...)`) qui lève l'exception métier manuellement.

### Erreur 3 — `AssertionError` dans [test_getVivants](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPiece.java#199-205) (ordre non garanti)
- **Cause** : `HashMap.values()` ne garantit **aucun ordre**. Comparer avec `assertEquals` sur une collection ordonnée échouait aléatoirement.
- **Solution** : Utiliser `assertThat(..., containsInAnyOrder(...))` de la librairie **Hamcrest**, qui valide le contenu indépendamment de l'ordre :

```java
// ✅ Correct avec Hamcrest
assertThat("Test getVivants", p.getVivants(), containsInAnyOrder(viv1, viv2));
```

---

## 3. La classe [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81)

### Conception
[Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81) est un `ElementStructurel` qui implémente l'interface [Activable](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#7-16). Elle relie **deux pièces** et possède un état.

```
ElementStructurel  +  Activable
        ↑
      Porte
  - etat : Etat         (FERME par défaut)
  - pieceA : Piece
  - pieceB : Piece
```

### Constructeur — enregistrement automatique
Le constructeur enregistre la porte dans les **deux pièces** via [addPorte()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#264-269) :

```java
public Porte(String nom, Monde monde, Piece pieceA, Piece pieceB)
        throws NomDEntiteDejaUtiliseDansLeMondeException {
    super(nom, monde);        // s'enregistre dans le Monde (via Entite)
    this.etat = Etat.FERME;
    this.pieceA = pieceA;
    this.pieceB = pieceB;
    this.pieceA.addPorte(this);   // la porte connaît la pièce ET la pièce connaît la porte
    this.pieceB.addPorte(this);
}
```

---

## 4. Gestion des portes dans [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#20-282)

Trois méthodes et un attribut ajoutés :

```java
private Map<String, Porte> tabPorte = new HashMap<>();

protected void addPorte(Porte porte)    // appelée par le constructeur de Porte (package-protected)
public boolean aLaPorte(Porte porte)    // recherche par objet (containsValue)
public boolean aLaPorte(String nom)     // recherche par nom (containsKey)
public Collection<Porte> getPortes()    // copie défensive
```

> [!NOTE]
> [addPorte()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#264-269) est `protected` et non `public` : seul le constructeur de [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81) (dans le même package) doit pouvoir enregistrer une porte dans une pièce.

---

## 5. Gestion des portes dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328)

### [franchir(Porte porte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) — logique
1. Vérifie que la porte est dans `this.piece` → sinon `PorteInexistanteDansLaPieceException`
2. Vérifie que la porte est [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81) → sinon `PorteFermeException`
3. Récupère `porte.getPieceAutreCote(this.getPiece())` et appelle [setPiece()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#135-171)

### [franchir(String nomPorte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) — logique
Parcourt `this.piece.getPortes()` pour trouver la porte par son nom, puis délègue à [franchir(Porte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) :

```java
public void franchir(String nomPorte) throws PorteInexistanteDansLaPieceException, PorteFermeException {
    Porte porte = null;
    for (Porte p : this.piece.getPortes()) {
        if (p.getNom().equals(nomPorte)) { porte = p; break; }
    }
    if (porte == null) {
        throw new PorteInexistanteDansLaPieceException("La porte \"" + nomPorte + "\" n'est pas dans la pièce.");
    }
    this.franchir(porte);
}
```

> [!TIP]
> Cette méthode utilise la version par objet pour éviter la duplication de la logique de vérification. C'est le pattern **overloading avec délégation**.

### Modification de [setPiece()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#135-171)
La signature a été simplifiée : [setPiece()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#135-171) ne déclare plus `throws VivantAbsentDeLaPieceException`. Les appels internes à [sortir()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#168-191)/[entrer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#205-227) sont wrappés dans un `try/catch` qui relève une `Error` (ce qui ne doit logiquement jamais arriver) :

```java
// Avant
public void setPiece(Piece piece) throws VivantAbsentDeLaPieceException { ... }

// Après
public void setPiece(Piece piece) {
    ...
    try {
        if (anciennePiece != null && anciennePiece.contientVivant(this))
            anciennePiece.sortir(this);
        if (this.piece != null && !this.piece.contientVivant(this))
            this.piece.entrer(this);
    } catch (VivantAbsentDeLaPieceException e) {
        throw new Error("Pas de sens que setPiece lève VivantAbsentDeLaPieceException");
    }
}
```

---

## 6. Erreurs supplémentaires rencontrées — Porte et Tests

### Erreur 4 — Bug logique dans [getPieceAutreCote()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#35-43) *(bug de copier-coller)*
**Symptôme :** après [franchir()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265), le vivant restait dans la même pièce.

**Cause :** les deux branches retournaient `pieceB` :
```java
// ❌ Avant
public Piece getPieceAutreCote(Piece piece) {
    if (piece.equals(pieceA)) { return pieceB; }
    else                      { return pieceB; } // BUG : devait être pieceA
}
```
```java
// ✅ Après
public Piece getPieceAutreCote(Piece piece) {
    if (piece.equals(pieceA)) { return pieceB; }
    else                      { return pieceA; }
}
```

### Erreur 5 — Bug logique dans [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#11-12) *(double if consécutif)*
**Symptôme :** appeler [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#11-12) sur une porte FERMÉE la laissait FERMÉE.

**Cause :** deux [if](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/AutomaticRifle.java#9-32) indépendants s'enchaînaient — après être passé OUVERT, le 2e [if](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/AutomaticRifle.java#9-32) repassait immédiatement à FERMÉ :
```java
// ❌ Avant — la porte ne pouvait jamais s'ouvrir
public void activer() throws ActivationImpossibleException {
    if (this.getEtat().equals(Etat.FERME))  { this.etat = Etat.OUVERT; } // FERME → OUVERT
    if (this.getEtat().equals(Etat.OUVERT)) { this.etat = Etat.FERME;  } // OUVERT → FERME aussitôt !
}
```
```java
// ✅ Après — if / else if
public void activer() throws ActivationImpossibleException {
    if      (this.etat == Etat.FERME)  { this.etat = Etat.OUVERT; }
    else if (this.etat == Etat.OUVERT) { this.etat = Etat.FERME;  }
}
```

### Erreur 6 — [TestPorte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java) non compilable (6 erreurs)

Le fichier de test initial comportait 6 erreurs bloquantes :

| # | Problème | Correction |
|---|---------|------------|
| 1 | Variable `p` non déclarée (ligne 46) | `p` → [p1](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#104-108) |
| 2 | [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328) initialisé avec `p` (ligne 48) | `p` → [p1](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#104-108) |
| 3 | [Porte(...)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81) sans `new` (ligne 51) | ajouter `new` |
| 4 | `porte1.get_etat()` inexistant (ligne 57) | `get_etat()` → [getEtat()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#31-34) |
| 5 | Référence `piece1` inexistante (lignes 62, 67) | `piece1` → `porte1` |
| 6 | Classe nommée [TestPiece](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPiece.java#24-213) au lieu de [TestPorte](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#18-158) | renommer la classe |

**Solution :** réécriture complète de [TestPorte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java). Choix d'utiliser [Coffre](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/Coffre.java#10-42) et [PiedDeBiche](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/PiedDeBiche.java#10-46) (classes concrètes déjà dans le projet) au lieu de redéfinir des classes internes [ObjetConcret](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPiece.java#215-224), qui auraient créé un **conflit de noms** lors de la compilation groupée avec [TestPiece.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPiece.java) (même package).

---

## Bilan final TP05

| Section | Statut | Résultat |
|---------|--------|----------|
| 1. Migration `HashMap` (Monde, Vivant, Piece) | ✅ | Tests verts |
| 2. Retours `Collection` avec copie défensive | ✅ | Tests verts |
| 3. Classe [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81) créée ([Activable](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#7-16)) | ✅ | Compilée |
| 4. Gestion portes dans [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#20-282) ([addPorte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#264-269), [aLaPorte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#270-273), [getPortes](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#278-281)) | ✅ | Tests verts |
| 5. [franchir(Porte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) + [franchir(String)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328) | ✅ | Tests verts |
| Bug [getPieceAutreCote()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#35-43) corrigé | ✅ | Tests verts |
| Bug [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#11-12) (double if) corrigé | ✅ | Tests verts |
| [TestPorte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java) réécrit (15 tests) | ✅ | 15/15 verts |

**Tous les tests (`AllTests`) passent. Le projet est prêt pour le TP06.**
