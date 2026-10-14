import math
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar
import time
from utils import CSVHandler, Buzzer
from config import LIDAR_MIN_RANGE, LIDAR_MAX_RANGE, SCAN_SKIP


class LIDAR:
    def __init__(self, port_name, 
                 min_range=LIDAR_MIN_RANGE, 
                 max_range=LIDAR_MAX_RANGE, 
                 quality_threshold=0,
                 min_angle=0,
                 max_angle=360,
                 ):
        """
        Initialise la classe LIDAR et configure les paramètres de mesure.

        Arguments:
        - port_name: nom du port série où est connecté le LiDAR
        - min_range: portée minimale en mm
        - max_range: portée maximale en mm
        - quality_threshold: seuil de qualité pour filtrer les mesures
        - min_angle: angle minimal pour filtrer les mesures (en degrés)
        - max_angle: angle maximal pour filtrer les mesures (en degrés)
        """
        self.lidar = RPLidar(port_name)
        self.quality_threshold = quality_threshold
        self.min_range = min_range
        self.max_range = max_range
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.scan_skip = SCAN_SKIP
        
    ######################################
    #    DEMARRAGE / ARRET DU LIDAR
    ######################################

    def start(self):
        """
        Démarre le LiDAR en activant son moteur.
        """
        self.lidar.start_motor()

    def stop(self):
        """
        Arrête le LiDAR, son moteur et déconnecte la connexion série.
        """
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    ######################################
    #    LECTURE DE SCANS
    ######################################
        
    def read_scan(self, warmup_scans=3):
        """
        Acquiert un scan complet 360°
        """
        self.lidar.clean_input()
        for idx, scan in enumerate(self.lidar.iter_scans()):
            if idx == warmup_scans:
                break
        filtered_scan = self.filter_scan(scan)
        points = self.polar_to_cartesian(filtered_scan)
        return time.time(), filtered_scan, points
    
    def iter_scans(self, skip=None):
        """
        Créer un générateur de scans.
        """
        self.lidar.clean_input()
        effective_skip = self.scan_skip if skip is None else max(1, skip)

        for idx, scan in enumerate(self.lidar.iter_scans(), start=1):
            if idx % effective_skip != 0:
                continue
            filtered_scan = self.filter_scan(scan)
            points = self.polar_to_cartesian(filtered_scan)
            yield time.time(), filtered_scan, points
    
    
    ######################################
    #    FILTRAGE DES POINTS DU SCAN
    ######################################

    def filter_range(self, scan):
        """
        Filtre les points du scan en fonction de la range de distance définie.
        """
        # A COMPLETER/MODIFIER
        
        return [meas for meas in scan if self.min_range <= meas[2] <= self.max_range]
        
    def filter_quality(self, scan):
        """
        Filtre les points du scan en ne conservant que ceux dont la qualité dépasse le seuil défini.
        """
        # A COMPLETER/MODIFIER
        return [meas for meas in scan if meas[0] >= self.quality_threshold]
    

    def filter_angle(self, scan):
        """
        Filtre les points du scan en fonction de la plage d'angle définie.
        """
        # A COMPLETER/MODIFIER
        filtered = []
        for meas in scan:
            quality, angle, distance = meas
            # si jamais on a 270° à 90°
            if self.min_angle <= self.max_angle:
                if self.min_angle <= angle <= self.max_angle:
                    filtered.append(meas)
            else:
                if angle >= self.min_angle or angle <= self.max_angle:
                    filtered.append(meas)
        return filtered

    def filter_scan(self, scan):
        """
        Filtre les points du scan selon la qualité, la plage d'angle et la range de distance
        """
        filtered = self.filter_quality(scan)
        filtered = self.filter_angle(filtered)
        filtered = self.filter_range(filtered)
        return filtered

    ######################################
    #    CONVERSION POLAIRE => CARTESIEN
    ######################################
    
    def polar_to_cartesian(self, scan):
        """
        Convertit les coordonnées polaires (angle, distance) en coordonnées cartésiennes (x, y).
        """
        
        # A COMPLETER/MODIFIER
        
        points = []
        for quality, angle, distance in scan:
            rad = math.radians(angle)
            x = distance * math.sin(rad)
            y = distance * math.cos(rad)
            points.append((x,y))
        return points
 
    ######################################
    #    AFFICHAGE
    ######################################
    
    def print_scan(self, scan):
        """
        Affichage console simple d'un scan.
        """
        print("Mesures :")
        for measurement in scan:
            print(measurement)
        print(f"Le scan contient {len(scan)} mesures")

    def print_points(self, points):
        """
        Affichage console simple des coordonnées cartésiennes.
        """
        print("\nCoordonnées des points dans le plan cartésien :")
        for x, y in points:
            print(f"({x}, {y})")