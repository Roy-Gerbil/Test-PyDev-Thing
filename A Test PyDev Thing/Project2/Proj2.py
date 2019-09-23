'''
Created on Sep. 20, 2019

@author: A
'''

##IMPORTS

import math
import numpy

import matplotlib.pyplot as plt

##FUNCTIONS


def maskImage(img): ##the basic method of restoring the image using the Laplace equation
    

    return img

def ImgRestoreBasic(img): ##the basic method of restoring the image using the Laplace equation
    

    return img

def getDiscrepancyScore(originalImg, restoredImg, damagedImg): ##obtain the chi squared discrapency between the restored image and the original image
    xvals = originalImg.shape[0]
    yvals = originalImg.shape[1]
    
    num = 0 ##the numerator in the equation for chi squared
    sigmasq = 0 ##sigma squared, the denominator in the equation for chi squared (but without the factor of 1/(n-1))
    n = 0 ##number of points
    Imean = 0 ##mean of data in the missing region
    
    ##find Imean
    for x in range(0, xvals):
        for y in range(0, yvals):
            if( damagedImg[x][y] == 0 ): ##sum over the pixels of the mission region only
                n = n + 1
                Imean = Imean + originalImg[x][y]
                
    Imean = Imean/n ##to get the actual mean value
    
    ##now, find chi squared
    for x in range(0, xvals):
        for y in range(0, yvals):
            if( damagedImg[x][y] == 0 ): ##sum over the pixels of the mission region only
                num = num + ( restoredImg[x][y] - originalImg[x][y] )**2
                sigmasq = sigmasq + ( originalImg - Imean )**2
    
    return ((n-1) / n) * (num/sigmasq)


##MAIN

if __name__ == '__main__':
    originalImg = importfile('C:\File.jpg') ##the original image
    damagedImg = maskImage(originalImg) ##image to be 'restored'
    
    
    
    ##start with simple method
    print('Beginning with the simple method...')
    restoredImg = ImgRestoreBasic(damagedImg)
    
    print('Discrepancy Score = ' + getDiscrepancyScore(originalImg, restoredImg, damagedImg))
    print('End')
pass



class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        