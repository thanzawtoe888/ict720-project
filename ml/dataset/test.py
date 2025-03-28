import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV file
df = pd.read_csv('group8_db.health_data.csv')  # Replace 'data.csv' with the actual file path

# Plot scatter plot
plt.figure(figsize=(8, 6))
colors = {1: 'blue', 2: 'red'}
for mode in df['excercise_mode'].unique():
    subset = df[df['excercise_mode'] == mode]
    plt.scatter(subset['spo2'], subset['bpm'], label=f'Exercise Mode {mode}', color=colors.get(mode, 'gray'), alpha=0.7)

plt.xlabel('SpO2')
plt.ylabel('BPM')
plt.title('Scatter Plot of SpO2 vs BPM')
plt.legend()
plt.grid(True)
plt.show()
