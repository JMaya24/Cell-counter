#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:46:20 2023

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



#############1)Defining variables

######Paths

i_path = "/Users/juanpablomayaarteaga/Desktop/structure_tensor/Data/"

img=i_path+"Iba.tif"

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
        
        
        

image=cv2.imread(img)
image=image[:,:,0]
plt.imshow(image)
        #image = cv2.resize(img, (0,0), fx=0.2, fy=0.2)

        #############4) Selecting the ROI by setting points using the mouse
cv2.namedWindow(img)
cv2.setMouseCallback(img, mouse_callback)
while True:
    image_copy = image.copy()
    if len(roi_points) >= 3:
        roi_points_array = np.array(roi_points)
        cv2.fillPoly(image_copy, [roi_points_array], (0,255,0))
                
        cv2.imshow(img, image_copy)
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
save_tif(roi, name="_ROI.tif", path=Masks, variable=roi)




        #############4)Getting the Area of your selected ROI

gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
ret, binary_image = cv2.threshold(roi, 1, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

total_area = 0
for contour in contours:
    area = cv2.contourArea(contour)
    total_area += area

save_tif(image, name="_polygon.tif", path=Masks, variable=binary_image)