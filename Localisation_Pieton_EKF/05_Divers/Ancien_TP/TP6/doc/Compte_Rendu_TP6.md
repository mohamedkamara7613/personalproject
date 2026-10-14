# Guide Détaillé - TP6 : Capteurs de Vision et Fusion Multi-Capteurs
**Module :** ITI32 Capteurs
**Sujet :** Acquisition asynchrone, multithreading et synchronisation (Caméra/LiDAR)

---

## 1. Reprise des acquis et Mise en place du LiDAR (Depuis TP3)

La première étape de ce TP consiste à reconnecter le LiDAR en implémentant les notions du TP3 dans la nouvelle classe mise à jour (`sensors/LIDAR/lidar.py`). Le driver RPLidar renvoie des tuples de forme `(qualité, angle, distance)`. Il faut donc compléter les filtres spatiaux et la conversion des coordonnées pour qu'ils s'intègrent au pipeline.

### 1.1 Filtrage Spacial (`sensors/LIDAR/lidar.py`)

L'astuce sur le filtre temporel/angulaire est qu'il doit prendre en compte un croisement du point zéro (Nord). La zone de détection peut traverser la ligne d'origine de la rotation (exemple : mesurer un champ se situant entre 270° et 90°).

```python
    def filter_range(self, scan):
        # On ne conserve que les points entre la portée minimale et maximale
        return [meas for meas in scan if self.min_range <= meas[2] <= self.max_range]

    def filter_quality(self, scan):
        # On supprime le bruit où la qualité du scan est jugée trop faible
        return [meas for meas in scan if meas[0] >= self.quality_threshold]

    def filter_angle(self, scan):
        filtered = []
        for meas in scan:
            quality, angle, distance = meas
            # Sécurité pour gérer les tranches de cap non consécutives sur 360°
            if self.min_angle <= self.max_angle:
                if self.min_angle <= angle <= self.max_angle:
                    filtered.append(meas)
            else:
                if angle >= self.min_angle or angle <= self.max_angle:
                    filtered.append(meas)
        return filtered
```

### 1.2 Conversion Polaire vers Cartésien
```python
    def polar_to_cartesian(self, scan):
        # Formules géométriques basiques (attention à convertir en Radians)
        # x = distance * sin(rad)
        # y = distance * cos(rad)
        points = []
        for quality, angle, distance in scan:
            rad = math.radians(angle)
            x = distance * math.sin(rad)
            y = distance * math.cos(rad)
            points.append((x, y))
        return points
```

---

## 2. Réponses aux questions de l'Acquisition Multi-Capteurs

**Q : Exécutez dans 2 terminaux séparés vos deux scripts d’acquisition. Pourquoi l’acquisition ne fonctionne pas ici ?**
Le bouton poussoir (bouton Start/Stop) et la LED emploient des ports (GPIO) bien définis. Si deux scripts distincts (`capture_lidar.py` et `capture_camera.py`) sont lancés séparément, un flag sera levé car l'état GPIO est monopolisé par le premier script.
Si l'on écrit un nouveau script intégrant ces deux captures sans "Thread" (de manière purement séquentielle `while True: scan... puis frame...`), l'acquisition perdra drastiquement en performance, car l'un va attendre l'autre. Le LiDAR étant plus lent à faire une révolution complète, il bloque la caméra qui ne capturera qu'une fraction des FPS dont elle est capable : c'est le **goulot d'étranglement (I/O Bottleneck)**.

**Q : Combien d'images/scans avez-vous obtenu ?**
*(Vos valeurs peuvent légèrement varier selon les tests)* : En règle générale, sur une poignée de secondes de rotation "libre" (multithreading), le Raspberry Pi parvient à conserver :
- Un énorme volume d'images (Ex : **300 images en 10 secondes**).
- Très peu de points de vue lasers  (Ex : **90 scans en 10 secondes**).

**Q : À partir des fichiers timestamps CSV, quelles sont les fréquences d’acquisitions des deux capteurs ? Comment varient ces fréquences au cours du temps ?**
En regardant les sauts entres chaque timestamp (les lignes successives des CSV `timestamps_frames.csv` et `timestamps_scans.csv` en faisant $\Delta t$) :
- **Caméra** : Une moyenne de `0.033 s` ($\approx 30 Hz$).
- **LiDAR** : Une moyenne de `0.1 s` à `0.2 s` ($\approx 5$ à $10 Hz$).
**Variation dans le temps** : Bien qu'on ait "libéré" chaque capteur sur son propre Thread de processeur, ce n'est pas garantis 100% constant. Les fréquences chutent brutalement quand le Raspberry doit orchestrer d'autres lourdes tâches d'arrière plan (notamment vider la file d'attente système d'écriture vers la carte Micro-SD, ce qui ajoute un délai/jitter).

---

## 3. Guide de Synchronisation (Extraits de code du Multithread)

### 3.1 Protection d'état des variables partagées (`capture_multisensor.py`)
Il est primordial d'utiliser la primitive de synchronisation **Lock** (`verrou` d'accès concurrent) afin qu'aucun Thread du capteur `A` ne modifie ou n'écrive sur les variables partagées (`state`) pendant que le capteur `B` vérifie une condition.

```python
# Exemple d'implémentation dans (camera_worker) ou (lidar_worker)
timestamp = time.time()
with lock:
    if state["is_acquiring"]:
        lidar.save_scan_sequence(points, state["scans_dir"], state["scan_index"])
        state["csv_scans"].append_row([timestamp, f"scan_{state['scan_index']:06d}.csv"])
        state["scan_index"] += 1
```

### 3.2 L'Appairage Temporel Hors Ligne (`postprocessing/synchronization.py`)
Pour coupler vos données disparates, il utilise la boucle séquentielle offline sur la base des relevés *temps* émis pendant l'acquisition au pas précédent. Le capteur avec la plus faible définition (donc les scans LiDAR ici) devient "l'ancre". On sélectionne toujours la frame caméra capturée géographiquement **au plus près du moment "t"** où le scan balayait la pièce.

*Algorithme au cœur du script :*
```python
        # timestamp caméra ciblé à chaque passe
        t_camera = frame_entry["timestamp"] 

        # 1. Recherche : Trouver le scan comportant l'écart / delta minium par rapport au t_camera cible
        closest_scan_idx = np.argmin([abs(s["timestamp"] - t_camera) for s in scan_entries])
        closest_scan = scan_entries[closest_scan_idx]
        
        t_lidar = closest_scan["timestamp"]
        # Ecart temporel entre la photo et le scan
        dt_s = abs(t_camera - t_lidar)

        # 2. Rejet de décalage : Si dt_s est trop grand, la paire n'est pas fiable, on l'ignore (continue)
        if dt_s > threshold:
            continue

        # 3. Rejet de doublons : On veut qu'un scan ne soit mappé qu'à UNE et une seule frame optimale
        if closest_scan_idx in used_scan_indices:
            continue
            
        used_scan_indices.add(closest_scan_idx)
```
Le processus final copie par `shutil` les éléments rescapés (Paires synchrones validées) dans un unique flux harmonisé `_synced` ! 

*(PS : N'oubliez pas les éléments optionnels pour la capture avec les 4 capteurs en vue du Projet final !)*
