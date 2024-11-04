import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results_enum.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)

# List of unique instances
instances = df['Instance'].unique()

# List of enumeration modes in order
enum_modes = ['bt', 'record', 'brave', 'cautious', 'auto']

# Create a mapping from enum mode to an index
enum_indices = {mode: idx for idx, mode in enumerate(enum_modes)}

# Plot for all instances
plt.figure(figsize=(12, 6))

for instance in instances:
    instance_data = df[df['Instance'] == instance]
    instance_data['Enum_Index'] = instance_data['Enum_Mode'].map(enum_indices)
    instance_data = instance_data.sort_values('Enum_Index')

    plt.plot(instance_data['Enum_Index'], instance_data['Time(s)'], marker='o', label=instance)

# Set X-axis labels to enumeration modes
plt.xticks(range(len(enum_modes)), enum_modes, rotation=45)
plt.xlabel('Enumeration Modes')
plt.ylabel('Time (s)')
plt.title('Time vs Enumeration Modes for All Instances')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
