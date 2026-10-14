# Guide Complet et Corrigé - TP6 : Fusion Multi-Capteurs (Caméra x LiDAR)
**Auteurs:** Kamara Mohamed et Diop Amsatou

Ce guide centralise l'ensemble des réponses théoriques, des méthodes de manipulations et des blocs de codes nécessaires pour compléter le **TP6** rapidement et efficacement.

---

## 2. Mise en Place : Mises à jour de la classe LiDAR

*(Fichier visé : `sensors/LIDAR/lidar.py` et `scripts/measure_distance.py`)*

Dans un premier temps, afin de rendre l'acquisition LiDAR saine sans les bugs du package de 2016, les méthodes de tri spatial abordées lors du **TP3** doivent être réinsérées.

### 2.1 - Complétion des filtres LiDAR (`sensors/LIDAR/lidar.py`)

```python
    def filter_range(self, scan):
        # Ne conserve que les points entre la portée minimale et maximale
        return [meas for meas in scan if self.min_range <= meas[2] <= self.max_range]

    def filter_quality(self, scan):
        # Exclut les bruits parasites selon un seuil paramétré
        return [meas for meas in scan if meas[0] >= self.quality_threshold]

    def filter_angle(self, scan):
        # Cas délicat : Gérer le franchissement de la ligne "Zéro/Nord" sur le plan
        filtered = []
        for meas in scan:
            quality, angle, distance = meas
            if self.min_angle <= self.max_angle:
                if self.min_angle <= angle <= self.max_angle:
                    filtered.append(meas)
            else:
                if angle >= self.min_angle or angle <= self.max_angle:
                    filtered.append(meas)
        return filtered
```

### 2.2 - Conversion Spatiale
```python
    def polar_to_cartesian(self, scan):
        # Conversion Rad = Angle * π / 180 (x=sin / y=cos)
        points = []
        for quality, angle, distance in scan:
            rad = math.radians(angle)
            x = distance * math.sin(rad)
            y = distance * math.cos(rad)
            points.append((x, y))
        return points
```

### 2.3 - Algorithme de distance (`scripts/measure_distance.py`)
```python
    for timestamp, scan, points in scan_iterator:
        distances = [meas[2] for meas in scan] # meas = (qualité, angle, distance)
        if len(distances) > 0:
            mean_distance = np.mean(distances)
            std_distance = np.std(distances)
        else:
            mean_distance = 0.0
            std_distance = 0.0
            
        yield timestamp, mean_distance, std_distance
```

---

## 3. Acquisition LiDAR

*(Fichier visé : `scripts/capture_lidar.py`)*

Il vous est demandé de réaliser un script d'enregistrement "LiDAR-only" similaire à celui de la caméra, mais dont l'intégrité de chaque révolution moteur sera écrite dans un fichier brut `CSV`. Ce processus passe par l'utilisation de `CSVHandler`. Servez-vous de vos scripts du TP3 (`measure_distance.py` et `LIDAR`) pour initialiser le capteur au début du fichier test.

---

## 4. Acquisition Multi-Capteurs (Multithreading)

*(Fichier visé : `scripts/capture_multisensor.py`)*

### Questions Théoriques :
> **Q : Pourquoi l'acquisition ne fonctionne pas ici (en exécutant deux scripts indépendants) ?** 

Si vous lancez les deux scripts dans des terminaux séparés, un conflit de port GPIO empêchera un périphérique d'interroger la ressource bloquée (ex: Le Bouton Start).
Si vous intégrez le tout sans "Thread", de manière séquentielle (`while True: scan... puis frame...`), l'acquisition perdra drastiquement en performance. Le LiDAR étant plus lent à réaliser une révolution, la caméra doit attendre et ne capturera qu'une fraction des FPS dont elle est capable. C'est le **goulot d'étranglement matériel (I/O Bottleneck)** affectant la fluidité.

Il faut obligatoirement utiliser du **Multithreading** pour dédier un processus au LiDAR ($`5-10 Hz`$) et un autre à la Caméra ($`30 Hz`$) de manière "Parallèle".

> **Q : Combien d’images/scans avez vous obtenu ?**

*(Exemple de réponse pour votre CR)* : "Placés de manière asynchrone, la caméra et le LiDAR tournent selon leur charge. Sur 10 secondes, nous générons environ `300 images BGR` contre `90 scans CSV` LiDAR. Les pertes sont infimes par rapport à la théorie pure."

> **Q : A partir des fichiers timestamps CSV, quelles sont les fréquences d’acquisitions des deux capteurs ? Comment varient ces fréquences au cours du temps ?**

En calculant le pas constant entre chaque ligne `(d_t = t_n - t_n-1)` : 
- Caméra : Une image toutes les $\approx 0.033 s$ **($30 Hz$)**.
- LiDAR : Un enregistrement toutes les $\approx 0.1 / 0.2 s$ **($5$ à $10 Hz$)**.
Ces fréquences connaissent du *Jitter* (Latence inattendue). Elles fluctuent lorsque la mémoire tampon d'écriture (IO) pour la carte micro-SD ou l'OS (Raspbian) doivent réguler les priorités, décalant irrégulièrement quelques millisecondes de l'enregistrement.

### Manipulation et Implémentation du Code :
Il est vital de gérer la ressource de la variable `state` à l'aide d'un verrou `lock` fourni par le module `threading`, évitant que la caméra n'essaye de modifier un attribut lorsque le LiDAR travaille dessus !

```python
# CODE A INCLURE DANS lidar_worker (Et refaire de même dans camera_worker)
timestamp = time.time()
with lock: # On ferme la zone critique !
    if state["is_acquiring"]:
        # Fonction propre permettant de cracher votre liste de points dans un fichier
        lidar.save_scan_sequence(points, state["scans_dir"], state["scan_index"])
        
        # Et on ajoute l'index au fichier global contenant le nom et son temps relatif !
        state["csv_scans"].append_row([timestamp, f"scan_{state['scan_index']:06d}.csv"])
        state["scan_index"] += 1
```

---

## 5. Synchronisation Offline

*(Fichier visé : `postprocessing/synchronization.py`)*

Fédérer les données issues des deux flux n'est possible que par **synchronisation "a posteriori"**. 
L'algorithme de ce script consiste à prendre la source au **FPS le plus faible** comme capteur "Maître" (ici le LiDAR). Pour chaque scan, il vient vérifier dans le DataFrame de la caméra quel est le Timestamp de création le plus "proche" chronologiquement. Si il concorde à moins de `0.1s` (Threshold limite), il les couple (Paired/Synced_data).

```python
        # timestamp caméra émis sur l'itération en cours
        t_camera = frame_entry["timestamp"]

        # 1. On cherche le scan LiDAR existant comportant le décalage minimum par rapport à l'image
        closest_scan_idx = np.argmin([abs(s["timestamp"] - t_camera) for s in scan_entries])
        closest_scan = scan_entries[closest_scan_idx]
        
        t_lidar = closest_scan["timestamp"]
        # Différence des deux
        dt_s = abs(t_camera - t_lidar)

        # 2. Si dt_s est trop grand et depasse le delta seuil max, on rejète la paire !
        if dt_s > threshold:
            continue

        # 3. Si l'enregistrement LiDAR a déjà été marié avec la toute dernière frame avant celle-ci, on rejète !
        if closest_scan_idx in used_scan_indices:
            continue
            
        used_scan_indices.add(closest_scan_idx)
```
Grâce a cet algorithme couplé au code `Shutil`, votre dossier `_synchronized` en sortie ne contiendra que les binômes Parfaits (1 Image capturée pour 1 Scan relevé, et ça avec moins de 100ms absolue d'écart entre la prise).

---
> **Projet Intégratif :** Comme suggéré à la section 6 du sujet, tout ce travail pose la base de l'acquisition finale. Le modèle asynchrone par "Threads + Lock" et par synchronisation "a posteriori (offline)" peut tout à fait se dupliquer pour ajouter l'IMU et le GPS de façon quasi identique !
