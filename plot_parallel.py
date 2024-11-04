import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('results_parallel.csv')

# Filter out entries with errors
df = df[df['Time(s)'] != 'Error']
df['Time(s)'] = df['Time(s)'].astype(float)
df['Threads'] = df['Threads'].astype(int)

# List of unique instances
instances = df['Instance'].unique()

# List of thread counts in order
thread_counts = sorted(df['Threads'].unique())

# Create a mapping from thread count to an index
thread_indices = {threads: idx for idx, threads in enumerate(thread_counts)}

# Plot for all instances
plt.figure(figsize=(12, 6))

for instance in instances:
    instance_data = df[df['Instance'] == instance]
    instance_data['Thread_Index'] = instance_data['Threads'].map(thread_indices)
    instance_data = instance_data.sort_values('Thread_Index')

    plt.plot(instance_data['Thread_Index'], instance_data['Time(s)'], marker='o', label=instance)

# Set X-axis labels to thread counts
plt.xticks(range(len(thread_counts)), thread_counts)
plt.xlabel('Number of Threads')
plt.ylabel('Time (s)')
plt.title('Time vs. Number of Threads for All Instances')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
