'''
Created on Sep. 20, 2019

@author: A
'''

##IMPORTS

import math
import numpy
import matplotlib.pyplot as plt
import skimage.io
import skimage.viewer
import sys

##FUNCTIONS
import DiscrepScore
import MaskImage
import ImgRestoreBasic
import CreateMask

##MAIN

if __name__ == '__main__':
    
    ###import image as greyscale, matrix of intensity values
    #Intensity matrix
    originalImg = skimage.io.imread('image.png',as_grey=True).astype(numpy.float32)
    plt.imshow(originalImg, cmap='gray', interpolation='nearest');
    plt.savefig('./Results/file.png')
    
    damagedImg = MaskImage.maskImage(originalImg) ##image to be 'restored'
    
    
    
    ##start with simple method
    print('Beginning with the simple method...')
    restoredImg = ImgRestoreBasic(damagedImg)
    
    print('Discrepancy Score = ' + DiscrepScore.discrepScore(originalImg, restoredImg, damagedImg, MaskImage))
    print('End')
pass   