#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 01:10:37 2023

@author: juanpablomayaarteaga
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure
import glob

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files

# Parameters
subjects = ["04", "06", "07", "03", "23", "47", "24", "43", "85", "46", "87"]
groups = ["H-alc", "H-ctr", "M-alc", "M-ctr"]
region = "PCM"



for group in groups:
    for subject in subjects:
        
        input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/Outputs/"
        
        im_list = list_png_files(input_path)
        
        output_path = input_path
        #os.makedirs(output_path, exist_ok=True)
        
        
        for im in im_list:
            image = io.imread(im)
            
            # Create a directory for each image
            image_dir = os.path.join(output_path, os.path.splitext(os.path.basename(im))[0])
            os.makedirs(image_dir, exist_ok=True)
            
            # Split CHANNELS
            neun_path = os.path.join(image_dir, "Neun")
            os.makedirs(neun_path, exist_ok=True)
            
            gfap_path = os.path.join(image_dir, "GFAP")
            os.makedirs(gfap_path, exist_ok=True)
            
            iba_path = os.path.join(image_dir, "IBA")
            os.makedirs(iba_path, exist_ok=True)
            
            neun = image[:, :, 0]  # Red channel
            iba = image[:, :, 1]  # Green channel
            gfap = image[:, :, 2]  # Blue channel
            
            # GAMMA CORRECTION
            gamma_values = [1.0, 0.7, 0.5, 0.4, 0.3]
            
            for gamma in gamma_values:
                neun_gamma = exposure.adjust_gamma(neun, gamma=gamma)
                gfap_gamma = exposure.adjust_gamma(gfap, gamma=gamma)
                iba_gamma = exposure.adjust_gamma(iba, gamma=gamma)
                
                plt.imshow(neun_gamma, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(neun_path, f"{os.path.splitext(os.path.basename(im))[0]}_neun_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
                
                plt.imshow(gfap_gamma, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(gfap_path, f"{os.path.splitext(os.path.basename(im))[0]}_gfap_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
                
                plt.imshow(iba_gamma, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(iba_path, f"{os.path.splitext(os.path.basename(im))[0]}_iba_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
                
                
                # Denoising
                neun_denoised = filters.gaussian(neun_gamma, sigma=1.0)
                gfap_denoised = filters.gaussian(gfap_gamma, sigma=1.0)
                iba_denoised = filters.gaussian(iba_gamma, sigma=1.0)
               
               # Watershed Segmentation
                threshold_neun = filters.threshold_otsu(neun_denoised)
                binary_neun = neun_denoised > threshold_neun
                binary_neun_cleaned = morphology.remove_small_objects(binary_neun, min_size=50)
                binary_neun_cleaned = morphology.binary_closing(binary_neun_cleaned, selem=morphology.disk(3))
                binary_neun_cleaned = morphology.binary_opening(binary_neun_cleaned, selem=morphology.disk(3))
                labeled_neun = measure.label(binary_neun_cleaned)
                distance_neun = ndi.distance_transform_edt(binary_neun_cleaned)
                coords_neun = feature.peak_local_max(distance_neun, min_distance=20, labels=binary_neun_cleaned)
                markers_neun = np.zeros(binary_neun_cleaned.shape, dtype=bool)
                markers_neun[tuple(coords_neun.T)] = True
                markers_neun, _ = ndi.label(markers_neun)
                labels_neun = segmentation.watershed(-distance_neun, markers_neun, mask=binary_neun_cleaned)
                num_cells_neun = np.max(labels_neun)
                print(f"Number of cells (Neun): {num_cells_neun}")
               
               # Repeat the above steps for gfap and iba channels
               
               # Save the processed images
                plt.imshow(neun_denoised, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(neun_path, f"{os.path.splitext(os.path.basename(im))[0]}_neun_denoised_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
