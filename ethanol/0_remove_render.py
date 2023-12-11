#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:43:02 2023

@author: juanpablomayaarteaga
"""

import os
import glob


subject="49"
group="M-ctr"
region="Lob"


input_path = "/Users/juanpablomayaarteaga/Desktop/"+region+"/"+group+"/"+subject+"/"

im_list = list(input_path)


def remove(directory, name):
    # Find all files matching the name pattern in the directory
    files = glob.glob(os.path.join(directory, f"*{name}*"))

    # Remove each file
    for file in files:
        os.remove(file)

################   REMOVE RENDER IMAGES
name_pattern = "_Render_"
remove(input_path, name_pattern)



def rename_lsm_files(directory):
    lsm_files = [f for f in os.listdir(directory) if f.endswith(".lsm")]
    lsm_files.sort()  # Sort the files alphabetically

    for i, file in enumerate(lsm_files):
        old_name = os.path.join(directory, file)
        new_name = os.path.join(directory, f"{chr(65 + i)}.tif")
        os.rename(old_name, new_name)


rename_lsm_files(input_path)