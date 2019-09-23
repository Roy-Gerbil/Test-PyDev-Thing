def createMask(img, type): ##creates the task of specified type for the image
    
    if (type == IRCG):   # Integer Random Computer Generated mask. Has random values of 0 (black) and 1 (white) for different pixels. 
        mask = np.zeros((img.shape[0],img.shape[1]),np.float32) 
            for p1 in range(0, img.shape[0]):
                for p2 in range(0, I.shape[1]): 
                    mask[p1,p2] += random.randint(0,1) 
        return mask
    if (type == RCG):   #  Random Computer Generated mask. Has random values between 0 (black) and 1 (white) for different pixels. 
        mask = np.zeros((img.shape[0],img.shape[1]),np.float32) 
            for p1 in range(0, img.shape[0]):
                for p2 in range(0, img.shape[1]): 
                    mask[p1,p2] += random.randint(0,1) 
        return mask
     if (type == FBRCG):   #  Random Computer Generated mask. Has random values between 0 (black) and 1 (white) for different pixels. 
        mask = np.zeros((img.shape[0],img.shape[1]),np.float32) 
            for p1 in range(0, img.shape[0]):
                for p2 in range(0, img.shape[1]): 
                    a0 = random.randint(0, img.shape[0]) # Creating random block. a0 is the starting pixel chosen at random for x-dimension
                    at = img.shape[0] - random.randint(0, img.shape[0]) + d # Creating random block. at is the finishing pixel chosen at random for x-dimension
                    b0 = random.randint(0, img.shape[1]) # Creating random block. a0 is the starting pixel chosen at random for x-dimension
                    bt = img.shape[1] - random.randint(0, img.shape[1]) + d # Creating random block. at is the finishing pixel chosen at random for x-dimension
                  
                    if( a0 <= p1 <= at  and b0 <= p2 <= bt):
                        mask[p1,p2] += random.randint(0,1) 
        return mask

    
    return mask
