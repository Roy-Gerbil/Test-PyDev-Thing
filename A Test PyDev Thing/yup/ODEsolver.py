import numpy

def valueGiver(Sfull, Ifull, Rfull, timeStepsPerHour):
    
    numPlaces = Sfull.shape[0]
    runLength = Sfull.shape[1]
    
    Stemp = numpy.zeros(numPlaces)
    Itemp = numpy.zeros(numPlaces)
    Rtemp = numpy.zeros(numPlaces)
    
    for pl in range(0, numPlaces):
        
        Stemp[pl] = Sfull[pl][0]
        Itemp[pl] = Ifull[pl][0]
        Rtemp[pl] = Rfull[pl][0]
    
    for h in range(0, runLength): ##every hour

        for t in range(0, timeStepsPerHour): ##number of times each hour
            
            for pl in range(0, numPlaces): ##every place
                
                S = Stemp[pl]
                I = Itemp[pl]
                R = Rtemp[pl]
                
                
            
                Stemp[pl] = Stemp[pl] + 1/6(F1 + 2*F2 + 2*F3 + F4)
                Itemp[pl] = Itemp[pl] + 1/6(G1 + 2*G2 + 2*G3 + G4)
                Rtemp[pl] = Rtemp[pl] + 1/6(K1 + 2*K2 + 2*K3 + K4)
        
        for pl in range(0, numPlaces): ##The current temp values are stored in the history of the 'actual' values
            
            Sfull[pl][h+1] = numpy.int(Stemp[pl])
            Ifull[pl][h+1] = numpy.int(Itemp[pl])
            Rfull[pl][h+1] = numpy.int(Rtemp[pl])
            
    return (Sfull, Ifull, Rfull)