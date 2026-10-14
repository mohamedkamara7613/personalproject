import pandas as pd
import matplotlib.pyplot as plt

df_gps = pd.read_csv('gps_data.csv')
df_ekf_real = pd.read_csv('kalman_realtime.csv')

# Clean GPS
df_gps = df_gps[(df_gps['Latitude'] >= -90) & (df_gps['Latitude'] <= 90)]

plt.figure(figsize=(10, 10))
plt.plot(df_gps['Longitude'], df_gps['Latitude'], 'ro', markersize=2, label='GPS Brut', alpha=0.5)

if 'Latitude' in df_ekf_real.columns:
    df_ekf_real = df_ekf_real.dropna(subset=['Latitude', 'Longitude'])
    plt.plot(df_ekf_real['Longitude'], df_ekf_real['Latitude'], 'b-', lw=2, label='EKF Realtime')

plt.title('Comparaison GPS et EKF Realtime')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
# Save to the artifacts dir of the conversation
plt.savefig('/home/mkamara/.gemini/antigravity/brain/1b9284cc-b913-4f75-95ee-a4b224a8daa3/map_comparison.png')
print("Image saved.")
