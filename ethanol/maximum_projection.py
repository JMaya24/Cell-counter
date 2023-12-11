#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:15:58 2023

@author: juanpablomayaarteaga
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure

im_list = ["A.tif", "B.tif", "C.tif"]


output_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/04/Outputs/"
os.makedirs(output_path, exist_ok=True)

input_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/04/"

for im in im_list:
    image_path = input_path + im
    image = io.imread(image_path)
    im_max = np.max(image, axis=0)
    
    plt.imshow(im_max)
    plt.axis('off')
    plt.savefig(output_path + f"{im[:-4]}_maximum_projection.png", bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
    plt.close()  # Close the figure after saving
    
    # IMAGE SHAPE
    height, width, channels = im_max.shape
    print("Image shape:", height, "height", "x", width, "width", "x", channels, "channels")
    
    # SPLIT CHANNELS
    neun_path = output_path + "Neun/"
    os.makedirs(neun_path, exist_ok=True)
    gfap_path = output_path + "GFAP/"
    os.makedirs(gfap_path, exist_ok=True)
    iba_path = output_path + "IBA/"
    os.makedirs(iba_path, exist_ok=True)
    
    neun = im_max[:, :, 0]  # Red channel
    iba = im_max[:, :, 1]  # Green channel
    gfap = im_max[:, :, 2]  # Blue channel
    
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



