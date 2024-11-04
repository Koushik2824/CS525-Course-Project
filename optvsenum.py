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
    index='Opt_Mode',
    columns='Enum_Mode',
    aggfunc='mean'
)

# Reorder the index and columns if necessary
opt_modes = ['opt', 'enum', 'optN', 'ignore']
enum_modes = ['bt', 'record', 'brave', 'cautious', 'auto']
pivot_table = pivot_table.reindex(index=opt_modes, columns=enum_modes)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap='viridis')
plt.title('Average Time (s) by Opt_Mode and Enum_Mode')
plt.xlabel('Enumeration Modes')
plt.ylabel('Optimization Modes')
plt.show()
