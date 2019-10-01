import numpy
import ApplyDiffusion
import matplotlib.pyplot as plt
from scipy.stats.morestats import levene

def sortThird(val): ##returns the second value of the list, here the T value
    return val[1]

def replaceT(band, x, y): ##removes the [x, y] point from the band, if it exists. This is used to replace the T value, instead of just adding another T, for clarity when debugging code
    for i in range(0, len(band)):
        if(band[i][0][0] == x and band[i][0][1] == y):
            del band[i]
            break
    return band

def initialize(I, mask): ##get initial values for Image
    ##each pixel has [0] T value, [1] grayscale value, [2] a flag (0) for boundary pixel, (1) for known pixel, in image, (2) for unknown, in mask
    Image = numpy.zeros((I.shape[0], I.shape[1], 3))
    narrowBand = []
    for x in range(0, I.shape[0]):
        for y in range(0, I.shape[1]):
            if(mask[x, y] == 0):
                Image[x, y, 0] = 10**6
                Image[x, y, 2] = 2
            else:
                Image[x, y, 1] = I[x, y]
                Image[x, y, 2] = 1
                if(x+1 < I.shape[0] and y+1 < I.shape[1] and x-1 >= 0 and y-1 >= 0):  
                    if(mask[x+1, y] == 0 or mask[x-1, y] == 0 or mask[x, y+1] == 0 or mask[x, y-1] == 0):
                        Image[x, y, 2] = 0
                        narrowBand.append(((x, y), Image[x, y, 0]))
    return (Image, narrowBand)

def inpaint(I, f, T, i, j): ##inpaints the pixel at [i, j] using nearby points
    Ia = 0
    s = 0
    gradI = numpy.array([0, 0])
    d = 2 ##distance to grab points with information to use to inpaint
    for x in range(i-d, i+d+1):
        for y in range(j-d, j+d+1):
            if(x == i and y == j):
                pass
            elif(f[x, y] == 1):
                k = x
                l = y
                r = numpy.array((k-i, l-j))
                lr = numpy.linalg.norm(r)
                gradT = numpy.array([T[i+1, j] - T[i-1, j], T[i, j+1] - T[i, j-1]])/2
                dirn = numpy.abs(numpy.dot(r, gradT)) / lr
                dst = 1/(lr**2)
                lev = 1/(1 + numpy.abs(T[k, l] - T[i, j]))
                w = dirn*dst*lev + 1*10**-6 ##to avoid zeros
                if(f[k+1, l] != 1 and f[k-1, l] != 1 and f[k, l+1] != 1 and f[k, l-1] != 1):
                    gradI = numpy.array([I[k+1, l] - I[k-1, l], I[k, l+1] - I[k, l-1]])/2
                Ia = Ia + w * (I[k, l] - numpy.dot(gradI, r))
                s = s + w
    Inew = Ia/s
    if(Inew < 0):
        Inew = 0
    elif(Inew > 1):
        Inew = 1
    return Inew

def solve(f, T, i1, j1, i2, j2):
    sol = 10**6
    if(f[i1, j1] == 1):
        if(f[i2, j2] == 1):
            r = numpy.sqrt(2 - (T[i1, j1] - T[i2, j2])**2)
            s = (T[i1, j1] + T[i2, j2] - r)/2
            if(s >= T[i1, j1] and s >= T[i2, j2]):
                sol = s
            else:
                s = s + r
                if(s >= T[i1, j1] and s >= T[i2, j2]):
                    sol = s
        else:
            sol = 1 + T[i1, j1]
    elif(f[i2, j2] == 1):
        sol = 1 + T[i2, j2]
    return sol

def restore(Io, mask): ##fast method of restoring the image, takes the image to restore and the mask that was applied
    
    ####NEW THING START
    (Image, narrowBand) = initialize(Io, mask)
    T = numpy.zeros(Io.shape)
    I = numpy.zeros(Io.shape)
    f = numpy.zeros(Io.shape)
    for x in range(0, I.shape[0]):
        for y in range(0, I.shape[1]):
            T[x, y] = Image[x, y, 0]
            I[x, y] = Image[x, y, 1]
            f[x, y] = Image[x, y, 2]
    while(len(narrowBand) != 0):
        print('looping... bandSize = ' + numpy.str(len(narrowBand)))
        narrowBand.sort(key = sortThird)
        curr = narrowBand.pop(0)
        i = curr[0][0]
        j = curr[0][1]
        f[i, j] = 1
        
        
        k = i-1
        l = j
        
        if(f[k, l] != 1):
            if(f[k, l] == 2):
                f[k, l] = 0
                I[k, l] = inpaint(I, f, T, k, l)
            T[k, l] = numpy.min((solve(f, T, k-1, l, k, l-1), solve(f, T, k+1, l, k, l-1), solve(f, T, k-1, l, k, l+1), solve(f, T, k+1, l, k, l+1)))
            narrowBand = replaceT(narrowBand, k, l)
            narrowBand.append(((k, l), T[k, l]))
        
        k = i+1
        l = j
        
        if(f[k, l] != 1):
            if(f[k, l] == 2):
                f[k, l] = 0
                I[k, l] = inpaint(I, f, T, k, l)
            T[k, l] = numpy.min((solve(f, T, k-1, l, k, l-1), solve(f, T, k+1, l, k, l-1), solve(f, T, k-1, l, k, l+1), solve(f, T, k+1, l, k, l+1)))
            narrowBand = replaceT(narrowBand, k, l)
            narrowBand.append(((k, l), T[k, l]))
            
        k = i
        l = j+1
        
        if(f[k, l] != 1):
            if(f[k, l] == 2):
                f[k, l] = 0
                I[k, l] = inpaint(I, f, T, k, l)
            T[k, l] = numpy.min((solve(f, T, k-1, l, k, l-1), solve(f, T, k+1, l, k, l-1), solve(f, T, k-1, l, k, l+1), solve(f, T, k+1, l, k, l+1)))
            narrowBand = replaceT(narrowBand, k, l)
            narrowBand.append(((k, l), T[k, l]))
            
        k = i-1
        l = j-1
        
        if(f[k, l] != 1):
            if(f[k, l] == 2):
                f[k, l] = 0
                I[k, l] = inpaint(I, f, T, k, l)
            T[k, l] = numpy.min((solve(f, T, k-1, l, k, l-1), solve(f, T, k+1, l, k, l-1), solve(f, T, k-1, l, k, l+1), solve(f, T, k+1, l, k, l+1)))
            narrowBand = replaceT(narrowBand, k, l)
            narrowBand.append(((k, l), T[k, l]))
            
            
    
    ####NEW THING END
    for x in range(0, I.shape[0]):
        for y in range(0, I.shape[1]):
            Io[x, y] = I[x, y]
    return Io