#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:40:38 2023

@author: juanpablomayaarteaga
"""


########### FLIP IMAGES

import numpy as np
from skimage import io


subject="03"
group="H-ctr"
region="PCM"

input_path = "/Users/juanpablomayaarteaga/Desktop/Inmuno/"+region+"/"+group+"/"+subject+"/"
output_path = input_path

slides = ["C_maximum_projection.png", "A_maximum_projection.png"]

for slide in slides:
    image_path = input_path + slide
    image = io.imread(image_path)

    # Flip the image horizontally
    flipped_image = np.fliplr(image)

    # Display or save the flipped image
    io.imshow(flipped_image)
    io.show()

    # Save the flipped image
    io.imsave(output_path + slide, flipped_image)
