# Compte Rendu TP1 : Module GNSS

## 1. Objectifs de la séance
L'objectif de ce TP est de manipuler un capteur GNSS (DFRobot TEL0157) avec une Raspberry Pi 4. Nous avons pour but de réceptionner des signaux satellites, d'analyser les trames NMEA, et d'effectuer des acquisitions en extérieur pour observer la précision du positionnement.

## 2. Mise en place

### 2.1 Matériel et Branchements
Nous avons utilisé le matériel suivant :
*   Raspberry Pi 4
*   Module GNSS DFRobot TEL0157
*   Afficheur LCD 1602

**Câblage I2C :**
Le branchement s'effectue via le bus I2C. Nous avons relié les broches de la Raspberry Pi aux modules (GNSS et LCD) en utilisant une breadboard :
*   **SDA** (Raspberry) $\leftrightarrow$ **SDA** (LCD) et **SDA** (GNSS)
*   **SCL** (Raspberry) $\leftrightarrow$ **SCL** (LCD) et **SCL** (GNSS)
*   Alimentation (VCC/GND) connectée en conséquence.

### 2.2 Détection des périphériques
Une fois les branchements effectués et l'environnement activé, nous avons vérifié la présence des périphériques sur le bus I2C avec la commande :
```bash
i2cdetect -y 1
```
Cela nous a permis de relever les adresses hexadécimales du module GNSS et de l'afficheur LCD pour configurer le fichier `config/constants.py`.

## 3. Lecture et Analyse des trames NMEA

Nous avons exécuté le script `scripts/get_nmea_frames.py` pour lire les trames brutes envoyées par le module. Le système GNSS est un système global de navigation par satellite.

### 3.1 Analyse d'une trame GNGGA
Voici les informations extraites d'un exemple de trame GNGGA reçue :
`$GNGGA,145748.000,4923.06331,N,00104.9899,E,1,07,3.9,69.6,M,45.3,M,,*70`

*   **UTC** : 145748.000 (14h 57m 48s)
*   **Latitude** : 4923.06331 (Format DDMM.MMMMM) -> Hémisphère **N** (Nord)
*   **Longitude** : 00104.9899 -> Hémisphère **E** (Est)
*   **Fix** : 1 (Fix GPS valide)
*   **Satellites** : 07 (Nombre de satellites utilisés)
*   **HDOP** : 3.9 (Précision horizontale)
*   **Altitude** : 69.6 M (Mètres au-dessus du niveau de la mer)
*   **Geoidal Separation** : 45.3 M

### 3.2 Analyse d'une trame RMC
Exemple de trame RMC :
`$GNRMC,145748.000,A,4923.06331,N,00104.09899,E,0.00,90.96,270126,,,A,V*38`

*   **UTC** : 145748.000
*   **Status** : A (Actif/Valide)
*   **Position** : 4923.06331 N, 00104.09899 E
*   **Speed** : 0.00 nœuds (Vitesse au sol)
*   **Course** : 90.96 degrés (Cap vrai)
*   **Date** : 270126 (27 Janvier 2026)
*   **Mode** : A (Autonome)

### 3.3 Identification des constellations
Nous avons testé la réception de différentes constellations en utilisant les arguments du script :

*   GPS uniquement : `python3 scripts/get_nmea_frames.py --mode gps`
*   BeiDou uniquement : `python3 scripts/get_nmea_frames.py --mode beidou`
*   GLONASS uniquement : `python3 scripts/get_nmea_frames.py --mode glonass`

<!-- Ajouter ici une capture d'écran des résultats si disponible -->

## 4. Coordonnées Géographiques

Nous avons étudié les différents formats de coordonnées.
Le format renvoyé par le module GNSS est le **Degrés Décimaux (DD)** (après conversion par la librairie ou le script, bien que la trame brute soit souvent en NMEA DDMM.MM).

Nous avons noté que la précision obtenue est de l'ordre du mètre, mais elle dépend fortement des conditions de réception.

## 5. Acquisitions et Observations

Nous avons réalisé une acquisition en extérieur en nous déplaçant ("balade") avec le dispositif.
Le script utilisé était : `scripts/get_position.py` (avec enregistrement CSV).

**Observation :**
Après avoir tracé le trajet, nous avons constaté que le relevé est **très bruité**. Le chemin tracé n'est pas parfaitement lisse et présente des sauts, témoignant des imprécisions du signal GNSS (phénomènes de réflexion, nombre de satellites visibles, etc.).

<!-- Ajouter ici la capture d'écran du tracé (ex: balade.html ou plot) -->

---
