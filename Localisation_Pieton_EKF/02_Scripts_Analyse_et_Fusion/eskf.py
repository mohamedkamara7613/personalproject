import numpy as np

# --- Utilitaires Quaternions ---
def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def rotate_vector(q, v):
    q_v = np.array([0, v[0], v[1], v[2]])
    res = quat_mult(quat_mult(q, q_v), quat_inv(q))
    return res[1:]

def quat_from_rotvec(r):
    theta = np.linalg.norm(r)
    if theta < 1e-8:
        return np.array([1.0, 0.0, 0.0, 0.0])
    axis = r / theta
    q = np.array([
        np.cos(theta/2.0),
        axis[0]*np.sin(theta/2.0),
        axis[1]*np.sin(theta/2.0),
        axis[2]*np.sin(theta/2.0)
    ])
    return q

def skew_symmetric(v):
    """Génère la matrice antisymétrique pour un vecteur 3D."""
    return np.array([
        [ 0,    -v[2],  v[1]],
        [ v[2],  0,    -v[0]],
        [-v[1],  v[0],  0   ]
    ])

def quat_to_matrix(q):
    """Convertit un quaternion en matrice de rotation 3x3."""
    w, x, y, z = q
    return np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w,       2*x*z + 2*y*w],
        [2*x*y + 2*z*w,       1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,       2*y*z + 2*x*w,       1 - 2*x**2 - 2*y**2]
    ])

class ESKF:
    def __init__(self, init_p, init_v, init_q, var_acc, var_gyro, var_gps):
        """
        Error-State Kalman Filter pour fusion IMU (100Hz) / GPS (1Hz)
        État nominal: p (3), v (3), q (4)
        État d'erreur (9D): dp (3), dv (3), dtheta (3)
        """
        self.p = np.array(init_p, dtype=float)  # Position (E, N, U)
        self.v = np.array(init_v, dtype=float)  # Vitesse (E, N, U)
        self.q = np.array(init_q, dtype=float)  # Orientation quaternion (w, x, y, z)
        
        self.P = np.eye(9) * 1.0  # Covariance de l'état d'erreur (9x9)
        self.g = np.array([0.0, 0.0, -9.80665])  # Gravité vers le bas
        
        # Bruits IMU (Densités spectrales continues)
        self.var_acc = var_acc
        self.var_gyro = var_gyro
        
        # Bruit GPS (Mesure)
        self.R_gps = np.diag([var_gps, var_gps]) # On mesure seulement l'Est et le Nord
        
        # Matrice d'observation H (9x9 d'état vers 2D de mesure GPS)
        self.H = np.zeros((2, 9))
        self.H[0, 0] = 1.0  # Mesure p_x (Est)
        self.H[1, 1] = 1.0  # Mesure p_y (Nord)

    def predict(self, acc, gyro, dt):
        """
        Prédiction de l'état nominal via la cinématique (IMU)
        acc: [ax, ay, az] dans le body frame (m/s^2)
        gyro: [wx, wy, wz] dans le body frame (rad/s)
        """
        # 1. Mise à jour de l'état nominal
        R = quat_to_matrix(self.q)
        acc_nav = R @ acc + self.g # projeter acc dans repère global et retirer gravité
        
        self.p = self.p + self.v * dt + 0.5 * acc_nav * dt**2
        self.v = self.v + acc_nav * dt
        
        dq = quat_from_rotvec(gyro * dt)
        self.q = quat_mult(self.q, dq)
        self.q /= np.linalg.norm(self.q) # Normalisation
        
        # 2. Mise à jour de la Covariance P de l'état d'erreur
        # Matrice de transition de l'état d'erreur F_x (9x9)
        F_x = np.eye(9)
        F_x[0:3, 3:6] = np.eye(3) * dt
        F_x[3:6, 6:9] = -skew_symmetric(R @ acc) * dt
        
        # Matrice de bruit de processus Q (9x9)
        Q = np.zeros((9, 9))
        Q[3:6, 3:6] = np.eye(3) * (self.var_acc * dt**2)
        Q[6:9, 6:9] = np.eye(3) * (self.var_gyro * dt**2)
        
        self.P = F_x @ self.P @ F_x.T + Q

    def update_gps(self, gps_p):
        """
        Correction via GPS
        gps_p: [gps_east, gps_north]
        """
        # 1. Calcul de l'erreur (Innovation)
        z = np.array(gps_p)
        h_nominal = np.array([self.p[0], self.p[1]])
        y = z - h_nominal
        
        # 2. Calcul du gain de Kalman K
        S = self.H @ self.P @ self.H.T + self.R_gps
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Filtre de Mahalanobis optionnel pour rejeter les sauts
        maha = y.T @ np.linalg.inv(S) @ y
        if maha > 15.0:  # Seuil de rejet
            return False
        
        # 3. Calcul de l'état d'erreur
        error_state = K @ y
        dp = error_state[0:3]
        dv = error_state[3:6]
        dtheta = error_state[6:9]
        
        # 4. Reset: Injection de l'erreur dans l'état nominal
        self.p = self.p + dp
        self.v = self.v + dv
        
        dq_err = quat_from_rotvec(dtheta)
        self.q = quat_mult(dq_err, self.q) # Multiplication à gauche pour le frame global
        self.q /= np.linalg.norm(self.q)
        
        # 5. Mise à jour de la matrice P
        I_KH = np.eye(9) - K @ self.H
        self.P = I_KH @ self.P @ I_KH.T + K @ self.R_gps @ K.T
        
        return True
