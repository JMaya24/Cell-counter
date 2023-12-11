#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:13:14 2023

@author: juanpablomayaarteaga
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure

im_list = ["A.tif", "B.tif", "C.tif", "D.tif"]


output_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/06/Outputs/"
os.makedirs(output_path, exist_ok=True)

input_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/06/"

for im in im_list:
    image_path = input_path + im
    image = io.imread(image_path)
    im_max = np.max(image, axis=0)
    
    plt.imshow(im_max)
    plt.axis('off')
    plt.savefig(output_path + f"{im[:-4]}_maximum_projection.png", bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
    plt.close()  # Close the figure after saving