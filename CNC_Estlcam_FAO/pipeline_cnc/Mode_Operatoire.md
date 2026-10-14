# Mode Opératoire : De SketchUp à la QueenBee Pro

Ce guide vous explique comment passer de votre dessin à la découpe finale sur votre machine CNC.

## Étape 1 : Importer le dessin et paramétrer les outils

Une fois que vous avez exporté votre dessin depuis SketchUp (au format `.DXF` pour du plat/2.5D ou `.STL` pour de la 3D) et que vous l'avez ouvert dans **Estlcam**, la toute première étape consiste à **configurer votre liste d'outils (vos fraises)**. 

C'est essentiel : Estlcam doit connaître les dimensions de la fraise pour calculer le bon parcours et ne pas couper au mauvais endroit.

### La Liste des Outils dans Estlcam

![Paramètres des outils Estlcam](./chemin_vers_votre_image_liste_outils.png)

*Dans cette fenêtre, vous définissez le comportement de chaque fraise.*

Voici la signification de chaque colonne importante :

* **Ø (Diamètre) :** Le diamètre exact de votre fraise (ex: 3.17mm ou 6mm). C'est ce qui permet à Estlcam de calculer le décalage (couper à l'extérieur ou à l'intérieur du trait).
* **Z+ (Profondeur de passe / Stepdown) :** L'épaisseur de matière enlevée à chaque passage. *(Ex: 1,00 mm signifie que pour couper une plaque de 12 mm, la fraise fera 12 passages).*
* **Fxy (Avance / Feed rate) :** La vitesse de déplacement horizontal de la machine pendant la coupe.
* **Fz (Plongée / Plunge rate) :** La vitesse à laquelle la fraise descend verticalement dans la matière. On la garde plus lente pour ne pas forcer sur la pointe de l'outil.
* **N (Vitesse de rotation broche / Spindle speed) :** Exprimée en `rpm` (Revolutions Per Minute - Tours par minute). C'est la vitesse à laquelle votre fraise tourne sur elle-même.

> **💡 Conseil :** Ces paramètres dépendent de la matière et de la fraise. Pour commencer, utilisez toujours des valeurs conservatrices.

### 📊 Tableau de référence (Paramètres de départ)

Valeurs conseillées pour démarrer en toute sécurité :

| Matériau | Fraise Ø | Passe (Z+) | Avance (Fxy) | Plongée (Fz) | Rotation (N) |
|---|---|---|---|---|---|
| **Bois Tendre** (Pin, MDF) | 3 mm | 1,5 mm | 800 mm/min | 200 mm/min | 18 000 rpm |
| **Bois Tendre** (Pin, MDF) | 6 mm | 2,0 mm | 1 200 mm/min| 400 mm/min | 18 000 rpm |
| **Bois Dur** (Chêne, Hêtre)| 6 mm | 1,5 mm | 800 mm/min | 300 mm/min | 16 000 rpm |
| **Plastique** (Acrylique)* | 3 mm | 1,0 mm | 1 000 mm/min| 300 mm/min | 14 000 rpm |

*\*Pour l'acrylique, utilisez impérativement une fraise "1 dent" (single flute) pour éviter que le plastique ne fonde et s'enroule autour de l'outil.*

---

## 🧠 Comprendre sa machine : Le rôle du VFD
Dans votre installation, la broche (le moteur qui coupe) ne reçoit pas son électricité directement du boîtier avec l'écran (le contrôleur DDCS). 
* Le **DDCS** est le **"Cerveau"** : il envoie de petits signaux électriques (pour dire "Allume-toi" ou "Tourne à 18000 tours").
* Le **VFD** (Variateur de Fréquence / Onduleur) est le **"Muscle"** : c'est le gros boîtier électrique qui reçoit les petits ordres du DDCS et libère la forte puissance nécessaire pour faire tourner la broche.

> **💡 Astuce visuelle :** Quand la broche reçoit correctement l'ordre de tourner, le petit voyant **"FWD"** (Forward / Marche avant) doit s'allumer sur la façade du boîtier VFD.

---

## 🛠️ Dépannage (Troubleshooting)

### La machine bouge mais la broche ne tourne pas (Code M5 sur le DDCS)
Si le contrôleur DDCS affiche **M5** (Spindle Stop) en bas de l'écran pendant l'usinage, c'est que l'ordre de démarrage n'a pas été envoyé.
- **Solution :** Allez dans Estlcam > *Configuration* > *Programmes CNC* > Onglet *Textes*. Vérifiez que la case **"Démarrage du programme"** contient bien la commande `M03`.

### Le contrôleur affiche M3 mais la broche ne tourne pas (Écran du VFD)
Si le contrôleur affiche bien M3 en bleu, regardez l'écran rouge du VFD :
- **S'il affiche un code d'erreur (ex: `OC -o`) :** Le VFD s'est mis en sécurité électrique (ex: surintensité ou parasites). Tant qu'il clignote avec cette alarme, il refusera de démarrer. 
  - **Solution :** Appuyez sur le bouton rouge **"STOP / RESET"** sur la façade du VFD pour effacer l'erreur.
- **S'il n'y a pas d'erreur mais que ça ne tourne toujours pas :** 
  - Dans le DDCS (Paramètre 227 - *Spindle switch Active level*), essayez d'inverser la polarité (de *High* à *Low* ou inversement).
  - Vérifiez le câblage entre le DDCS (ports M3 et VSO) et le VFD (ports FWD et 10V_IN).
