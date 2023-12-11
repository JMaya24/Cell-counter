#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:11:46 2023

@author: juanpablomayaarteaga
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import glob
import czifile
import tifffile

# Path to the directory containing CZI images
input_path = "/Users/juanpablomayaarteaga/Desktop/Confocal_MOR/Mor_S3_CPu_Dorsal/Otro_formato/"

# Output directory for TIFF images
output_path = f"{input_path}TIF/"
os.makedirs(output_path, exist_ok=True)



# DEF

def list_czi_images(directory):
    czi_images = glob.glob(directory + "/*.czi")
    return czi_images





# List all CZI images in the input directory
im_list = list_czi_images(input_path)
print(im_list)

# Loop through each CZI image
for image_path in im_list:
    # Open the CZI file
    with czifile.CziFile(image_path) as czi:
        # Get the pixel data as a numpy array
        data = czi.asarray()
        
        # Print the shape of the image
        print("Image shape:", data.shape)
        
        print(" - -"*20)
        
        print(f"Image {image_path} shape:", data.shape)