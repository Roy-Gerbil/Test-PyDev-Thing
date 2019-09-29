import numpy
import ApplyDiffusion
import matplotlib.pyplot as plt

def getBoundary(I, mask):
    Boundary = numpy.zeros((I.shape[0], I.shape[1]))
    for x in range(0, I.shape[0]):
        for y in range(0, I.shape[1]):
            if(mask[x, y] == 0):
                if (mask[x-1,y] == 1): # Left
                    Boundary[x,y] = 1
                if (mask[x+1,y] == 1): # Right 
                    Boundary[x,y] = 2
                if (mask[x,y-1] == 1): # Top
                    Boundary[x,y] = 3
                if (mask[x,y+1] == 1): # Bottom
                    Boundary[x,y] = 4
                if (mask[x-1,y] == 1 and mask[x,y-1] == 1): #Left - Top
                    Boundary[x,y] = 5
                if (mask[x-1,y] == 1 and mask[x,y+1] == 1): #Left - Bottom
                    Boundary[x,y] = 6
                if (mask[x+1,y] == 1 and mask[x,y-1] == 1): #Right - Top
                    Boundary[x,y] = 7
                if (mask[x+1,y] == 1 and mask[x,y+1] == 1): #Right - Bottom
                    Boundary[x,y] = 8
    return(Boundary)

def getBounds(mask):
    bounds = numpy.zeros(mask.shape) + 1 ###0 when in-bounds
    for x in range(0, mask.shape[0]):
            for y in range(0, mask.shape[1]):
                if(mask[x, y] == 0):
                    bounds[x, y] = 0
                    bounds[x+1, y] = 0
                    bounds[x+2, y] = 0
                    bounds[x, y+1] = 0
                    bounds[x, y+2] = 0
                    bounds[x+1, y+1] = 0
                    bounds[x-1, y-1] = 0
                    bounds[x+1, y-1] = 0
                    bounds[x-1, y+1] = 0
                    bounds[x-1, y] = 0
                    bounds[x-2, y] = 0
                    bounds[x, y-1] = 0
                    bounds[x, y-2] = 0

    return bounds

def restore(I, mask): ##navier-stokes method of restoring the image, takes the image to restore and the mask that was applied
    ###The method used involved successive iteration over the masked part of the image (mask[x,y] == 0)
    
    L = numpy.zeros(I.shape)
    Ndir = numpy.zeros((I.shape[0], I.shape[1], 2))
    delL = numpy.zeros((I.shape[0], I.shape[1], 2))
    B = numpy.zeros(I.shape)
    It = numpy.zeros(I.shape)
    Ix = numpy.zeros(I.shape)
    Iy = numpy.zeros(I.shape)
    Ixx = numpy.zeros(I.shape)
    Iyy = numpy.zeros(I.shape)
    absGrad = numpy.zeros(I.shape)
    
    bounds = getBounds(mask)
    boundary = getBoundary(I, bounds)
    
    
    tempI = I ##for iteration, after each step newI is set to I
    dt = 0.1 #timestep
    Ttimes = 0 ##number of iterations, if using this stop condition
    EPS = 4 * 10**-5 ##largest pixel difference between steps before stopping, if using this stop condition
    looping = True
    while looping: ##restoration loop, A steps of inpainting, B steps of diffusion, and so on until the stop condition
        Ttimes += 1
        for A in range(0, 15): ## the inpainting loop
            print('A = ' +numpy.str(A))
            for x in range(0, I.shape[0]):
                for y in range(0, I.shape[1]):
                    if(bounds[x, y] == 0):
                        
                        if(boundary[x,y] == 1 or boundary[x,y] == 5 or boundary[x,y] == 6): #Left
                            Ix[x,y] = (3*I[x,y] - 4*I[x-1,y]+I[x-2,y])/2
                            Ixx[x,y] = (2*I[x,y] - 5*I[x-1,y] + 4*I[x-2,y]-I[x-3,y])
                        elif(boundary[x,y] == 2 or boundary[x,y] == 7 or boundary[x,y] == 8): #Right
                            Ix[x,y] = (-3*I[x,y] + 4*I[x+1,y]-I[x+2,y])/2
                            Ixx[x,y] = (2*I[x,y] - 5*I[x+1,y] + 4*I[x+2,y]-I[x+3,y])
                        else: #Center
                            Ix[x,y] = (I[x+1,y] + I[x-1,y])/2
                            Ixx[x,y] = (I[x+1,y] - 2*I[x,y] + I[x-1,y])
                            
                        if(boundary[x,y] == 3 or boundary[x,y] == 5 or boundary[x,y] == 7): #Top
                            Iy[x,y] = (-3*I[x,y] + 4*I[x,y+1]-I[x,y+2])/2
                            Iyy[x,y] = (2*I[x,y] - 5*I[x,y+1] + 4*I[x,y+2]-I[x,y+3])
                        elif(boundary[x,y] == 4 or boundary[x,y] == 6 or boundary[x,y] == 8): #Bottom
                            Iy[x,y] = (3*I[x,y] - 4*I[x,y-1]+I[x,y-2])/2
                            Iyy[x,y] = (2*I[x,y] - 5*I[x,y-1] + 4*I[x,y-2]-I[x,y-3])
                        else: #Center
                            Iy[x,y] = (I[x,y+1] + I[x,y-1])/2
                            Iyy[x,y] = (I[x,y+1] - 2*I[x,y] + I[x,y-1])
                        
                        L[x, y] = Ixx[x, y] + Iyy[x, y] ##2D smoothness estimation
                        
            for x in range(0, I.shape[0]):
                for y in range(0, I.shape[1]):
                    if(mask[x,y] == 0): ##only actually update pixels inside the mask
                        delL[x, y] = ( L[x+1, y] - L[x-1, y], L[x, y+1] - L[x, y-1]) ## a vector, x and y derivs of L (laplacian)
                        if( Iy[x, y] == 0 and Ix[x, y] == 0):
                            Ndir[x, y] = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
                        B[x, y] = numpy.dot( delL[x, y], Ndir[x, y] )#projection of delL onto Ndir
                        
                        if(B[x, y] > 0):
                            absGrad[x, y] = numpy.sqrt((min(I[x,y]-I[x-1,y], 0)**2) + (max(I[x+1,y]-I[x,y], 0)**2) + (min(I[x,y]-I[x,y-1], 0)**2) + (max(I[x,y+1]-I[x,y], 0)**2))
                        elif(B[x, y] < 0):
                            absGrad[x, y] = numpy.sqrt((max(I[x,y]-I[x-1,y], 0)**2) + (min(I[x+1,y]-I[x,y], 0)**2) + (max(I[x,y]-I[x,y-1], 0)**2) + (min(I[x,y+1]-I[x,y], 0)**2)) 
            
                        It[x, y] = B[x, y] * absGrad[x, y] ## derivative in time
                        ##here multiply B by a slop-limited version of the norm of the gradient of the image
                        
                        I[x, y] = I[x, y] + dt * It[x, y]
                        
        I = ApplyDiffusion.diffusify(I, bounds, 2, boundary, mask) ##the image, area to be diffused, number of diffusion steps, and boundary as above
                   
        #save current image 
        plt.imshow(I, cmap='gray', interpolation='nearest');
        plt.savefig('Iterations/restoredImgAdv' + numpy.str(Ttimes) +'.png')
    
        ##check if still looping
        maxDelta = (numpy.abs(I - tempI)).max() 
        if( maxDelta < EPS):
            looping = False
        else:
            print('Max delta = ' + numpy.str(maxDelta))
            print('Max It = ' + (numpy.abs(It)).max())
            tempI = I
            
        if(Ttimes == 100):
            looping = False
    
    return I