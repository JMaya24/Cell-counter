#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 18:40:36 2023

@author: juanpablomayaarteaga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:40:38 2023

@author: juanpablomayaarteaga
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import glob
from skimage import io, exposure, filters, morphology, feature, measure, segmentation, restoration

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files

region="PCM"
group="H-alc"
subject="06"
cell_type=["GFAP", "Iba", "Neun"]

input_path = "/Users/juanpablomayaarteaga/Desktop/Inmuno/" + region + "/" + group + "/" + subject + "/"+ cell_type +"/"
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

    neun = image[:, :, 0]  # Red channel
    iba = image[:, :, 1]  # Green channel
    gfap = image[:, :, 2]  # Blue channel

    # GAMMA CORRECTION
    gamma_values = [1.0, 1.2, 0.7, 0.5, 0.4, 0.3]

    for gamma in gamma_values:
        neun_gamma = exposure.adjust_gamma(neun, gamma=gamma)
        gfap_gamma = exposure.adjust_gamma(gfap, gamma=gamma)
        iba_gamma = exposure.adjust_gamma(iba, gamma=gamma)

        # Non-local Means Denoising
        denoised_neun = restoration.denoise_nl_means(neun_gamma, patch_size=5, patch_distance=7, h=0.1)
        denoised_gfap = restoration.denoise_nl_means(gfap_gamma, patch_size=5, patch_distance=7, h=0.1)
        denoised_iba = restoration.denoise_nl_means(iba_gamma, patch_size=5, patch_distance=7, h=0.1)

        plt.imshow(denoised_neun, cmap='gray')
        plt.axis('off')
        plt.savefig(os.path.join(neun_path, f"{os.path.splitext(os.path.basename(im))[0]}_neun_gamma{gamma}_denoised.png"),
                    bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()

        plt.imshow(denoised_gfap, cmap='gray')
        plt.axis('off')
        plt.savefig(os.path.join(gfap_path, f"{os.path.splitext(os.path.basename(im))[0]}_gfap_gamma{gamma}_denoised.png"),
                    bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()

        plt.imshow(denoised_iba, cmap='gray')
        plt.axis('off')
        plt.savefig(os.path.join(iba_path, f"{os.path.splitext(os.path.basename(im))[0]}_iba_gamma{gamma}_denoised.png"),
                    bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
        plt.close()

        

