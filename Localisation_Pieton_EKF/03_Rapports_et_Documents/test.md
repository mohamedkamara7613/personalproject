- Interférences magnétiques majeures : Magnétomètre inutilisable en milieu urbain / perturbations internes de la carte. $\rightarrow$ Solution : Abandon total du magnétomètre. Architecture EKF purement cinématique reposant sur l'intégration du gyroscope pour le cap.

- Dérive exponentielle de l'accéléromètre : La double intégration de l'accélération (bruitée + gravité) rendait la position aberrante en quelques secondes. $\rightarrow$ Solution : Arrêt de l'intégration spatiale. L'accéléromètre sert uniquement à adapter dynamiquement la variance du bruit de marche (matrice $Q$).

- Absence de vitesse native GPS : Le script d'acquisition final n'enregistrait pas la vitesse Doppler (la plus fiable). $\rightarrow$ Solution : Calcul de la vitesse scalaire $v$ par dérivation spatiale entre deux trames GPS dans le script de post-traitement.

- Sauts de position GPS (Effet Multipath) : Erreurs brutales de localisation dues aux reflets urbains, entraînant l'EKF. $\rightarrow$ Solution : Mise en place d'un filtre anti-outliers (Validation Gate) basé sur la distance de Mahalanobis, rejetant statistiquement toute donnée $> \chi^2$.

Interférences magnétiques majeures : Magnétomètre inutilisable en milieu urbain / perturbations internes de la carte. → Solution : Abandon total du magnétomètre. Architecture EKF purement cinématique reposant sur l'intégration du gyroscope pour le cap.

Dérive exponentielle de l'accéléromètre : La double intégration de l'accélération (bruitée + gravité) rendait la position aberrante en quelques secondes. → Solution : Arrêt de l'intégration spatiale. L'accéléromètre sert uniquement à adapter dynamiquement la variance du bruit de marche (matrice Q).

Absence de vitesse native GPS : Le script d'acquisition final n'enregistrait pas la vitesse Doppler (la plus fiable). → Solution : Calcul de la vitesse scalaire v par dérivation spatiale entre deux trames GPS dans le script de post-traitement.

Sauts de position GPS (Effet Multipath) : Erreurs brutales de localisation dues aux reflets urbains, entraînant l'EKF. → Solution : Mise en place d'un filtre anti-outliers (Validation Gate) basé sur la distance de Mahalanobis, rejetant statistiquement toute donnée > Chi².