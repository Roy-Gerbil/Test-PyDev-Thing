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
import ImgRestoreAdvanced
import ImgRestoreBasic
import CreateMask

##MAIN

if __name__ == '__main__':
    ###import image as greyscale, matrix of intensity values
    #Intensity matrix, values from 0 (black) to 1 (white)
    originalImg = skimage.io.imread('empt.png',as_gray=True).astype(numpy.float32)
    maskforImage = CreateMask.createMask(originalImg, 'FBRCG', 9) ##creates the mask for the image
    #maskforImage = skimage.io.imread('testmask.png',as_gray=True).astype(numpy.float32)
    damagedImg = originalImg * maskforImage ##image to be 'restored'
    
    #print(maskforImage)
    ##start with simple method
    print('Beginning with the simple method...')
    relaxationFactor = 1.8 ##should be between 0 and 2
    restoredImg = ImgRestoreBasic.restore(damagedImg, maskforImage, relaxationFactor)
    
    
    plt.imshow(originalImg, cmap='gray', interpolation='nearest');
    plt.savefig('orgininalImg.png')
    plt.imshow(maskforImage, cmap='gray', interpolation='nearest');
    plt.savefig('maskforImage.png')
    plt.imshow(damagedImg, cmap='gray', interpolation='nearest');
    plt.savefig('damagedImg.png')
    plt.imshow(restoredImg, cmap='gray', interpolation='nearest');
    plt.savefig('restoredImg.png')
    
    print('Done...')
    
    
    print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage)))
    
    
    #===========================================================================
    # print('Now the advanced method...')
    # 
    # restoredImg = ImgRestoreAdvanced.restore(damagedImg, maskforImage, relaxationFactor)
    # 
    # print('Done...')
    # print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage)))
    #===========================================================================
    
    print('End')
pass   