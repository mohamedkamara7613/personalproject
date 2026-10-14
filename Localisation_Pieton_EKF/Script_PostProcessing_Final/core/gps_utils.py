import numpy as np
import csv

def gps_to_local_meters(lat, lon, lat_origin, lon_origin):
    """
    Convertit des coordonnées GPS (Latitude, Longitude) en degrés
    vers un repère cartésien local (X, Y) en mètres.
    
    L'axe X pointe vers l'Est (Longitude).
    L'axe Y pointe vers le Nord (Latitude).
    
    :param lat: Latitude actuelle en degrés
    :param lon: Longitude actuelle en degrés
    :param lat_origin: Latitude du point d'origine (0,0) en degrés
    :param lon_origin: Longitude du point d'origine (0,0) en degrés
    :return: (x, y) en mètres
    """
    R_earth = 6378137.0  # Rayon moyen de la terre en mètres
    
    # Conversion en radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    lat_ori_rad = np.radians(lat_origin)
    lon_ori_rad = np.radians(lon_origin)
    
    # Approximation de projection plate (Equirectangular projection)
    #  à l'échelle d'une ville (< 100km)
    x = R_earth * (lon_rad - lon_ori_rad) * np.cos(lat_ori_rad)
    y = R_earth * (lat_rad - lat_ori_rad)
    
    return x, y

def local_meters_to_gps(x, y, lat_origin, lon_origin):
    """
    Fonction inverse : Convertit des coordonnées locales (X, Y) en mètres
    vers des coordonnées mondiales (Latitude, Longitude) en degrés.
    """
    R_earth = 6378137.0
    
    lat_ori_rad = np.radians(lat_origin)
    lon_ori_rad = np.radians(lon_origin)
    
    # Inversion de l'approximation de projection plate
    lat_rad = (y / R_earth) + lat_ori_rad
    lon_rad = (x / (R_earth * np.cos(lat_ori_rad))) + lon_ori_rad
    
    lat = np.degrees(lat_rad)
    lon = np.degrees(lon_rad)
    
    return lat, lon

def read_gps_csv(file_path):
    """
    Lit un fichier GPS et convertit toutes les positions en mètres 
    par rapport au premier point du fichier.
    Retourne une liste de tuples: (timestamp, x_meters, y_meters)
    """
    data_en_metres = []
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Lire la première ligne pour définir l'origine (0,0)
        first_row = next(reader)
        lat_origin = float(first_row[2])
        lon_origin = float(first_row[3])
        
        # Le premier point est à (0, 0)
        t0 = float(first_row[0])
        data_en_metres.append((t0, 0.0, 0.0))
        
        # Traiter les lignes suivantes
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            t = float(row[0])
            lat = float(row[2])
            lon = float(row[3])
            
            # FILTRE 1: Ignorer les valeurs GPS hors limites mondiales
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                print(f"-----> Ligne {reader.line_num} ignorée (Hors limites: {lat}, {lon})")
                continue
            
            x, y = gps_to_local_meters(lat, lon, lat_origin, lon_origin)
            
            # FILTRE 2: Ignorer les "téléportations" aberrantes
            if abs(x) > 1000 or abs(y) > 1000:
                print(f"-----> Ligne {reader.line_num} ignorée (Téléportation détectée: X={x:.0f}m, Y={y:.0f}m)")
                continue
                
            data_en_metres.append((t, x, y))
            
    return data_en_metres, lat_origin, lon_origin

if __name__ == "__main__":
    fichier = "calibrationGPS_beitou.csv"
    donnees, lat0, lon0 = read_gps_csv(fichier)
    
    print(f"Chargement de {len(donnees)} points GPS.")
    print("Affichage des 5 premiers points (Timestamp, X en mètres, Y en mètres) :")
    for d in donnees[:5]:
        print(f"  T: {d[0]:.2f}s | X: {d[1]:.2f}m | Y: {d[2]:.2f}m")
