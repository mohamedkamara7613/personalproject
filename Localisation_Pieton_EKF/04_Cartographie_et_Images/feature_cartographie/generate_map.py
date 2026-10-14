"""
Générateur de carte interactive (Folium) avec incrustation de photos géolocalisées.
Ce script fusionne le fichier de trajectoire (Kalman) avec le journal des photos (Caméra).
"""

import os
import csv
import time
import pandas as pd
import numpy as np
import folium
from folium import IFrame
from folium.plugins import MarkerCluster
import base64

def get_base64_image(image_path):
    """ Encode une image locale en Base64 pour l'intégrer directement dans le fichier HTML. """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Erreur lors de la lecture de l'image {image_path}: {e}")
        return None

def generate_interactive_map(kalman_csv, photos_csv, output_html="carte_photos.html"):
    print(f"--- Génération de la Carte Interactive ---")
    
    # 1. Vérification des fichiers
    if not os.path.exists(kalman_csv):
        print(f"Erreur : Fichier trajectoire introuvable ({kalman_csv})")
        return
        
    try:
        k_data = pd.read_csv(kalman_csv)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Kalman : {e}")
        return

    # Centre de la carte = Premier point de la trajectoire
    start_lat = k_data['Latitude'].iloc[0]
    start_lon = k_data['Longitude'].iloc[0]
    
    m = folium.Map(location=[start_lat, start_lon], zoom_start=18, tiles="OpenStreetMap")
    
    # Création du groupe de marqueurs (gère l'empilement)
    marker_cluster = MarkerCluster().add_to(m)
    
    # 2. Tracé de la trajectoire globale (Ligne Bleue)
    kalman_points = list(zip(k_data['Latitude'], k_data['Longitude']))
    folium.PolyLine(kalman_points, color="blue", weight=4, opacity=0.8, tooltip="Trajet Piéton").add_to(m)
    
    # 3. Traitement des photos (Synchronisation Temporelle)
    if os.path.exists(photos_csv):
        p_data = pd.read_csv(photos_csv)
        print(f"Journal des photos trouvé : {len(p_data)} photos à géolocaliser.")
        
        for index, row in p_data.iterrows():
            photo_time = float(row['Timestamp'])
            photo_file = row['Filename']
            
            # --- SYNCHRONISATION ---
            # On cherche l'index dans le CSV Kalman où le Timestamp est le plus proche de photo_time
            # np.abs(k_data['Timestamp'] - photo_time).idxmin() retourne la ligne la plus proche
            closest_idx = np.abs(k_data['Timestamp'].astype(float) - photo_time).idxmin()
            
            lat = k_data.loc[closest_idx, 'Latitude']
            lon = k_data.loc[closest_idx, 'Longitude']
            # -----------------------
            
            # Embed de l'image
            encoded_img = get_base64_image(photo_file)
            if encoded_img:
                # Création d'un mini-cadre HTML (Popup) contenant la photo
                html = f'''
                    <div style="text-align: center;">
                        <b>Photo prise à {photo_time:.1f}s</b><br>
                        <img src="data:image/jpeg;base64,{encoded_img}" width="280" style="border-radius: 5px; margin-top: 5px;">
                    </div>
                '''
                iframe = IFrame(html, width=310, height=250)
                popup = folium.Popup(iframe, max_width=310)
                
                # Ajout de l'épingle (Icône de caméra Violette)
                folium.Marker(
                    [lat, lon], 
                    popup=popup, 
                    tooltip="Voir la photo",
                    icon=folium.Icon(color='red', icon='picture') # Icône standard picture
                ).add_to(marker_cluster)
                
                print(f" -> {photo_file} géolocalisée à [Lat: {lat:.5f}, Lon: {lon:.5f}]")
    else:
        print("Aucun fichier photos_log.csv trouvé. La carte affichera uniquement la trajectoire.")

    # 4. Sauvegarde
    m.save(output_html)
    print(f"Terminé ! La carte a été sauvegardée dans : {output_html}")
    print("Ouvrez ce fichier dans n'importe quel navigateur web pour voir le résultat.")

if __name__ == "__main__":
    # Noms des fichiers par défaut si le script est lancé depuis ce dossier
    # (Ces chemins seront sûrement à ajuster plus tard lors de l'intégration dans le repo global)
    kalman_log = "kalman_realtime.csv" # MOCK (A modifier selon où sont les données)
    photos_log = "photos_log.csv"
    
    # Pour le test, on va générer un faux fichier kalman_realtime.csv s'il n'existe pas
    if not os.path.exists(kalman_log):
        print("Fichier Kalman introuvable pour le test. Création d'un mock...")
        with open(kalman_log, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Position_X_m", "Position_Y_m", "Latitude", "Longitude"])
            # Ligne bidon proche de la Tour Eiffel pour l'exemple
            writer.writerow([time.time(), 0, 0, 48.8584, 2.2945])
            

    generate_interactive_map(kalman_log, photos_log, "carte_photos.html")
