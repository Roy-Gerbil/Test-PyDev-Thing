'''
Created on Sep. 20, 2019

@author: A
'''

##IMPORTS

import numpy
import matplotlib.pyplot as plt
import skimage.io
import skimage.viewer

##FUNCTIONS
import DiscrepScore
import MaskImage
import ImgRestoreBasic
import CreateMask

##MAIN

if __name__ == '__main__':
    
    ###import image as greyscale, matrix of intensity values
    #Intensity matrix, values from 0 (black) to 1 (white)
    originalImg = skimage.io.imread('image.png',as_grey=True).astype(numpy.float32)
    maskforImage = CreateMask.createMask(originalImg, 1) ##creates the mask for the image
    damagedImg = originalImg * maskforImage ##image to be 'restored'
    
    
    
    ##start with simple method
    print('Beginning with the simple method...')
    relaxationFactor = 1.9 ##should be between 0 and 2
    restoredImg = ImgRestoreBasic(damagedImg, maskforImage, relaxationFactor)
    
    plt.imshow(originalImg, cmap='gray', interpolation='nearest');
    plt.savefig('./Results/file.png')
    
    print('Discrepancy Score = ' + DiscrepScore.discrepScore(originalImg, restoredImg, damagedImg, maskforImage))
    print('End')
pass   