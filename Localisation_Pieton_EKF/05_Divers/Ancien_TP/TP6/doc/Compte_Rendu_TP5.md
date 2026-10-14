# Compte Rendu - TP5 Capteurs et Caméra
**Module:** ITI32 Capteurs
**Sujet:** Calibration caméra et correction de distorsion
**Auteurs et Autrices** : Kamara Mohamed et Diop Amsatou

---

## 2. Échec et mat

**Q : À quoi sert le damier ici pour la calibration ? Que va-t-on détecter ?**  
Le damier sert de mire de calibration, offrant un motif géométrique régulier avec des dimensions connues. L'objectif est de détecter les intersections intérieures (les "coins") entre les carrés noirs et blancs. Puisque ces points sont coplanaires et symétriques et ont une taille régulière, leurs coordonnées théoriques dans l'espace (3D) sont connues. En les comparant à celles détectées dans l'image (2D), l'algorithme est en mesure de calculer les paramètres optiques et la déformation de la lentille de la caméra. *(Réf : CM8 sur la distorsion et Modelisation par sténopé / Pinhole Camera Model)*.

![Setup Caméra](./code_from_rpi/code/im_capture_ecran_tp/setup-1.jpg)
![Damier de calibration](./code_from_rpi/code/im_capture_ecran_tp/setup-2.jpg)

---

## 3. Calibration (le gros truc complexe du TP)

### 3.1 Checkpoint 1
**Q : Complétez les variables DIM_GRID et SQUARE_SIZE du fichier config/constants.py**  
Les valeurs ont été configurées dans `config/constants.py` :
```python
# config/constants.py
DIM_GRID = (7, 6) # Dimension de la grille d'échecs (nombre de coins intérieurs par ligne et par colonne)
SQUARE_SIZE = 20 # Taille du carré en mm
```

**Q : À quoi correspondent ces deux variables ? Quelles informations importantes donnent-elles pour la calibration ?**  
- **DIM_GRID** : Représente le nombre de coins intérieurs du damier (Le nombre de cases diminue de 1 pour compter les arêtes, 8x7 devient 7x6 colonnes/lignes entières).
- **SQUARE_SIZE** : Représente la taille physique du côté d'un carré du damier, ici 20 mm.
Ces variables fournissent la "réalité terrain" (la géométrie exacte de l'objet) indispensable à OpenCV pour relier les pixels de l'image au référentiel du monde réel 3D. *(Réf : Documentation PiCamera2 pour la gestion des captures, et CM9 pour le traitement des caractéristiques de l'image)*.

**Q : Est-ce que la détection des coins est précise ? Au pixel près ?**  
Avec l'algorithme `cv2.findChessboardCorners`, la détection trouve initialement les coins en coordonnées entières "au pixel près". Bien que cela soit visuellement précis, l'approximation du pixel algorithmique est insuffisante pour obtenir une calibration parfaite (les matrices de transformations optiques ont besoin de repères purement mathématiques pour éviter des erreurs cumulées).

![Checkpoint 1](./code_from_rpi/code/im_capture_ecran_tp/camera_calibration_checkpoint_1-1.png)

### 3.2 Checkpoint 2
**Q : Que fait la fonction d’OpenCV cornerSubPix ?**  
Comme l'indique la doc officielle, `cv2.cornerSubPix` affine mathématiquement les positions entières des coins (trouvées à l'étape précédente) pour accroître fortement la précision en atteignant le niveau "sous-pixel" (sub-pixel accuracy). Elle évalue la distribution de l'image autour du coin pour atteindre un emplacement fractionnaire en décimale *(Réf : CM9 / OpenCV Documentation)*.

*Extrait du code (`core/calibration.py`) :*
```python
found, corners = cv2.findChessboardCorners(gray, (cols, rows), None)

if found:
    corners_refined = cv2.cornerSubPix(
        gray,
        corners,
        (11, 11),
        (-1, -1),
        criteria
    )
```

![Checkpoint 2: Coins Affinés](./code_from_rpi/code/im_capture_ecran_tp/camera_calibration_checkpoint_1et2.png)

**Q : Que contiennent les objets affichés `objp` et `corners_refined` ?**  
- **`objp`** : Contient le nuage de points théoriques, les coordonnées 3D réelles et physiques `(X, Y, Z=0)` des coins sur le plan du damier, calculées via les constantes `SQUARE_SIZE`.
- **`corners_refined`** : Contient les valeurs 2D décimales `(u, v)` de l'empreinte de ce damier sur la photo, obtenues par `cornerSubPix`.

### 3.3 Checkpoint 3
**Q : Combien d’images valides avez-vous eues ? Est-ce que les coins détectés étaient tous corrects ?**  
Sur toutes les poses enregistrées, le système a évalué les images et n'a conservé que les "images valides" pour l'intégration. Une image est gardée lorsque l'intégralité du nuage (`7x6=42` coins) est détecté correctement. Les coins étaient tous très propres, sans contorsion indésirable grâce aux conditions de visibilité (bonnes inclinaisons, bon éclairage, sans obstruction).

### 3.4 Checkpoint 4
**Q : À quoi correspondent chacune des variables retournées par la fonction `calibrateCamera` d’OpenCV ?**  
Selon la doc OpenCV et *(Le cours CM8 sur les matrices intrin/extrin)*, `cv2.calibrateCamera` nous retourne plusieurs paramètres fondamentaux :
- **`var1 (rms_error)`** : L'Erreur Quadratique Moyenne (Root Mean Square Reprojection Error). Donne l'écart moyen en pixels entre un point physique du damier re-projeté virtuellement sur la photo, et son emplacement réel de détection.
- **`var2 (camera_matrix)`** : La matrice des propriétés intrinsèques ($K$) de caméra (focus $fx, fy$ et centre optique effectif $cx, cy$).
- **`var3 (dist_coeffs)`** : Les coefficients paramétriques représentant la distorsion radiale de la lentille grand angle et la distorsion tangentielle d'alignement du capteur. *(Réf: RPi Camera Module 3 Product Brief qui aborde la structure physique optique de l'objectif)*.
- **`var4 (rvecs)`** : Les vecteurs de rotation pour cette position (paramètre extrinsèque posant la caméra dans l'espace pour chaque image).
- **`var5 (tvecs)`** : Les vecteurs de translation dans l'espace pour chaque image.

*Extrait du code (`core/calibration.py`) :*
```python
var1, var2, var3, var4, var5 = cv2.calibrateCamera(
    object_points,
    image_points,
    image_size,
    None,
    None
)
```

![Checkpoint 4 : Variables Matrice](./code_from_rpi/code/im_capture_ecran_tp/camera_calibration_checkpoint_4-1.png)
![Checkpoint 4 : Autres Variables](./code_from_rpi/code/im_capture_ecran_tp/camera_calibration_checkpoint_4-2.png)

**Q : Est-ce que votre calibration est bonne ? Quelle variable vous indique la qualité de votre calibration ?**  
C'est la variable `var1` (`rms_error`), qui nous indique une valeur typiquement inférieure à environ $1.0$. Plus sa valeur se rapproche de $0$, plus la calibration est excellente et modélise fidèlement et précisément le Raspberry Py Module 3.

![Matrice Sans Parametre](./code_from_rpi/code/im_capture_ecran_tp/camera_calibration_sans_parametre.png)

---

## 4. Correction

**Q : Comment la taille de l’image impacte la calibration de la caméra ?**  
La taille capturée impacte directement la dimension en pixel du champ optique de la caméra. Les variables de la matrice intrinsèque ($fx, fy, cx, cy$) calculées précédemment ont pour unité le pixel de résolution de travail. Si la taille d'image d'acquisition change `CAMERA_RESOLUTION`, l'échelle n'est plus la même et la matrice, calculée sans mise à l'échelle, générera une dé-distorsion abrupte, faussée voire inutile, écrasant les bords par de larges lignes noires. Il faut impérativement accorder les résolutions de l'undistortion aux images initiales ! *(Réf. CM8 sur les plans cartographiques et points d'images associés)*.

*Extrait du code (`core/calibration.py`) :*
```python
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, dist_coeffs, (w, h), 1, (w, h)
)

undistorted = cv2.undistort(
    image, camera_matrix, dist_coeffs, None, new_camera_matrix
)
```

![Comparaison Undistorsion avec bonne Calibration](./code_from_rpi/code/im_capture_ecran_tp/undistorsion_comparasion.png)

_L'effet d'une matrice qui a foiré due à un mauvais paramétrage :_

![Mauvaise Calibration Undistortion 1](./code_from_rpi/code/im_capture_ecran_tp/undistorsion_comparision_mal_calibré-1.png)
![Mauvaise Calibration Undistortion 2](./code_from_rpi/code/im_capture_ecran_tp/undistorsion_comparision_mal_calibré-2.png)

---

## 5. Dans le mille ! - Cible et Marqueur

![Aperçu de la cible à viser](./code_from_rpi/code/im_capture_ecran_tp/cible.jpg)

### 5.4 Calcul du score obtenu

**(Détection cible et extraction HSV du marqueur)**
Le code permet de modéliser le cercle parfait extérieur puis on analyse l'impact vert qui servira de marqueur. 
L'espace HSV modélise les couleurs en dissociant la couleur même de la luminosité (Teinte, Saturation, Valeur). Ceci est fondamental et assure une très grande efficience car les variations d'éblouissement du TP dans la salle n'affectent pas la teinte verte. *(Réf : CM9 / Espace Colorimétrique)*.

*Extrait du code (`scripts/target_scoring.py`) :*
```python
# Tracé du lien entre le marqueur et la cible
draw_target_marker_link(display, center_target, marker_center)

# Calcul distance et score
dist_px = math.dist(center_target, marker_center)
ratio_cm_per_px = TARGET_DIAMETER_CM / (2 * radius_pixel)
dist_cm = dist_px * ratio_cm_per_px

max_radius_cm = TARGET_DIAMETER_CM / 2
zone_width_cm = max_radius_cm / 10

if dist_cm > max_radius_cm:
    score = 0
else:
    score = 10 - int(dist_cm / zone_width_cm)
    if score <= 0:
        score = 1
```

![Détection couleur verte](./code_from_rpi/code/im_capture_ecran_tp/detection_vert.png)

**Q : Est-ce que la détection est robuste ? Est-ce que le score obtenu est correct ?**  
Oui, une fois la distorsion optique corrigée, l'image correspond aux dimensions mathématiques planes du monde réel. Le cercle détecté correspond ainsi sur toute sa surface à une unité paramétrique égale. L'algorithme se sert du diamètre de l'objet de référence en cm `TARGET_DIAMETER_CM` pour créer une corrélation au ratio `CM/Pixel`. Cette dimension calculée par le rayon, croisée avec le masque de détection colorimétrique robuste HSV, crée une vraie certitude du repère et la distance Euclidienne devient infaillible.  Le score est donc exact. Un marqueur très sombre ou masqué, et dont la Teinte sort de l'intervalle configuré pourrait néanmoins perturber l'algorithme.

![Résultat final : Cible, Score et Distances](./code_from_rpi/code/im_capture_ecran_tp/cible_distance_score_un_impact.png)

---

## 6. Ajout : Problèmes de dépendances MediaPipe (capture_pinch)

L'utilisation de Mediapipe (qui réalise le Hand Tracking pour la feature de pincement dans `capture_pinch`) a soulevé des conflits de paquets limitant son intégration aboutie lors de cette séance dans l'environnement virtuel (`.venv`) du Raspberry Pi. 

**Recommandations pour la prochaine fois afin d'éviter ces conflits d'environnement :**

1. **Création d'un environnement restreint et neuf** : Privilégier la création d'un second `.venv` complètement isolé pour des packages lourds et capricieux comme mediapipe avec la commande `python -m venv mediapipe_env --clear`.
2. **Utiliser des "wheels" précompilés pour ARM** : Les librairies complexes sur Raspberry Pi rencontrent des soucis de compilation C++. Cherchez s'il existe des "wheels" `.whl` précompilés pour l'architecture ARM64 `aarch64` fournis par la communauté (souvent disponibles via l'outil `piwheels`). 
3. **Paramètre "no-cache" lors de l'installation** : Lors de l'installation des dépendances (`pip install mediapipe opencv-python`), utilisez l'option `--no-cache-dir`. Le cache de pip garde parfois des sous-versions conflictuelles ou corrompues.
4. **Isoler les requirements** : Éviter d'installer tous les paquets dans l'environnement global d'un coup. Utiliser un fichier `requirements_mediapipe.txt` dédié spécifiquement à  ce script, et vérifier qu'il ne rentre pas en collision avec les versions de NumPy d'OpenCV préalablement installées.
