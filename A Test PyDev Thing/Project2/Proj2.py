'''
Created on Sep. 20, 2019

@author: A
'''

##IMPORTS

import math
import numpy

import matplotlib.pyplot as plt
import DiscrepScore

##FUNCTIONS


def maskImage(img): ##the basic method of restoring the image using the Laplace equation
    

    return img

def ImgRestoreBasic(img): ##the basic method of restoring the image using the Laplace equation
    

    return img

##MAIN

if __name__ == '__main__':
    originalImg = importfile('C:\File.jpg') ##the original image(s)
    damagedImg = maskImage(originalImg) ##image to be 'restored'
    
    
    
    ##start with simple method
    print('Beginning with the simple method...')
    restoredImg = ImgRestoreBasic(damagedImg)
    
    print('Discrepancy Score = ' + DiscrepScore.get(originalImg, restoredImg, damagedImg))
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
        