# 🔍 Diagnostic Sécurisé : Bug de l'Axe Z (Sauts & Profondeur)

> **Problème :** L'axe Z monte/descend parfois de manière aléatoire. La profondeur d'usinage s'en retrouve totalement faussée.
> **Objectif :** Isoler la cause (mécanique, électrique ou logicielle) sans utiliser de fraise ni risquer de casser la machine.

---

## 🛠️ PISTE 1 : Le test du "Faux Contact" (Le plus probable)

Le câble de l'axe Z bouge beaucoup lors des déplacements de la machine. Un fil légèrement dénudé ou mal vissé crée des sauts aléatoires.

**Test à faire (Machine allumée) :**
1. Mettre le DDCS en mode **Continu** (Cont) avec une vitesse lente.
2. Déplacer l'axe Z de haut en bas avec les boutons Z+ / Z-.
3. Pendant que l'axe Z bouge, **triture et plie légèrement le câble noir de l'axe Z avec tes mains** (surtout au niveau des connecteurs près du moteur, et au niveau de la gaine articulée).
4. **Résultat :** Si le moteur broute, change de direction tout seul, ou s'arrête brusquement quand tu touches le câble → **Bingo**. C'est un fil mal serti ou cassé à l'intérieur de la gaine (souvent le fil "DIR").
5. **Solution :** Ouvrir les connecteurs de l'axe Z, revisser fermement les fils sur les dominos ou remplacer la portion de câble abîmée.

---

## ⚙️ PISTE 2 : Le point de blocage mécanique (Perte de pas)

Si l'axe Z force trop à un certain endroit (poussière, écrou trop serré), le moteur "saute des pas". La machine croit être descendue de 5mm, mais le moteur a bloqué et n'est descendu que de 2mm. La profondeur sera fausse.

**Test à faire (Machine éteinte) :**
1. Éteindre le boîtier électrique de la QueenBee.
2. Saisir la vis sans fin (la grande tige filetée) de l'axe Z avec les doigts.
3. La faire tourner manuellement sur toute sa longueur (de tout en haut à tout en bas).
4. **Résultat :** La rotation doit être fluide et régulière, avec la même résistance partout. S'il y a un point dur où ça bloque ou grince → L'axe Z s'enraye en plein travail.
5. **Solution :** Nettoyer la vis, la graisser (graisse au lithium), ou vérifier que le chariot n'est pas de travers.

---

## 💻 PISTE 3 : Le test de calibration pure (Le réglage Steps/mm)

Si l'axe Z bouge parfaitement sans jamais saccader ni s'inverser (pistes 1 et 2 validées), mais que la profondeur est systématiquement fausse, c'est le paramètre logiciel qui est mauvais.

**Test à faire (Test de l'air) :**
1. Machine allumée, sans mèche.
2. Placer un bloc de référence (ou mesurer avec un réglet la distance entre la pince et la table).
3. Aller sur le DDCS, se mettre en mode "STEP" ou "MDI".
4. Commander une descente de **Z = -20 mm**.
5. Remesurer la distance avec le réglet.
6. **Résultat :** Si la pince est descendue de 16 mm au lieu de 20 mm → Le paramètre **#36 (Steps/mm)** dans le DDCS est incorrect. 
7. **Solution :** Appliquer la formule de correction détaillée dans ton fichier `Fiche_Calibration_Steps_Z.md`.

---

> 🛑 **Règle de sécurité absolue :** Tant que l'Axe Z n'a pas passé ces 3 tests "à vide" de manière 100% fiable, ne **jamais** lancer d'usinage avec une fraise dans la matière.
