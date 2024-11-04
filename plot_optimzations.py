import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results_opt.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)

# List of unique instances
instances = df['Instance'].unique()

# List of optimization modes in order
opt_modes = ['opt', 'enum', 'optN', 'ignore']

# Create a mapping from optimization mode to an index
opt_indices = {mode: idx for idx, mode in enumerate(opt_modes)}

# Plot for all instances
plt.figure(figsize=(12, 6))

for instance in instances:
    instance_data = df[df['Instance'] == instance]
    instance_data['Opt_Index'] = instance_data['Opt_Mode'].map(opt_indices)
    instance_data = instance_data.sort_values('Opt_Index')

    plt.plot(instance_data['Opt_Index'], instance_data['Time(s)'], marker='o', label=instance)

# Set X-axis labels to optimization modes
plt.xticks(range(len(opt_modes)), opt_modes, rotation=45)
plt.xlabel('Optimization Modes')
plt.ylabel('Time (s)')
plt.title('Time vs Optimization Modes for All Instances')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
