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
import glob

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files


subject="49"
group="M-ctr"
region="Lob"

input_path = "/Users/juanpablomayaarteaga/Desktop/"+region+"/"+group+"/"+subject + "/Outputs"

im_list = list_png_files(input_path)

output_path = input_path
os.makedirs(output_path, exist_ok=True)

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

    neun = image[:, :, 2]  # Red channel
    iba = image[:, :, 1]  # Green channel
    gfap = image[:, :, 0]  # Blue channel

    # GAMMA CORRECTION
    gamma_values = [0.3, 0.4, 0.5, 0.7, 1.0]

    for gamma in gamma_values:
        neun_gamma = exposure.adjust_gamma(neun, gamma=gamma)
        gfap_gamma = exposure.adjust_gamma(gfap, gamma=gamma)
        iba_gamma = exposure.adjust_gamma(iba, gamma=gamma)

        plt.imshow(neun_gamma, cmap='plasma')
        plt.axis('off')
        plt.savefig(os.path.join(neun_path, f"{os.path.splitext(os.path.basename(im))[0]}_neun_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()

        plt.imshow(gfap_gamma, cmap='viridis')
        plt.axis('off')
        plt.savefig(os.path.join(gfap_path, f"{os.path.splitext(os.path.basename(im))[0]}_gfap_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()

        plt.imshow(iba_gamma, cmap='magma')
        plt.axis('off')
        plt.savefig(os.path.join(iba_path, f"{os.path.splitext(os.path.basename(im))[0]}_iba_gamma{gamma}.png"), bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()
