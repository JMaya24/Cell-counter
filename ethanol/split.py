#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:40:38 2023

@author: juanpablomayaarteaga
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure

im_list = ["A_maximum_projection.png", "B_maximum_projection.png", "C_maximum_projection.png"]

output_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/04/Outputs/"
os.makedirs(output_path, exist_ok=True)

for im in im_list:
    image_path = output_path + im
    image = io.imread(image_path)
    
    # Create a directory for each image
    image_dir = output_path + im[:-4] + "/"
    os.makedirs(image_dir, exist_ok=True)
    
    # Split CHANNELS
    neun_path = image_dir + "Neun/"
    os.makedirs(neun_path, exist_ok=True)
    gfap_path = image_dir + "GFAP/"
    os.makedirs(gfap_path, exist_ok=True)
    iba_path = image_dir + "IBA/"
    os.makedirs(iba_path, exist_ok=True)
    
    neun = image[:, :, 0]  # Red channel
    iba = image[:, :, 1]  # Green channel
    gfap = image[:, :, 2]  # Blue channel
    
    # GAMMA CORRECTION
    gamma_values = [1.0, 1.2, 0.7, 0.5, 1.5]
    
    for gamma in gamma_values:
        neun_gamma = exposure.adjust_gamma(neun, gamma=gamma)
        gfap_gamma = exposure.adjust_gamma(gfap, gamma=gamma)
        iba_gamma = exposure.adjust_gamma(iba, gamma=gamma)
        
        plt.imshow(neun_gamma, cmap='plasma')
        plt.axis('off')
        plt.savefig(neun_path + f"{im[:-4]}_neun_gamma{gamma}.png", bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()
        
        plt.imshow(gfap_gamma, cmap='viridis')
        plt.axis('off')
        plt.savefig(gfap_path + f"{im[:-4]}_gfap_gamma{gamma}.png", bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()
        
        plt.imshow(iba_gamma, cmap='magma')
        plt.axis('off')
        plt.savefig(iba_path + f"{im[:-4]}_iba_gamma{gamma}.png", bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()
        
