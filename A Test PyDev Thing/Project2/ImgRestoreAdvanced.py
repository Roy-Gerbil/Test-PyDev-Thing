import numpy
def restore(I, mask): ##a navier-stokes method of restoring the image, takes the image to restore and the mask that was applied
    ###The method used involved successive iteration over the masked part of the image (mask[x,y] == 0)
    
    ##first calculate 2D smoothness estimation L
    
    It[x, y] = numpy.dot(delL[x, y], Ndir[x, y]) * |gradI[x, y]| ## derivative in time
    
    delL[x, y] = ( L[x+1, y] - L[x-1, y], L[x, y+1] - L[x, y-1]) ## a vector, x and y derivs of L (laplacian)
    
    L[x, y] = Ixx[x, y] + Iyy[x, y] ##2D smoothness estimation
    
    Ndir = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
    
    B = numpy.dot( delL[x, y], Ndir[x, y])#projection of delL onto Ndir
    
    if(B > 0):
        absGrad = numpy.sqrt(  )
    elif(B < 0):
        absGrad = numpy.sqrt(  )
    else:
        absGrad = 0 ##? maybe
    
    
    
    delt = 0.1 #timestep?
    Ttimes = 100 ##number of iterations
    for T in range(0, Ttimes):
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                if(mask[x,y] == 0):
                    I[x, y] = imgTemp[x, y] + delt * It[x, y]
    
    
    
    
    
    return I

def g(s):##perona-malik anisotropic diffusion function
    K = 10**-12 ##diffusion parameter
    g = 1/(1+(s/K)**2)
    return g