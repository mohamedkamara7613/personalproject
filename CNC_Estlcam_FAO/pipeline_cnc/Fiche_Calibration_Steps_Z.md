# 🔧 Fiche Calibration Steps/mm — Axe Z (DDCS V3.3)

> **Statut :** 🔴 ACTION REQUISE — diagnostic confirmé par 3 experts forum
> **Consensus forum (02/07/2026) :** Kevin Schnitzer + Jbaero + Jean-Pierre Tramunti
> **Lié à :** [[Project_State]] | [[Journal_Evolution]] | [[Fiche_Reponse_Forum_Kevin]]

---

## 🧠 Diagnostic confirmé : Steps/mm de l'axe Z incorrect

Les 3 experts du forum pointent vers la **même cause** :

> *"Le pas de l'axe n'est pas correct"* — Jean-Pierre Tramunti
> *"Fais un test de contrôle avec calibrage de l'axe Z et contrôle la distance"* — Jean-Pierre
> *"Fais un déplacement de 1mm et vérifie qu'elle a bien bougé d'1mm"* — Kevin Schnitzer
> *"Regarde le delta, certainement un réglage dans les paramètres"* — Jbaero

**Steps/mm** = le paramètre qui dit au DDCS "combien de pas moteur = 1 mm de déplacement réel".
Si ce chiffre est faux → la profondeur sera systématiquement incorrecte.

---

## 📋 Procédure complète — Test + Calibration

### ÉTAPE 1 — Faire le test de mesure

**Matériel nécessaire :** un pied à coulisse (ou une règle très précise)

1. Allumer le DDCS, ne pas faire le homing
2. En mode **Jog (manuel)**, approcher la fraise près de la surface de la table
3. Marquer la position actuelle de Z sur l'afficheur DDCS (ex: Z = 50.000)
4. Poser une feuille de papier sur la table — faire toucher la fraise (Z=0 approximatif)
5. Commander un déplacement de **Z = -20,00 mm** (vers le bas, mais laisser de la marge)
   - Mieux : remonter Z de +20mm depuis une position fixe, et mesurer l'écart
6. **Mesurer la distance réelle** parcourue avec le pied à coulisse

**Exemple de résultats :**
- Commandé : 20,00 mm → Mesuré : 20,00 mm → ✅ Steps/mm correct
- Commandé : 20,00 mm → Mesuré : 10,00 mm → ❌ Steps/mm = moitié de ce qu'il faut
- Commandé : 20,00 mm → Mesuré : 5,00 mm → ❌ Steps/mm = ¼ de ce qu'il faut
- Commandé : 20,00 mm → Mesuré : 40,00 mm → ❌ Steps/mm = double de ce qu'il faut

---

### ÉTAPE 2 — Trouver le paramètre Steps/mm dans le DDCS V3.3

Sur le DDCS V3.3 :

1. Appuyer sur **Param Page** (ou Menu → Paramètres)
2. Chercher le paramètre lié à l'axe Z — il s'appelle souvent :
   - **Z Pulse Equivalent** (équivalent impulsion Z)
   - ou **Steps/mm Z**
   - Paramètre numéro autour de **P22 ou P25** selon la version firmware

> **Conseil :** Photographier la valeur actuelle AVANT de la modifier.

**Valeur actuelle de Steps/mm Z :** `__________` *(à noter sur place)*

---

### ÉTAPE 3 — Calculer la valeur correcte

Si le test donne un écart :

```
Nouveau Steps/mm = Ancien Steps/mm × (Distance commandée ÷ Distance réelle mesurée)
```

**Exemples :**
| Commandé | Mesuré | Formule | Nouveau Steps/mm (si actuel = 200) |
|---|---|---|---|
| 20 mm | 10 mm | 200 × (20 ÷ 10) | **400** |
| 20 mm | 5 mm | 200 × (20 ÷ 5) | **800** |
| 20 mm | 40 mm | 200 × (20 ÷ 40) | **100** |
| 20 mm | 20 mm | 200 × (20 ÷ 20) | **200** ← correct |

---

### ÉTAPE 4 — Modifier la valeur dans le DDCS et re-tester

1. Aller dans les paramètres DDCS → trouver Steps/mm Z
2. Entrer la **nouvelle valeur calculée**
3. Sauvegarder / confirmer
4. **Refaire le test de mesure** (commande 20mm → mesurer) pour vérifier
5. Répéter si nécessaire jusqu'à ce que la mesure corresponde exactement

---

## ✉️ Réponse à poster sur le forum (après avoir fait le test)

```
Merci à tous les trois — Kevin, Jbaero, Jean-Pierre — vous pointez tous vers la même chose :
le Steps/mm de l'axe Z.

J'ai fait le test :
- Déplacement commandé : 20 mm
- Distance réelle mesurée au pied à coulisse : X mm
- Écart : Y mm

La valeur Steps/mm Z actuelle dans le DDCS est : ___
La valeur corrigée calculée est : ___

Je vais modifier le paramètre et refaire le test. Je reviens avec le résultat.
```

*(Compléter X, Y et les valeurs Steps/mm avant de poster)*

---

## 📝 À noter dans [[Journal_Evolution]] après le test

Format :
```
### 2026-07-XX — Calibration Steps/mm axe Z
Contexte : ...
Valeur avant : ___ steps/mm
Test : commandé 20mm / mesuré ___ mm
Valeur après : ___ steps/mm
Re-test : commandé 20mm / mesuré ___ mm → ✅/❌
```

---

*→ Retour au tableau de bord : [[Project_State]]*
