#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 19:25:36 2021

@author: chinmay
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from numpy import random
import os
import matplotlib.image as mpimg


#%%choose number of images to print at once

n_plots = 20

#%% plotting function
def plot_image(image, boxes, class_desc):
    """
    Plots specified bounding boxes on the image
    
    box[0] is XMax, box[2] is YMax
    box[1] is XMin, box[3] is YMin
    box[4] is class_id
    
    """
    
    im = np.array(image)
    height, width = im.shape[0], im.shape[1]

    # Create figure and axes
    fig, ax = plt.subplots(1)
    # Display the image
    ax.imshow(im)



    # Create a Rectangle patch
    for box in boxes:
        
        class_id = int(box[4])
        class_name = class_desc['class'][class_id]
        
        upper_left_x = box[1]
        upper_left_y = box[3]
        rect = patches.Rectangle(
            (upper_left_x * width, upper_left_y * height),
            (box[0]-box[1]) * width,
            (box[2] - box[3]) * height,
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        # Add the patch to the Axes
        ax.add_patch(rect)
        #Add class-text to picture
        ax.text(box[0]*width,box[2]*height, class_name, fontsize=10, color = 'red')
    plt.show()
        
        



#%%
def main(): 
    
    #Read data from files
    label_list = os.listdir('data/labels')
    class_desc = pd.read_csv (r'class-descriptions-boxable.csv', header=None)
    class_desc.columns = ["mid", "class"]

    #Loop for randomly printing images in directory along with bboxes
    for i in range(n_plots):  
        x = random.randint(len(label_list))
        labelname = label_list[x]
        full_label_path = os.path.join('data/labels', labelname)
        label = pd.read_csv(full_label_path, delimiter = "\t", header=None)
        label = label[0].str.split(" ", n=1, expand = True)
        ImagePath = label[0][0]
        boxes = label[1].str.split(",", n=4, expand = True)
        boxes = np.array(boxes).astype(np.float32)
        image = mpimg.imread(ImagePath)
        
        plot_image(image, boxes, class_desc)
        
        
if __name__ == "__main__":
    main()
    

  



  






























