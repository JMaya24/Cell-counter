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



#0) Initial Message
layout = [[sg.Text('\n \n   Hello! \n \n To do the cell count, follow the steps below:  \n \n 1) Select the directory which contains the images to be analyzed.\n \n 2) Then, the images will be displayed on the screen.  \n \n 3) By left clicking, delimite the region of interest (ROI). \n      By rigth clicking, erease the selected area. \n \n 4) Once you have finished selecting your ROI, press "q" key to visualize your area. \n Press "q" key again to continue with the next image. \n \n ', 
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

o_path=i_path+"/Output_images/"
if not os.path.isdir(o_path):
    os.mkdir(o_path)

Masks=o_path+"Masks/"
if not os.path.isdir(Masks):
    os.mkdir(Masks)
    
Plots=o_path+"Plots/"
if not os.path.isdir(Plots):
    os.mkdir(Plots)
    
csv_doc=o_path+"Data/"
if not os.path.isdir(excel_sheet):
    os.mkdir(csv_doc)

df= pd.DataFrame(columns=["Image", "Cells_number", "Area"])


#Use the mouse to select points, and add them to a list
roi_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points.append((x,y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        roi_points.clear()
    
    


#2)Loop through all the files in the input directory
for filename in os.listdir(i_path):
    if filename.endswith(".tif"):
        
        #######3)Reading the file
        input_file = os.path.join(i_path, filename)
        image=cv2.imread(input_file)
        #image = cv2.resize(img, (0,0), fx=0.2, fy=0.2)

        #############4) Selecting the ROI
        cv2.namedWindow(filename)
        cv2.setMouseCallback(filename, mouse_callback)
        while True:
            image_copy = image.copy()
            if len(roi_points) >= 3:
                roi_points_array = np.array(roi_points)
                cv2.fillPoly(image_copy, [roi_points_array], (0,255,0))
                
            cv2.imshow(filename, image_copy)
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
       

        #Save ROI Image
        output_filename = filename[:-4] + '_ROI.tif'
        output_path = os.path.join(Masks, output_filename)
        tiff.imwrite(output_path, roi)

        #############4)Getting the Area of your selected ROI

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, binary_image = cv2.threshold(roi, 1, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        total_area = 0
        for contour in contours:
              area = cv2.contourArea(contour)
              total_area += area

        ######SAVE Polygon
        output_filename = filename[:-4] + "_polygon.tif"
        output_path = os.path.join(Masks, output_filename)
        tiff.imwrite(output_path, binary_image)
        
        
        
        #############5)Counting cells

        ##Preprocessing
        #A)Cropping the image to adjust to the ROI
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        cropped = roi[y:y+h, x:x+w]
        roi=cropped[:,:,2]
        
            

        #B)Gamma Correction: Non-lineal preprocessing to denoissign the image
        
        def gammaCorrection(src, gamma):
            invGamma = 1 / gamma
        
            table = [((i / 255) ** invGamma) * 255 for i in range(256)]
            table = np.array(table, np.uint8)
        
            return cv2.LUT(src, table)
        
        gammaImg = gammaCorrection(roi, 0.5)
        ######SAVE Gamma
        output_filename = filename[:-4] + "_gamma.tif"
        output_path = os.path.join(Masks, output_filename)
        tiff.imwrite(output_path, gammaImg)
        
        
        
        #C)Opening preprocessing to dealing with the branches
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(gammaImg,cv2.MORPH_OPEN,kernel, iterations = 1)
        ######SAVE Opening
        output_filename = filename[:-4] + "_opening.tif"
        output_path = os.path.join(Masks, output_filename)
        tiff.imwrite(output_path, opening)
        
        
        
        #D)Setting a threshold
        ret, thresh = cv2.threshold(opening, 28, 255, cv2.THRESH_BINARY)
        ######SAVE Thresh
        output_filename = filename[:-4] + "_binary.tif"
        output_path = os.path.join(Masks, output_filename)
        tiff.imwrite(output_path, thresh)
        
        #Labeling
        labels, num_cells = label(thresh)
        fig, ax = plt.subplots()
        ax.imshow(thresh, cmap="gray")
        max_area= 350
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
        
        
        #############7)Storage data into a Dataframe
        df.loc[len(df)]=[filename, num_cells, total_area ]
        

#Export Dataframe to csv file
df.to_csv(csv_doc+"Morfina_Apotome_measurements.csv", index=False)
# Message
layout = [[sg.Text('\n \n \n  Process completed! \n \n \n Inside the selected folder, there will be a directory called "Output_images". \n \n This directory will contain:\n \n A) "Masks", a folder containing the preprocessed images. \n \n B) "Plots", a folder containing plots with the identified cells. \n \n C) "Data", a folder containing the csv document with the image name, number of cells detected and area of the ROI selected \n \n \n \n', 
                   font=('Helvetica', 20, 'bold'))]]
window = sg.Window("Proccess done", layout)
event, values = window.read()
window.close()

        
        
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                  
