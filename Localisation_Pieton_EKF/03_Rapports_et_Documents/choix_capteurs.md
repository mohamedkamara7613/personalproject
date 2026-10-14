# Analyse et Choix des Capteurs pour le Projet ITINERAIRE

Ce document résume les réflexions sur la sélection des capteurs pour la Partie 1 du projet ITINERAIRE (Estimation de trajectoire), en se basant sur les exigences du sujet et les `notes.txt`.

## Le Défi de l'Estimation de Trajectoire
L'objectif est de réaliser un système de suivi GPS "dernier cri" en fusionnant les données de plusieurs capteurs via un **Filtre de Kalman**.

---

## 1. Le GPS (La base absolue)
* **Rôle :** Fournit la position globale absolue sur la carte (Latitude / Longitude / Altitude). C'est indispensable pour placer le trajet final sur OpenStreetMap.
* **Limites :** 
  * Fréquence de rafraîchissement très faible (généralement 1 Hz).
  * Signal bruité et sujet aux erreurs liées à l'environnement (perte de signal sous les arbres ou en intérieur, "multipath" ou rebonds sur les bâtiments).

## 2. L'IMU (La pièce maîtresse du Filtre de Kalman)
*Dans tes notes, tu te demandais : "Pourquoi et qu'est-ce qu'il peut amener de plus ?"*

L'IMU (Centrale à Inertie) est composé d'un accéléromètre et d'un gyroscope. Il est la réponse directe aux défauts du GPS.
* **Ce qu'il apporte en plus :**
  1. **Haute Fréquence :** L'IMU enregistre les données très rapidement (ex: 100 Hz). Il permet de suivre le mouvement exact du téléphone *entre* deux pings GPS lents.
  2. **Navigation à l'estime (Dead Reckoning) :** En cas de perte totale du signal GPS (tunnel, bâtiment), l'IMU permet de continuer à calculer la trajectoire en intégrant mathématiquement l'accélération.
  3. **Complémentarité pour la Fusion :** L'IMU est très précis à court terme mais dérive sur le long terme. Le GPS est bruité à court terme mais ne dérive pas. Dans un Filtre de Kalman, l'IMU gère la **"Prédiction"** (dynamique rapide), et le GPS fait la **"Correction"** (recalage spatial).

## 3. Le LiDAR 2D et la Caméra (Odométrie Locale)
* **Rôle :** Percevoir l'environnement immédiat autour du smartphone pour mesurer le déplacement relatif.
* **Odométrie Visuelle / LiDAR SLAM :** En comparant deux images successives (Caméra) ou deux balayages lasers successifs (LiDAR), on peut calculer la vitesse et la direction du déplacement par rapport aux murs et obstacles.
* **Avantage :** Très précis pour les mouvements locaux, sans dépendre des satellites extérieurs. Le sujet recommande d'ailleurs de s'appuyer sur le **TP6 (Caméra LiDAR)** comme base de code pour le projet.

---

## Synthèse et Recommandation

Pour obtenir une trajectoire robuste et répondre aux critères d'évaluation, une combinaison **IMU + GPS + LiDAR (ou Caméra)** est idéale :

1. **IMU** : Fournit le modèle dynamique à haute fréquence (prédiction de Kalman).
2. **LiDAR / Caméra** : Donne une odométrie locale très fine (correction locale).
3. **GPS** : Ancre la trajectoire sur une carte globale (correction absolue).

## Prochaines Étapes
Comme mentionné dans tes notes, il sera très utile de récupérer et d'analyser les codes des anciens TP :
* Le code du **TP Kalman** (pour la structure de fusion).
* Le code du **TP6 (Caméra LiDAR)** (recommandé par le sujet).
* Les scripts de calibration de la caméra (`Calibration.ipynb`).
* Les codes de lecture du GPS.
