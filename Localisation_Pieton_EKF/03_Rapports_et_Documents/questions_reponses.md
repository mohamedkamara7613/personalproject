# Réponses aux Questions Ouvertes — EKF Piéton GPS/IMU

## Q1 : La matrice R est-elle estimée ou calibrée ?

**Réponse : Calibrée sur données réelles, réutilisée directement.**

Dans `get_IMU_GPS.py` (ligne 81) :
```python
R_calibree = np.diag([1.20, 0.07])  # [x=Est, y=Nord] en m²
```
Cette matrice n'est **pas symétrique** : le GPS est ~17× plus précis en latitude (Nord, 0.07 m²) qu'en longitude (Est, 1.20 m²). Cette asymétrie est typique d'un capteur GNSS en conditions de multipath (bâtiments, arbres). La valeur a été obtenue lors d'une séance de calibration statique dédiée. **On la réutilise telle quelle dans notre EKF.**

> Pour une future acquisition, si les conditions de réception GPS changent (zone très urbaine, ciel dégagé), une recalibration peut être demandée à l'équipe.

---

## Q2 : Les valeurs de Q sont-elles estimées ou calibrées ?

**Réponse : Q est recalculée à chaque intervalle GPS (approche adaptive).**

Le paramètre de base `sigma_a = 0.8596 m/s²` vient de `get_IMU_GPS.py` (ligne 80). Mais on ne l'utilise pas comme valeur fixe. La fonction `compute_sigma_a()` calcule le **RMS de l'accélération horizontale IMU** sur chaque intervalle GPS :

```
sigma_a(k) = sqrt( mean( (aY² + aZ²) ) )  pour les trames IMU entre GPS[k-1] et GPS[k]
```

Résultat sur notre acquisition : min=0.574, moy=2.246, max=5.000 m/s².
Cela signifie que Q "gonfle" dynamiquement quand le piéton accélère ou tourne, et "rétrécit" quand il marche en ligne droite. **C'est exactement le comportement souhaité : on fait moins confiance au modèle (plus grand Q) quand le mouvement est irrégulier.**

> Si on veut recalibrer, il faut refaire une acquisition avec un IMU immobile et mesurer la variance résiduelle du bruit propre du capteur. L'équipe peut le faire.

---

## Q3 : La vitesse v — intégration ou GPS direct ?

**Réponse : GPS direct. On ne fait aucune intégration d'accéléromètre pour la position ou la vitesse.**

```python
v[k] = |delta_position_GPS| / delta_t
     = sqrt( (x_gps[k] - x_gps[k-1])² + (y_gps[k] - y_gps[k-1])² ) / dt
```

Cette approche est **robuste** : pas de drift, pas d'accumulation d'erreur. Le seul risque est le bruit GPS à faible vitesse (quand le piéton est quasi-immobile, le GPS bouge quand même de ~1m → v artificielle). C'est géré par le modèle EKF qui lisse ces petites variations.

**Option future :** Demander à l'équipe d'ajouter la vitesse NMEA (`Speed over Ground`) dans les données GPS. Le GPS calcule lui-même la vitesse depuis l'effet Doppler de la porteuse, ce qui est plus précis que notre delta-position. Une combinaison des deux (moyenne pondérée) serait idéale.

---

## Q4 : Le nettoyage GPS rate-t-il des outliers ?

**Réponse : Oui, et c'est normal. On a deux étages de protection.**

Le filtre IQR (pré-Kalman) élimine les points géographiquement très éloignés de la médiane. Mais certains outliers "discrets" (quelques dizaines de mètres de décalage) passent ce filtre car ils sont statistiquement proches du nuage de points.

La **gate de Mahalanobis** (dans l'EKF) est le 2ème étage : elle rejette les points incohérents avec l'état prédit par le filtre. Sur notre acquisition : **15 points rejetés** (visible en orange sur la carte), dont les 3 outliers résiduels identifiés visuellement.

**Remarque de ta critique :** "Pour ce jeu de données" — c'est juste. Les seuils actuels (IQR ×1.5 et chi² 99%) sont des compromis. Sur un jeu de données différent (pluie, bâtiments), il faudrait potentiellement ajuster le seuil Mahalanobis ou ajouter un filtre de vitesse (`v > 5 m/s pendant marche → rejet`).

---

## Q5 : Faut-il l'IMU, ou le GPS seul suffit-il ?

**Réponse : Le GPS seul suffirait pour la position, mais l'IMU apporte deux choses essentielles.**

1. **Q adaptive** : L'IMU permet de moduler l'incertitude du modèle à chaque pas. Sans IMU, on utilise une Q fixe (moins précis dans les phases de forte accélération).
2. **ω (vitesse de rotation)** : Le cap θ est contraint par le gyroscope. Sans lui, on n'aurait que `v` du GPS et pas d'information sur les rotations → la prédiction du cap serait purement extrapolée, moins précise dans les virages.

**Verdict :** Le GPS seul avec Kalman linéaire (modèle vitesse constante, comme dans `kalman_gps_imu.py`) donne déjà un bon lissage. L'EKF piéton avec le Gyro apporte une meilleure gestion des virages et une Q adaptive. **Pour la suite : garder l'EKF piéton.**

---

## Q6 : Décalage GPS/Strava de 44m — d'où vient-il ?

**Réponse : Très probablement le "cold start" GPS.**

Le GPS a besoin de plusieurs dizaines de secondes pour acquérir les satellites et calculer une position précise. Les ~15 premières secondes sont retirées (`filtre 3` dans `clean_gps()`), mais si le lock GPS a mis plus de temps, le premier point "propre" peut encore être décalé.

**Observation** : La forme du parcours est cohérente entre GPS et Strava (même boucle, même direction). Il ne s'agit donc pas d'une erreur de cap ou de qualité GPS, juste d'un décalage spatial à l'origine. Pour les futures acquisitions, **attendre que le GPS soit stable avant de commencer à marcher** (observer les premières coordonnées, attendre qu'elles ne bougent plus).

---

## Q7 : L'orientation du capteur est-elle toujours la même ?

**Réponse : Non, et c'est un problème réel à adresser.**

Dans notre code, on exploite le fait que `Gyro_X` = vitesse angulaire verticale (axe Up). Cela repose sur le fait que l'axe X du capteur pointe vers le haut, ce qu'on a vérifié empiriquement (`Accel_X_moyen ≈ +1g`).

Si la plaque est tenue différemment lors d'une future acquisition, l'axe Up peut changer. **Solution propre (à implémenter) :**

```python
# Détection automatique de l'axe vertical
accel_mean = imu[['Accel X','Accel Y','Accel Z']].iloc[:200].mean().abs()
vertical_axis = accel_mean.idxmax()   # 'Accel X', 'Accel Y', ou 'Accel Z'
gyro_axis = 'Gyro ' + vertical_axis[-1]  # 'Gyro X', 'Gyro Y', ou 'Gyro Z'
```

Ainsi le code s'adapte automatiquement à la façon de tenir la plaque.

---

## Résultat actuel et prochaines étapes

### Ce qu'on a obtenu
- ✅ EKF piéton fonctionnel, résultat cohérent avec Strava
- ✅ Outliers GPS éliminés (2 étages : IQR + Mahalanobis)
- ✅ Matrices R et Q calibrées / adaptatives
- ✅ Zéro intégration d'accéléromètre pour la position

### Critiques légitimes et pistes d'amélioration
- ⚠️ Le décalage de 44m avec Strava : impossible à corriger sans recalage temporel précis
- ⚠️ Sur d'autres jeux de données, les seuils de rejet pourraient nécessiter un ajustement
- ⚠️ La vitesse `v` depuis le delta-GPS est bruitée à faible vitesse → demander le `Speed` NMEA
- ⚠️ L'axe vertical du capteur devrait être auto-détecté pour robustesse
