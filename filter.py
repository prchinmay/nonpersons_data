#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 16:38:04 2021

@author: chinmay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:38:47 2021

@author: chinmay
"""


import pandas as pd


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
def generate_ImageIds(annot_filt, n_images):   
    filename = "ImageIds.txt"
    file = open(filename, 'w')
    for id in annot_filt.ImageID.unique()[:n_images]:
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
    ImageIDs = v_annot.loc[v_annot['LabelName'].isin(mids)]['ImageID']
    ImageIDs = ImageIDs.drop_duplicates()
    v_annot = v_annot.loc[~v_annot['ImageID'].isin(ImageIDs)]

    #Preserve only those annotations having confidence score = 1
    idxs = list(zip(v_annot.ImageID.values, v_annot.LabelName.values))
    annot_filt = annot[pd.Series(list(zip(annot.ImageID, annot.LabelName)), 
                             index=annot.index).isin(idxs)]

    #Generate ImageID's to download and save filtered annotation file
    generate_ImageIds(annot_filt, n_images)
    annot_filt.to_csv ('annotations.csv', header=True)

if __name__ == "__main__":
    main()
