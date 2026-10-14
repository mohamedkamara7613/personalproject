import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv('/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Acquisition1_20_05/test_rotations.csv')

# Centrer les données sur 0 temporel
df['Time'] = df['Timestamp'] - df['Timestamp'].min()

plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['Magneto X'], label='Mag X', lw=2)
plt.plot(df['Time'], df['Magneto Y'], label='Mag Y', lw=2)
plt.plot(df['Time'], df['Magneto Z'], label='Mag Z', lw=2)
plt.title("Données brutes Magnétomètre (Test de rotation)")
plt.xlabel("Temps (s)")
plt.ylabel("Champ magnétique (Gauss)")
plt.legend()
plt.grid(True)
plt.savefig('/home/mkamara/.gemini/antigravity/brain/1b9284cc-b913-4f75-95ee-a4b224a8daa3/magneto_plot.png')

# Calculate atan2 options
theta_1 = np.degrees(np.arctan2(df['Magneto Y'], df['Magneto X']))
theta_2 = np.degrees(np.arctan2(-df['Magneto Y'], df['Magneto X']))
theta_3 = np.degrees(np.arctan2(df['Magneto Y'], -df['Magneto X']))
theta_4 = np.degrees(np.arctan2(df['Magneto X'], df['Magneto Y']))

plt.figure(figsize=(10, 6))
plt.plot(df['Time'], theta_1, label='atan2(Y, X)', alpha=0.7)
plt.plot(df['Time'], theta_2, label='atan2(-Y, X)', alpha=0.7)
plt.plot(df['Time'], theta_3, label='atan2(Y, -X)', alpha=0.7)
plt.plot(df['Time'], theta_4, label='atan2(X, Y)', alpha=0.7)
plt.title("Calcul d'angle (Cap) selon différentes conventions")
plt.xlabel("Temps (s)")
plt.ylabel("Angle (Degrés)")
plt.legend()
plt.grid(True)
plt.savefig('/home/mkamara/.gemini/antigravity/brain/1b9284cc-b913-4f75-95ee-a4b224a8daa3/magneto_angles.png')
