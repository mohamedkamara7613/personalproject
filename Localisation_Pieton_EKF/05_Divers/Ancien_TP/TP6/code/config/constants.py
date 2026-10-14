# Ports GPIO
PORT_LIDAR = ...      # Port USB connecté au LiDAR
PORT_BUTTON = ... # Port GPIO du Bouton
PORT_LED = ... # Port GPIO de la LED

# Constantes de configuration du LiDAR
LIDAR_MIN_RANGE = ...                  # Portée minimale du LiDAR en mm
LIDAR_MAX_RANGE = ...                # Portée maximale du LiDAR en mm

ACQUISITION_ROOT = 'data/'

DISPLAY_SIZE = (640, 480) # Taille d'affichage par défaut de la fenêtre

# Constantes de calibration
DIM_GRID = ... # Dimension de la grille d'échecs (nombre de coins intérieurs par ligne et par colonne)
SQUARE_SIZE = ... # Taille du carré en mm