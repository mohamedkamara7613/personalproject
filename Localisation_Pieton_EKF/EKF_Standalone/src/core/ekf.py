# core/ekf.py
import numpy as np

class ArpenteurEKF:
    def __init__(self, lat_ori, lon_ori, R_gps, sigma_omega, sigma_mag):
        self.lat_origin = lat_ori
        self.lon_origin = lon_ori
        self.X = np.zeros((3, 1))
        self.P = np.eye(3) * 1.0
        self.R_GPS = R_gps
        self.var_mag = sigma_mag**2
        self.sigma_omega = sigma_omega

    def predict(self, v, omega, dt):
        """
        Étape de prédiction (Non linéaire)
        u = [v, omega] (vitesse estimée par le pas et vitesse angulaire du gyro)
        """
        theta = self.X[2, 0]

        # 1. Équation de transition non linéaire f(x, u)
        self.X[0, 0] += v * dt * np.cos(theta)
        self.X[1, 0] += v * dt * np.sin(theta)
        self.X[2, 0] += omega * dt
        # Normalisation de l'angle entre -pi et pi
        self.X[2, 0] = (self.X[2, 0] + np.pi) % (2 * np.pi) - np.pi

        # 2. Jacobienne de f par rapport à l'état X (Matrice A ou F_x)
        F_x = np.array([
            [1.0, 0.0, -v * dt * np.sin(theta)],
            [0.0, 1.0, v * dt * np.cos(theta)],
            [0.0, 0.0, 1.0]
        ])

        # 3. Jacobienne de f par rapport au bruit de commande (Matrice Gamma)
        Gamma = np.array([
            [dt * np.cos(theta), 0.0],
            [dt * np.sin(theta), 0.0],
            [0.0, dt]
        ])

        # Covariance du bruit de commande
        # On estime la variance sur la vitesse linéaire et la vitesse angulaire
        Q_u = np.array([
            [0.25, 0.0],  # Incertitude sur l'estimation de la vitesse du marcheur
            [0.0, self.sigma_omega ** 2]
        ])

        Q = Gamma @ Q_u @ Gamma.T

        # 4. Mise à jour de la covariance de l'état
        self.P = F_x @ self.P @ F_x.T + Q

    def update_gps(self, x_meas, y_meas):
        """Correction par le point GPS (Mesure de x et y)"""
        Z = np.array([[x_meas], [y_meas]])
        H = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ])

        Y = Z - H @ self.X
        S = H @ self.P @ H.T + self.R_GPS
        K = self.P @ H.T @ np.linalg.inv(S)

        self.X = self.X + K @ Y
        self.P = (np.eye(3) - K @ H) @ self.P

    def update_mag(self, theta_mag):
        """Correction par la boussole (Mesure directe de theta)"""
        Z = np.array([[theta_mag]])
        H = np.array([[0.0, 0.0, 1.0]])

        # Gestion du saut de phase de l'innovation (entre -pi et pi)
        Y = Z - H @ self.X
        Y[0, 0] = (Y[0, 0] + np.pi) % (2 * np.pi) - np.pi

        S = H @ self.P @ H.T + self.var_mag
        K = self.P @ H.T / S[0, 0]

        self.X = self.X + K @ Y
        self.P = (np.eye(3) - K @ H) @ self.P