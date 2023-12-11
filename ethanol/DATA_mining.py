#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:11:35 2023

@author: juanpablomayaarteaga
"""

import pandas as pd

region="Crus"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(f"/Users/juanpablomayaarteaga/Desktop/{region}.csv")

# Group the data by 'subject' and 'cell' and calculate the mean of 'total_area' for each cell type
Neun_mean_area = df[df['cell'] == 'Neun'].groupby('subject')['total_area'].mean()
Iba_mean_area = df[df['cell'] == 'Iba'].groupby('subject')['total_area'].mean()
GFAP_mean_area = df[df['cell'] == 'GFAP'].groupby('subject')['total_area'].mean()

# Calculate the overall mean area as the sum of the mean areas for each cell type
subject_mean_area = Neun_mean_area.add(Iba_mean_area, fill_value=0).add(GFAP_mean_area, fill_value=0)

# Add the new columns to the DataFrame
df['subject_mean_area'] = df['subject'].map(subject_mean_area)
df['Neun_mean_area'] = df['subject'].map(Neun_mean_area)
df['Iba_mean_area'] = df['subject'].map(Iba_mean_area)
df['GFAP_mean_area'] = df['subject'].map(GFAP_mean_area)



# Group the data by 'subject' and 'cell' and calculate the mean of 'total_area' for each cell type
Neun_mean_density = df[df['cell'] == 'Neun'].groupby('subject')['density'].mean()
Iba_mean_density = df[df['cell'] == 'Iba'].groupby('subject')['density'].mean()
GFAP_mean_density = df[df['cell'] == 'GFAP'].groupby('subject')['density'].mean()

# Calculate the overall mean area as the sum of the mean areas for each cell type
subject_mean_density = Neun_mean_density.add(Iba_mean_density, fill_value=0).add(GFAP_mean_density, fill_value=0)

# Add the new columns to the DataFrame
df['subject_mean_density'] = df['subject'].map(subject_mean_density)
df['Neun_mean_density'] = df['subject'].map(Neun_mean_density)
df['Iba_mean_density'] = df['subject'].map(Iba_mean_density)
df['GFAP_mean_density'] = df['subject'].map(GFAP_mean_density)



# Group the data by 'subject' and 'cell' and calculate the mean of 'total_area' for each cell type
Neun_mean_max_area = df[df['cell'] == 'Neun'].groupby('subject')['max_area'].mean()
Iba_mean_max_area = df[df['cell'] == 'Iba'].groupby('subject')['max_area'].mean()
GFAP_mean_max_area = df[df['cell'] == 'GFAP'].groupby('subject')['max_area'].mean()

# Calculate the overall mean area as the sum of the mean areas for each cell type
subject_mean_max_area = Neun_mean_max_area.add(Iba_mean_max_area, fill_value=0).add(GFAP_mean_max_area, fill_value=0)

# Add the new columns to the DataFrame
df['max_mean_area_subject'] = df['subject'].map(subject_mean_max_area)
df['max_mean_area_Neun'] = df['subject'].map(Neun_mean_max_area)
df['max_mean_area_Iba'] = df['subject'].map(Iba_mean_max_area)
df['max_mean_area_GFAP'] = df['subject'].map(GFAP_mean_max_area)


# Save the modified DataFrame back to the CSV file
df.to_csv(f"/Users/juanpablomayaarteaga/Desktop/{region}_mean.csv", index=False)



