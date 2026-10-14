# Feature "Carte Interactive & Photos"

## 💡 L'Idée Principale
L'objectif est d'ajouter une couche visuelle et interactive aux données brutes du capteur.
Lors de l'acquisition du parcours, une caméra tourne sur le Raspberry Pi. Grâce à **Mediapipe**, si une main est détectée dans le champ (ou via un bouton poussoir si échec), le script prend une photo automatiquement. 

De retour sur PC, la trajectoire lissée par le Filtre de Kalman est dessinée sur une carte du monde **OpenStreetMap (via la librairie Folium)**. Les photos prises pendant le trajet sont ensuite placées sous forme d'épingles cliquables aux endroits géographiques exacts où elles ont été prises !

## 🔄 Le Flux de Données

### 1. Acquisition (Temps réel sur le terrain)
- `main_acquisition.py` sauvegarde le GPS et l'IMU en tâche de fond comme prévu.
- Le nouveau script `capture_mediapipe.py` tourne en parallèle, lit le flux vidéo, et détecte les gestes. 
- Lorsqu'un geste est validé $\rightarrow$ sauvegarde de l'image (ex: `photo_01.jpg`) + enregistrement du **Timestamp précis** de la capture dans un journal.

### 2. Synchronisation (Post-traitement sur le PC)
- Le Filtre de Kalman fusionne le GPS et l'IMU et génère `trajectoire_fusionnee.csv`.
- Le script croise le Timestamp de chaque photo avec la trajectoire du Kalman pour obtenir la position locale $(X, Y)$ exacte du piéton au moment de la photo.
- Ces coordonnées $(X, Y)$ en mètres sont reconverties mathématiquement en coordonnées mondiales universelles (Latitude, Longitude).

### 3. Génération de la Carte (Post-traitement sur le PC)
- Le script `generate_map.py` utilise la librairie `folium`.
- Il trace la trajectoire complète en bleu sur un fond de carte OpenStreetMap.
- Il place des marqueurs (épingles rouges) aux coordonnées des photos. Un clic sur le marqueur ouvre un petit popup HTML contenant la photo capturée au-dessus de la carte.
