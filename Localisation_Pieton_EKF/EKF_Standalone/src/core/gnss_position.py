import time
from sensors.GNSS import GNSS
from utils import CSVHandler, LCD
from config import GNSS_DEVICE_ADDR, LCD_DEVICE_ADDR, MODE_GNSS


def gnss_position(mode=MODE_GNSS, csv_out=None, display_LCD=False, data_queue=None, stop_event_arg=None):
    """
    Lit les données GNSS et les sauvegarde dans un fichier.
    """
    gnss = GNSS(1, GNSS_DEVICE_ADDR)
    gnss.initialisation(mode)

    record = None
    if csv_out:
        if not csv_out.endswith(".csv"):
            csv_out += ".csv"
        record = CSVHandler(csv_out)
        record.create_csv_with_header(["Timestamp", "UTC", "Latitude", "Longitude"])

    try:
        while not stop_event_arg.is_set():

            # Récupération du prochain scan GPS
            gnss.wait_for_next_scan(timeout=1.0)

            # Gestion d'un signal mauvais
            if not(gnss.reception_ok):
                print("Recherche de signal GNSS...")
                continue

            if record is not None:
                record.append_row([gnss.timestamp, gnss.utc, gnss.latitude.coordinates_DD, gnss.longitude.coordinates_DD])

            # Récupération des coordonnées
            latitude = gnss.latitude.coordinates_DD
            longitude = gnss.longitude.coordinates_DD
            
            # Envoi des données dans la Queue pour le Kalman Temps Réel
            if data_queue is not None:
                data_queue.put(('GPS', gnss.timestamp, latitude, longitude, gnss.SOG * 0.5144, gnss.number_satellites))

            latitude_DMS = gnss.latitude.coordinates_DMS
            longitude_DMS = gnss.longitude.coordinates_DMS

            latitude_DMM = gnss.latitude.coordinates_DMM
            longitude_DMM = gnss.longitude.coordinates_DMM
            

    except KeyboardInterrupt:
        print("Arrêt du programme")
