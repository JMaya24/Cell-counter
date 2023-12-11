#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:43:38 2023

@author: juanpablomayaarteaga
"""


import os
from morpho import set_path
import cv2
import numpy as np
import matplotlib.pyplot as plt



i_path = "/Users/juanpablomayaarteaga/Desktop/PCM"
o_path = set_path(i_path + "/Output_images/")

def calculate_area(image):
    # Read the  image
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)


    # Apply thresholding to convert to binary image
    _, thresholded_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    
    # Find connected components and label them
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresholded_image, connectivity=8)
    
    # Find the label with the largest area
    largest_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1  # Exclude background label (0)
    
    # Create a mask to keep only the largest object
    mask = np.where(labels == largest_label, 255, 0).astype(np.uint8)
    
    # Apply the mask to the original image to keep only the largest object
    result_img = cv2.bitwise_and(image, image, mask=mask)

    # Count the white pixels (foreground)
    area = cv2.countNonZero(result_img)

    return area, result_img




groups = ["H-alc"]
RID = ["04"]
cell = ["GFAP"]

for g in groups:
    for r in RID:
        for c in cell:
            img_directory = f"/{g}/{r}/{c}/"
            image_path = i_path + img_directory

            for image_name in os.listdir(image_path):
                if image_name.endswith(".png"):
                    # Construct the full path to the image
                    full_image_path = os.path.join(image_path, image_name)

                    # Read the image
                    #image = cv2.imread(full_image_path, cv2.IMREAD_GRAYSCALE)
                    
                    # Apply thresholding to convert to binary image
                    #_, thresholded_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
                    #plt.imshow(thresholded_image)

                    # Calculate the area
                    area, result_img = calculate_area(full_image_path)
                    print(f"Area of {image_name}: {area}")
                    plt.imshow(result_img)
                    #plt.title(f"Image: {image_name}")
                    plt.show()
                    cv2.imwrite(o_path+"_object.png", result_img)
                             
                             
                             