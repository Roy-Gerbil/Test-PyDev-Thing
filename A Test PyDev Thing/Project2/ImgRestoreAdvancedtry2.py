import numpy
import ApplyDiffusion
import matplotlib.pyplot as plt
from scipy.stats.morestats import levene
import cv2
import scipy.ndimage.filters

def restore(Io, mask): ##navier-stokes method of restoring the image, takes the image to restore and the mask that was applied
    I = Io * mask
    N = numpy.zeros((I.shape[0], I.shape[1], 2))
    Ndir = numpy.zeros((I.shape[0], I.shape[1], 2))
    delL = numpy.zeros((I.shape[0], I.shape[1], 2))
    absGrad = numpy.zeros(I.shape)
    B = numpy.zeros(I.shape)
    eps = 2 #distance from pixel to consider for inpainting
    dt = 0.1 #timestep, change to change magnitude of changes per step
    ###The method used involved successive iteration over the masked part of the image (mask[x,y] == 0)
    gradient = numpy.gradient(I)
    laplace = scipy.ndimage.filters.laplace(I)
    for x in range(1, I.shape[0]-1):
        for y in range(1, I.shape[1]-1):
            N[x, y, 0] = - gradient[1][x, y]
            N[x, y, 1] = gradient[0][x, y]
            Ndir[x, y] = N[x, y] / (numpy.linalg.norm(N[x, y]))
            delL[x, y] = numpy.array(([laplace[x+1, y] - laplace[x-1, y], laplace[x, y+1] - laplace[x, y-1] ])) / 2
            B[x, y] = numpy.dot(delL[x, y], Ndir[x, y])
            if(B[x, y] > 0):
                absGrad[x, y] = numpy.sqrt((min(I[x,y]-I[x-1,y], 0)**2) + (max(I[x+1,y]-I[x,y], 0)**2) + (min(I[x,y]-I[x,y-1], 0)**2) + (max(I[x,y+1]-I[x,y], 0)**2))
            elif(B[x, y] < 0):
                absGrad[x, y] = numpy.sqrt((max(I[x,y]-I[x-1,y], 0)**2) + (min(I[x+1,y]-I[x,y], 0)**2) + (max(I[x,y]-I[x,y-1], 0)**2) + (min(I[x,y+1]-I[x,y], 0)**2))
    It = B * absGrad
    I = I + dt * It
    return I