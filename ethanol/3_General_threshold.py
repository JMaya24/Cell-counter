#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 22:18:09 2023

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

region = "PCM"
groups = ["H-alc", "H-ctr", "M-alc", "M-ctr"]
subjects = ["04"]
cells = ["Neun"]


#subjects= ["04", "06", "07", "03", "23", "47", "24", "43", "85", "46", "87"]


for group in groups:
    
    for subject in subjects:
        
        for cell in cells:
            input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/{cell}"
            im_list = list_png_files(input_path)

        for im in im_list:
            image = io.imread(im)
    
            # Apply Sauvola thresholding
            window_size = 51  # Adjust this value according to the size of your cells
            thresholded_image = filters.threshold_sauvola(image, window_size)
    
            # Convert thresholded image to binary
            binary_image = image > thresholded_image
            
            threshold_path = os.path.join(input_path, "Threshold")
            os.makedirs(threshold_path, exist_ok=True)
    
            # Save the thresholded image
            output_filename = os.path.splitext(os.path.basename(im))[0] + "_thresholded.png"
            output_filepath = os.path.join(threshold_path, output_filename)
            io.imsave(output_filepath, binary_image.astype(np.uint8) * 255)
        