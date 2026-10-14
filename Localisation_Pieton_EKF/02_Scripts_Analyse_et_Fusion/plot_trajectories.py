import pandas as pd
import folium
import os

# Chemin des fichiers
gps_file = "gps_data.csv"
kalman_file = "kalman_realtime.csv"

# Chargement des données
try:
    df_gps = pd.read_csv(gps_file)
    df_kalman = pd.read_csv(kalman_file)
except Exception as e:
    print(f"Erreur de lecture des CSV : {e}")
    exit(1)

# On nettoie les éventuelles lignes bizarres (comme celles avec 255:255:255)
df_gps = df_gps[df_gps['Latitude'] < 90]
df_kalman = df_kalman[df_kalman['Latitude'] < 90]

# Création de la carte centrée sur le premier point GPS
start_lat = df_gps['Latitude'].iloc[0]
start_lon = df_gps['Longitude'].iloc[0]

m = folium.Map(location=[start_lat, start_lon], zoom_start=18)

# Tracer la trajectoire GPS (en bleu)
gps_coords = list(zip(df_gps['Latitude'], df_gps['Longitude']))
folium.PolyLine(
    gps_coords,
    color='blue',
    weight=3,
    opacity=0.8,
    tooltip="Trajectoire GPS brute"
).add_to(m)

# Tracer la trajectoire Kalman (en rouge)
# Attention, vu l'explosion de Kalman, ça risque de dézoomer fortement la carte
kalman_coords = list(zip(df_kalman['Latitude'], df_kalman['Longitude']))
folium.PolyLine(
    kalman_coords,
    color='red',
    weight=3,
    opacity=0.8,
    tooltip="Trajectoire estimée par Kalman"
).add_to(m)

# Ajouter des marqueurs de départ
folium.Marker(location=[start_lat, start_lon], popup="Départ", icon=folium.Icon(color="green")).add_to(m)

output_map = "comparaison_trajectoires.html"
m.save(output_map)
print(f"Carte générée avec succès : {output_map}")
