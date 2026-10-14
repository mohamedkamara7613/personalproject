import numpy as np

def R_matrix(phi, theta, psi):
    """Matrice de rotation du Body frame vers le Nav frame (ENU)"""
    # R_z(psi) * R_y(theta) * R_x(phi)
    c_phi, s_phi = np.cos(phi), np.sin(phi)
    c_th, s_th = np.cos(theta), np.sin(theta)
    c_psi, s_psi = np.cos(psi), np.sin(psi)
    
    R = np.array([
        [c_psi*c_th, c_psi*s_th*s_phi - s_psi*c_phi, c_psi*s_th*c_phi + s_psi*s_phi],
        [s_psi*c_th, s_psi*s_th*s_phi + c_psi*c_phi, s_psi*s_th*c_phi - c_psi*s_phi],
        [-s_th,      c_th*s_phi,                     c_th*c_phi]
    ])
    return R

def euler_rates(phi, theta, psi, wx, wy, wz):
    """Calcul des dérivées des angles d'Euler"""
    # Protection contre gimbal lock (theta = 90 deg)
    c_th = np.cos(theta)
    if np.abs(c_th) < 1e-4:
        c_th = 1e-4 * np.sign(c_th)
        
    t_th = np.tan(theta)
    s_phi, c_phi = np.sin(phi), np.cos(phi)
    
    d_phi = wx + s_phi*t_th*wy + c_phi*t_th*wz
    d_th = c_phi*wy - s_phi*wz
    d_psi = (s_phi/c_th)*wy + (c_phi/c_th)*wz
    
    return np.array([d_phi, d_th, d_psi])

def state_transition(X, u, dt):
    """
    Fonction de transition d'état non-linéaire f(X, u).
    X = [x, y, vx, vy, phi, theta, psi]
    u = [ax, ay, az, wx, wy, wz]
    """
    x, y, vx, vy, phi, theta, psi = X
    ax, ay, az, wx, wy, wz = u
    
    # 1. Orientation
    d_euler = euler_rates(phi, theta, psi, wx, wy, wz)
    phi_new = phi + d_euler[0] * dt
    theta_new = theta + d_euler[1] * dt
    psi_new = psi + d_euler[2] * dt
    
    # 2. Accélération
    R = R_matrix(phi_new, theta_new, psi_new) # Utilise la nouvelle orientation pour l'accel
    acc_body = np.array([ax, ay, az])
    acc_nav = R @ acc_body
    
    # Retirer la gravité (9.81 sur l'axe Z, Up)
    # L'accéléromètre mesure g vers le haut au repos, donc on soustrait
    acc_lin = acc_nav - np.array([0.0, 0.0, 9.80665])
    
    # 3. Position et Vitesse
    x_new = x + vx * dt + 0.5 * acc_lin[0] * dt**2
    y_new = y + vy * dt + 0.5 * acc_lin[1] * dt**2
    vx_new = vx + acc_lin[0] * dt
    vy_new = vy + acc_lin[1] * dt
    
    return np.array([x_new, y_new, vx_new, vy_new, phi_new, theta_new, psi_new])

class EKF:
    def __init__(self, init_X, var_acc, var_gyro, var_gps):
        """
        EKF (Extended Kalman Filter) standard.
        État X (7D) = [x, y, vx, vy, phi, theta, psi]
        """
        self.X = np.array(init_X, dtype=float)
        self.P = np.eye(7) * 1.0
        
        self.var_acc = var_acc
        self.var_gyro = var_gyro
        self.var_gps = var_gps
        
        self.H = np.zeros((2, 7))
        self.H[0, 0] = 1.0 # x
        self.H[1, 1] = 1.0 # y
        
        self.R = np.diag([var_gps, var_gps])
        
    def predict(self, u, dt):
        # Calcul de la Jacobienne Numérique F
        eps = 1e-5
        F = np.zeros((7, 7))
        for i in range(7):
            X_plus = self.X.copy()
            X_plus[i] += eps
            X_minus = self.X.copy()
            X_minus[i] -= eps
            F[:, i] = (state_transition(X_plus, u, dt) - state_transition(X_minus, u, dt)) / (2 * eps)
            
        # Mise à jour de l'état
        self.X = state_transition(self.X, u, dt)
        
        # Bruit de process Q
        Q = np.zeros((7, 7))
        Q[2,2] = self.var_acc * dt**2
        Q[3,3] = self.var_acc * dt**2
        Q[4,4] = self.var_gyro * dt**2
        Q[5,5] = self.var_gyro * dt**2
        Q[6,6] = self.var_gyro * dt**2
        
        self.P = F @ self.P @ F.T + Q

    def update_gps(self, gps_p):
        z = np.array(gps_p)
        y = z - (self.H @ self.X)
        
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Rejet d'outliers
        maha = y.T @ np.linalg.inv(S) @ y
        if maha > 15.0:
            return False
            
        self.X = self.X + K @ y
        self.P = (np.eye(7) - K @ self.H) @ self.P
        
        return True
