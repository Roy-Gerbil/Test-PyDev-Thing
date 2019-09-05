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
    humanContactsPerHour = numpy.zeros(numPlaces, 24) + 0.5 ##average contact one person has each hour, for each place and each hour ##CURRENTLY each hour is indentical
    
    #initially infected
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
    timeStep = 1.0 ##units of hours
    
    
    
    
    totalTime = 60*24 ##in hours
    ##settings end
    
    ###Iterates for set amount of totalTime
    for hour in range(0, totalTime):##iteration of 1 hour, calls for changes in each population due to biological factors, then moves people around
        for i in range(0, numPlaces):##per population, this happens
            ##get biological population changes
            changes = numpy.zeros(2) = rungeKuttaInfect(I[i], S[i], R[i], humanContactsPerHour[i][0], recovRate) ##index 0 = recovered population, 1 = newly infected
            I[i] = I[i] + changes[1] - changes [0]
            R[i] = R[i] + changes[0]
            S[i] = S[i] - changes[1]
    
    
    

    
    print('done')
    #ended
pass