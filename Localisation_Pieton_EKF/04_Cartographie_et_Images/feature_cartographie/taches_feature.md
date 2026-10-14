# Plan d'Action - Feature Cartographie

Ce document regroupe toutes les étapes pour accomplir l'intégration de la carte interactive avec photos.

- [ ] **Tâche 1 : Mise en place matérielle**
  - Brancher la caméra sur le Raspberry Pi.
  - S'assurer que les bibliothèques `opencv-python` et `mediapipe` s'exécutent correctement sur le Pi.

- [ ] **Tâche 2 : Logique de détection (Mediapipe)**
  - Implémenter la détection de main dans `capture_mediapipe.py`.
  - Gérer l'enregistrement de l'image (fichier `.jpg`) et du Timestamp précis dans un fichier journal (`photos_log.csv`).

- [ ] **Tâche 3 : Calcul mathématique inverse**
  - Coder la fonction inverse dans `generate_map.py` pour passer des $(X, Y)$ locaux (en mètres, issus de Kalman) aux vraies `Latitude` et `Longitude` mondiales (en degrés).

- [ ] **Tâche 4 : Génération de la Carte (Folium)**
  - Coder la lecture des deux CSV (`trajectoire_fusionnee.csv` et `photos_log.csv`).
  - Utiliser `folium.PolyLine` pour tracer le chemin lissé.
  - Utiliser `folium.Marker` avec un argument `popup` en HTML (`<img src="...">`) pour accrocher la photo.
  - Sauvegarder le rendu en `carte.html`.

- [ ] **Tâche 5 : Déploiement et Test d'intégration**
  - Lancer un vrai test sur le campus : marcher 50 mètres, faire coucou à la caméra 2 ou 3 fois, revenir au point de départ.
  - Lancer la pipeline de fusion complète sur le PC et vérifier que la carte HTML s'ouvre avec les photos aux bons endroits.
