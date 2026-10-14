# Rapport d'Avancement — Projet Java Aventure (TP05 & TP06)

> **Mis à jour :** 17 mars 2026

---

## 1. Architecture actuelle du projet

```
src/fr/insarouen/iti/prog/aventure/
├── Monde.java                          ✅ + genererNom() ajouté
├── exceptions...                       ✅
└── elements/
    ├── Entite.java / Etat.java / Activable.java  ✅
    ├── objets/
    │   ├── Objet.java / Coffre.java / PiedDeBiche.java / AutomaticRifle.java  ✅
    │   └── serrurerie/                 ← nouveau package TP06
    │       ├── Cle.java                ⚠️ constructeur public (devrait être package-private)
    │       └── Serrure.java            ✅ logique OK
    ├── structure/
    │   ├── Piece.java                  ✅
    │   └── Porte.java                  ⚠️ activerAvec(PiedDeBiche) ne retire pas la serrure
    └── vivants/
        └── Vivant.java                 ✅ franchir() implémenté
```

---

## 2. TP05 — État final ✅ TERMINÉ

| Section | Statut |
|---------|--------|
| Migration `HashMap` (Monde, Vivant, Piece) | ✅ |
| Retours `Collection<T>` avec copie défensive | ✅ |
| Classe [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#20-110) créée | ✅ |
| Gestion portes dans [Piece](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Piece.java#20-282) | ✅ |
| [franchir(Porte)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) + [franchir(String)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#250-265) dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328) | ✅ |
| [TestPorte.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java) réécrit (15 tests) | ✅ |

**Tous les tests TP05 passent.**

---

## 3. TP06 — État d'avancement

### Section 1 — `Monde.genererNom()` ✅ FAIT

```java
public String genererNom(String prefixe) {
    String nom = null;
    do {
        nom = prefixe + (int)(Math.random() * Integer.MAX_VALUE);
    } while (this.getEntite(nom) != null);
    return nom;
}
```

### Section 2 — Classes [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92) & [Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#12-34) ✅ FAIT (avec réserves)

Créées dans un **nouveau package** `elements.objets.serrurerie`.

**[Serrure.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java)** — logique correcte :
- États : `VERROUILLE` (défaut) / `DEVERROUILLE`
- [activableAvec(obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#39-47) → vérifie si `obj.equals(this.cle)`
- [activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#66-80) → lève toujours `ActivationImpossibleException` ✅
- [activerAvec(obj)](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#13-14) → toggle VERROUILLE ↔ DEVERROUILLE avec la bonne clé ✅
- [creerCle()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#82-91) → crée via [genererNom("Cle_")](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#162-169), retourne `null` si déjà créée ✅
- Constructeur sans nom utilise [genererNom("Monde_")](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/Monde.java#162-169) ✅

**[Cle.java](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java)** — fonctionnelle mais :

> [!WARNING]
> Le constructeur de [Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#12-34) est `public` alors qu'il devrait être **package-private** (pas de modificateur, ou au moins `protected`) pour que seule [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92) puisse instancier une [Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#12-34). Si le prof teste ça, `new Cle(...)` ne devrait pas compiler depuis l'extérieur du package.
> **Correction si ça pose problème :** retirer le `public` devant le constructeur.

### Section 3 — Modification de [Porte](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#20-110) ⚠️ PARTIELLEMENT FAIT

Deux constructeurs ajoutés ✅ :
```java
// Sans serrure (existant)
Porte(String nom, Monde monde, Piece pieceA, Piece pieceB)
// Avec serrure (nouveau)
Porte(String nom, Monde monde, Serrure serrure, Piece pieceA, Piece pieceB)
```

[activableAvec()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#39-47) ✅ : `false` si pas de serrure, `true` pour [PiedDeBiche](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/PiedDeBiche.java#10-46), délègue à `serrure.activableAvec()` pour la clé.

[activer()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/structure/Porte.java#66-80) ✅ : lève exception si serrure VERROUILLÉE, sinon toggle normal.

**Bug potentiel dans [activerAvec()](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/Activable.java#13-14) avec [PiedDeBiche](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/PiedDeBiche.java#10-46) :**

```java
// Code actuel
else if(obj instanceof PiedDeBiche) {
    this.etat = Etat.OUVERT;  // ⚠️ la serrure n'est pas retirée (this.serrure = null) 
}
```

> [!WARNING]
> D'après le TP06 : avec un [PiedDeBiche](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/PiedDeBiche.java#10-46), la serrure **doit être retirée** de la porte (`this.serrure = null`) ET la porte passe à [OUVERT](file:///home/mkamara/Bureau/repos/java_aventure/codes/srctest/fr/insarouen/iti/prog/aventure/elements/struture/TestPorte.java#76-81). Si ce n'est pas fait, la porte sera encore considérée comme ayant une serrure après le coup de pied de biche.
> **Correction :** ajouter `this.serrure = null;` avant `this.etat = Etat.OUVERT;`

### Section 4 — Classe `Monstre` ❌ NON FAIT

La classe `Monstre` avec `executer()` n'est pas encore créée.

---

## 4. Workflow tests — Situation actuelle

> [!IMPORTANT]
> Le prof fournit des binaires de tests (`.class`) compilés dans [testsUnitaires.zip](file:///home/mkamara/Bureau/repos/java_aventure/testsUnitaires.zip). Pour les utiliser :
> - **Ne pas recompiler** les tests (`make run-tests-prof` au lieu de `make run-tests`)
> - `run-tests-prof` = `make build` (compile seulement les sources) + exécution des tests profs déjà en `classestest`
> - Si tu recompiles avec `make` ou `make run-tests`, tes tests remplacent les binaires du prof → il faut recopier depuis le zip.
>
> **Pensée à garder :** toujours utiliser `make run-tests-prof` pour valider avant de rendre.

---

## 5. Ce qui reste à faire

### Corrections à apporter

- [ ] **`Porte.activerAvec(PiedDeBiche)`** → ajouter `this.serrure = null;` avant `this.etat = Etat.OUVERT;`
- [ ] **[Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#12-34) constructeur** → envisager de retirer `public` si le prof teste l'encapsulation

### TP06 — Reste à implémenter

- [ ] Créer `Monstre.java` dans `elements/vivants/`
  - `executer()` : perd 1 PV, cherche porte (stream), franchit, échange inventaire
  - Nécessite d'exposer [PointVie](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#78-88) dans [Vivant](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/vivants/Vivant.java#26-328) (passer à `protected` ou ajouter `perdreVie()`)
- [ ] Tests unitaires pour [Serrure](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Serrure.java#19-92), [Cle](file:///home/mkamara/Bureau/repos/java_aventure/codes/src/fr/insarouen/iti/prog/aventure/elements/objets/serrurerie/Cle.java#12-34), `Porte+serrure`, `Monstre`
- [ ] **Valider avec `make run-tests-prof`**
