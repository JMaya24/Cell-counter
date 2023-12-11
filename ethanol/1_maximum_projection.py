#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:13:14 2023

@author: juanpablomayaarteaga
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import glob

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.tif")
    return png_files


subject="49"
group="M-ctr"
region="Lob"

input_path = "/Users/juanpablomayaarteaga/Desktop/"+region+"/"+group+"/"+subject+"/"


im_list = list_png_files(input_path)
print(im_list)

output_path = input_path+"/Outputs/"
os.makedirs(output_path, exist_ok=True)

for im in im_list:
    image = io.imread(im)
    im_max = np.max(image, axis=0)
    
    plt.imshow(im_max)
    plt.axis('off')
    output_filename = os.path.join(output_path, f"{os.path.basename(im)[:-4]}_maximum_projection.png")
    plt.savefig(output_filename, bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
    plt.close()  # Close the figure after saving
