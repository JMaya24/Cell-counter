#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 23:43:33 2023

@author: juanpablomayaarteaga
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import glob
from skimage import io, restoration

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files

region = "PCM"
groups = ["H-alc"]
subjects = ["04"]
cells = ["Neun"]

for group in groups:
    for subject in subjects:
        for cell in cells:
            input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/{cell}"
            im_list = list_png_files(input_path)
            
            for im in im_list:
                image = io.imread(im)
            
                # Non-local Means Denoising
                denoised_image = restoration.denoise_nl_means(image, patch_size=5, patch_distance=7, h=0.1)
                
                # Create a unique directory for each image's denoised output
                filename = os.path.splitext(os.path.basename(im))[0]
                denoisse_path = os.path.join(input_path, "Denoisse", f"{filename}_denoised")
                os.makedirs(denoisse_path, exist_ok=True)
            
                plt.close()
            
                plt.imshow(denoised_image, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(denoisse_path, f"{filename}_{cell}_gamma_denoised.png"),
                            bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
