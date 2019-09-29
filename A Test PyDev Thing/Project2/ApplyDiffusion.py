import numpy
def g(s):##perona-malik anisotropic diffusion function
    K = 10**-12 ##diffusion parameter
    g = 1/(1+(s/K)**2)
    return g

def diffusify(I, bounds, n, boundary, mask): ##applies the diffusion to the area of the mask, n times
    
    L = numpy.zeros(I.shape)
    Ndir = numpy.zeros((I.shape[0], I.shape[1], 2))
    delL = numpy.zeros((I.shape[0], I.shape[1], 2))
    B = numpy.zeros(I.shape)
    Ix = numpy.zeros(I.shape)
    Iy = numpy.zeros(I.shape)
    Ixx = numpy.zeros(I.shape)
    Iyy = numpy.zeros(I.shape)
    diffusion = numpy.zeros(I.shape)
    absGrad = numpy.zeros(I.shape)
    gArray = numpy.zeros(I.shape)
    
    dt = 0.1 ##timestep
    for C in range(0, n): ##the diffusion loop
        print('C = ' +numpy.str(C))
        
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
                        Ndir[x, y] = 0
                    else:
                        Ndir[x, y] = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
                    #print(numpy.dot( delL[x, y], Ndir[x, y] ))
                    B[x, y] = numpy.dot( delL[x, y], Ndir[x, y] )#projection of delL onto Ndir
                    if(B[x, y] > 0):
                        absGrad[x, y] = numpy.sqrt((min(I[x,y]-I[x-1,y], 0)**2) + (max(I[x+1,y]-I[x,y], 0)**2) + (min(I[x,y]-I[x,y-1], 0)**2) + (max(I[x,y+1]-I[x,y], 0)**2))
                    elif(B[x, y] < 0):
                        absGrad[x, y] = numpy.sqrt((max(I[x,y]-I[x-1,y], 0)**2) + (min(I[x+1,y]-I[x,y], 0)**2) + (max(I[x,y]-I[x,y-1], 0)**2) + (min(I[x,y+1]-I[x,y], 0)**2)) 
    
                    
                    gArray[x, y] = g(absGrad[x, y])
        diffusion = 1/dt * (numpy.gradient( gArray * Ix )[0] + numpy.gradient( gArray * Iy )[1])
        for x in range(0, I.shape[0]):
            for y in range(0, I.shape[1]):
                if(mask[x,y] == 0): ##only actually update pixels inside the mask
                    I[x, y] = I[x, y] + dt*diffusion[x, y]
                    if(I[x, y] < 0):
                        I[x, y] = 0
                    elif(I[x, y] > 1):
                        I[x, y] = 1
    return I