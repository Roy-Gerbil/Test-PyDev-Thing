import numpy
def restore(img, mask, relax): ##the basic method of restoring the image using the Laplace equation, takes the image to restore, the mask that damaged it, and the relaxation factor
    ###The method used is successive over-relaxation
    rest = numpy.zeros((mask.shape[0]+2, mask.shape[1]+2)) ##restoration points, using the mask to determine which points are being restored (interior sites are 0 in the mask). larger than mask to accomodate neumann boundaries
    NBs = mask * 0 ##number of neumann boundary points around each point
    print('Initialization...')
    for x in range(0, mask.shape[0]):
        for y in range(0, mask.shape[1]):
                if(mask[x,y] == 0):
                    
                    ##set initial guess
                    #rest[x+1,y+1] == 0.5 ##initial guess of half-intensity
                    d = 0
                    while(d != -1):
                        d += 1
                        print('d = '+ numpy.str(d))
                        for xd in range(0, d):
                            for yd in range(0, d):
                                if not( (x+xd) > img.shape[0]-1 or (y+yd) > img.shape[1]-1 or (x+ xd) < 0 or (y+yd) < 0 or mask[x+xd,y+yd] == 0 ):
                                    rest[x+1,y+1] = img[x+xd, y+yd] ##initial guess of intensity equal to the nearest bounday's intensity... more or less
                                    d = -1
                                    break
                            else:
                                continue
                            break
                    
                    ##now set all possible boundary points, using for points outside of image the Neumann condition
                    xd = 1##boundary 1
                    yd = 0##boundary 1
                    if( (x+xd) > img.shape[0]-1 or (y+yd) > img.shape[1]-1 or (x+ xd) < 0 or (y+yd) < 0 ):
                        NBs[x, y] += 1
                    else:
                        if(mask[x+xd, y+yd] == 1):
                            rest[x+1+xd,y+1+yd] = img[x+xd, y+yd]
                    xd = -1##boundary 2
                    yd = 0##boundary 2
                    if( (x+xd) > img.shape[0]-1 or (y+yd) > img.shape[1]-1 or (x+ xd) < 0 or (y+yd) < 0 ):
                        NBs[x, y] += 1
                    else:
                        if(mask[x+xd, y+yd] == 1):
                            rest[x+1+xd,y+1+yd] = img[x+xd, y+yd]
                    xd = 0##boundary 3
                    yd = 1##boundary 3
                    if( (x+xd) > img.shape[0]-1 or (y+yd) > img.shape[1]-1 or (x+ xd) < 0 or (y+yd) < 0 ):
                        NBs[x, y] += 1
                    else:
                        if(mask[x+xd, y+yd] == 1):
                            rest[x+1+xd,y+1+yd] = img[x+xd, y+yd]
                    xd = 0##boundary 4
                    yd = -1##boundary 4
                    if( (x+xd) > img.shape[0]-1 or (y+yd) > img.shape[1]-1 or (x+ xd) < 0 or (y+yd) < 0 ):
                        NBs[x, y] += 1
                    else:
                        if(mask[x+xd, y+yd] == 1):
                            rest[x+1+xd,y+1+yd] = img[x+xd, y+yd]
    print('Restoration...')
    looping = True ##looping until convergence condition is satisfied
    EPS = 5.13121*10**-4 ##when the largest difference between two points after a sweep is lower than this, convergence is satisfied
    while looping:
        restTemp = rest + 0##to store the values of the previous sweep, each sweep
        for x in range(0, mask.shape[0]):
            for y in range(0, mask.shape[1]):
                if(mask[x,y] == 0):
                    ##the updating
                    rest[x+1,y+1] = ( (1-relax)*rest[x+1, y+1] + ( (relax / (4-NBs[x,y])) * (rest[x+2, y+1] + rest[x+0, y+1] + rest[x+1, y+0] + rest[x+1, y+2]) ) )
        if((numpy.abs(rest - restTemp)).max() < EPS):
            looping = False
        else:
            print('Max delta = ' + numpy.str((numpy.abs(rest - restTemp)).max()))
    
    restoredPart = mask * 0##setting the in-boundary part of rest to be used
    for x in range(0, mask.shape[0]):
        for y in range(0, mask.shape[1]):
            if(mask[x,y] == 0):
                restoredPart[x,y] = rest[x+1,y+1]
    #print(restoredPart)
    return (img + restoredPart)