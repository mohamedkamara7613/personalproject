import pandas as pd
import numpy as np

imu = pd.read_csv("imu_data.csv")
accel = imu[['Accel X', 'Accel Y', 'Accel Z']].values
# Remove gravity by looking at mean over a sliding window? No, just take variance.
print("Variance Accel X:", np.var(accel[:,0]))
print("Variance Accel Y:", np.var(accel[:,1]))
print("Variance Accel Z:", np.var(accel[:,2]))

# Let's see the mean values
print("Mean Accel X:", np.mean(accel[:,0]))
print("Mean Accel Y:", np.mean(accel[:,1]))
print("Mean Accel Z:", np.mean(accel[:,2]))

