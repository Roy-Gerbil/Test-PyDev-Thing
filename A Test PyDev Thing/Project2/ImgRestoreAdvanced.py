import numpy
def g(s):##perona-malik anisotropic diffusion function
    K = 10**-12 ##diffusion parameter
    g = 1/(1+(s/K)**2)
    return g

def boundary(I, mask):
    Boundary = numpy.zeros((I.shape[0], I.shape[1], 4))
    for x in range(0, I.shape[0]):
        for y in range(0, I.shape[1]):
            if (mask[x,y] == 0 and mask[x-1,y] == 1): # Left
                Boundary[x,y,0] = 1
            if (mask[x,y] == 0 and mask[x+1,y] == 1): # Right 
                Boundary[x,y,1] = 2
            if (mask[x,y] == 0 and mask[x,y-1] == 1): # Top
                Boundary[x,y,2] = 3
            if (mask[x,y] == 0 and mask[x,y+1] == 1): # Bottom
                Boundary[x,y,3] = 4
                return(Boundary)

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
    diffusion = numpy.zeros(I.shape)
    absGrad = numpy.zeros(I.shape)
    gArray = numpy.zeros(I.shape)
    
    tempI = I ##for iteration, after each step newI is set to I
    dt = 0.1 #timestep
    #Ttimes = 100 ##number of iterations, if using this stop condition
    EPS = 4 * 10**-5 ##largest pixel difference between steps before stopping, if using this stop condition
    looping = True
    while looping: ##restoration loop, A steps of inpainting, B steps of diffusion, and so on until the stop condition
        
        for A in range(0, 15): ## the inpainting loop
            print('A = ' +numpy.str(A))
            for x in range(0, I.shape[0]):
                for y in range(0, I.shape[1]):
                    
                    Ix[x,y] = (I[x+1,y] + I[x-1,y])/2
                    Iy[x,y] = (I[x,y+1] + I[x,y-1])/2
                    Ixx[x,y] = (I[x+1,y] - 2*I[x,y] + I[x-1,y])
                    Iyy[x,y] = (I[x,y+1] - 2*I[x,y] + I[x,y-1])
                    
                    if(boundary(I,mask)[x,y,2] == 3): # and boundary(i,mask)[x,y,3] != Bottom  ):
                        Iy[x,y] = (-3*I[x,y] + 4*I[x,y+1]-I[x,y+2])/2
                        Iyy[x,y] = (2*I[x,y] - 5*I[x,y+1] + 4*I[x,y+2]-I[x,y+3])
                    if(boundary(I,mask)[x,y,3] == 4): # and boundary(i,mask)[x,y,2] != Top  ):
                        Iy[x,y] = (3*I[x,y] - 4*I[x,y-1]+I[x,y-2])/2
                        Iyy[x,y] = (2*I[x,y] - 5*I[x,y-1] + 4*I[x,y-2]-I[x,y-3])
                    if(boundary(I,mask)[x,y,1] == 2): # and boundary(i,mask)[x,y,0] != Right):
                        Ix[x,y] = (-3*I[x,y] + 4*I[x+1,y]-I[x+2,y])/2
                        Ixx[x,y] = (2*I[x,y] - 5*I[x+1,y] + 4*I[x+2,y]-I[x+3,y])
                    if(boundary(I,mask)[x,y,0] == 1): #and boundary(i,mask)[x,y,1] != Left ):
                        Ix[x,y] = (3*I[x,y] - 4*I[x-1,y]+I[x-2,y])/2
                        Ixx[x,y] = (2*I[x,y] - 5*I[x-1,y] + 4*I[x-2,y]-I[x-3,y])
                                     
                    L[x, y] = Ixx[x, y] + Iyy[x, y] ##2D smoothness estimation
                    Ndir[x, y] = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
                    delL[x, y] = ( L[x+1, y] - L[x-1, y], L[x, y+1] - L[x, y-1]) ## a vector, x and y derivs of L (laplacian)
                    B[x, y] = numpy.dot( delL[x, y], Ndir[x, y] )#projection of delL onto Ndir
                    if(B[x, y] > 0):
                        absGrad[x, y] = numpy.sqrt((min(I[x,y]-I[x-1,y], 0)**2) + (max(I[x+1,y]-I[x,y], 0)**2) + (min(I[x,y]-I[x,y-1], 0)**2) + (max(I[x,y+1]-I[x,y], 0)**2))
                    elif(B[x, y] < 0):
                        absGrad[x, y] = numpy.sqrt((max(I[x,y]-I[x-1,y], 0)**2) + (min(I[x+1,y]-I[x,y], 0)**2) + (max(I[x,y]-I[x,y-1], 0)**2) + (min(I[x,y+1]-I[x,y], 0)**2)) 

                    It[x, y] = B[x, y] * absGrad[x, y] ## derivative in time
                    ##here multiply B by a slop-limited version of the norm of the gradient of the image
                    
                    if(mask[x,y] == 0): ##only actually update pixels inside the mask
                        I[x, y] = I[x, y] + dt * It[x, y]
                        
        for B in range(0, 2): ##the diffusion loop
            print('B = ' +numpy.str(B))
            #Ix = numpy.gradient(I)[0]
            #Iy = numpy.gradient(I)[1]
            
            for x in range(0, I.shape[0]):
                for y in range(0, I.shape[1]):
                    
                    if(boundary(I,mask)[x,y,2] == 3): # and boundary(i,mask)[x,y,3] != Bottom  ):
                        Iy[x,y] = (-3*I[x,y] + 4*I[x,y+1]-I[x,y+2])/2
                        Iyy[x,y] = (2*I[x,y] - 5*I[x,y+1] + 4*I[x,y+2]-I[x,y+3])
                    if(boundary(I,mask)[x,y,3] == 4): # and boundary(i,mask)[x,y,2] != Top  ):
                        Iy[x,y] = (3*I[x,y] - 4*I[x,y-1]+I[x,y-2])/2
                        Iyy[x,y] = (2*I[x,y] - 5*I[x,y-1] + 4*I[x,y-2]-I[x,y-3])
                    if(boundary(I,mask)[x,y,1] == 2): # and boundary(i,mask)[x,y,0] != Right):
                        Ix[x,y] = (-3*I[x,y] + 4*I[x+1,y]-I[x+2,y])/2
                        Ixx[x,y] = (2*I[x,y] - 5*I[x+1,y] + 4*I[x+2,y]-I[x+3,y])
                    if(boundary(I,mask)[x,y,0] == 1): #and boundary(i,mask)[x,y,1] != Left ):
                        Ix[x,y] = (3*I[x,y] - 4*I[x-1,y]+I[x-2,y])/2
                        Ixx[x,y] = (2*I[x,y] - 5*I[x-1,y] + 4*I[x-2,y]-I[x-3,y])
                                    
                    L[x, y] = Ixx[x, y] + Iyy[x, y] ##2D smoothness estimation
                    Ndir[x, y] = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
                    delL[x, y] = ( L[x+1, y] - L[x-1, y], L[x, y+1] - L[x, y-1]) ## a vector, x and y derivs of L (laplacian)
                    B[x, y] = numpy.dot( delL[x, y], Ndir[x, y])#projection of delL onto Ndir
                    if(B[x, y] > 0):
                        absGrad[x, y] = numpy.sqrt((min(I[x,y]-I[x-1,y], 0)**2) + (max(I[x+1,y]-I[x,y], 0)**2) + (min(I[x,y]-I[x,y-1], 0)**2) + (max(I[x,y+1]-I[x,y], 0)**2))
                    elif(B[x, y] < 0):
                        absGrad[x, y] = numpy.sqrt((max(I[x,y]-I[x-1,y], 0)**2) + (min(I[x+1,y]-I[x,y], 0)**2) + (max(I[x,y]-I[x,y-1], 0)**2) + (min(I[x,y+1]-I[x,y], 0)**2)) 

                    
                    gArray[x, y] = g(absGrad[x, y])
            diffusion = 1/dt * (numpy.gradient( gArray * Ix )[0] + numpy.gradient( gArray * Iy )[1])
            I = I + dt*diffusion     
                    
        ##check if still looping
        maxDelta = (numpy.abs(I - tempI)).max() 
        if( maxDelta < EPS):
            looping = False
        else:
            print('Max delta = ' + numpy.str(maxDelta))
            print('Max It = ' + (numpy.abs(It)).max())
            tempI = I
    
    return I