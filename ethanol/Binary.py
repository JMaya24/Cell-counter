#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 20:01:17 2023

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
group = "H-alc"
subject = "06"
cells = ["Neun", "GFAP", "Iba"]

input_base_path = "/Users/juanpablomayaarteaga/Desktop/Inmuno/" + region + "/" + group + "/" + subject

for cell in cells:
    input_path = os.path.join(input_base_path, cell, "Thresholding")
    im_list = list_png_files(input_path)

    output_path = os.path.join(input_path, "Binary_Mask")
    os.makedirs(output_path, exist_ok=True)

    for im in im_list:
        image = io.imread(im)

        # Convert image to binary
        binary_image = image > 0  # Adjust the threshold value as needed

        # Save the segmented image
        output_filename = os.path.splitext(os.path.basename(im))[0] + "_binary.png"
        output_filepath = os.path.join(output_path, output_filename)
        io.imsave(output_filepath, binary_image.astype(np.uint8) * 255)
