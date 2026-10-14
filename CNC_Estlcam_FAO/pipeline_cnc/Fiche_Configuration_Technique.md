# ⚙️ Fiche Configuration Technique — Estlcam + DDCS V3

> **Pré-requis :** Avoir complété la [[Fiche_Questions_Inspection_Visite]] sur place.  
> Lié à : [[Project_State]] | [[Fiche_Objectif_Ligne_Directrice]]  
> **Niveau :** Guide pas-à-pas — suit les étapes dans l'ordre

---

## ✅ Checklist de progression

- [ ] Étape 1 — Post-processeur configuré
- [ ] Étape 2 — Paramètres de sécurité (Safe Z) réglés
- [ ] Étape 3 — Bibliothèque d'outils créée
- [ ] Étape 4 — Premier test à vide (Air Cutting) validé
- [ ] Étape 5 — Premier usinage réel validé

---

## 📌 Étape 1 — Configurer le Post-Processeur dans Estlcam

> Le post-processeur dit à Estlcam dans quel "dialecte G-code" écrire le fichier pour que le DDCS le comprenne.

1. Ouvre **Estlcam**
2. Menu → **Configuration** → **Programmes CNC** (ou *CNC Programs*)
3. Onglet **Préréglages (Presets)** :
   - Sélectionne **Mach3** ✅ *(choix prioritaire, le plus compatible avec les contrôleurs autonomes comme le DDCS)*
   - Alternative si problème : **LinuxCNC**
4. Onglet **Paramètres (Settings)** :
   - **Extension de fichier :** `.nc` ou `.tap` *(le DDCS lit bien ces deux extensions)*
   - **Unités :** Millimètres ⚠️ *(vérifier que ce n'est pas en pouces)*

> 📝 **Note :** Après la visite, si tu as accès aux menus du DDCS, confirme qu'il est aussi réglé en mm.

je confirme le reglage en mm, la version c'est ddcs v3.3


---

## 📌 Étape 2 — Plan de Dégagement (Safe Z)

> Ce paramètre empêche la fraise de percuter les fixations ou la matière entre deux parcours.

1. **Configuration** → **Programmes CNC**
2. Paramètre : **Plan de dégagement** *(Clearance plane / Z-Safe)*
3. Valeur recommandée : **10 mm** *(minimum 5 mm)*
   - La fraise remontera toujours à +10 mm au-dessus du Z=0 pièce avant tout déplacement horizontal.

---

## 📌 Étape 3 — Créer la Bibliothèque d'Outils

> Tu dois renseigner chaque fraise disponible dans l'atelier. Récupère les infos avec [[Fiche_Questions_Inspection_Visite]].

### Comment trouver les bons paramètres de fraise ?

**Sources fiables (par ordre de priorité) :**
1. **L'étiquette ou la fiche du fabricant** de la fraise *(souvent livrée avec ou disponible sur le site)*
2. **Le site du fournisseur** (Sorotec, Precise Bits, Carbide 3D, Amana Tool) — cherche le modèle exact
3. **Tableaux de référence génériques** *(voir tableau ci-dessous)*
4. **Formules de calcul** : si tu connais le matériau, la vitesse broche et le diamètre fraise, tu peux calculer l'avance

### 📊 Tableau de référence — Paramètres de départ (Bois)

| Paramètre               | Fraise 3mm (bois tendre) | Fraise 6mm (bois tendre) | Fraise 6mm (bois dur) | Fraise 6mm (acrylique) |
| ----------------------- | ------------------------ | ------------------------ | --------------------- | ---------------------- |
| **Vitesse broche**      | 18 000 rpm               | 18 000 rpm               | 16 000 rpm            | 14 000 rpm             |
| **Avance XY (Feed)**    | 800 mm/min               | 1 200 mm/min             | 800 mm/min            | 1 000 mm/min           |
| **Plongée Z (Plunge)**  | 200 mm/min               | 400 mm/min               | 300 mm/min            | 300 mm/min             |
| **Profondeur de passe** | 1,5 mm                   | 2–3 mm                   | 1,5 mm                | 1 mm                   |

> ⚠️ Ces valeurs sont **conservatrices et sûres pour commencer**. Augmenter progressivement (par paliers de 10–15%) selon les résultats.

### Adaptation selon le matériau

| Matériau | Avance XY | Profondeur de passe | Conseil |
|---|---|---|---|
| **Mousse / MDF tendre** | +20% vs tableau | Max possible | Idéal pour les premiers tests |
| **Bois tendre (pin, peuplier)** | Valeurs du tableau | 2–3 mm | Référence de base |
| **Bois dur (chêne, hêtre)** | -20% vs tableau | 1–1,5 mm | Aller doucement |
| **Contreplaqué** | Valeurs du tableau | 2 mm | Attention aux noeuds |
| **Acrylique (Plexiglas)** | Valeurs du tableau | 1 mm | Fraise 1 dent (single flute) obligatoire |
| **Aluminium** | -50% vs tableau | 0,5 mm | Uniquement avec lubrification |

### Comment renseigner un outil dans Estlcam

Dans la liste d'outils d'Estlcam, pour **chaque fraise** :

| Champ | Valeur |
|---|---|
| **D (Diamètre)** | Diamètre exact en mm (ex: 3.175, 6.0) |
| **Z+ (Stepdown)** | Profondeur de passe par tour |
| **F(xy) (Feed rate)** | Avance horizontale en mm/min |
| **F(z) (Plunge rate)** | Vitesse de plongée verticale en mm/min |
| **Nom / Commentaire** | Ex: "Fraise 6mm 2 dents — Bois tendre" |

### 🧰 Outils configurés (Relevé sur place)

D'après la configuration actuelle sur place et nos recommandations, voici les outils renseignés dans Estlcam :

| No. | Nom | Ø (Diamètre) | Z+ (Passe) | a (Angle) | Fxy (Avance) | Fz (Plongée) | N (Rotation) |
|---|---|---|---|---|---|---|---|
| 1 | Exemple outil | 3,00mm | 1,00mm | 20,00° | 600mm/min | 300mm/min | 24000rpm |
| 2 | Nouvelle outil | 3,00mm | 1,00mm | 20,00° | 600mm/min | 300mm/min | 24000rpm |
| 3 | ST2F-D3.1-L17 (Bois) | 3,17mm | 1,50mm | 20,00° | 1000mm/min | 300mm/min | 18000rpm |

> 💡 **Analyse de cette configuration :** 
> - L'outil 3 correspond à votre fraise droite 2 dents, avec des paramètres optimisés pour le bois (copeaux corrects, pas de brûlure).
> - Le **Safe Z (Hauteur de dégagement)** est réglé sur **10 mm**.
> - Le post-processeur est réglé sur **Mach3 (en mm)** et l'extension de fichier est **.nc**.

---

## 📌 Exemple Pratique : Usinage du Test (Carré 48mm et Cercle central)

D'après votre capture d'écran, voici comment reproduire la pièce test (carré de 4,8 cm de côté avec un cercle au centre) dans une plaque de **12 mm d'épaisseur**, avec la fraise **ST2F-D3.1-L17** :

### 1. Préparation du dessin
- Dessinez le carré de 48 mm × 48 mm.
- Dessinez le cercle au centre (diamètre au choix).

### 2. Programmation Estlcam
*Sélectionnez l'outil n°3 (ST2F-D3.1-L17) dans la liste.*

**Pour le Cercle central (Poche / Ne traverse pas) :**
- Outil Estlcam : Cliquez sur **Découpe intérieure** (Inside).
- Cliquez sur la ligne du cercle.
- **Profondeur totale (Toolpath depth) :** Cliquez sur "Demander" et tapez une valeur inférieure à 12 mm (par exemple `5.00mm` ou `6.00mm`).
- **Évider le centre :** Dans la petite fenêtre en bas à droite, à côté de **Poche**, sélectionnez `Linéaire` ou `Parallèle`. Estlcam va calculer le parcours pour creuser tout l'intérieur du cercle à la profondeur indiquée, sans traverser la plaque.

**Pour le Carré (Découpe extérieure / Traverse la plaque) :**
- Outil Estlcam : Cliquez sur **Découpe extérieure** (Outside).
- Cliquez sur la ligne du carré.
- **Profondeur totale :** `12.2 mm` ou `12.5 mm`.
- **⚠️ TRES IMPORTANT : Attaches (Holding Tabs) :** Cliquez sur l'outil **Attaches** et placez-en au moins 2 à 4 sur le contour du carré. Cela empêchera la pièce de s'envoler ou de casser la fraise à la toute dernière passe.

### 3. Génération du G-Code
- Fichier → **Enregistrer Programme CNC** (Save CNC program).
- Nommez-le par exemple `Test_Carre_Cercle_12mm.nc` et placez-le sur la clé USB pour le DDCS.

---

## 📌 Étape 4 — Utilisation du DDCS V3 (Exécution G-code)

### Procédure complète pour lancer un programme

```
1. Allumer le DDCS V3
   └── Attendre l'écran d'accueil

2. Faire le HOMING (prise d'origine machine)
   └── Menu → Home (ou bouton dédié)
   └── La machine va se caler dans son coin de référence

3. Fixer la pièce à usiner sur la table

4. Installer la fraise dans la broche
   └── Serrer la pince correctement

5. Faire le ZÉRO PIÈCE (Work Zero)
   ├── Approcher manuellement la fraise de l'angle avant-gauche de la pièce.
   ├── **Pour mettre X à Zéro :** Appuyez sur `SHIFT` → `Y-` → `X+` → `Z-`
   ├── **Pour mettre Y à Zéro :** Appuyez sur `SHIFT` → `Y-` → `Y+` → `Z-`
   └── **Pour le Z=0 (Hauteur) :** 
       ├── Descendre la fraise très doucement jusqu'à effleurer la surface (utiliser une feuille de papier qui doit légèrement frotter).
       └── Appuyez sur `SHIFT` → `Y-` → `Z+` → `Z-` (Combinaison probable à confirmer pour le Z).

6. Insérer la clé USB contenant le fichier .nc

7. Menu → Charger programme (Load File / Open)
   └── Sélectionner le fichier .nc

8. Vérifier la trajectoire (si le DDCS le permet — aperçu graphique)

9. S'assurer que :
   ├── Le bouton E-Stop est accessible
   └── Personne n'est dans la zone de travail

10. Démarrer (Start/Cycle Start)
    └── Rester près de l'E-Stop pendant les premières minutes
```

---

## 📌 Étape 5 — Premier Test à Vide (Air Cutting)

> **Ne jamais faire le premier test directement sur une vraie pièce.** Toujours valider d'abord en "coupant l'air".

### Procédure

1. Créer un dessin test simple dans Estlcam : **carré 10 cm × 10 cm**
2. Générer le G-code → Fichier `.nc` sur clé USB
3. Sur le DDCS : positionner le Z=0 à **5 cm au-dessus de la table** (pas sur la pièce)
4. Lancer le programme
5. Observer :
   - [ ] La broche démarre-t-elle ?
   - [ ] Les axes bougent-ils dans le bon sens ?
   - [ ] Le carré dessiné en l'air semble-t-il proportionnel (10x10) ?
   - [ ] Aucun bruit étrange ni comportement erratique ?

✅ **Si tout est OK → passer à l'usinage réel dans du bois tendre (MDF ou pin)**

---

## 🚨 Erreurs fréquentes et comment les éviter

| Problème | Cause probable | Solution |
|---|---|---|
| Machine se bloque au démarrage | Fins de course non câblés ou en erreur | Vérifier câblage + paramètre "Home direction" dans DDCS |
| Pièce de mauvaise taille | Steps/mm mal calibrés | Recalibrer les pas moteurs dans DDCS |
| Fraise plonge trop profond | Z=0 mal fait ou Safe Z insuffisant | Refaire le zéro Z avec précaution |
| Moteurs font du bruit sans bouger | Courant driver trop faible | Vérifier réglage potentiomètre sur les drivers |
| Plastique acrylique fond | Mauvaise fraise ou avance trop lente | Fraise 1 dent (single flute) + augmenter la vitesse d'avance |

---

*→ Retour au tableau de bord : [[Project_State]]*
