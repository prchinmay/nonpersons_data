#!/usr/bin/env bash

wget https://raw.githubusercontent.com/openimages/dataset/master/downloader.py

                                                         
mkdir data
mkdir data/images
mkdir data/labels 
                                                                                                                                                   
python filter.py                                                                                        
python downloader.py ImageIds.txt --download_folder=data/images --num_processes=5




