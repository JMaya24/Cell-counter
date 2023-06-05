#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 18:16:19 2023

@author: juanpablomayaarteaga
"""

import numpy as np
import cv2



def gammaCorrection(image, gamma):

    table = [((i / 255) ** gamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(image, table)



from PIL import Image

def padding(image_path, padding_rows, padding_cols):
    # Load the image
    image = Image.open(image_path).convert("L")

    # Get the dimensions of the original image
    width, height = image.size

    # Create a new image with the desired dimensions
    new_width = width + 2 * padding_cols
    new_height = height + 2 * padding_rows
    new_image = Image.new("L", (new_width, new_height), 0)

    # Paste the original image into the new image, leaving the padding area empty
    new_image.paste(image, (padding_cols, padding_rows))

    # Save the modified image
    new_image.save("padded_image.tiff")
    padded_image=np.array(new_image)

    print("Padding added successfully.")
    return padded_image


from scipy.ndimage import label, generate_binary_structure

def erase(image, elements):
    x=elements
    structure=generate_binary_structure(2,2)
    labeled_image, num_labels = label(image, structure)
    label_sizes=np.bincount(labeled_image.ravel())
    mask=label_sizes[labeled_image]>x
    erased_image=np.where(mask, image, 0)
    
    return erased_image



import os


def set_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        
    return path



import os
import tifffile as tiff


def save_tif(filename, name=None, path=None, variable=None):
    if name is None:
        name = "add_name"  # Replace "add_name" with your desired default value

    if path is None:
        path = "default/path"  # Replace "default/path" with your desired default value

    if variable is None:
        raise ValueError("The 'variable' argument is required.")

    output_filename = filename[:-4] + name
    output_path = os.path.join(path, output_filename)
    tiff.imwrite(output_path, variable)


