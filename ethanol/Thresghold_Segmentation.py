#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 19:59:10 2023

@author: juanpablomayaarteaga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 19:42:27 2023
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

    output_path = os.path.join(input_path, "Segmentation")
    os.makedirs(output_path, exist_ok=True)

    for im in im_list:
        image = io.imread(im)

        # Apply Sauvola thresholding
        window_size = 51  # Adjust this value according to the size of your cells
        thresholded_image = filters.threshold_sauvola(image, window_size)

        # Convert thresholded image to binary
        binary_image = image > thresholded_image

        # Apply watershed segmentation
        distance = morphology.distance_transform_edt(binary_image)
        local_maxima = feature.peak_local_max(distance, min_distance=20, labels=binary_image)
        markers = measure.label(local_maxima)
        segmented_image = segmentation.watershed(-distance, markers, mask=binary_image)

        # Save the segmented image
        output_filename = os.path.splitext(os.path.basename(im))[0] + "_segmented.png"
        output_filepath = os.path.join(output_path, output_filename)
        io.imsave(output_filepath, segmented_image.astype(np.uint8) * 255)
