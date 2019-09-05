'''
Created on Sep. 5, 2019
@authors: a
'''
##IMPORTS

import math
import numpy

if __name__ == '__main__':
    #Variable Initialization: Populations
    numPlaces = 2
    placePop = numpy.zeros(numPlaces)
    placePop[0] = 5000
    placePop[1] = 10000
    
    infectionProbPerContact = 0.05 ##probability to infect person per human-human contact
    recovRate = 0.01 ## fraction of people per day
    
    #initally infected
    infectedFrac = numpy.zeros(2)
    infectedFrac[0] = 0.02
    infectedFrac[1] = 0.0
    
    ##The Numbers (1 = 1 person)
    S = numpy.zeros(numPlaces) ##susceptible
    I = numpy.zeros(numPlaces) ## infected
    R = numpy.zeros(numPlaces) ##recovered
    
    for i in range(0,numPlaces):
        I[i] = placePop[i]*infectedFrac[i]
        R[i] = 0
        S[i] = placePop[i] - I[i]
        
        
    ###Iterate
    ##settings
    timeStep = 1.0 ##units of days
    
    
    
    
    
    ##settings end
    for i in range(0, numPlaces):
        I[i] = rungeKutta(I[i], S[i], R[i])
    
    ##Infections Happen
    
    
    
    ##Movements Happen
    
    print('done')
    #ended
pass