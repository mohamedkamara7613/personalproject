# A COMPLETER

# Adresses I2C et USB des composants
LSM6DSO_ADDR = 0x6b             # Adresse I2C du capteur LSM6DSO (Accéléromètre/Gyroscope)
LIS3MDL_ADDR = 0x1E           # Adresse I2C du capteur LIS3MDL (Magnétomètre)

# Constantes des registres de configuration de l'IMU
CTRL1_XL = 0x10                   # Registre de configuration de l'accéléromètre
CTRL2_G = 0x11                    # Registre de configuration du gyroscope
OUTX_L_A = 0x28                   # Registre de lecture de l'accéléromètre
OUTX_L_G = 0x22                  # Registre de lecture du gyroscope

# Mappages des fréquences (Hz) pour l'accéléromètre
CONFIG_XL_FREQ = {
    12.5             : "0001",
    26             : "0010",
    52            : "0011",
    104             : "0010",
    208             : "0101",
    416           : "0110",
    833             : "0111",
    1.66e3           : "1000",
    3.33e3             : "1001",
    6.66e3             : "1010",
}

# Mappages des plages (full-scale range) pour l'accéléromètre
CONFIG_XL_RANGE = {
    2    :   "00",
    16   :   "01",
    4    :   "10",
    8    :   "11"
    
}

# Sensibilités des capteurs pour conversion des données brutes en unités physiques
CONFIG_XL_SENSITIVITY = {
    2 : 0.061,
    4 : 0.122,
    8 : 0.244, 
    16 : 0.488}

# Mappages des fréquences (Hz) pour le gyroscope
CONFIG_G_FREQ = {
    12.5             : "0001",
    26             : "0010",
    52            : "0011",
    104             : "0100",
    208             : "0101",
    416           : "0110",
    833             : "0111",
    1.66e3           : "1000",
    3.33e3             : "1001",
    6.66e3             : "1010",
}

# Mappages des plages (full-scale range) pour le gyroscope
CONFIG_G_RANGE = {
    250  : "00",
    500 : "01",
    1000 : "10",
    2000 : "11"
}

# Sensibilités des capteurs pour conversion des données brutes en unités physiques
CONFIG_G_SENSITIVITY = {
    125 : 4.375,
    250 : 8.75,
    500 : 17.5,
    1000 : 35,
    2000 : 70}
