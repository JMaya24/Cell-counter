#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:19:21 2023

@author: juanpablomayaarteaga
"""

import os

def rename_lsm_files(directory):
    lsm_files = [f for f in os.listdir(directory) if f.endswith(".lsm")]
    lsm_files.sort()  # Sort the files alphabetically

    for i, file in enumerate(lsm_files):
        old_name = os.path.join(directory, file)
        new_name = os.path.join(directory, f"{chr(65 + i)}.tif")
        os.rename(old_name, new_name)

# Specify the directory path
directory_path = "/path/to/lsm_files_directory"

# Call the function to rename the .lsm files
rename_lsm_files(directory_path)
