import numpy
def restore(I, mask): ##a navier-stokes method of restoring the image, takes the image to restore and the mask that was applied
    ###The method used involved successive iteration over the masked part of the image (mask[x,y] == 0)
    
    L = numpy.zeros(I.shape)
    Ndir = numpy.zeros((I.shape[0], I.shape[1], 2))
    delL = numpy.zeros(I.shape)
    B = numpy.zeros(I.shape)
    It = numpy.zeros(I.shape)
    Ix = numpy.zeros(I.shape)
    Iy = numpy.zeros(I.shape)
    Ixx = numpy.zeros(I.shape)
    Iyy = numpy.zeros(I.shape)
    
    if(B > 0):
        absGrad = numpy.sqrt(  )
    elif(B < 0):
        absGrad = numpy.sqrt(  )
    else:
        absGrad = 0 ##? maybe
    
    
    newI = I ##for iteration, after each step I is set to newI
    delt = 0.1 #timestep?
    Ttimes = 100 ##number of iterations, if using this stop condition
    EPS = 4 * 10**-5 ##largest pixel difference between steps before stopping, if using this stop condition
    looping = True
    while looping: ##restoration loop, A steps of inpainting, B steps of diffusion, and so on until the stop condition
        
        for A in range(0, 15): ## the inpainting loop
            for x in range(0, I.shape[0]):
                for y in range(0, I.shape[1]):
                    L[x, y] = Ixx[x, y] + Iyy[x, y] ##2D smoothness estimation
                    Ndir[x, y] = ( -Iy[x, y], Ix[x, y]) / (numpy.sqrt( (Ix[x, y])**2 + (Iy[x, y])**2 )) ##N[x,y,n]/|N[x,y,n]|, also a vector, is the isophote direction
                    B = numpy.dot( delL[x, y], Ndir[x, y])#projection of delL onto Ndir
                    delL[x, y] = ( L[x+1, y] - L[x-1, y], L[x, y+1] - L[x, y-1]) ## a vector, x and y derivs of L (laplacian)
                    It[x, y] = numpy.dot(delL[x, y], Ndir[x, y]) * absGrad[x, y] ## derivative in time
                    ##here multiply B by a slop-limited version of the norm of the gradient of the image
                    
                    
                    if(mask[x,y] == 0): ##only actually update pixels inside the mask
                        I[x, y] = imgTemp[x, y] + delt * It[x, y]
                        
        for B in range(0, 2): ##the diffusion loop
            
                        
        ##check if still looping
        maxDelta = (numpy.abs(rest - restTemp)).max() 
        if( maxDelta < EPS):
            looping = False
        else:
            print('Max delta = ' + numpy.str(maxDelta))
    
    
    
    
    
    return I

def g(s):##perona-malik anisotropic diffusion function
    K = 10**-12 ##diffusion parameter
    g = 1/(1+(s/K)**2)
    return g