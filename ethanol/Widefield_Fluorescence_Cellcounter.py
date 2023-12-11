#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: juanpablomayaarteaga
"""

#Libraries
import os
import cv2
import numpy as np
import pandas as pd
import tkinter as tk
import tifffile as tiff
import PySimpleGUI as sg
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.ndimage.measurements import label
from preprocess import gammaCorrection
from path import set_path
from save import save_tif



#0) Initial Message
layout = [[sg.Text('\n \n   Hello! \n \n To do the cell count, follow the steps below:  \n \n 1) Select the directory which contains the images to be analyzed.\n \n 2) Then, the images will be displayed on the screen.  \n \n 3) By left clicking, delimite the region of interest (ROI). \n     By rigth clicking, erease the selected area. \n \n 4) Once you have finished selecting your ROI, press "q" key to visualize your area. \n     Press "q" key again to continue with the next image. \n \n ', 
                    font=("Helvetica", 20, "bold"))],
          [sg.Button("Ok")]]
                       
window = sg.Window("Cell counter: Maya", layout)
event, values = window.read()
window.close()




#############1)Defining variables

######Paths
root = tk.Tk()
root.withdraw()
i_path = filedialog.askdirectory()
#i_path="/Users/juanpablomayaarteaga/Desktop/Prueba_Apotome/"

o_path= set_path(i_path+"/Output_images/")

Masks= set_path(o_path+"Masks/")

Plots= set_path(o_path+"Plots/")

csv_doc= set_path(o_path+"Data/")


df= pd.DataFrame(columns=["Image", "Cells_number", 'Total Area (um^2)'])


#Use the mouse to select points, and add them to a list
roi_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points.append((x,y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        roi_points.clear()
        
        
      # Pixel-to-um conversion factors
# Pixel-to-um conversion factors
pixel_size_original = 5.86  # micrometers
pixel_size_reduced = 0.73  # micrometers

# Loop through all the files in the input directory
for images in os.listdir(i_path):
    if images.endswith(".png"):
        # Read the file
        input_file = os.path.join(i_path, images)
        image = cv2.imread(input_file)

        # Selecting the ROI by setting points using the mouse
        cv2.namedWindow(images)
        cv2.setMouseCallback(images, mouse_callback)
        while True:
            image_copy = image.copy()
            if len(roi_points) >= 3:
                roi_points_array = np.array(roi_points)
                cv2.fillPoly(image_copy, [roi_points_array], (0, 255, 0))

            cv2.imshow(images, image_copy)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        if len(roi_points) >= 3:
            mask = np.zeros_like(image[:, :, 0])
            roi_points_array = np.array([roi_points])
            cv2.fillPoly(mask, roi_points_array, 255)
            roi = cv2.bitwise_and(image, image, mask=mask)

            cv2.imshow("ROI Selected, press 'q'", roi)
            cv2.waitKey(0)

            # Save ROI Image
            save_tif(images, name="_ROI.tif", path=Masks, variable=roi)

            # Getting the Area of your selected ROI
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            ret, binary_image = cv2.threshold(roi, 1, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            total_area = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                total_area += area

            save_tif(images, name="_polygon.tif", path=Masks, variable=binary_image)

            # Counting cells
            pixel_size = pixel_size_reduced  # Use the appropriate pixel size here
            pixel_to_um = pixel_size / 512  # um/pixel
            # Labeling
            labels, num_cells = label(binary_image[:, :, 0])
            fig, ax = plt.subplots()
            ax.imshow(binary_image[:, :, 0], cmap="gray")
            max_area = 250000000000000
            min_area = 1
            num_cells_filtered = 0
            cells_areas = []

            # Counting
            for i in range(1, num_cells + 1):
                y, x = np.where(labels == i)
                area = len(x)

                if area >= min_area and area < max_area:
                    num_cells_filtered += 1
                    cells_areas.append(np.sum(labels == i))
                    xc = (x.max() + x.min()) / 2
                    yc = (y.max() + y.min()) / 2
                    ax.text(xc, yc, str(num_cells_filtered), color="r", fontsize=8, ha="center", va="center")

            # Save Plot
            total_area_pixels = np.sum(cells_areas)
            total_area_um2 = total_area_pixels * (pixel_to_um ** 2)
            # Turn off the axis
            ax.axis("off")
            output_plot = images[:-4] + "_area.png"
            fig_path = os.path.join(Plots, output_plot)
            plt.savefig(fig_path)

            # Storage data into a DataFrame
            df.loc[len(df)] = [images, num_cells_filtered, total_area_um2]

# Export DataFrame to CSV file
df.to_csv(csv_doc + "Area.csv", index=False)


# Message
layout = [[sg.Text('\n \n \n  Process completed! \n \n \n Inside the selected folder, there will be a directory called "Output_images". \n \n This directory will contain:\n \n A) "Masks", a folder containing the preprocessed images. \n \n B) "Plots", a folder containing plots with the identified cells. \n \n C) "Data", a folder containing the csv document with the image name, number of cells detected and area of the ROI selected \n \n \n \n', 
                   font=('Helvetica', 20, 'bold'))]]
window = sg.Window("Proccess done", layout)
event, values = window.read()
window.close()

        
        
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
larger_area = 103683  # square micrometers
smaller_area = 1306  # square micrometers

times_larger = larger_area / smaller_area

print(f"{times_larger:.2f} times")
     
        
import math

diameter = 20  # micrometers

radius = diameter / 2
surface_area = math.pi * radius ** 2

print(f"Surface area of the circle: {surface_area:.2f} square micrometers")

        
        
        
        
        
        
        
        
        
        
        
                  
