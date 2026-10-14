import argparse

from sensors.LIDAR import LIDAR
from utils import Buzzer
from config import (
    PORT_LIDAR,
    MIN_DETECTION_RANGE,
    MAX_DETECTION_RANGE,
    QUALITY_THRESHOLD,
    PORT_BUZZER,
    LIDAR_MAX_RANGE
)


def scan_to_bins(scan, num_bins=36, default_distance=None):
    """
    Convertit un scan LiDAR en signature angulaire discrète.
    
    En partant du principe que le scan d'un LiDAR comprend 360 mesures, avec 1° d'écart par mesure, la fonction renvoie une liste de taille (num_bins), 
    où chaque élément correspond à la moyenne des scans dans une plage angulaire de taille (360/num_bins)°
    """

    if default_distance is None:
        default_distance = LIDAR_MAX_RANGE

    bins = [[] for _ in range(num_bins)]
    bin_width = 360.0 / num_bins

    for quality, angle_deg, distance_mm in scan:
        angle_deg = angle_deg % 360.0
        bin_index = int(angle_deg // bin_width)

        if bin_index >= num_bins:
            bin_index = num_bins - 1

        bins[bin_index].append(distance_mm)

    signature = []

    for values in bins:
        if values:
            signature.append(sum(values) / len(values))
        else:
            signature.append(None)

    return signature


def motion_monitor(scan_iterator,
                   buzzer,
                   max_range=LIDAR_MAX_RANGE,
                   motion_threshold=200.0,
                   num_bins=36):
    """
    Détecte un mouvement en comparant chaque scan au précédent.
    """

    for timestamp, scan, points in scan_iterator:

        signature = scan_to_bins(
            scan,
            num_bins=num_bins,
            default_distance=max_range
        )

        # A COMPLETER
        ...

def main(max_range,motion_threshold, num_bins):

    print("Connexion au LiDAR...")
    lidar = LIDAR(
        PORT_LIDAR,
        quality_threshold=QUALITY_THRESHOLD,
        min_range=MIN_DETECTION_RANGE,
        max_range=MAX_DETECTION_RANGE,
        min_angle=0,
        max_angle=360,
    )

    print("Initialisation du buzzer...")
    buzzer = Buzzer(PORT_BUZZER)

    try:

        print("Démarrage du LiDAR...")
        lidar.start()

        print("Détection de mouvement à 360°...")

        motion_monitor(
            lidar.iter_scans(),
            buzzer=buzzer,
            max_range=max_range,
            motion_threshold=motion_threshold,
            num_bins=num_bins,
        )

    except KeyboardInterrupt:

        print("\nSurveillance interrompue par l'utilisateur.")

    finally:

        print("Arrêt du buzzer...")
        buzzer.stop()

        print("Arrêt du LiDAR...")
        lidar.stop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--max-range",
        type=float,
        default=LIDAR_MAX_RANGE,
        help="Range maximum de détection (peut être inférieure à la range maximum du LiDAR)"
    )

    parser.add_argument(
        "--motion-threshold",
        type=float,
        default=500.0,
        help="Seuil de variation moyenne (en mm) pour détecter un mouvement."
    )

    parser.add_argument(
        "--num-bins",
        type=int,
        default=36,
        help="Nombre de secteurs angulaires pour discrétiser le scan."
    )

    args = parser.parse_args()

    main(args.max_range, args.motion_threshold, args.num_bins)