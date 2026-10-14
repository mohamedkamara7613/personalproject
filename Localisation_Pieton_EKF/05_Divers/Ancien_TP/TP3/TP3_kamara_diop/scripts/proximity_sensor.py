from sensors.LIDAR import LIDAR
from utils import Buzzer
from time import sleep
from config import (
    PORT_LIDAR,
    MIN_DETECTION_RANGE,
    MAX_DETECTION_RANGE,
    MIN_DETECTION_ANGLE,
    MAX_DETECTION_ANGLE,
    QUALITY_THRESHOLD,
    PORT_BUZZER,
)
import argparse


def proximity_monitor(scan_iterator, buzzer, alert_distance):
    """
    Active le buzzer lorsqu'un obstacle est détecté
    à une distance inférieure au seuil.
    """

    for timestamp, scan, points in scan_iterator:
        # A COMPLETER
        distances = [meas[2] for meas in scan]
        if any(d < alert_distance for d in distances):
            """
            Do: 261.63 Hz
            Re: 293.66 Hz
            Mi: 329.63 Hz
            Fa: 349.23 Hz
            Sol: 392.00 Hz
            La: 440.00 Hz
            Si: 493.88 Hz
            """
            buzzer.play(261.63)
            sleep(1)            
            buzzer.play(293.66)
            sleep(1)            
            
            buzzer.play(329.63)
            sleep(1)            
            
            buzzer.play(349.23)
            sleep(1)            
            
            buzzer.play(392.00)
            sleep(1)            
            
            buzzer.play(440.00)
            sleep(1)            
            
            buzzer.play(493.88)
        else:
            buzzer.stop()
        


def main(alert_distance):
    print("Connexion au LiDAR...")
    lidar = LIDAR(
        PORT_LIDAR,
        quality_threshold=QUALITY_THRESHOLD,
        min_range=MIN_DETECTION_RANGE,
        max_range=MAX_DETECTION_RANGE,
        min_angle=MIN_DETECTION_ANGLE,
        max_angle=MAX_DETECTION_ANGLE
    )

    print("Initialisation du buzzer...")
    buzzer = Buzzer(PORT_BUZZER)

    try:
        print("Démarrage du LiDAR...")
        lidar.start()

        print("Surveillance de proximité à 360°...")
        proximity_monitor(
            lidar.iter_scans(),
            buzzer=buzzer,
            alert_distance=alert_distance,
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
        "--alert-distance", "-d",
        type=float,
        default=500.0,
        help="Distance seuil en mm pour activer le buzzer."
    )
    args = parser.parse_args()

    main(args.alert_distance)