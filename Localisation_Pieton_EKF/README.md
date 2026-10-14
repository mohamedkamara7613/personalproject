# 📍 Localisation Piéton & Fusion Stochastique de Capteurs (EKF)

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scientific](https://img.shields.io/badge/Stack-NumPy_%7C_SciPy_%7C_Folium-013243?style=for-the-badge)](https://numpy.org/)
[![Algorithm](https://img.shields.io/badge/Algorithm-Extended_Kalman_Filter-blueviolet?style=for-the-badge)](#)

Système de **localisation piéton haute précision** par fusion stochastique de données hétérogènes (**GPS + IMU 9-DOF + Odométrie**), développé à l'**INSA Rouen Normandie** (Département ISIA).  
L'enjeu est de reconstruire une trajectoire continue et robuste en milieu urbain dense (canyons urbains, passages sous porches) où le GPS subit des coupures sévères et du multitrajets (*multipath*).

---

## 🔬 Formulation Mathématique du Filtre (EKF)

### 1. Vecteur d'État Cinématique
L'état du piéton dans le repère local NED (*North-East-Down*) est modélisé par :
$$\mathbf{x}_k = \begin{bmatrix} p_N \\ v_N \\ p_E \\ v_E \end{bmatrix}_k$$

### 2. Équation de Transition & Bruit de Procédé $\mathbf{Q}$
Avec une hypothèse de vitesse quasi-constante soumise à des accélérations stochastiques :
$$\mathbf{x}_{k+1} = \mathbf{F} \mathbf{x}_k + \mathbf{w}_k, \quad \mathbf{w}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{Q}(dt))$$

La matrice de covariance de bruit de procédé $\mathbf{Q}$ est calibrée expérimentalement à partir des variances de l'accéléromètre en mouvement :
$$\mathbf{Q}(dt) = \sigma_a^2 \begin{bmatrix} \frac{\Delta t^4}{4} & \frac{\Delta t^3}{2} & 0 & 0 \\ \frac{\Delta t^3}{2} & \Delta t^2 & 0 & 0 \\ 0 & 0 & \frac{\Delta t^4}{4} & \frac{\Delta t^3}{2} \\ 0 & 0 & \frac{\Delta t^3}{2} & \Delta t^2 \end{bmatrix}, \quad \sigma_a = 0.8596\text{ m/s}^2$$

### 3. Gating de Mahalanobis pour le Rejet d'Outliers
Les sauts de position aberrants dus à des réflexions satellites ou trames NMEA corrompues sont rejetés grâce à la distance statistique de Mahalanobis :
$$D_M^2 = (\mathbf{z}_k - \mathbf{H}\hat{\mathbf{x}}_k^-)^T \mathbf{S}_k^{-1} (\mathbf{z}_k - \mathbf{H}\hat{\mathbf{x}}_k^-) < \gamma$$
Pour 2 degrés de liberté à un niveau de confiance de $99\%$, le seuil est fixé à $\gamma = 9.21$. En cas de dépassement, la mesure GPS est ignorée et la trajectoire est propagée par la dynamique pure du modèle cinématique.

---

## 📊 Visualisations & Analyse des Signaux

| Analyse Accélérométrique IMU (Axe X) | Modélisation Boussole & Orientation |
| :---: | :---: |
| ![Signaux IMU](./04_Cartographie_et_Images/diagramme_imu_axe_x.png) | ![Modèle Boussole](./04_Cartographie_et_Images/model_boussole.png) |

---

## 🚀 Exécution & Rendu Cartographique

### 1. Installation des dépendances
```bash
pip install numpy pandas folium scipy matplotlib
```

### 2. Lancer la fusion et générer la carte interactive
```bash
python3 kalman_gps_imu.py
```
Le script génère une carte interactive HTML (`carte_trajectoire.html`) visualisable dans n'importe quel navigateur, comparant :
- **Trace GPS brute (rouge) :** Bruitée, avec décrochages urbains.
- **Trace GPS nettoyée (orange) :** Après filtrage IQR et élimination des trames aberrantes.
- **Trajectoire estimée par l'EKF (bleue) :** Lisse, continue et fidèle au parcours réel.

---

## 📑 Rapport Technique & Documents Scientifiques
- 📄 [Consulter le Rapport de Fusion Capteurs & EKF (PDF)](./docs/Rapport_Fusion_EKF.pdf)
- 📊 [Consulter la Présentation de Fusion Stochastique & Filtrage de Kalman (PDF)](./03_Rapports_et_Documents/Beamer_Capteur_CM6_Kalman.pdf)
