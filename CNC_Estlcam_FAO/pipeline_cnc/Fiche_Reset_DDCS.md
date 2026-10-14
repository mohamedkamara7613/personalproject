# 🔄 Fiche Réinitialisation DDCS — Version & Options Reset

> **Statut :** 📚 Documentation technique — basée sur le manuel officiel DS_DDCSV3.1.pdf (44 pages)
> **Date :** 2026-07-07
> **Lié à :** [[Project_State]] | [[Fiche_Calibration_Steps_Z]] | [[Journal_Evolution]]

---

## 1. Version réelle du DDCS

| Champ | Valeur |
|---|---|
| **Nom affiché au démarrage** | **DDCS4 V3.1** |
| **Fabricant** | Digital Dream Numerical Technology Co., Ltd |
| **Type** | 4 Axis Motion Controller |
| **Architecture** | ARM9 (interface) + FPGA (algorithme) |
| **OS interne** | Linux |
| **Écran** | 5 pouces TFT, 480×272 pixels |
| **Touches** | 17 touches physiques |
| **Source** | Photo écran de démarrage + manuel DS_DDCSV3.1.pdf |

> ⚠️ **Correction importante :** L'appareil était référencé "DDCS V3.3" dans les fiches précédentes. La photo de l'écran de démarrage confirme **DDCS4 V3.1**. Toutes les références futures doivent utiliser cette dénomination correcte.

---

## 2. Problèmes observés sur la machine

Les problèmes remontés sont les suivants :

| Problème | Fréquence | Impact |
|---|---|---|
| Bouton SELECT qui ne répond plus | Intermittent | Bloquant : impossible de naviguer dans les menus |
| Navigation dans les fichiers USB difficile | Régulier | Gênant : chargement de fichier compliqué |
| Boutons de commandes qui ne fonctionnent pas | Intermittent | Bloquant : impossible de piloter les axes |

---

## 3. Est-ce qu'une réinitialisation est possible ?

### Réponse courte : **Oui, mais de deux façons très différentes.**

---

### Option A — Réinitialisation des paramètres uniquement (RECOMMANDÉE)

**Principe :** Recharger le fichier de configuration par défaut (`setting.set`) depuis une clé USB. Cela remet tous les paramètres machine à leurs valeurs d'usine.

**Ce qui est réinitialisé :**
- ✅ Tous les paramètres moteur (#33, #34, #35, #36... Steps/mm, accélérations...)
- ✅ Tous les paramètres de broche (#98, #220, #221...)
- ✅ Tous les paramètres IO, limites, home (#400 à #415, #52 à #86...)
- ✅ Les paramètres d'affichage, langue, accès (#1, #2, #499...)
- ✅ Les coordonnées de travail G54~G59

**Ce qui N'EST PAS réinitialisé :**
- ❌ Le firmware lui-même (le programme interne)
- ❌ Les problèmes matériels (touches, câblage)
- ❌ Les fichiers G-code sur la clé USB

**Procédure (manuel §3.4.1 p.34) :**
1. Télécharger ou créer un fichier `setting.set` avec les valeurs par défaut
2. Copier ce fichier à la **racine** de la clé USB
3. Insérer la clé USB dans le DDCS
4. Appuyer sur RESET jusqu'à afficher **READY**
5. Aller dans **File Page** (touche PAGE R)
6. Sélectionner le fichier `setting.set`
7. Appuyer sur ENTER — le contrôleur passe en RESET clignotant → c'est bon
8. Reprendre la configuration depuis zéro (Steps/mm, etc.)

> ⚠️ **Important (manuel §3.3.1 p.22) :** Si le fichier `setting.set` est dans le dossier INSTALL (pour firmware), il sera chargé comme une mise à jour et écrasera aussi les paramètres courants. Ne pas confondre les deux.

---

### Option B — Mise à jour du firmware (Réinitialisation complète)

**Principe :** Réinstaller le firmware complet depuis une clé USB. Efface et réécrit le programme interne du contrôleur.

**Ce qui est réinitialisé :**
- ✅ Le programme interne (firmware) → version remise à zéro
- ✅ Tous les paramètres (si le fichier `setting.set` est inclus dans l'install)

**Ce qui N'EST PAS résolu :**
- ❌ Les problèmes matériels (boutons physiques défectueux, câblage)
- ❌ Un écran cassé ou des touches mécaniquement défaillantes

**Procédure (manuel §3.5 p.40) :**
1. Télécharger la dernière version du firmware depuis `www.ddcnc.com`
2. Décompresser dans un dossier `INSTALL/` à la **racine** de la clé USB
3. **Éteindre** le DDCS, attendre 10 secondes
4. Insérer la clé USB **avant** de rallumer
5. Rallumer → le contrôleur détecte et lance la mise à jour automatiquement
6. Attendre ~30 secondes sans toucher à rien
7. Après redémarrage, la nouvelle version apparaît sur l'écran principal

> ⚠️ **Avertissement critique (manuel §3.5) :** Si le fichier `setting.set` est présent dans le dossier INSTALL, **tous vos paramètres seront effacés**. Pour conserver vos paramètres, supprimer `setting.set` du dossier INSTALL avant de lancer la mise à jour.

> ⚠️ **Avertissement structure :** Le dossier doit s'appeler exactement `INSTALL` (pas `install`, pas `Install`). Un sous-dossier ne fonctionne pas. La clé USB doit contenir exactement : `INSTALL/` à la racine.

---

## 4. Analyse objective : est-ce que le reset va résoudre les problèmes ?

### 🔴 Problème 1 : Bouton SELECT qui ne fonctionne plus

**Cause probable :** Défaut matériel (touche physique usée, contact oxydé, ou membrane tactile défaillante).

**Est-ce que le reset résout ça ?** → **NON.**

Un reset logiciel/firmware ne peut pas réparer un bouton physiquement défaillant. Si la touche est mécaniquement morte, la seule solution est de :
- Contacter Digital Dream pour remplacement
- Ou trouver un contournement fonctionnel (utiliser d'autres touches)

> Note du manuel : La touche SELECT (A+) sert à valider une sélection. Si elle ne fonctionne plus, certaines opérations sont impossibles depuis le panneau. Il faut vérifier si l'option peut être faite via le fichier `setting.set` à la place.

---

### 🟡 Problème 2 : Navigation fichiers USB difficile

**Cause probable :** Peut être logicielle (bug firmware) **ou** matérielle (touches Y+/Y- qui répondent mal).

**Est-ce que le reset résout ça ?** → **PEUT-ÊTRE.**

- Si c'est un bug firmware → une mise à jour (Option B) peut corriger
- Si c'est les touches Y+/Y- qui sont physiquement en cause → non

**Test à faire :** Essayer de naviguer avec une clé USB neuve/reformatée en FAT32. Un bug de compatibilité USB peut causer des lenteurs de navigation.

---

### 🟡 Problème 3 : Boutons de commandes qui ne fonctionnent pas

**Cause probable :** Peut être logicielle (état RESET non résolu, mode incorrect) **ou** matérielle.

**Est-ce que le reset résout ça ?** → **DÉPEND.**

- Si le DDCS est en état RESET clignotant → appuyer sur RESET pour repasser en READY, les touches redeviennent actives (c'est normal)
- Si les touches ne répondent plus même en READY → problème matériel

---

## 5. Recommandations — dans l'ordre

### Étape 1 (Avant tout) — Sauvegarder les paramètres actuels

> ⚠️ **PRIORITAIRE** — Avant toute réinitialisation, sauvegarder le fichier `setting.set` actuel sur la clé USB.

**Où se trouve `setting.set` ?**
Ce fichier est stocké dans la **mémoire interne du DDCS** (pas sur l'ordinateur, pas sur la clé USB). On y accède uniquement depuis l'écran du contrôleur.

**Procédure de sauvegarde sur clé USB :**
1. Insérer la clé USB dans le port USB du DDCS
2. Appuyer sur **RESET** jusqu'à afficher **READY**
3. Appuyer sur **PAGE R** → entrer dans la File Page
4. Naviguer avec **Y+ / Y-** pour trouver `setting.set` dans la mémoire interne
   - Si tu vois d'abord le contenu de la clé USB → naviguer vers `..` pour remonter à la mémoire interne
   - Le fichier peut aussi s'appeler **`Uservar.set`** selon la version firmware
5. Mettre le curseur bleu sur `setting.set`
6. Appuyer sur **TAB** pour copier
7. Naviguer vers la clé USB
8. Appuyer sur **SHIFT** pour coller
9. Vérifier que le fichier est bien sur la clé

**⚠️ Si le fichier `setting.set` est introuvable :**
Ne pas paniquer. Aller dans la **Page Configuration** (PAGE R × 2) et noter à la main les valeurs suivantes avant tout reset :

| Paramètre | Valeur sur l'écran | Signification |
|---|---|---|
| **#34** | ________ | Steps/mm axe X |
| **#35** | ________ | Steps/mm axe Y |
| **#36** | ________ | Steps/mm axe Z |
| #98 | ________ | Vitesse max broche (rpm) |
| #221 | ________ | Vitesse broche défaut (rpm) |
| #224 | ________ | Délai démarrage broche M3 (s) |

---

### Étape 2 — Reset paramètres (Option A)

Télécharger le fichier `setting.set` par défaut depuis le site Digital Dream ou générer un fichier avec les valeurs du tableau (§3.4.3 du manuel). Recharger depuis la clé USB.

**Risque :** Les Steps/mm et tous les paramètres machine retournent aux valeurs d'usine (valeur par défaut : **640 pulse/mm** pour tous les axes — voir §3.4.3 #34 à #36). Il faudra recalibrer entièrement.

---

### Étape 3 — Mise à jour firmware (Option B) si le reset paramètres ne suffit pas

Uniquement si les bugs persistent après reset des paramètres.

**Risque :** Plus invasif. En cas d'échec de mise à jour (coupure courant, mauvais fichier), le contrôleur peut devenir inutilisable.

---

### Étape 4 — Contacter Digital Dream pour support matériel

Si les touches sont physiquement défaillantes, aucun reset logiciel ne réglera le problème. Contacter :
- **Email :** info@ddcnc.com
- **Site :** www.ddcnc.com

---

## 6. Tableau des paramètres clés — valeurs par défaut usine

Pour référence lors de la reconfiguration après reset :

| Paramètre | Définition | Valeur défaut | Unité |
|---|---|---|---|
| **#34** | Steps/mm axe X | 640 | pulse/mm |
| **#35** | Steps/mm axe Y | 640 | pulse/mm |
| **#36** | Steps/mm axe Z | 640 | pulse/mm |
| #98 | Vitesse max broche | 24 000 | rpm |
| #221 | Vitesse broche défaut | 12 000 | rpm |
| #224 | Délai démarrage broche (M3) | 3 | secondes |
| #100 | Vitesse jog X | 8 000 | mm/min |
| #102 | Vitesse jog Z | 4 000 | mm/min |
| #1 | Langue | 1 | 0=EN, 1=CN |

> ⚠️ Les Steps/mm par défaut (**640 pulse/mm**) sont probablement incorrects pour la QueenBee Pro. Ils devront être recalibrés selon la procédure dans [[Fiche_Calibration_Steps_Z]].

---

*→ Retour au tableau de bord : [[Project_State]]*
*→ Procédure calibration : [[Fiche_Calibration_Steps_Z]]*
