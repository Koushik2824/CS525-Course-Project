import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results_combinations.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)

# Pivot the data to create a heatmap
pivot_table = df.pivot_table(values='Time(s)', index='Opt_Mode', columns='Configuration', aggfunc='mean')

plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap='viridis')
plt.title('Average Time (s) by Opt_Mode and Configuration')
plt.show()
