# 🗺️ Répartition des Tâches - PI Itinéraire

**Objectif immédiat :** Rendre le système d'acquisition autonome pour pouvoir sortir faire des relevés de données (GPS + IMU) en extérieur. Ces données réelles nous sont indispensables pour travailler sur la fusion et le Filtre de Kalman.

---

## 🏗️ 1. Responsable Hardware & Acquisition Embarquée (1 personne)
* **Mission :** Rendre la boîtier Raspberry Pi totalement autonome (lancement avec bouton poussoir).
* **Ce qui est déjà fait (Base) :** Les scripts d'acquisition individuels pour le GPS (TP1) et l'IMU (TP2).
* **À faire en urgence :**
  - Créer le point d'entrée `main_acquisition.py`.
  - Intégrer la lecture du bouton poussoir (GPIO) pour démarrer/arrêter l'enregistrement.
  - Lancer les enregistrements GPS et IMU en parallèle avec des timestamps synchronisés.
  - Alimenter les LEDs de statut (Enregistrement en cours / Erreur).

## 🛰️ 2. Expert GPS & Cartographie (1 personne)
* **Mission :** Nettoyer le signal GPS et préparer la comparaison avec la vérité terrain.
* **Ce qui est déjà fait (Base) :** Lecture NMEA sur port série, extraction Lat/Lon, affichage sur carte (TP1).
* **À faire :**
  - **Crucial :** Convertir les coordonnées géographiques (Lat/Lon) en mètres locaux (repère cartésien ENU) car le Filtre de Kalman ne fonctionne qu'avec des mètres.
  - Utiliser le script `conversion_gpx.py` pour superposer nos traces à celles de Strava.

## 🚀 3. Expert IMU & Prétraitement (1 personne)
* **Mission :** Traiter les données de l'accéléromètre et du gyroscope pour supprimer le bruit.
* **Ce qui est déjà fait (Base) :** Lecture des registres en I2C, tracé des graphes bruts (TP2).
* **À faire en urgence :**
  - **Calibration :** Coder un script qui lit l'IMU au repos pendant 10 secondes pour calculer le "biais" (l'erreur fixe) et le bruit.
  - Soustraire ce biais en temps réel aux données récoltées.
  - Appliquer un filtre numérique basique (passe-bas) pour réduire les vibrations parasites de la course.

## 🧠 4. Équipe Filtre de Kalman (Binôme - 2 personnes)
* **Mission :** Fusionner mathématiquement le GPS lent et l'IMU rapide. C'est la tâche la plus complexe du projet.
* **Ce qui est déjà fait (Base) :** La structure algorithmique (`TDM8.ipynb` et `utils.py`).
* **À faire (dès qu'on a nos premières données en extérieur) :**
  - **Membre 4A (Théorie) :** Définir le vecteur d'état et adapter les matrices de transition pour coller à la cinématique (IMU).
  - **Membre 4B (Synchronisation) :** Créer la boucle temporelle qui met à jour l'état à 100 Hz (avec l'IMU) et qui corrige à 1 Hz (avec le GPS).
  - Ajuster les paramètres d'incertitude (Q et R) à partir des calculs de variance de l'expert IMU.

## 📸 5. Fonctionnalité Bonus & Data (Toute l'équipe)
* **Mission :** Fonctionnalité fun et points bonus sur le partage des données.
* **Idée retenue :** Vision par ordinateur avec la Caméra Pi + **Mediapipe**. 
  - *Exemples : Démarrage gestuel d'acquisition avec la main, ou analyse de posture du coureur.*
* **À faire :**
  - S'assurer que le format de nos dossiers d'acquisition respecte scrupuleusement le dépôt Gitlab `pi-itineraire-data`.
  - Commencer le Proof of Concept avec Mediapipe en parallèle du Filtre de Kalman.

---

> 💡 **Feuille de route pour les prochains jours :** 
> 1. Le Rôle 1 configure le bouton et le `main` pendant que les autres font fonctionner les vieux codes TP sur la Pi.
> 2. On lance notre **première acquisition en extérieur**.
> 3. Avec ces vraies données dans nos `.csv`, les experts nettoient le signal et l'équipe Kalman commence la fusion !
