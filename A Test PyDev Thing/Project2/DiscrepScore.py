def discrepScore(originalImg, restoredImg, maskforImg): ##obtain the chi squared discrapency between the restored image and the original image
    xvals = originalImg.shape[0]
    yvals = originalImg.shape[1]
    
    num = 0 ##the numerator in the equation for chi squared
    sigmasq = 0 ##sigma squared, the denominator in the equation for chi squared (but without the factor of 1/(n-1))
    n = 0 ##number of points
    Imean = 0 ##mean of data in the missing region
    
    ##find Imean
    for x in range(0, xvals):
        for y in range(0, yvals):
            if( maskforImg[x,y] == 0 ): ##sum over the pixels of the mission region only
                n = n + 1
                Imean = Imean + originalImg[x,y]
                
    Imean = Imean/n ##to get the actual mean value
    
    ##now, find chi squared
    for x in range(0, xvals):
        print(x)
        for y in range(0, yvals):
            if( maskforImg[x,y] == 0 ): ##sum over the pixels of the mission region only
                num = num + ( restoredImg[x,y] - originalImg[x,y] )**2
                sigmasq = sigmasq + ( originalImg[x,y] - Imean )**2
    
    return (((n-1) / n) * (num/sigmasq))