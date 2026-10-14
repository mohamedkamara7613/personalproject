# 📓 Journal d'Évolution — Pipeline CNC

> Journal chronologique des décisions, découvertes et impasses.  
> Lié à : [[Project_State]] | [[Rules]]

---

## Format d'entrée

```
### YYYY-MM-DD — [Titre court]
**Contexte :** ...
**Décision/Découverte :** ...
**Impact :** ...
**Lié à :** [[Fiche_X]]
```

---

## Entrées

### 2026-07-02 — Consensus forum : Steps/mm axe Z non calibré

**Contexte :** Post forum publié le 2026-06-30. Trois experts ont répondu : Kevin Schnitzer, Jbaero, Jean-Pierre Tramunti.

**Découverte :** Consensus unanime → le paramètre **Steps/mm de l'axe Z** dans le DDCS est incorrect. C'est la cause racine probable de la profondeur incorrecte.

**Diagnostic recommandé par le forum :**
1. En mode manuel sur le DDCS, commander un déplacement de Z de 20mm
2. Mesurer la distance réelle au pied à coulisse
3. Calculer le nouveau Steps/mm = ancien × (commandé ÷ réel)
4. Modifier le paramètre dans le DDCS et re-tester

**Impact :** La calibration Steps/mm Z n'a jamais été vérifiée. C'est une étape de mise en service basique qui aurait dû être faite par l'ingénieur hardware.

**Prochaine action :** Faire le test de mesure avec pied à coulisse. Procédure dans [[Fiche_Calibration_Steps_Z]].

**Lié à :** [[Fiche_Calibration_Steps_Z]] | [[Fiche_Reponse_Forum_Kevin]] | [[Project_State]]

---

### 2026-06-30 — Premier usinage MDF : forme OK, profondeur Z incorrecte

**Contexte :** Après validation du test à vide, premier usinage réel effectué sur une plaque MDF. Zéro Z défini à la surface de la plaque (méthode papier). Fraise utilisée : ST2F-D3.1-L17.

**Découvertes :**
1. ✅ **Trajectoire XY correcte** — La forme prévue est bien suivie par la machine. Le post-processeur Mach3 et le G-code `.nc` fonctionnent.
2. ❌ **Profondeur Z incorrecte** — La profondeur d'usinage ne correspond pas à la valeur programmée dans Estlcam. Le parcours de fraise sur l'axe Z est anormal (profondeurs de passes incorrectes).
3. ⚠️ **Bug Z intermittent (hardware)** — Un comportement erratique de l'axe Z est observé de façon aléatoire (présent parfois, absent d'autres fois). Hypothèse principale : **faux contact électrique** (câblage ou connecteur du moteur Z ou des fins de course).

**Hypothèses à investiguer pour le problème de profondeur Z :**
- Le `Steps/mm` de l'axe Z n'est peut-être pas calibré correctement dans le DDCS (calibration hardware non confirmée).
- Le Z=0 pièce est peut-être mal défini (procédure à revérifier).
- Le Safe Z ou la profondeur de passe dans Estlcam est peut-être mal interprété.
- Le bug de faux contact peut amplifier ou simuler un décalage Z.

**Impact :** Phase 4 (premier usinage réel) partiellement validée. L'axe XY est opérationnel. L'axe Z doit être diagnostiqué avant tout usinage de précision.

**Prochaine action :** Poster sur un forum spécialisé (OpenBuilds / r/hobbycnc) pour diagnostic externe. Post rédigé le 2026-06-30.

**Lié à :** [[Project_State]] | [[Fiche_Configuration_Technique]] | [[Mode_Operatoire]]

---

### 2026-06-30 — Test à vide (Air Cutting) validé

**Contexte :** Exécution du test à vide sur le DDCS V3.3. Programme carré simple généré depuis Estlcam.

**Découverte :** Test globalement validé. La broche démarre, les axes bougent. Bug Z aléatoire déjà observé à cette étape.

**Impact :** Phase 3 (Air Cutting) validée. ✅

**Lié à :** [[Fiche_Configuration_Technique]] | [[Project_State]]

---

### 2026-06-21 — Initialisation du projet

**Contexte :** Premier cadrage du projet après discussion avec l'ami. L'ingénieur hardware a déjà câblé la QueenBee Pro + DDCS V3. Mon rôle = intégrateur FAO↔Machine.

**Décision :** Le périmètre est clair — pas de développement logiciel, uniquement configuration Estlcam + DDCS. Priorité à la visite technique pour collecter les informations manquantes.

**Impact :** Architecture Obsidian créée avec 3 fiches principales.

**Lié à :** [[Fiche_Objectif_Ligne_Directrice]] | [[Fiche_Questions_Inspection_Visite]] | [[Fiche_Configuration_Technique]]

---

*→ Ajouter une entrée après chaque session de travail significative.*
