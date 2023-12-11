#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:24:49 2023

@author: juanpablomayaarteaga
"""


import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

region = "PCM"
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

# Create the plot
fig, ax = plt.subplots()
sns.swarmplot(x=df_filtered["group"],
              y=df_filtered["subject_mean_area"],
              palette=color_palette,
              order=group_order,
              ax=ax)

# Set subplot title and labels
ax.set_xlabel("Groups")
ax.set_ylabel("Mean area", weight='bold')


# Save the plot
plot_file = f"{plot_path}{region}_stripplot.png"
plt.savefig(plot_file)
plt.show()

