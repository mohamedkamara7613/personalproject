# 🪟 Projet : Couvercle en Bois avec Fenêtre en Plexiglas

> **Statut :** 🔵 En cours de préparation et d'analyse
> **Fichiers de référence :** Anciens fichiers dans `fwdfichierscnc/old/`
> **Captures liées :** `trou plexi partie A-E12.png`, `trou plexi partie B-E12.png`

---

## 🎯 Objectif du projet

Fabriquer un couvercle de boîte en bois (MDF ou autre), comportant une ouverture rectangulaire dans laquelle viendra s'encastrer parfaitement une plaque de plexiglas transparent.

## ⚠️ Le défi technique principal : L'encastrement (Inlay)

Faire rentrer une pièce dure (plexi) dans une autre (bois) usinées toutes les deux à la CNC soulève deux problèmes classiques ("les soucis de marge") :

### 1. Le problème des coins arrondis
- **Le trou dans le bois (Découpe Intérieure) :** La fraise étant ronde (ex: 3.17 mm), elle ne peut pas usiner un coin intérieur parfaitement à angle droit (90°). Les coins du trou seront forcément **arrondis** (avec un rayon équivalent à la moitié de la fraise, soit ~1.58 mm).
- **Le plexiglas (Découpe Extérieure) :** Lors de la découpe de l'extérieur du rectangle en plexi, la fraise tourne autour, ce qui produit des coins extérieurs parfaitement **pointus** (à 90°).
- **Le problème :** Un carré pointu ne rentre pas dans un trou aux coins arrondis.
- **✅ La Solution :** Il est très fortement recommandé d'**arrondir les coins de votre dessin original** (bois ET plexi) avec un rayon supérieur à celui de la fraise (ex: rayon de 3 mm ou 5 mm). C'est beaucoup plus esthétique pour un couvercle visible. L'alternative est d'utiliser la fonction "Dégagement de coin" (Overcut/Dogbone) d'Estlcam sur le bois, mais cela fait de petits trous visibles dans les angles.

### 2. Le problème de la tolérance (Le Jeu)
- Si vous dessinez un trou de 100x100 mm et un plexi de 100x100 mm, le plexi sera **très difficile** à insérer (il risque de coincer ou de forcer).
- **✅ La Solution :** Il faut prévoir une marge (un jeu). Si la plaque de plexiglas est déjà prête, il faut **agrandir le trou dans le bois** d'environ **0.2 mm à 0.4 mm** par rapport aux dimensions exactes du plexiglas.
- **Dans Estlcam (La traduction est trompeuse !) :** 
  - Pour agrandir le trou : Mettez une valeur négative dans la case **"Finition..."** (ex: `-0.20 mm`). C'est cette case qui sert d'Allowance / Tolérance de jeu. La fraise "mangera" 0.2 mm de plus sur tout le contour.
  - Pour les angles pointus : Cliquez sur le bouton **"Surcoupe"** tout en bas (icône rouge avec un angle), puis cliquez sur les 4 coins intérieurs de votre dessin. Cela va créer le "Dégagement d'angle" (oreilles de Mickey). Il n'y a pas de chiffre à paramétrer pour ça, juste des clics !

---

## 📋 Plan d'action pour la suite

- [ ] **Étape 1 : Isoler le rectangle (Nettoyage du fichier)**
  - Ouvrir l'ancien fichier complexe dans Estlcam.
  - Sélectionner uniquement le rectangle qui nous intéresse.
  - Le copier (`Copier/Insérer`), ouvrir un "Nouveau" fichier vide, et le coller pour l'isoler des autres dessins.
  - L'enregistrer sous un nom clair (ex: `Test_Rectangle_Plexi_Seul`).
- [ ] **Étape 2 : Dessiner / Adapter le parcours**
  - Pièce A (Le Bois) : Configurer la découpe intérieure (trou).
  - *Rappel : Gérer le problème des coins arrondis (arrondir le dessin ou utiliser le dégagement "Overcut").*
- [ ] **Étape 3 : Paramétrer le Bois dans Estlcam**
  - Outil : ST2F-D3.1-L17
  - Fonction : **Découpe Intérieure** (ou Poche/Évider le centre)
  - **Marge (Jeu) :** Dans la case **Finition...**, tapez `-0.20 mm`
  - **Coins pointus :** Sélectionnez l'outil **Surcoupe** (en bas) et cliquez sur les 4 coins pour faire le dégagement.
  - Profondeur : Selon l'épaisseur voulue (ex: 6.00 mm).
- [ ] **Étape 4 : Usinage et Test d'emboîtement**
