import random
import numpy as np
def R_float(start, stop, step = 10**(-17)): # Random generator between [0,1] unlike random.random() which is between [0,1). Note that the (10**-17) is to have the same step as the random.random has (i.e. as many decimals)
    return random.randint(0, int((stop - start) / step)) * step + start
    
def createMask(img, type,n): ##creates the mask of specified type for the image. n determines the number of objects for different types of masks. 
    
    mask = np.zeros((img.shape[0],img.shape[1]),np.float32) + 1
    
    if (type == "IRCG"):   # Integer Random Computer Generated mask. Has random values of 0 (black) and 1 (white) for different pixels. 
        for p1 in range(5, img.shape[0]-5):
            for p2 in range(5, img.shape[1]-5): 
                mask[p1,p2] -= random.randint(0,1) 
                
    if (type == "RCG"):   #  Random Computer Generated mask. Has random values between 0 (black) and 1 (white) for different pixels. 
        for p1 in range(5, img.shape[0]-5):
            for p2 in range(5, img.shape[1]-5): 
                mask[p1,p2] -= random.random() # Problem with this is that it only takes values less than 1, not equal to 1. If 1 should be indluded use code below. 
                #mask[p1,p2] -= R_float(start, stop, )
                
    if (type == "FBRCG"):   #  Random Computer Generated mask. Has random values between 0 (black) and 1 (white) for different pixels. 
        for t in range(0,n): #
            a0 = random.randint(0, img.shape[0]) # Creating random block. a0 is the starting pixel chosen at random for x-dimension
            at = img.shape[0] - random.randint(0, img.shape[0]) + a0 # Creating random block. at is the finishing pixel chosen at random for x-dimension
            b0 = random.randint(0, img.shape[1]) # Creating random block. a0 is the starting pixel chosen at random for x-dimension
            bt = img.shape[1] - random.randint(0, img.shape[1]) + b0 # Creating random block. at is the finishing pixel chosen at random for x-dimension
            
            for p1 in range(5, img.shape[0]-5):
                for p2 in range(5, img.shape[1]-5):
                    if( a0 <= p1 <= at  and b0 <= p2 <= bt):
                        mask[p1,p2] -= random.randint(0,1) # + 1  # the random int gives random spread for the blocks whereas + 1 gives one solid block
                        if(mask[p1,p2] < 0):
                            mask[p1,p2] = 0
    if (type == "WCCG"): # Whole Circles- Computer Generated mask.                     
        for t in range(0,n): 
            # Determining a random middle-point for the circle
            c0y = random.randint(0, img.shape[0]) 
            c0x = random.randint(0, img.shape[1])
            #Creating a random radius for the circle while not exceeding the map (This must be done separately for all the four quadrants)
            if(c0y > img.shape[0]/2 and c0x > img.shape[1]/2 ): #Quadrant 1 
                d = min((img.shape[0] - c0y), (img.shape[1] -c0x))
                r = random.randint(0 , np.int(d/6))
                for p1 in range(5, img.shape[0]-5):
                    for p2 in range(5, img.shape[1]-5):
                        if( ((p1-c0y)**2) + ((p2-c0x)**2) <= r**2 ):
                            mask[p1,p2] -= 1 #+= R_float(start, stop, )
                            if(mask[p1,p2] < 0):
                                mask[p1,p2] = 0
            if(c0y > img.shape[0]/2 and c0x < img.shape[1]/2 ): #Quadrant 2 
                d = min((img.shape[0] - c0y), (c0x))
                r = random.randint(0 , np.int(d/6))
                for p1 in range(5, img.shape[0]-5):
                    for p2 in range(5, img.shape[1]-5):
                        if( ((p1-c0y)**2) + ((p2-c0x)**2) <= r**2 ):
                            mask[p1,p2] -= 1 #+= R_float(start, stop, )
                            if(mask[p1,p2] < 0 ):
                                mask[p1,p2] = 0
                        
            if(c0y < img.shape[0]/2 and c0x < img.shape[1]/2 ):  # Quadrant 3
                d = min(( c0y), (c0x))
                r = random.randint(0 , np.int(d/6))
                for p1 in range(5, img.shape[0]-5):
                    for p2 in range(5, img.shape[1]-5):
                        if( ((p1-c0y)**2) + ((p2-c0x)**2) <= r**2 ):
                            mask[p1,p2] -= 1 #+= R_float(start, stop, )
                            if(mask[p1,p2] < 0):
                                mask[p1,p2] = 0            
            if(c0y < img.shape[0]/2 and c0x > img.shape[1]/2 ):  #Quadrant 4 
                d = min((c0y), (img.shape[1] -c0x))
                r = random.randint(0 , np.int(d/6))
                for p1 in range(5, img.shape[0]-5):
                    for p2 in range(5, img.shape[1]-5):
                        if( ((p1-c0y)**2) + ((p2-c0x)**2) <= r**2 ):
                            mask[p1,p2] -= 1 #+= R_float(start, stop, )
                            if(mask[p1,p2] < 0):
                                mask[p1,p2] = 0
    if (type == "CCG"): # Circles- Computer Generated mask.                     
        for t in range(0,n): 
            # Determining a random middle-point for the circle
            c0y = random.randint(0, img.shape[0]) 
            c0x = random.randint(0, img.shape[1])
            d = min(img.shape[0] , img.shape[1] )
            r = random.randint(0 , np.int(d/14)) # Divided by four so that the radii are not to big. 
            for p1 in range(5, img.shape[0]-5):
                for p2 in range(5, img.shape[1]-5):
                    if( ((p1-c0y)**2) + ((p2-c0x)**2) <= r**2 ):
                        mask[p1,p2] -= 1 #+= R_float(start, stop, )
                        if(mask[p1,p2] < 0):
                            mask[p1,p2] = 0

    #plt.imshow(mask, cmap='gray', interpolation='nearest');
    return mask