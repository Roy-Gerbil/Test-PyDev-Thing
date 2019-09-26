import numpy
def restore(img, mask): ##a navier-stokes method of restoring the image, takes the image to restore and the mask that was applied
    ###The method used is successive over-relaxation
    imgtemp = img ##for iteration
    
    looping = True
    while looping:
        imgtemp = img
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                if(mask[x,y] == 0):
                    img[x,y] = imgtemp[x,y] + dt*( -numpy.abs(u) * (( imgtemp[x + numpy.sign(u),y] - imgtemp[x,y] )/ dx) -numpy.abs(v) * (( imgtemp[x,y + numpy.sign(v)] - imgtemp[x,y] )/ dy) + nu(diffdiscret))
    return (img)