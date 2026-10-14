# 📮 Réponse Forum — Kevin Schnitzer (02/07/2026)

> **Statut :** 🔵 Prête à poster
> **Thread :** Bug Z profondeur incorrecte — DDCS V3.3 + Estlcam
> **Lié à :** [[Journal_Evolution]] | [[Project_State]]

---

## ✉️ Réponse à poster

---

Merci Kevin pour les précisions.

**Sur la confusion Z+ / 1.5mm :**
Tu as raison de le pointer. Dans mon post j'ai mélangé deux choses :
- `Z+` est le nom de la colonne dans Estlcam (c'est leur notation pour la profondeur de passe, le "+" indique la direction de plongée)
- La valeur **1,5 mm** vient d'un tableau de référence général — mais dans ma configuration réelle, l'outil est réglé à **1,00 mm** comme le montre la capture. Désolé pour la confusion.

**Sur le test MDI :**
Je vais faire le test. Pour être sûr de bien le faire : je commande un déplacement de Z de -10mm depuis la position actuelle, et je mesure l'écart réel avec un pied à coulisse entre la position avant et après. C'est ça ?

**Sur l'écart de profondeur :**
Je n'ai pas encore mesuré précisément (c'est dans ma checklist). Ce que j'ai observé visuellement c'est que la fraise semblait couper moins profond que prévu, mais je dois mesurer pour te donner un chiffre réel.

Je reviens dès que j'ai le résultat du test MDI et la mesure au pied à coulisse.

---

## 📋 Actions à faire AVANT de répondre

- [ ] **Test MDI / Manuel sur le DDCS :**
  1. Mettre la fraise à une position Z quelconque
  2. Marquer la position (ou noter la valeur affichée)
  3. Commander un déplacement de **-10,00 mm** (vers le bas) en mode manuel/MDI
  4. **Mesurer** l'écart réel avec un pied à coulisse
  5. Comparer : est-ce que la machine a bien bougé de 10,00 mm ?

- [ ] **Mesure de l'écart Z sur la pièce usinée :**
  1. Reprendre la pièce MDF déjà usinée
  2. Mesurer la profondeur réelle de la poche/rainure au pied à coulisse
  3. Comparer avec la valeur programmée dans Estlcam
  4. Calculer l'écart : **profondeur programmée X mm → profondeur réelle Y mm**

- [ ] **Photo du résultat du test MDI** (si possible, pour joindre au post suivant)

---

## 🧠 Ce que ça va nous apprendre

| Résultat du test MDI | Interprétation |
|---|---|
| La machine bouge exactement 10mm | Steps/mm Z OK → problème vient d'ailleurs (zéro Z mal fait ?) |
| La machine bouge moins de 10mm | Steps/mm Z trop faible → recalibrer dans DDCS |
| La machine bouge plus de 10mm | Steps/mm Z trop élevé → recalibrer dans DDCS |
| La machine bouge de façon aléatoire | Confirme le faux contact hardware |

---

*→ Retour au tableau de bord : [[Project_State]]*
