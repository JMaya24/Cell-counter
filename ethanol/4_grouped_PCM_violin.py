import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

region = "Lob"
csv_path = "/Users/juanpablomayaarteaga/Desktop/"
csv_file = f"{region}_mean.csv"
input_file = csv_path + csv_file

plot_path = "/Users/juanpablomayaarteaga/Desktop/Plots/"
os.makedirs(plot_path, exist_ok=True)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Set color palette, group order, and region order
color_palette = {"ctr": "blue", "alc": "red"}
group_order = ["ctr", "alc"]
region_order = [region]

# Filter the data based on the desired region
df_filtered = df[df["region"] == region]

# Create a figure with multiple subplots
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Plot the first subplot with subject_mean_area
sns.violinplot(x=df_filtered["group"],
               y=df_filtered["Neun_mean_area"],
               hue=df_filtered["group"],
               split=False,
               inner="quart",
               width=-0.8,
               palette=color_palette,
               hue_order=group_order,
               order=group_order,
               ax=axes[0])
axes[0].set_ylabel("Mean area", weight='bold')
axes[0].legend([],[], frameon=False)  # Remove the legend

# Plot the second subplot with subject_mean_density
sns.violinplot(x=df_filtered["group"],
               y=df_filtered["GFAP_mean_area"],
               hue=df_filtered["group"],
               split=False,
               linewidth=1,
               inner="quart",
               width=-0.8,  # Adjust the width
               palette=color_palette,
               hue_order=group_order,
               order=group_order,
               ax=axes[1])
axes[1].set_ylabel("Mean density", weight='bold')
axes[1].legend([],[], frameon=False)  # Remove the legend

# Plot the third subplot with max_mean_area_subject
sns.violinplot(x=df_filtered["group"],
               y=df_filtered["Iba_mean_area"],
               hue=df_filtered["group"],
               split=False,
               linewidth=1,
               inner="quart",
               width=-0.8,  # Adjust the width
               palette=color_palette,
               hue_order=group_order,
               order=group_order,
               ax=axes[2])
axes[2].set_ylabel("Max mean area", weight='bold')
#axes[2].legend([],[], frameon=True)  # Remove the legend

# Adjust the spacing between subplots
fig.tight_layout()

# Save the plot
plot_file = f"{plot_path}{region}_mean_violinplots.png"
plt.savefig(plot_file)
plt.show()
print("Plot stored at: "+ plot_file)
