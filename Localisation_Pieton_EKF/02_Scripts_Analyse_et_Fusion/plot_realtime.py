import pandas as pd
import folium
import numpy as np

# Load realtime EKF data
df_ekf = pd.read_csv('/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Acquisition1_20_05/Acquisition_Code_fusion/kalman_realtime.csv')
df_gps = pd.read_csv('/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Acquisition1_20_05/Acquisition_Code_fusion/gps_data.csv')

# Clean raw GPS
df_gps = df_gps[(df_gps['Latitude'] >= -90) & (df_gps['Latitude'] <= 90)]

if len(df_gps) > 0:
    start_lat = df_gps['Latitude'].iloc[0]
    start_lon = df_gps['Longitude'].iloc[0]
else:
    start_lat, start_lon = 49.384, 1.068

m = folium.Map(location=[start_lat, start_lon], zoom_start=18)

# Legend HTML
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: auto; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color: white;
            padding: 10px;">
    <b>Légende EKF Temps Réel</b><br>
    <i style="color:red; font-size:18px;">●</i> GPS Brut<br>
    <i style="color:green; font-size:18px;">●</i> GPS Traité (Accepté)<br>
    <i style="color:orange; font-size:18px;">●</i> GPS Rejeté (Mahalanobis)<br>
    <i style="color:blue; font-size:18px;">▬</i> Trajectoire EKF
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# To find which GPS was accepted, we match timestamps approximately
# df_ekf has 'Timestamp' and 'GPS_accepted'
# df_gps has 'Timestamp', 'Latitude', 'Longitude'

# Plot raw GPS (Red)
for _, row in df_gps.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=2, color='red', fill=True, tooltip='GPS Brut'
    ).add_to(m)

# Match GPS points with EKF acceptance
if 'GPS_accepted' in df_ekf.columns:
    for _, ekf_row in df_ekf.iterrows():
        # Find closest GPS point
        closest_gps = df_gps.iloc[(df_gps['Timestamp'] - ekf_row['Timestamp']).abs().argsort()[:1]]
        if not closest_gps.empty:
            gps_lat = closest_gps['Latitude'].values[0]
            gps_lon = closest_gps['Longitude'].values[0]
            
            accepted = str(ekf_row['GPS_accepted']).strip().lower() in ['true', '1.0', '1']
            if accepted:
                folium.CircleMarker(
                    location=[gps_lat, gps_lon],
                    radius=4, color='green', fill=True, tooltip='GPS Accepté'
                ).add_to(m)
            else:
                folium.CircleMarker(
                    location=[gps_lat, gps_lon],
                    radius=4, color='orange', fill=True, tooltip='GPS Rejeté'
                ).add_to(m)

# Plot EKF trajectory (Blue line)
df_ekf_valid = df_ekf.dropna(subset=['Latitude', 'Longitude'])
ekf_coords = list(zip(df_ekf_valid['Latitude'], df_ekf_valid['Longitude']))
folium.PolyLine(
    ekf_coords, color='blue', weight=4, opacity=0.8, tooltip='EKF (Temps réel)'
).add_to(m)

map_path = '/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Acquisition1_20_05/Acquisition_Code_fusion/realtime_map.html'
m.save(map_path)
print(f"Map saved to {map_path}")
