#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: juanpablomayaarteaga
"""
#enviroment Garza-Lab
#pip install opencv-python
#pip install tifffile
#pip install pandas
#pip install PySimpleGUI
#pip install matplotlib
#pip install scipy

#Libraries
import os
import cv2
import numpy as np
import pandas as pd
import tkinter as tk
import PySimpleGUI as sg
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.ndimage.measurements import label
from preprocess import gammaCorrection, set_path, save_tif

#############0) Initial Message
layout = [[sg.Text('\n \n   Hello! \n \n To do the cell count, follow the steps below:  \n \n 1) Select the directory which contains the images to be analyzed.\n \n 2) Then, the images will be displayed on the screen.  \n \n 3) By left clicking, delimite the region of interest (ROI). \n     By rigth clicking, erease the selected area. \n \n 4) Once you have finished selecting your ROI, press "q" key to visualize your area. \n     Press "q" key again to continue with the next image. \n \n ', 
                    font=("Helvetica", 20, "bold"))],
          [sg.Button("Ok")]]
                       
window = sg.Window("Cell counter: Maya", layout)
event, values = window.read()
window.close()


#############1)Setting Paths

######Paths
root = tk.Tk()
root.withdraw()
i_path = filedialog.askdirectory()
#i_path="/Users/juanpablomayaarteaga/Desktop/Prueba_Conteo/"

o_path= set_path(i_path+"/Output_images/")

Masks= set_path(o_path+"Masks/")

Plots= set_path(o_path+"Plots/")

csv_doc= set_path(o_path+"Data/")

df= pd.DataFrame(columns=["Image", "Cells_number", "Area"])


#Use the mouse to select points, and add them to a list
roi_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points.append((x,y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        roi_points.clear()


#############2)Loop through all the files in the input directory
for images in os.listdir(i_path):
    if images.endswith(".tif"):
        
        #######Reading the image
        input_file = os.path.join(i_path, images)
        image=cv2.imread(input_file)
        #image = cv2.resize(img, (0,0), fx=0.2, fy=0.2)

        #############Selecting the ROI by setting points using the mouse
        cv2.namedWindow(images)
        cv2.setMouseCallback(images, mouse_callback)
        while True:
            image_copy = image.copy()
            if len(roi_points) >= 3:
                roi_points_array = np.array(roi_points)
                cv2.fillPoly(image_copy, [roi_points_array], (0,255,0))
                
            cv2.imshow(images, image_copy)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        if len(roi_points) >= 3:
            mask = np.zeros_like(image[:,:,0])
            roi_points_array = np.array([roi_points])
            cv2.fillPoly(mask, roi_points_array, 255)
            roi = cv2.bitwise_and(image, image, mask=mask)

            cv2.imshow("ROI Selected, press 'q'", roi)
            cv2.waitKey(0)
            
        cv2.destroyAllWindows()
        save_tif(images, name="_ROI.tif", path=Masks, variable=roi)


        #############3)Getting the Area of your selected ROI
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, binary_image = cv2.threshold(roi, 1, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        total_area = 0
        for contour in contours:
              area = cv2.contourArea(contour)
              total_area += area

        save_tif(images, name="_polygon.tif", path=Masks, variable=binary_image)
        
        
        #############4) Preprocessing
        
        #A)Cropping the image to adjust to the ROI
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        cropped = roi[y:y+h, x:x+w]
        roi=cropped[:,:,2]
        
        
        #B)Gamma Correction: Non-lineal preprocessing to denoissign the image
        gammaImg = gammaCorrection(roi, 2)
        save_tif(images, "_gamma.tif", Masks, gammaImg)
      
        
        #C)Opening preprocessing to dealing with the branches
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(gammaImg,cv2.MORPH_OPEN,kernel, iterations = 1)
        save_tif(images, name="_opening.tif", path=Masks, variable=opening)
        
        
        
        #D)Setting a threshold
        ret, thresh = cv2.threshold(opening, 28, 255, cv2.THRESH_BINARY)
        save_tif(images, name="_binary.tif", path=Masks, variable=thresh)
        
        #############5)Counting Cells
        #Labeling
        labels, num_cells = label(thresh)
        fig, ax = plt.subplots()
        ax.imshow(thresh, cmap="gray")
        max_area= 250
        min_area= 10
        num_cells_filtered=0
        cells_areas = []
        
        #Counting 
        for i in range(1, num_cells+1):
            y, x = np.where(labels == i)
            area=len(x)
        
            if area >= min_area and area < max_area:
                num_cells_filtered +=1
                cells_areas.append(np.sum(labels == i))
                xc = (x.max() + x.min())/2
                yc = (y.max() + y.min())/2
                ax.text(xc, yc, str(num_cells_filtered), color="r", fontsize=8, ha="center", va="center")
                ax.set_title(f"{num_cells_filtered} cells")
        
        ######Saving Plot
        output_plot = images[:-4] + "_cell_counter.png"
        fig_path = os.path.join(Plots, output_plot)
        plt.savefig(fig_path)
        
        
        #############6)Storage data into a Dataframe
        df.loc[len(df)]=[images, num_cells_filtered, total_area ]
        

##############8)Export Dataframe to csv file
df.to_csv(csv_doc+"Morfina_Apotome_measurements.csv", index=False)

# Ending Message
layout = [[sg.Text('\n \n \n  Process completed! \n \n \n Inside the selected folder, there will be a directory called "Output_images". \n \n This directory will contain:\n \n A) "Masks", a folder containing the preprocessed images. \n \n B) "Plots", a folder containing plots with the identified cells. \n \n C) "Data", a folder containing the csv document with the image name, number of cells detected and area of the ROI selected \n \n \n \n', 
                   font=('Helvetica', 20, 'bold'))]]
window = sg.Window("Proccess done", layout)
event, values = window.read()
window.close()

        
        
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                  
