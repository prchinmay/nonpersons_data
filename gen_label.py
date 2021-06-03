#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:49:09 2021

@author: chinmay
"""

import pandas as pd
import numpy as np
import os
import matplotlib.image as mpimg
from pathlib import Path

#%% Function to generate labels in YOLOV3 format
def generate_labels(annot, class_desc):
    annot = np.array(annot)
    label_path = 'data/labels/'
    image_path = 'data/images/'

    
    for count,(ID, mid, xmin, xmax, ymin, ymax) in enumerate(annot):
        
        class_id = class_desc.index[class_desc['mid'] == str(mid)].tolist()[0]
        
        labelname = str(ID) + ".txt"
        imagename = str(ID) + ".jpg"
        full_label_path = os.path.join(label_path, labelname)
        full_image_path = os.path.join(image_path, imagename)
        im = np.array(mpimg.imread(full_image_path))
        height, width = im.shape[0], im.shape[1]
        if Path(full_label_path).is_file():
            full_image_path = ""
            file = open(full_label_path, "a+")
            file.write(" " + str(int(xmin*width)) + "," + str(int(xmax*width)) + "," + 
                   str(int(ymin*height)) + "," + str(int(ymax*height)) + "," + str(class_id))
            file.close()
        else:
            file = open(full_label_path, "a+")
            file.write(full_image_path + " " + str(int(xmin*width)) + "," + str(int(xmax*width)) + "," + 
                   str(int(ymin*height)) + "," + str(int(ymax*height)) + "," + str(class_id))
            file.close()
            
#%% Main function
def main(): 
    #Necessary imports
    class_desc = pd.read_csv (r'class-descriptions-boxable.csv', header=None)
    annot = pd.read_csv ('annotations.csv', usecols=range(1,7))
    ImageIds = pd.read_csv('ImageIds.txt', delimiter = "\t", header=None)
    
    #Filter annotation file to choose only Images that were downloaded
    class_desc.columns = ["mid", "class"]
    ImageIds = ImageIds[0].str.split("/", n=1, expand = True)[1]
    annot = annot.loc[annot['ImageID'].isin(ImageIds)]
    
    #Generate labels    
    generate_labels(annot, class_desc)
    
if __name__ == "__main__":
    main()
            