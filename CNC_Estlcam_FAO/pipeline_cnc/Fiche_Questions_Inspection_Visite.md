# 🔍 Fiche Visite Technique — Questions & Vérifications sur Place

> **C'est la fiche la plus importante avant la visite.**  
> Objective : repartir avec TOUTES les infos nécessaires pour faire la configuration à distance ou sur place.  
> Lié à : [[Project_State]] | [[Fiche_Configuration_Technique]] | [[Fiche_Objectif_Ligne_Directrice]]

---

## 🎒 Ce qu'il faut emmener

- [x] Un carnet ou téléphone pour prendre des notes
- [x] Une règle ou mètre ruban (pour mesurer les courses X/Y/Z si pas dans la doc)
- [x] Un ordinateur portable avec **Estlcam installé** *(si possible)*
- [x] Une clé USB formatée FAT32 *(pour tester le transfert de fichier vers le DDCS)*
- [x] Ce fichier imprimé ou accessible sur téléphone 📱

---

## 🗣️ SECTION A — Questions à poser à l'ami (Besoins & Usage)

> Ces questions définissent comment configurer Estlcam et ce que tu dois paramétrer en priorité.

### Sur l'usage de la machine

- [ ] **Que vas-tu usiner principalement ?**
  - Bois tendre (pin, peuplier) / Bois dur (chêne, hêtre) / MDF / Contreplaqué / Acrylique / Aluminium ?
  - → *Impacte les vitesses de coupe à paramétrer*

- [ ] **Quels types de projets (maintenant et à l'avenir) ?**
  - Découpe 2D plates (contournage) ?
  - Creusement de poches (Pocketing) ?
  - Gravure de texte ou motifs ?
  - Relief 3D sculpté (vraie 3D avec courbes) ?
  - → *Détermine si on configure le mode 2.5D ou 3D dans Estlcam*

- [ ] **D'où viennent tes dessins / fichiers CAO ?**
  - SketchUp uniquement ? Illustrator, Inkscape, AutoCAD, Fusion 360 ?
  - Télécharges-tu des fichiers DXF/SVG sur internet ?
  - → *Permet de préparer la procédure d'import dans Estlcam*

- [ ] **Tu veux usiner de l'acrylique (verre synthétique) ?**
  - Si oui : confirmer que ce n'est PAS du vrai verre (risque de casse)
  - → *Nécessite une fraise 1 dent (single flute) spécifique*

### Sur les projets d'arc-en-ciel (contexte spécifique)

- [ ] Les arcs-en-ciel sont-ils **plats** (découpe de contours et poches) ou ont-ils **un relief bombé** (3D sculpté) ?
- [ ] Y a-t-il des **encoches ou poches pour LEDs** à creuser au dos ?
- [ ] Y aura-t-il des **trous ou perçages** (pour boutons, câbles, assemblages) ?

### Sur son niveau et ses attentes

- [ ] A-t-il déjà utilisé Estlcam ? Si oui, jusqu'où ?
- [ ] Quel niveau d'autonomie vise-t-il ? *(Tout faire seul / Juste lancer les programmes / Juste surveiller ?)*
- [ ] Veut-il un document de procédure (SOP) imprimable à garder dans l'atelier ?

---

## 🔌 SECTION B — Vérifications sur le Contrôleur DDCS V3

> Allume le DDCS et navigue dans les menus. Ne rien modifier — observer et noter.

### B1 — État général du DDCS

- [x] **Le DDCS démarre-t-il correctement ?** *(écran qui s'affiche, pas de message d'erreur)*
- [ ] **En quelle version firmware est-il ?** *(souvent indiqué au démarrage ou dans les infos système)*
- [ ] **Les unités sont-elles en mm ?** *(vérifier dans les paramètres — risque d'être en pouces)*
- [x] **Y a-t-il un logiciel PC fourni avec le DDCS ?** *(parfois un CD ou clé avec logiciel de config)* -> **Non (visiblement non)**

### B2 — Test de mouvement manuel (Jog)

- [x] **Axe X :** Bouger à droite → La machine va-t-elle bien à droite ? *(noter si inversé)*
- [x] **Axe Y :** Bouger vers l'avant → La machine va-t-elle bien vers l'avant ?
- [x] **Axe Z :** Bouger vers le haut (Z+) → La broche **monte**-t-elle bien ? ⚠️ *(très important — si inversé, la fraise plongera dans la table !)*
- [x] **Les 3 axes bougent-ils sans à-coups ni bruits anormaux ?**

### B3 — Calibration Steps/mm (CRITIQUE)

> Si mal calibré, même un G-code parfait donnera des pièces de mauvaises dimensions.

- [ ] **Les Steps/mm ont-ils été configurés par l'ingénieur ?**
- [ ] **Faire le test de précision :**
  1. Marquer un point de départ physiquement sur la table
  2. Demander au DDCS de déplacer l'axe X de **100 mm** exactement
  3. Mesurer avec une règle si le déplacement réel est bien de 100 mm
  4. Répéter pour Y et Z
  - [ ] X : mesuré = ________ mm (attendu = 100 mm)
  - [ ] Y : mesuré = ________ mm (attendu = 100 mm)
  - [ ] Z : mesuré = ________ mm (attendu = 100 mm)
  - → *Si écart > 0,5 mm, la calibration doit être refaite (noter les valeurs actuelles de Steps/mm)*

### B4 — Homing (Prise d'Origine Machine)

- [x] **Y a-t-il des fins de course (limit switches) installés ?** *(petits capteurs dans les coins de la machine)*
- [ ] **Le Homing fonctionne-t-il ?** *(lancer Home — la machine doit se caler dans un coin sans erreur)*  --> **Réponse : Sur la façade du DDCS, il y a un bouton "HOME" (souvent avec une icône de maison). Appuyez dessus, puis choisissez l'axe (X, Y ou Z) ou "All" pour faire l'origine.**
- [ ] **Où se positionne la machine après le Homing ?** *(coin avant-gauche ? arrière-droite ?)*
- [x] **Les soft limits (limites logicielles) sont-elles configurées ?** *(plage de travail définie dans DDCS) --> **Réponse : Oui, vous entendez un "bip" quand la machine atteint les limites, ce qui prouve que les Soft ou Hard Limits sont actives.**

---

## 🔧 SECTION C — Vérifications sur la Machine QueenBee Pro

### C1 — Dimensions et Course Utile

> Mesurer ou demander à l'ingénieur. Nécessaire pour configurer Estlcam.

- [ ] **Course maximale X (gauche→droite) :** ________ mm
- [ ] **Course maximale Y (avant→arrière) :** ________ mm
- [ ] **Course maximale Z (bas→haut) :** ________ mm
- [ ] **Épaisseur maximale de pièce pouvant être usinée :** ________ mm

### C2 — État mécanique (Inspection visuelle rapide)

- [x] **Les rails linéaires (HGR) sont-ils propres et légèrement huilés ?** *(pas de rouille ni poussière de coupe accumulée)*
- [x] **Les vis à billes (ballscrews) ont-elles du jeu ?** *(secouer légèrement le chariot — aucun jeu ne doit être perceptible)*
- [x] **L'équerrage est-il bon ?** *(poser une équerre sur la table — la broche doit être perpendiculaire à la table)*
- [x] **La broche tourne-t-elle rond ?** *(lancer broche à vide et écouter — vibrations = problème de concentricité)*
- [x] **Les fixations de table sont-elles présentes ?** *(vis en T, brides de serrage, système de fixation pièce)* -> **Pas spécialement, mais la plaque est fixée avec du bricolage.**

### C3 — Palpeur Z (Z-Probe)

- [x] **Y a-t-il un palpeur Z ?** *(bloc métallique avec câble + pince crocodile)* -> **Non, pas de palpeur trouvé.**
- [x] **Où est-il rangé ?** -> N/A
- [ ] **Une routine de palpage est-elle programmée dans le DDCS ?** -> N/A
- [ ] **Le tester** : poser le palpeur sur la table, poser la pince sur la fraise → le DDCS reconnaît-il le contact ? -> N/A

*(Note : Le boîtier branché que vous avez vu est le MPG Pendant (Manual Pulse Generator), il sert effectivement à piloter la machine manuellement à la place des touches du DDCS).*

### C4 — La Broche

- [ ] **Quelle est la marque et le modèle de la broche (spindle) ?**
- [ ] **Y a-t-il un variateur de fréquence (VFD / Inverter) ?** *(boîtier qui contrôle la vitesse de rotation)*
- [ ] **Comment contrôle-t-on la vitesse ?** *(potentiomètre manuel sur le VFD / commande depuis le DDCS ?)*
- [ ] **Quelle est la plage de vitesse broche ?** *(min / max en RPM)*
- [ ] **Quel type de pince (Collet) ?** *(ER11 / ER16 / ER20 — détermine les diamètres de fraises compatibles)*

---

## 🔩 SECTION D — Inventaire des Fraises (TRÈS IMPORTANT)

> Sans cette info, impossible de créer la bibliothèque d'outils dans Estlcam.

**Pour CHAQUE fraise disponible, noter ou photographier :**

| N° | Diamètre | Nombre de dents | Longueur de coupe | Matériau fraise | Type | Référence fabricant |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

**Types courants à identifier :**
- Fraise plate (End mill)
- Fraise boule (Ball nose) — pour la 3D
- Fraise V (V-bit / Engraving) — pour la gravure
- Fraise 1 dent (Single flute) — pour l'acrylique
- Fraise spirale montante / descendante *(Upcut / Downcut)*

> 💡 **Astuce :** Prends une photo de chaque fraise à côté d'une règle + photo de son emballage si disponible. C'est la méthode la plus rapide et la plus fiable.

---

## 💻 SECTION E — L'environnement Logiciel Existant

- [ ] **Estlcam est-il déjà installé ?** Sur quel PC ? Quelle version ?
- [ ] **A-t-il une licence Estlcam ?** *(le logiciel a une version d'essai gratuite mais la licence (~60€) débloque toutes les fonctions)*
- [ ] **SketchUp est-il installé ?** Quelle version ? *(SketchUp Make (gratuit) ou SketchUp Pro ?)*
- [ ] **Y a-t-il un PC dédié à la CNC ou utilise-t-il son PC personnel ?**
- [ ] **Le post-processeur DDCS a-t-il déjà été configuré ?** *(vérifier si un fichier de config existe déjà dans Estlcam)*
- [x] **Y a-t-il des fichiers G-code déjà générés à tester ?** oui

---

## 📸 SECTION F — Photos à Prendre Impérativement

- [ ] Vue générale de la machine QueenBee (face + profil)
- [ ] Boîtier DDCS V3 (face — affichage et boutons)
- [ ] Câblage arrière du DDCS *(drivers moteurs, fins de course, VFD)*
- [ ] Fins de course installés sur la machine *(si présents)*
- [ ] Broche + pince (collet) + type de montage
- [ ] Palpeur Z *(si présent)*
- [ ] Toutes les fraises disponibles *(avec emballage si possible)*
- [ ] Écran DDCS avec les paramètres Steps/mm affichés
- [ ] Matériaux disponibles dans l'atelier *(types de bois, etc.)*

---

## 📝 SECTION G — Notes Libres sur Place

> Espace pour noter tout ce qui n'est pas prévu dans les sections précédentes.

```
Notes : il utilise le bois medium (mdf)




```

---

## 🎯 Ce que tu DOIS repartir avec

- [ ] Photos de tout ce qui est dans la Section F
- [ ] Dimensions X/Y/Z de la machine (Section C1)
- [ ] Références de toutes les fraises (Section D)
- [ ] Résultat du test Steps/mm (Section B3)
- [ ] Confirmation que le DDCS démarre et bouge les 3 axes
- [ ] Réponses aux questions de la Section A (besoins de l'ami)

---

*→ Une fois la visite faite, revenir à [[Fiche_Configuration_Technique]] pour commencer la config.*  
*→ Mise à jour du tableau de bord : [[Project_State]]*
