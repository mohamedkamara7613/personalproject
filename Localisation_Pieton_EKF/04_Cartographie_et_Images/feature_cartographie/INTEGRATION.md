# Guide d'Intégration : Module Cartographie & Photos

Ce dossier contient la **Fonctionnalité 2** (Capture photo hybride IA/Bouton et Cartographie interactive).
Comme convenu en équipe, ce code a été développé en isolation ("en bac à sable") pour ne pas perturber le fonctionnement stable du système temps réel IMU/GPS (Filtre de Kalman).

## Éléments à discuter avec l'équipe avant l'intégration :

### 1. Architecture des dossiers
Où souhaitons-nous placer ces scripts dans le dépôt `pi_itineraire_26_28` ?
- Proposition : Créer un dossier `code/Code_fusion/features/camera/` pour y glisser `capture_mediapipe.py` et le modèle IA `hand_landmarker.task`.
- Proposition : Glisser `generate_map.py` dans le dossier existant `code/Code_fusion/postprocessing/`.

### 2. Gestion du Bouton Physique (Hardware)
- Le script utilise `gpiozero`. 
- Il faut se mettre d'accord sur le Pin GPIO utilisé pour brancher le bouton poussoir sur le Raspberry Pi (actuellement codé en dur sur `BUTTON_PIN = 2`).

### 3. Ressources Système (Raspberry Pi)
- Le script `capture_mediapipe.py` fait tourner un modèle IA (TensorFlow Lite) en temps réel.
- Il faudra tester si le Raspberry Pi supporte de faire tourner : `get_IMU_GPS.py` (Kalman) + `capture_mediapipe.py` (Caméra IA) simultanément sans surchauffer ou faire chuter la fréquence d'acquisition de l'IMU (100 Hz).

## Ce qui est prêt pour le "Merge"
1. Les fichiers sources :
   - `capture_mediapipe.py` (Le démon de capture)
   - `hand_landmarker.task` (Le modèle IA Google pré-téléchargé)
   - `generate_map.py` (Le générateur de carte Folium avec photos Base64)
2. Les dépendances ont déjà été ajoutées dans le fichier `requirements.txt` à la racine du dépôt distant (`mediapipe`, `opencv-python`, `gpiozero`).
