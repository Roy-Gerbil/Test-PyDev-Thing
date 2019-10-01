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
import ImgRestoreAdvancedtry2
import ImgRestoreAdvanced
import ImgRestoreBasic
import CreateMask
import ApplyDiffusion

##MAIN

if __name__ == '__main__':
    ###import image as greyscale, matrix of intensity values
    #Intensity matrix, values from 0 (black) to 1 (white)
    originalImg = skimage.io.imread('falco.png',as_gray=True).astype(numpy.float32)
    #maskforImage = CreateMask.createMask(originalImg, 'WCCG', 6) ##creates the mask for the image
    maskforImage = skimage.io.imread('falcomask.png',as_gray=True).astype(numpy.float32)
    damagedImg = originalImg * maskforImage ##image to be 'restored'
    
    plt.imshow(originalImg, cmap='gray', interpolation='nearest');
    plt.savefig('orgininalImg.png')
    plt.imshow(maskforImage, cmap='gray', interpolation='nearest');
    plt.savefig('maskforImage.png')
    plt.imshow(damagedImg, cmap='gray', interpolation='nearest');
    plt.savefig('damagedImg.png')
    
    #print(maskforImage)
    ##start with simple method
    #===========================================================================
    # print('Beginning with the simple method...')
    # relaxationFactor = 1.8 ##should be between 0 and 2
    # restoredImg = ImgRestoreBasic.restore(damagedImg, maskforImage, relaxationFactor)
    # plt.imshow(restoredImg, cmap='gray', interpolation='nearest');
    # plt.savefig('restoredImg.png')
    # 
    # print('Done...')
    # print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage)))
    #===========================================================================
    
    ##then the advanced one
    print('Now the advanced method...')
    
    #===========================================================================
    # shape = numpy.zeros(originalImg.shape)
    # ##perform some diffusion steps initially
    # for x in range(originalImg.shape[0]):
    #     for y in range(originalImg.shape[1]):
    #         if(y == 0 or x == 0 or y == originalImg.shape[0]-1 or x == originalImg.shape[1] - 1):
    #             shape[x, y] = 1
    # diffusedImage = ApplyDiffusion.diffusify(originalImg, shape, 5, ImgRestoreAdvanced.getBoundary(numpy.zeros(originalImg.shape), numpy.zeros(originalImg.shape)),  shape)
    # plt.imshow(diffusedImage, cmap='gray', interpolation='nearest');
    # plt.savefig('diffusedImg.png')
    #===========================================================================
    
    #restoredImg = ImgRestoreAdvanced.restore(damagedImg, maskforImage)
    restoredImg = ImgRestoreAdvancedtry2.restore(damagedImg, maskforImage)
    plt.imshow(restoredImg, cmap='gray', interpolation='nearest');
    plt.savefig('restoredImgAdv.png')
     
    print('Done...')
    print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage)))
    
    print('End')
pass   