# Guide TP06 — Projet Java Aventure

> **Prérequis :** TP05 terminé et tous les tests verts (AllTests passe).

---

## Section 1 — `Monde.genererNom(String prefixe)`

### Ce que ça fait
Génère un nom **unique** dans le monde en accolant un numéro aléatoire à un préfixe donné.

### Fichier à modifier
[Monde.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java)

### Implémentation
```java
public String genererNom(String prefixe) {
    String nom;
    do {
        nom = prefixe + (int)(Math.random() * Integer.MAX_VALUE);
    } while (getEntite(nom) != null);
    return nom;
}
```

> [!NOTE]
> La boucle `do/while` garantit qu'on génère **au moins une fois** avant de vérifier, ce qui est plus propre qu'un `while` avec une init.

### Test à écrire (dans [TestMonde.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/TestMonde.java))
```java
@Test
public void test_genererNom() {
    String nom = m1.genererNom("Hero");
    assertTrue("Le nom doit commencer par le préfixe", nom.startsWith("Hero"));
    assertNull("Le nom généré ne doit pas exister dans le monde", m1.getEntite(nom));
}
```

---

## Section 2 — Classes `Serrure` et `Cle`

### Architecture à comprendre

```
Objet (abstract)
 ├── Serrure   → non déplaçable, états : VERROUILLE / DEVERROUILLE
 │               crée et détient sa propre Cle
 └── Cle       → déplaçable, créée UNIQUEMENT par Serrure
```

> [!IMPORTANT]
> `Cle` ne doit **pas** avoir de constructeur public — seule `Serrure` peut en créer une. Passe le constructeur de `Cle` en package-private (pas de `public`).
> [Etat.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Etat.java) contient déjà `VERROUILLE` et `DEVERROUILLE` ✅

### 2a — Fichier `Cle.java`

Package : `fr.insarouen.iti.prog.aventure.elements.objets`

```java
public class Cle extends Objet {

    // constructeur package-private : seule Serrure peut instancier Cle
    Cle(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde);
    }

    @Override
    public boolean estDeplacable() {
        return true;
    }

    @Override
    public String toString() { ... }
}
```

### 2b — Fichier `Serrure.java`

Package : `fr.insarouen.iti.prog.aventure.elements.objets`

**Attributs :**
- `private Etat etat` → initialisé à `Etat.VERROUILLE`
- `private Cle cle` → initialisé à `null` (pas encore créée)

**Constructeurs :**
```java
public Serrure(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException { ... }
public Serrure(Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
    this("Serrure", monde); // nom par défaut
}
```

**Méthode `creerCle()`  ← la plus importante :**
```java
public Cle creerCle() throws NomDEntiteDejaUtiliseDansLeMondeException {
    if (this.cle != null) {
        return null; // déjà créée -> retourner null
    }
    // le nom de la clé est lié à la serrure pour pouvoir l'identifier après
    this.cle = new Cle(getMonde().genererNom("Cle"), getMonde());
    return this.cle;
}
```

**Méthode [activableAvec(Objet obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#44-47) :**
```java
@Override
public boolean activableAvec(Objet obj) {
    return obj.equals(this.cle); // seule la bonne clé fonctionne
}
```

**Méthode [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#48-57) :**
```java
@Override
public void activer() throws ActivationImpossibleException {
    throw new ActivationImpossibleException("La serrure ne s'active pas seule.");
}
```

**Méthode [activerAvec(Objet obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#13-14) :**
```java
@Override
public void activerAvec(Objet obj) throws ActivationImpossibleAvecObjetException, ActivationImpossibleException {
    if (!activableAvec(obj)) {
        throw new ActivationImpossibleAvecObjetException("Mauvaise clé ou objet incorrect.");
    }
    // la bonne clé déverrouille la serrure
    this.etat = Etat.DEVERROUILLE;
}
```

**Méthode utilitaire :**
```java
public Etat getEtat() { return this.etat; }
```

> [!TIP]
> `Serrure` extend [Objet](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#100-111) et implements [Activable](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#7-16) — même pattern que [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81).

### Tests `Serrure` & `Cle` à écrire

```java
// creerCle() retourne une Cle la 1ère fois
Cle c = serrure.creerCle();
assertNotNull(c);

// creerCle() retourne null la 2ème fois
assertNull(serrure.creerCle());

// Serrure verrouillée par défaut
assertEquals(Etat.VERROUILLE, serrure.getEtat());

// activableAvec la bonne clé -> true
assertTrue(serrure.activableAvec(c));

// activableAvec un autre objet -> false
assertFalse(serrure.activableAvec(autreObjet));

// activerAvec la bonne clé -> déverrouille
serrure.activerAvec(c);
assertEquals(Etat.DEVERROUILLE, serrure.getEtat());

// activer() seule -> exception
assertThrows(ActivationImpossibleException.class, () -> serrure.activer());
```

---

## Section 3 — Modification de [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#16-81) (gestion serrure)

### Fichier à modifier
[Porte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java)

### Nouveau constructeur (avec serrure)
```java
public Porte(String nom, Monde monde, Piece pieceA, Piece pieceB, Serrure serrure)
        throws NomDEntiteDejaUtiliseDansLeMondeException {
    this(nom, monde, pieceA, pieceB); // appelle le constructeur existant
    this.serrure = serrure;
    this.etat = Etat.FERME; // toujours FERME, serrure est distincte
}
```

Ajouter l'attribut : `private Serrure serrure = null;`

### Diagramme d'états de la Porte avec serrure

```
[FERME + serrure VERROUILLE]
      │
      │  activerAvec(PiedDeBiche)   → retire la serrure, passe à OUVERT
      │  activerAvec(bonneClé)      → déverrouille la serrure (serrure passe à DEVERROUILLE)
      ▼
[FERME + serrure DEVERROUILLE]
      │
      │  activer() / activerAvec(n'importe quoi)  → toggle normal OUVERT/FERME
      ▼
[OUVERT]  ←──────→  [FERME + serrure DEVERROUILLE]
```

### Modifier [activableAvec(Objet obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#44-47)
```java
@Override
public boolean activableAvec(Objet obj) {
    if (this.serrure == null) return false;
    // PiedDeBiche force la serrure
    if (obj instanceof PiedDeBiche) return true;
    // La bonne clé déverrouille la serrure
    return this.serrure.activableAvec(obj);
}
```

> [!IMPORTANT]
> Ajouter l'import : `import fr.insarouen.iti.prog.aventure.elements.objets.PiedDeBiche;`

### Modifier [activerAvec(Objet obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#13-14)
```java
@Override
public void activerAvec(Objet obj) throws ActivationImpossibleAvecObjetException, ActivationImpossibleException {
    if (!activableAvec(obj)) {
        throw new ActivationImpossibleAvecObjetException("Impossible d'activer la porte avec " + obj.getNom());
    }
    if (obj instanceof PiedDeBiche) {
        // Le pied de biche arrache la serrure → porte s'ouvre, serrure disparaît
        this.serrure = null;
        this.etat = Etat.OUVERT;
    } else {
        // Bonne clé → déverrouille la serrure, porte reste FERME
        this.serrure.activerAvec(obj);
    }
}
```

### Modifier [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#48-57)
```java
@Override
public void activer() throws ActivationImpossibleException {
    if (this.serrure != null && this.serrure.getEtat() == Etat.VERROUILLE) {
        throw new ActivationImpossibleException("La porte est verrouillée, utilisez la clé.");
    }
    // comportement normal toggle
    if (this.etat == Etat.FERME) {
        this.etat = Etat.OUVERT;
    } else if (this.etat == Etat.OUVERT) {
        this.etat = Etat.FERME;
    }
}
```

> [!CAUTION]
> Ne pas oublier de mettre à jour [franchir(Porte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#266-280) dans [Vivant.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java) si nécessaire — actuellement il vérifie `Etat.FERME` ce qui empêche de franchir une porte VERROUILLE aussi (comportement correct car une porte verrouillée est aussi fermée).

---

## Section 4 — Classe `Monstre`

### Fichier à créer
`src/fr/insarouen/iti/prog/aventure/elements/vivants/Monstre.java`

### Ce que fait `executer()`
1. Si le monstre est **mort** ([getPointVie() <= 0](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#78-88)) → ne fait rien
2. **Perd 1 point de vie** (attribut privé à décrémenter)
3. **Cherche une porte** dans sa pièce avec un stream (OUVERT ou FERME, pas VERROUILLE)
4. **Franchit la porte** (en l'ouvrant d'abord avec [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#48-57) si elle est FERME)
5. Si changement de pièce réussi → **échange tout l'inventaire** avec les objets de la nouvelle pièce

### Structure de `Monstre.java`

```java
package fr.insarouen.iti.prog.aventure.elements.vivants;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Etat;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.elements.structure.Porte;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.structure.VivantAbsentDeLaPieceException;

import java.util.Collection;
import java.util.Optional;

public class Monstre extends Vivant {

    public Monstre(String nom, Monde monde, int pointVie, int pointForce, Piece piece, Objet... objets)
            throws NomDEntiteDejaUtiliseDansLeMondeException, VivantAbsentDeLaPieceException {
        super(nom, monde, pointVie, pointForce, piece, objets);
    }

    public void executer() {
        // 1. Vérifier si vivant
        if (getPointVie() <= 0) return;

        // 2. Perdre 1 point de vie
        // ⚠️ PointVie est privé dans Vivant → il faudra soit l'exposer
        // (ajouter setPointVie ou un décrément), soit le rendre protected

        // 3. Chercher une porte franchissable avec stream
        Optional<Porte> porteOpt = getPiece().getPortes().stream()
            .filter(p -> p.getEtat() == Etat.OUVERT || p.getEtat() == Etat.FERME)
            .findFirst();

        if (porteOpt.isEmpty()) return;

        // 4. Ouvrir si nécessaire et franchir
        Porte porte = porteOpt.get();
        Piece anciennePiece = getPiece();
        try {
            if (porte.getEtat() == Etat.FERME) {
                porte.activer(); // FERME -> OUVERT
            }
            franchir(porte);
        } catch (Exception e) {
            return; // franchissement impossible, on abandonne
        }

        // 5. Échanger l'inventaire si changement de pièce réussi
        if (!getPiece().equals(anciennePiece)) {
            echangerInventaire(anciennePiece);
        }
    }

    private void echangerInventaire(Piece anciennePiece) {
        // Récupérer les objets du monstre et de la nouvelle pièce
        Collection<Objet> objetsMonastre = getObjets();   // copie défensive
        Collection<Objet> objetsPiece = getPiece().getObjets(); // copie défensive
        
        // Déposer les objets du monstre dans la nouvelle pièce
        for (Objet obj : objetsMonastre) {
            try { deposer(obj); } catch (Exception e) { /* ignore */ }
        }
        // Ramasser les objets de la nouvelle pièce
        for (Objet obj : objetsPiece) {
            try { prendre(obj); } catch (Exception e) { /* ignore */ }
        }
    }
}
```

> [!WARNING]
> **[PointVie](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#78-88) est `private` dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328)** — il faut soit le passer à `protected`, soit ajouter une méthode `protected void perdreVie(int points)` dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328). C'est la seule modification à faire sur [Vivant.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java).

### Modification à faire dans [Vivant.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java)
Ajouter cette méthode :
```java
protected void perdreVie(int points) {
    this.PointVie -= points;
}
```
Ou simplement passer `private int PointVie;` → `protected int PointVie;`.

### Tests `Monstre` à écrire

```java
@Test
public void test_executer_perteDeVie() {
    int vieBefore = monstre.getPointVie();
    monstre.executer();
    assertEquals("Monstre perd 1 PV par executer()", vieBefore - 1, monstre.getPointVie());
}

@Test
public void test_executer_changePiece() throws Exception {
    porte.activer(); // ouvrir d'abord si nécessaire, ou laisser Monstre le faire
    monstre.executer();
    // le monstre devrait avoir changé de pièce
    assertNotEquals("Monstre doit changer de pièce", p1, monstre.getPiece());
}

@Test
public void test_executer_echangeInventaire() throws Exception {
    // setup : un objet dans p2, un objet dans l'inventaire du monstre
    ...
    monstre.executer();
    assertTrue("Monstre possède l'objet de la pièce", monstre.possede(objetDeLaPiece));
    assertTrue("La pièce contient l'objet du monstre", p2.contientObjet(objetDuMonstre));
}

@Test
public void test_executer_mort() {
    Monstre monstreMort = new Monstre("Zombie", m, 0, 100, p1);
    monstreMort.executer();
    assertEquals("Monstre mort ne perd pas de PV", 0, monstreMort.getPointVie());
}
```

---

## Ordre d'implémentation recommandé

```
1. genererNom()     → Monde.java          (5 min)
   ↓ Make + Tests
2. Cle.java         → nouveau fichier      (10 min)
3. Serrure.java     → nouveau fichier      (15 min)
   ↓ Make + Tests
4. Porte.java       → ajouts + modifs      (20 min)
   ↓ Make + Tests
5. Vivant.java      → ajouter perdreVie()  (2 min)
6. Monstre.java     → nouveau fichier      (25 min)
   ↓ Make + AllTests
```

> [!TIP]
> **Règle d'or du TP :** `Compilation et Test !!!` après chaque section. Ne pas enchaîner plusieurs sections sans vérifier que les tests passent !
