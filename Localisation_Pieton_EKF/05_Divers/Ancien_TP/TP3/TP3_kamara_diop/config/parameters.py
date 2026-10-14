# Paramètres du LiDAR
MIN_DETECTION_RANGE = 60       # Portée minimale appliquée du LiDAR en mm
MAX_DETECTION_RANGE = 3000        # Portée maximale appliquée du LiDAR en mm
MIN_DETECTION_ANGLE = 270        # Angle minimal du scan en degrés
MAX_DETECTION_ANGLE = 90       # Angle maximal du scan en degrés
QUALITY_THRESHOLD = 12          # Seuil de qualité des mesures du LiDAR (entre 0 et 15)
SCAN_SKIP = 3                    # Ignorer X scans pour alléger l'affichage (via stream_scan.py)