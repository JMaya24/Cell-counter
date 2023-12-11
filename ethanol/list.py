#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:29:42 2023

@author: juanpablomayaarteaga
"""

import glob

def list(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files





subject="06"


input_path = "/Users/juanpablomayaarteaga/Desktop/PCM/H-alc/"+subject+"/Outputs/"

im_list = list(input_path)
print(im_list)