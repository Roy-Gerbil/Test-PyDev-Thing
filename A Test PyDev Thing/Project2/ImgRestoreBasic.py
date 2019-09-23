def ImgRestoreBasic(img, mask): ##the basic method of restoring the image using the Laplace equation
    ###The method used is successive over-relaxation
    rest = numpy.zeros((mask.shape[0]+2, mask.shape[1]+2)) ##restoration points, using the mask to determine which points are being restored (interior sites are 0 in the mask). larger than mask to accomodate neumann boundaries
    NBs = mask * 0 ##number of neumann boundary points around each point
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
                if(mask[x,y] == 0):
                    rest[x+1,y+1] = 0.5 ##initial guess of half-intensity, +1 because oversized matrix
                    ##now set all possible boundary points, using for points outside of image the Neumann condition
                    xd = 1##boundary 1
                    yd = 0##boundary 1
                    if( (x+xd) > img.shape[0] or (y+yd) > img.shape[1] or (x+ xd) < 0 or (y+yd) < 0 ):
                        rest[x+xd,y+yd] = 0
                        NBs[x, y] += 1
                    else:
                        rest[x+xd,y+yd] = img[x+xd, y+yd]
    
    return img * mask + rest