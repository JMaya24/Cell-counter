import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


region = "Lob"
path = "/Users/juanpablomayaarteaga/Desktop/"

output_path = path + "Data/"
os.makedirs(output_path, exist_ok=True)

plot_path = path + "Plot/"
os.makedirs(plot_path, exist_ok=True)


# Read the CSV file into a pandas DataFrame
df = pd.read_csv(f"{path}{region}_mean.csv")

# Filter the DataFrame to get the number of cells per cell type for each subject
filtered_data = df.groupby(['subject', 'cell'])['cell_number'].count().reset_index()

# Pivot the filtered DataFrame
pivoted_data = filtered_data.pivot(index='subject', columns='cell', values='cell_number')

# Merge the pivoted DataFrame with the original DataFrame
df = pd.merge(df, pivoted_data, on='subject', how='left')

# Create new columns "GFAP", "Neun", "Iba" and populate them with the corresponding values
df['GFAP'] = df.loc[df['cell'] == 'GFAP', 'cell_number']
df['Neun'] = df.loc[df['cell'] == 'Neun', 'cell_number']
df['Iba'] = df.loc[df['cell'] == 'Iba', 'cell_number']


df['Neun_mean_number'] = df.groupby('subject')['Neun'].transform('mean')
df['GFAP_mean_number'] = df.groupby('subject')['GFAP'].transform('mean')
df['Iba_mean_number'] = df.groupby('subject')['Iba'].transform('mean')


# Save the modified DataFrame to a CSV file
df.to_csv(f"{output_path}{region}_mean_cells.csv", index=False)


# Remove duplicate rows based on "Neun_mean_number", "GFAP_mean_number", and "Iba_mean_number"
df.drop_duplicates(subset=['Neun_mean_number', 'GFAP_mean_number', 'Iba_mean_number'], inplace=True)

# Modify the magnitude of the columns "Neun_mean_area," "GFAP_mean_area," and "Iba_mean_area"
df['Neun_mean_area'] = df['Neun_mean_area'] / 1e6
df['GFAP_mean_area'] = df['GFAP_mean_area'] / 1e6
df['Iba_mean_area'] = df['Iba_mean_area'] / 1e6

# Modify the magnitude of the columns "Neun_mean_number," "GFAP_mean_number," and "Iba_mean_number"
df['Neun_mean_number'] = df['Neun_mean_number'] / 1e3
df['GFAP_mean_number'] = df['GFAP_mean_number'] / 1e3
df['Iba_mean_number'] = df['Iba_mean_number'] / 1e3


# Save the modified DataFrame to a CSV file
df.to_csv(f"{output_path}{region}_mean_number.csv", index=False)



# Create three subplots side by side using seaborn
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

# Plot 1: Neun_mean_area vs Neun_mean_number
sns.scatterplot(data=df, x='Neun_mean_area', y='Neun_mean_number', hue='group', palette={'ctr': 'blue', 'alc': 'red'}, ax=axs[0])
axs[0].set_xlabel('Area')
axs[0].set_ylabel('Cell Counting')
axs[0].set_title('Neun')
for _, row in df.iterrows():
    axs[0].text(row['Neun_mean_area'], row['Neun_mean_number'], row['subject'])

# Plot 2: GFAP_mean_area vs GFAP_mean_number
sns.scatterplot(data=df, x='GFAP_mean_area', y='GFAP_mean_number', hue='group', palette={'ctr': 'blue', 'alc': 'red'}, ax=axs[1])
axs[1].set_xlabel('Area')
axs[1].set_ylabel('Cell Counting')
axs[1].set_title('GFAP')
for _, row in df.iterrows():
    axs[1].text(row['GFAP_mean_area'], row['GFAP_mean_number'], row['subject'])

# Plot 3: Iba_mean_area vs Iba_mean_number
sns.scatterplot(data=df, x='Iba_mean_area', y='Iba_mean_number', hue='group', palette={'ctr': 'blue', 'alc': 'red'}, ax=axs[2])
axs[2].set_xlabel('Area')
axs[2].set_ylabel('Cell Counting')
axs[2].set_title('Iba')
for _, row in df.iterrows():
    axs[2].text(row['Iba_mean_area'], row['Iba_mean_number'], row['subject'])

# Adjust spacing between subplots
plt.tight_layout()

# Save the plots
plt.savefig(f"{plot_path}{region}_mean_plots.png")

# Show the plots
plt.show()