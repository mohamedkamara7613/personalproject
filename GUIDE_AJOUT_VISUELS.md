# 📸 Guide d'Ajout des Visuels Complémentaires

Ce guide récapitule les visuels recommandés pour sublimer la présentation de vos projets sur GitHub, avec les emplacements précis et les noms de fichiers attendus.

---

## 🤖 1. SmartRobot_C (Robot Autonome en C Embarqué)
* **Emplacement :** `SmartRobot_C/docs/`
* **Fichiers suggérés :**
  - `robot_reel.jpg` (ou `.png`) : Photo du robot physique réel (châssis, capteurs IR/couleur suiveur de ligne, écran LCD, carte microcontrôleur).
  - `demo_robot.gif` : Court GIF ou vidéo du robot en train de naviguer sur la grille du labyrinthe.
* **Intégration automatique :** Si vous nommez le fichier `robot_reel.png` ou `demo_robot.gif`, il sera automatiquement affiché en tête du `SmartRobot_C/README.md`.

---

## 🧭 2. Localisation_Pieton_EKF (Fusion Capteurs EKF)
* **Emplacement :** `Localisation_Pieton_EKF/docs/`
* **Fichiers suggérés :**
  - `trajectoire_fusion_ekf.png` : Tracé 2D (ou 3D) issu de Matplotlib montrant la comparaison entre :
    - Trajectoire GPS brute (points bruités)
    - Trajectoire estimée EKF (courbe lissée par fusion IMU + ZUPT)
    - Vérité terrain (si mesurée)
* **Intégration :** Idéal pour illustrer concrètement le gain de précision du filtre de Kalman.

---

## 🗄️ 3. SGBD_SQL_Java21 (Moteur SGBD Relationnel en Java 21)
* **Emplacement :** `SGBD_SQL_Java21/docs/`
* **Fichiers suggérés :**
  - `demo_terminal_sgbd.png` : Capture d'écran du terminal montrant :
    - L'invite de commande SQL interactive
    - L'exécution d'un `SELECT ... FROM ... WHERE ...`
    - Le temps d'exécution ou les logs du Buffer Manager / Index B+Tree
* **Intégration :** Démontre instantanément que le moteur est fonctionnel et exécutable.

---

## 🎵 4. AutoDecomposer_Audio_NMF (Séparation de Sources Audio)
* **Emplacement :** `AutoDecomposer_Audio_NMF/docs/`
* **Fichiers suggérés :**
  - `spectrogrammes_separation.png` : Visualisation des spectrogrammes (STFT) :
    - Spectrogramme du signal mélangé (gauche)
    - Spectrogrammes des sources séparées $W \times H$ (droite)
* **Intégration :** Valide visuellement l'efficacité de la factorisation NMF.

---

## 🎙️ 5. Shazam_Khassida (Reconnaissance Vocale & Audio)
* **Emplacement :** `Shazam_Khassida/docs/`
* **Fichiers suggérés :**
  - `demo_interface_wakhmu.png` : Capture d'écran de l'application web React (`wakhmu`) lors de l'écoute ou de l'affichage des résultats d'identification.
  - `constellation_map.png` : Graphique des pics spectraux et paires de hachage (Constellation Map).

---

## 💡 Procédure pour les ajouter :
1. Déposez simplement vos fichiers images (`.png`, `.jpg`, `.gif`) dans les dossiers `docs/` indiqués ci-dessus.
2. Ouvrez un terminal dans le dépôt `personalproject_github` et faites :
   ```bash
   git add .
   git commit -m "docs: ajout des visuels complementaires pour les projets phares"
   git push origin feature/showcase-portfolio
   ```
