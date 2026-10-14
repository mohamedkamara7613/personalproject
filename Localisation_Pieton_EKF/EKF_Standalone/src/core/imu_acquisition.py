import time
from utils import CSVHandler
from sensors.IMU import read_IMU, initialize_sensors

def get_imu_data(XL_addr, MAG_addr, accel_range, accel_freq, gyro_range, gyro_freq, magneto_range, magneto_freq, csv_out=None, data_queue=None, stop_event_arg=None):
    """
    Fait l'acquisition des données IMU (accéléromètre et gyroscope) en fonction des paramètres d'acquisition.

    Arguments:
    - XL_addr: l'adresse I2C du LSM6DSO 
    - accel_range: la plage de mesure de l'accéléromètre (g).
    - accel_freq: la fréquence d'échantillonnage de l'accéléromètre (Hz).
    - gyro_range: la plage de mesure du gyroscope (dps).
    - gyro_freq: la fréquence d'échantillonnage du gyroscope (Hz).
    - csv_out: le chemin du fichier CSV d'enregistrement (si définit à None, aucun enregistrement n'est effectué)
    """
    
    # Calculer l'intervalle en secondes (en fonction de la fréquence)
    interval = 1 / min(accel_freq,gyro_freq)

    # Création du fichier CSV d'enregistrement
    save_csv = False
    if csv_out is not None:
        save_csv = True
        if not csv_out.endswith('.csv'):
            csv_out += '.csv'
        record = CSVHandler(csv_out)
        record.create_csv_with_header(['Timestamp', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Magneto X', 'Magneto Y', 'Magneto Z'])

    # Initialisation des capteurs
    initialize_sensors(XL_addr, MAG_addr, accel_range, accel_freq, gyro_range, gyro_freq, magneto_range, magneto_freq)

    try:
        while not stop_event_arg.is_set():
            start_time = time.time()

            # Lecture des données
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magneto_x, magneto_y, magneto_z = read_IMU(XL_addr, MAG_addr, accel_range, gyro_range, magneto_range)

            # Enregistrement des données dans le fichier CSV
            if save_csv:
                record.append_row([time.time(), accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magneto_x, magneto_y, magneto_z])
                
            # Envoi des données dans la Queue pour le Kalman Temps Réel
            if data_queue is not None:
                data_queue.put(('IMU', time.time(), accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magneto_x, magneto_y, magneto_z))

            # Calcul de la durée de la boucle et ajustement du délai
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, interval - elapsed_time)
            time.sleep(time_to_sleep)

    except KeyboardInterrupt:
        print("Arrêt du programme.")
