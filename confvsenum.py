import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results_combinations.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)

# Create a pivot table
pivot_table = df.pivot_table(
    values='Time(s)',
    index='Configuration',
    columns='Enum_Mode',
    aggfunc='mean'
)

# Reorder the index and columns if necessary
configurations = ['auto', 'frumpy', 'jumpy', 'tweety', 'handy', 'crafty', 'trendy', 'many']
enum_modes = ['bt', 'record', 'brave', 'cautious', 'auto']
pivot_table = pivot_table.reindex(index=configurations, columns=enum_modes)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap='magma')
plt.title('Average Time (s) by Configuration and Enum_Mode')
plt.xlabel('Enumeration Modes')
plt.ylabel('Configurations')
plt.show()
