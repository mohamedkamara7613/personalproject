# 🧭 Ligne Directrice — Vision Globale du Projet

> *À relire chaque fois que tu te sens perdu ou que tu perds le fil.*  
> Lié à : [[Project_State]] | [[Fiche_Configuration_Technique]] | [[Fiche_Questions_Inspection_Visite]]

---

## 🎯 L'objectif en une phrase

**Faire en sorte que ton ami puisse, de manière autonome, passer d'un dessin SketchUp à une pièce usinée sur sa QueenBee Pro, en utilisant Estlcam et le DDCS V3.**

---

## 🗺️ Le Pipeline Complet (la "chaîne de production")

```
[SketchUp]  →  [Estlcam]  →  [Clé USB]  →  [DDCS V3]  →  [QueenBee Pro]
  (CAO)         (FAO)        (transfert)    (contrôleur)     (machine)
  Dessin      G-code .nc     Fichier .nc    Lit & exécute    Usine la pièce
```

**Ton rôle :** Tu n'es pas développeur sur ce projet. Tu es **intégrateur et configurateur**. Tu fais le pont entre les logiciels et la machine. Aucune ligne de code à écrire.

---

## 🧩 Ce que tu dois livrer au final

1. **Estlcam correctement configuré** (post-processeur Mach3/LinuxCNC, bibliothèque d'outils)
2. **Un flux de travail validé** (un fichier G-code tourne sans erreur sur le DDCS)
3. **Un Mode Opératoire Standard (SOP)** — un document simple (PDF ou carnet) que ton ami peut suivre seul, avec captures d'écran

---

## 🏗️ Les 3 blocs que tu dois maîtriser

### Bloc A — Estlcam (FAO)
- Importer un fichier DXF (2.5D) ou STL (3D depuis SketchUp)
- Sélectionner un parcours d'outil (contournage, poche, gravure)
- Renseigner les paramètres de fraise
- Générer et exporter le G-code en `.nc` ou `.tap`

### Bloc B — DDCS V3 (Contrôleur)
- Naviguer dans les menus
- Faire le "Homing" (prise d'origine machine)
- Faire le zéro pièce (X=0, Y=0, Z=0 sur la pièce à usiner)
- Charger et lancer un programme depuis la clé USB

### Bloc C — QueenBee Pro (Machine)
- Connaître ses courses maximales (X, Y, Z)
- Savoir que les rails linéaires + vis à billes lui donnent une bonne rigidité
- Comprendre ses limites matériaux (bois, plastique, alu avec précautions)

---

## 💡 Contexte important à ne pas oublier

- L'ami dessine des **arcs-en-ciel** (projets décoratifs/artistiques) — il veut ajouter des **LEDs** et éventuellement usiner de l'**acrylique** (pas du vrai verre)
- Il veut être **autonome** une fois la configuration faite
- L'ingénieur hardware a déjà câblé et potentiellement calibré la machine — ton travail commence *là où il s'est arrêté*
- La difficulté technique est **6/10 en logique CNC**, et **1/10 en programmation pure**

---

## 📏 Définition du succès

> ✅ **Mission accomplie quand :** ton ami peut, seul, créer un parcours dans Estlcam, générer un `.nc`, le mettre sur clé USB, lancer le DDCS, et obtenir une pièce usinée conforme à son dessin.

---

## 🔗 Liens utiles à explorer

- Documentation officielle Estlcam : https://www.estlcam.de/
- Forum QueenBee / OpenBuilds : https://openbuilds.com/
- Documentation DDCS V3 (chercher "DDCS V3 manual PDF" — souvent en anglais + chinois)
- Fichiers de référence des paramètres fraises bois : voir [[Fiche_Configuration_Technique]]
