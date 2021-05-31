#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:38:47 2021

@author: chinmay
"""


import pandas as pd
import numpy as np
import os

#%% Determine which classes to delete
class_to_remove = ['Person','Man','Boy','Girl', 'Mammal','Woman', 'Human mouth', 
                   'Human body', 'Human foot', 'Human leg', 
                   'Human ear', 'Human hair', 'Human head',
                   'Human arm','Human face', 'Human nose',
                   'Human hand', 'Human eye', 'Human beard']  


#select number of images to download
n_images = 2000 
split = "validation" #Do not change this. 
                     #Code has assumed that you downloaded validation annotations.

#%%  Function to genearte label files in YOLOv3 format 
def generate_labels(annot_filt, n_images, class_desc):
    annot_filt = np.array(annot_filt)
    label_path = 'data/labels/'
    image_path = 'data/images/'
    unq_id= []
    
    for count,(ID, mid, xmin, xmax, ymin, ymax) in enumerate(annot_filt):
        
        class_id = class_desc.index[class_desc['mid'] == str(mid)].tolist()[0]
    
        if ID not in unq_id:
            unq_id.append(ID)
            
        if len(unq_id)==n_images+1:
            break
        
        labelname = str(ID) + ".txt"
        imagename = str(ID) + ".jpg"
        full_label_path = os.path.join(label_path, labelname)
        full_image_path = os.path.join(image_path, imagename)
    
        file = open(full_label_path, "a+")
        file.write(full_image_path + " " + str(xmin) + "," + str(xmax) + "," + 
                   str(ymin) + "," + str(ymax) + "," + str(class_id) + "\n")
        file.close()
        

    return unq_id[:-1]

#Function to generate .txt file with unique Image ID's for download
def generate_Image_Ids(unq_ids):
    
    filename = "ImageIds.txt"
    file = open(filename, 'w')

    for id in unq_ids:
        file.write(split + '/' + id+'\n')
    file.close()



#%% Main function
def main(): 
    #Import data using pandas
    annot = pd.read_csv (r'validation-annotations-bbox.csv')
    annot = annot[['ImageID','LabelName','XMin', 'XMax', 'YMin', 'YMax']]

    class_desc = pd.read_csv (r'class-descriptions-boxable.csv', header=None)
    class_desc.columns = ["mid", "class"]

    v_annot = pd.read_csv (r'validation-annotations-human-imagelabels-boxable.csv')
    v_annot = v_annot[v_annot['Confidence']==1]


    #filtering data by removing selected classes 
    mids = class_desc[class_desc['class'].isin(class_to_remove)]['mid']
    v_annot = v_annot[~v_annot['LabelName'].isin(list(mids))]
    #annot_filt = annot[~annot['LabelName'].isin(list(mids))]

    #Preserve only those annotations having confidence score = 1
    idxs = list(zip(v_annot.ImageID.values, v_annot.LabelName.values))
    annot_filt = annot[pd.Series(list(zip(annot.ImageID, annot.LabelName)), 
                             index=annot.index).isin(idxs)]


    #Generate ImageID's to download and label files in YOLOv3 format 
    unq_ids = generate_labels(annot_filt, n_images, class_desc)
    generate_Image_Ids(unq_ids)

if __name__ == "__main__":
    main()


    
    