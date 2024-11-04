import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)

# List of unique instances
instances = df['Instance'].unique()

# List of configurations in order
configurations = ['auto', 'frumpy', 'jumpy', 'tweety', 'handy', 'crafty', 'trendy', 'many']

# Create a mapping from configuration to an index
config_indices = {config: idx for idx, config in enumerate(configurations)}

# Plot for all instances
plt.figure(figsize=(12, 6))

for instance in instances:
    instance_data = df[df['Instance'] == instance]
    instance_data['Config_Index'] = instance_data['Configuration'].map(config_indices)
    instance_data = instance_data.sort_values('Config_Index')

    plt.plot(instance_data['Config_Index'], instance_data['Time(s)'], marker='o', label=instance)

# Set X-axis labels to configurations
plt.xticks(range(len(configurations)), configurations, rotation=45)
plt.xlabel('Configurations')
plt.ylabel('Time (s)')
plt.title('Time vs Configurations for All Instances')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
