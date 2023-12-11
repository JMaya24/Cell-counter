#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 12:45:38 2023

@author: juanpablomayaarteaga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:40:38 2023
@author: juanpablomayaarteaga
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from skimage import io, exposure, restoration, filters, measure
from skimage.filters import threshold_otsu
import time
import pandas as pd

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files

def measure_execution_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

def process_images():
    region = "PCM"
    sex= "M-"
    group = "ctr"
    subjects = ["24", "85"]
    #subjects = ["04", "06", "07"] 
    #################################     INVERTED
    cells = ["GFAP", "Iba", "Neun",]
    results = []

    input_path = "/Users/juanpablomayaarteaga/Desktop/Inmuno/" + region + "/" + sex + group + "/"
    
    for subject in subjects:
        input_path_subject = os.path.join(input_path, subject)
        im_list_subject = list_png_files(input_path_subject)

        for cell in cells:
            derivatives_path = os.path.join(input_path_subject, "Derivatives", cell)
            os.makedirs(derivatives_path, exist_ok=True)

            image_path = os.path.join(derivatives_path, cell)
            os.makedirs(image_path, exist_ok=True)

            denoise_path = os.path.join(derivatives_path, "Denoise")
            os.makedirs(denoise_path, exist_ok=True)

            gamma_path = os.path.join(derivatives_path, "Gamma")
            os.makedirs(gamma_path, exist_ok=True)

            threshold_path = os.path.join(derivatives_path, "Threshold")
            os.makedirs(threshold_path, exist_ok=True)

            for im in im_list_subject:
                image = io.imread(im)

                # Split CHANNELS
                channel_path = os.path.join(image_path)
                os.makedirs(channel_path, exist_ok=True)

                channel_image = image[:, :, cells.index(cell)]  # Channel image

                # Save channel image
                plt.imshow(channel_image, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(channel_path, f"{os.path.splitext(os.path.basename(im))[0]}.png"),
                            bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()

                # GAMMA CORRECTION
                gamma_values = [0.5, 0.4, 0.3, 0.6, 0.7]

                for gamma in gamma_values:
                    gamma_image = exposure.adjust_gamma(channel_image, gamma=gamma)

                    # Save gamma-corrected image
                    plt.imshow(gamma_image, cmap='gray')
                    plt.axis('off')
                    plt.savefig(os.path.join(gamma_path, f"{os.path.splitext(os.path.basename(im))[0]}_gamma{gamma}.png"),
                                bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                    plt.close()

                    # Non-local Means Denoising
                    denoised_image = restoration.denoise_nl_means(gamma_image, patch_size=5, patch_distance=7, h=0.1)

                    # Save denoised image
                    plt.imshow(denoised_image, cmap='gray')
                    plt.axis('off')
                    plt.savefig(os.path.join(denoise_path, f"{os.path.splitext(os.path.basename(im))[0]}_gamma{gamma}_denoised.png"),
                                bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                    plt.close()

                    # Apply Otsu's thresholding
                    threshold_value = threshold_otsu(denoised_image)
                    binary_image = denoised_image > threshold_value
                    
                    # Convert binary image to np.uint8 data type
                    binary_image = binary_image.astype(np.uint8) * 255

                    # Save the thresholded image
                    output_filename = os.path.splitext(os.path.basename(im))[0] + f"_gamma{gamma}_denoised_thresholded.png"
                    output_filepath = os.path.join(threshold_path, output_filename)
                    io.imsave(output_filepath, binary_image)


# Measure the execution time of the image processing function
measure_execution_time(process_images)



