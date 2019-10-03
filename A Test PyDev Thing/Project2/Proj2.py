'''
Created on Sep. 20, 2019


@author: Alexandros Pallaris, Hilmi Kycyku
'''

##IMPORTS

import numpy
import matplotlib.pyplot as plt
import skimage.io
import cv2
##The functions in the other files
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
    originalImg = skimage.io.imread('img2.png',as_gray=True).astype(numpy.float32)
    ###import image as an array of RGB values to get colour
    img = cv2.imread('img2.png', cv2.IMREAD_COLOR)
    maskforImage = CreateMask.createMask(originalImg, 'CCG', 7) ##creates the mask for the image
    #maskforImage = skimage.io.imread('anothermask2.png',as_gray=True).astype(numpy.float32)
    
    ##make sure that mask values are 1 or 0
    for x in range(maskforImage.shape[0]):
        for y in range(maskforImage.shape[1]):
            if(maskforImage[x, y] < 0.9):
                maskforImage[x, y] = 0
            else:
                maskforImage[x, y] = 1
    
    
    
    damagedImg = originalImg * maskforImage ##image to be 'restored'
    
    plt.imshow(originalImg, cmap='gray', interpolation='nearest');
    plt.savefig('orgininalImg.png')
    cv2.imwrite('orgininalImg.png', originalImg*256)
    plt.imshow(maskforImage, cmap='gray', interpolation='nearest');
    plt.savefig('maskforImage.png')
    cv2.imwrite('maskforImage.png', maskforImage*256)
    plt.imshow(damagedImg, cmap='gray', interpolation='nearest');
    plt.savefig('damagedImg.png')
    cv2.imwrite('damagedImg.png', damagedImg*256)
    
    
    #separate the array of RGB into three, one for each color
    R = numpy.zeros((img.shape[0], img.shape[1]))
    G = numpy.zeros((img.shape[0], img.shape[1]))
    B = numpy.zeros((img.shape[0], img.shape[1]))

    
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            R[x, y] = img[x, y, 0]
            G[x, y] = img[x, y, 1]
            B[x, y] = img[x, y, 2]
    
    ###scale down the values to keep the same scheme as with the grayscale image, later to be scaled back up for printing
    Rscale = numpy.max(R)
    R = R * maskforImage/Rscale##could have just multiplied the mask in to the original array, but did this instead
    Gscale = numpy.max(G)
    G = G * maskforImage/Gscale
    Bscale = numpy.max(B)
    B = B * maskforImage/Bscale
    
    for x in range(0, img.shape[0]): 
        for y in range(0, img.shape[1]):
            img[x, y, 0] = R[x, y]*Rscale
            img[x, y, 1] = G[x, y]*Gscale
            img[x, y, 2] = B[x, y]*Bscale
    cv2.imwrite('damagedInColour.jpg', img) ##saves the damaged image in a file
    
    #print(maskforImage)
    #start with simple method
    
    print('Beginning with the simple method...')
    relaxationFactor = 1.8 ##should be between 0 and 2 
    #===========================================================================
    # restoredImg = ImgRestoreBasic.restore(damagedImg, maskforImage, relaxationFactor)
    # plt.imshow(restoredImg, cmap='gray', interpolation='nearest');
    # plt.savefig('restoredImg.png') ##save the result in a file
    # cv2.imwrite('restoredImg.png', restoredImg*256)
    #  
    # print('Done...')
    # print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage)))
    #===========================================================================
    
    
    ##color version
    print('R')
    restoredImgR = ImgRestoreBasic.restore(R*maskforImage, maskforImage, relaxationFactor)
    print('G')
    restoredImgG = ImgRestoreBasic.restore(G*maskforImage, maskforImage, relaxationFactor)
    print('B')
    restoredImgB = ImgRestoreBasic.restore(B*maskforImage, maskforImage, relaxationFactor)
    
    for x in range(0, img.shape[0]): ##rescale coloured values back up
        for y in range(0, img.shape[1]):
            img[x, y, 0] = restoredImgR[x, y]*Rscale
            img[x, y, 1] = restoredImgG[x, y]*Gscale
            img[x, y, 2] = restoredImgB[x, y]*Bscale
            
    cv2.imwrite('restoredImgColor.jpg', img) ##saves the result in the image file
            
    ##for colour, R G and B discrepancy scores
    
    print('R Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgR, maskforImage))) 
    print('G Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgG, maskforImage))) 
    print('B Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgB, maskforImage))) 
    
    ##then the advanced one
    print('Now the advanced method...')
    
    #===========================================================================NOT USED CURRENTLY
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
    
    ##color version
    print('R')
    restoredImgR = ImgRestoreAdvanced.restore(R*maskforImage, maskforImage, 6)
    print('G')
    restoredImgG = ImgRestoreAdvanced.restore(G*maskforImage, maskforImage, 6)
    print('B')
    restoredImgB = ImgRestoreAdvanced.restore(B*maskforImage, maskforImage, 6)
    
    for x in range(0, img.shape[0]): ##rescale coloured values back up
        for y in range(0, img.shape[1]):
            img[x, y, 0] = restoredImgR[x, y]*Rscale
            img[x, y, 1] = restoredImgG[x, y]*Gscale
            img[x, y, 2] = restoredImgB[x, y]*Bscale
    
    cv2.imwrite('restoredImgColorAdv.jpg', img) ##saves the result in the image file
    
    
    ##grayscale version
    #===========================================================================
    # restoredImg = ImgRestoreAdvanced.restore(damagedImg, maskforImage, 6)
    # #restoredImg = ImgRestoreAdvancedtry2.restore(damagedImg, maskforImage) ##NOT USED CURRENTLY
    # plt.imshow(restoredImg, cmap='gray', interpolation='nearest');
    # plt.savefig('restoredImgAdv.png')
    # cv2.imwrite('restoredImgAdv.png', restoredImg*256)
    #  
    # print('Done...')
    # print('Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImg, maskforImage))) 
    #===========================================================================
    
    
    ##for colour, R G and B discrepancy scores
    
    print('R Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgR, maskforImage))) 
    print('G Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgG, maskforImage))) 
    print('B Discrepancy Score = ' + numpy.str(DiscrepScore.discrepScore(originalImg, restoredImgB, maskforImage))) 
    
    print('End')
pass   