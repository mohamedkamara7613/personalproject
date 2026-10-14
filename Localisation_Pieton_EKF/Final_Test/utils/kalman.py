import numpy as np

class KalmanFilter:
    def __init__(self, initial_x, initial_y, var_accel, var_gps, dt_imu=0.01, R=None, Q=None):
        """
        Initialise le filtre de Kalman pour une fusion IMU/GPS 2D.
        
        :param initial_x: Position X de départ (m)
        :param initial_y: Position Y de départ (m)
        :param dt_imu: Pas de temps par défaut de l'IMU en secondes  0.01 pour 100H
        :param var_accel: Variance de l'accélération mesurée
        :param var_gps: Variance de la position mesurée
        """
        # Vecteur d'état X = [x, y, vx, vy]^T
        self.X = np.array([
            [initial_x],
            [initial_y],
            [0.0],
            [0.0]
        ], dtype=float)
        
        # Matrice de Covariance de l'état P (Incertitude initiale)
        self.P = np.eye(4) * 1.0 
        
        self.dt = dt_imu
        self.var_accel = var_accel
        self.var_gps = var_gps
        
        # Matrice d'Observation H, il  n'y a que x et y qui nous interresse ici
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=float)
        
        # Matrice de Bruit de Mesure R (Confiance dans le GPS)
        if R is None:
            self.R = np.array([
                [self.var_gps, 0],
                [0, self.var_gps]
            ], dtype=float)
        else:
            self.R = R
        
        # Matrice Identité 4x4
        self.I = np.eye(4)
        
        # Sauvegarde de la matrice Q manuellement
        self.user_defined_Q = Q

    def _update_matrices(self, dt):
        """ Met à jour les matrices F, B et Q en fonction du dt (temps écoulé) actuel """
        # Matrice de Transition F
        self.F = np.array([
            [1, 0, dt, 0 ],
            [0, 1, 0,  dt],
            [0, 0, 1,  0 ],
            [0, 0, 0,  1 ]
        ], dtype=float)
        
        # Matrice de Contrôle B
        self.B = np.array([
            [0.5 * dt**2, 0          ],
            [0,           0.5 * dt**2],
            [dt,          0          ],
            [0,           dt         ]
        ], dtype=float)
        
        # Matrice de Bruit de Processus Q
        # Q = var_accel * (B @ B^T) si non fournie manuellement
        if self.user_defined_Q is not None:
            self.Q = self.user_defined_Q
        else:
            self.Q = self.var_accel * (self.B @ self.B.T)
        
    def predict(self, ax, ay, dt=None):
        """
        Étape 1 : Prédiction avec l'IMU.
        À appeler à chaque fois qu'une nouvelle donnée IMU arrive.
        
        :param ax: Accélération en X (m/s^2)
        :param ay: Accélération en Y (m/s^2)
        :param dt: Temps écoulé depuis la dernière prédiction (optionnel)
        """
        if dt is not None:
            self._update_matrices(dt)
        else:
            self._update_matrices(self.dt)
            
        # Vecteur de commande U
        U = np.array([[ax], [ay]], dtype=float)
        
        # 1. Prédiction de l'état
        self.X = self.F @ self.X + self.B @ U
        
        # 2. Prédiction de la covariance
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.X

    def update(self, gps_x, gps_y, maha_threshold=9.21):
        """
        Étape 2 : Correction avec le GPS.
        À appeler à chaque fois qu'une nouvelle donnée GPS arrive.
        
        :param gps_x: Position locale X donnée par le GPS (m)
        :param gps_y: Position locale Y donnée par le GPS (m)

        Diapo 48-49 du cours 
        """
        # Vecteur de mesure Z
        Z = np.array([[gps_x], [gps_y]], dtype=float)
        
        # 1. Calcul de l'Innovation
        Y = Z - (self.H @ self.X)
        
        # 2. Covariance de l'innovation
        S = self.H @ self.P @ self.H.T + self.R
        
        # maha = Y^T * S^-1 * Y
        maha = Y.T @ np.linalg.inv(S) @ Y
        maha_value = maha[0, 0] # valeur scalaire
        
        if maha_value > maha_threshold:
            # Rejet de la donnée GPS  on garde la prédiction de l'IMU intacte, o
            return self.X, False # False signifie "GPS rejeté"
        
        # 3. Calcul du Gain de Kalman
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # 4. Mise à jour de l'état
        self.X = self.X + (K @ Y)
        
        # 5. Mise à jour de la covariance
        self.P = (self.I - K @ self.H) @ self.P
        
        return self.X, True # True GPS accepté

    def get_state(self):
        """ Retourne l'état actuel sous forme de dictionnaire pour faciliter la lecture """
        return {
            "x": self.X[0, 0],
            "y": self.X[1, 0],
            "vx": self.X[2, 0],
            "vy": self.X[3, 0]
        }

class EKFSansMagneto:
    def __init__(self, x0, y0, theta0, sigma_omega=0.01):
        """
        EKF pour Piéton (Modèle Cinématique sans Magnétomètre).
        État : [X_est, Y_nord, Theta_cap]
        """
        self.x = np.array([x0, y0, theta0])
        self.P = np.diag([1.0, 1.0, 0.1])
        self.sigma_omega = sigma_omega

    def predict(self, v, omega, dt, sigma_a):
        theta = self.x[2]
        
        # Prédiction de l'état
        self.x[0] += v * np.cos(theta) * dt
        self.x[1] += v * np.sin(theta) * dt
        self.x[2] += omega * dt
        
        # Normalisation de l'angle entre -pi et pi
        self.x[2] = (self.x[2] + np.pi) % (2 * np.pi) - np.pi

        # Jacobienne F
        F = np.eye(3)
        F[0, 2] = -v * np.sin(theta) * dt
        F[1, 2] =  v * np.cos(theta) * dt

        # Bruit de processus (Q)
        var_v = (sigma_a * dt)**2
        var_theta = (self.sigma_omega * dt)**2
        
        Q = np.zeros((3, 3))
        Q[0, 0] = var_v * (np.cos(theta) * dt)**2
        Q[1, 1] = var_v * (np.sin(theta) * dt)**2
        Q[2, 2] = var_theta
        
        self.P = F @ self.P @ F.T + Q

    def update(self, z_x, z_y):
        """Mise à jour avec la position GPS"""
        H = np.array([[1.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0]])
        
        R = np.array([[2.0**2, 0],
                      [0, 2.0**2]])
                      
        z = np.array([z_x, z_y])
        y_innov = z - self.x[0:2]
        
        S = H @ self.P @ H.T + R
        
        # Filtre anti-aberration (Mahalanobis)
        maha_dist = y_innov.T @ np.linalg.inv(S) @ y_innov
        if maha_dist > 9.21:
            return False

        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y_innov
        self.x[2] = (self.x[2] + np.pi) % (2 * np.pi) - np.pi
        self.P = (np.eye(3) - K @ H) @ self.P
        return True

    def get_state(self):
        """Retourne l'état actuel sous forme de dictionnaire (Compatibilité)"""
        return {
            "x": self.x[0],
            "y": self.x[1]
        }
