import numpy

def valueGiver(S, I, R, timeStepsPerHour):
    
    numPlaces = S.shape[0]
    runLength = S.shape[1]
    
    
    
    for pl in range(0, numPlaces):
        
        Stemp = S[pl][0]
        Itemp = I[pl][0]
        Rtemp = R[pl][0]
        
        for h in range(0, runLength):

            for t in range(0, timeStepsPerHour):
                
                Stemp = Stemp + 1/6(F1 + 2*F2 + 2*F3 + F4)
                
                Itemp = Itemp + 1/6(G1 + 2*G2 + 2*G3 + G4)
                
                Rtemp = Rtemp + 1/6(H1 + 2*H2 + 2*H3 + H4)
            
            S[pl][h+1] = numpy.int(Stemp)
            I[pl][h+1] = numpy.int(Itemp)
            R[pl][h+1] = numpy.int(Rtemp)
            
    return (S, I, R)