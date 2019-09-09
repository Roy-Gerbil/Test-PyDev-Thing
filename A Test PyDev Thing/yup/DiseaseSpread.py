'''
Created on Sep. 5, 2019
Last edited on Sep. 5, 2019
@authors: a
'''
##IMPORTS

import math
import numpy
import matplotlib.pyplot as plt
import Plotter

if __name__ == '__main__':
    
    ##First off, decide for how long to run the simulation (in units of hours)
    
    runLength = 24*30*6
    

    #Variable Initialization: Populations, lists (each index is [place]) of arrays
    
    numPlaces = 2
    placePop = numpy.zeros(numPlaces)
    placePop[0] = 5000
    placePop[1] = 10000
    
    infectionProbPerContact = 0.05 ##probability to infect person per human-human contact
    recovRate = 0.01 ## fraction of people per day
    humanContactsPerHour = numpy.zeros((numPlaces, 24)) + 0.5 ##average contact one person has each hour, for each place and each hour ##CURRENTLY each hour is identical
    
    #initially infected
    infectedFrac = numpy.zeros(2)
    infectedFrac[0] = 0.02
    infectedFrac[1] = 0.0
    
    ##movement probabilities, movementChance[i][j][h] is fractional probability for 1 person to move from place i to place j in hour h. ##CURRENTLY each hour (and location) is identical
    movementChances = numpy.zeros((numPlaces,numPlaces,24)) + 0.0001
    
    
    
    ##The Numbers (in units of 1 person)
    S = numpy.zeros((runLength,numPlaces)) ##susceptible
    I = numpy.zeros((runLength,numPlaces)) ## infected
    R = numpy.zeros((runLength,numPlaces)) ##recovered
    
    changes = numpy.zeros(2) ##for the iteration, biological changes
    movementChanges = numpy.zeros((numPlaces,3)) ##for the iteration, movement changes

    
    for i in range(0,numPlaces):
        I[0][i] = placePop[i]*infectedFrac[i]
        R[0][i] = 0
        S[0][i] = placePop[i] - I[i]
        
        
    Stemp = S[0] ##susceptible, temp for iteration
    Itemp = I[0] ##infected, temp for iteration
    Rtemp = R[0] ##recovered/immune, temp for iteration
    
    ###Iterate
    ##settings
    timeStep = 1.0 ##units of hours
    
    
    

    ##settings end
    
    ###Iterates for set amount of totalTime
    for hour in range(0, runLength):##iteration of 1 hour, calls for changes in each population due to biological factors, then moves people around
        
        Stemp = S[hour] ##susceptible, temp for iteration
        Itemp = I[hour] ##infected, temp for iteration
        Rtemp = R[hour] ##recovered/immune, temp for iteration
        
        for i in range(0, numPlaces):##per population, this happens
            ##get biological population changes
            changes = rungeKuttaInfect(Itemp[i], Stemp[i], Rtemp[i], humanContactsPerHour[i] * infectionProbPerContact, recovRate/24) 
            ## gives population numbers of infected, susceptible, recovered/immune, average human contacts per hour (currently just take any index, ex: humanContactsPerHour[i][0]) * fractional chance to infect a susceptible person per contact, then fractional recovery rate per hour
            ##changes index 0 = recovered population, 1 = newly infected
            Itemp[i] = Itemp[i] + changes[1] - changes [0]
            Rtemp[i] = Rtemp[i] + changes[0]
            Stemp[i] = Stemp[i] - changes[1]
            
            ##population transfer changes
            ##movementChanges[i][j] is people of type j moving from this area (i) to area k. index 0 = S pop, 1 = I pop, 2 = R pop
            movementChanges = rungeKuttaMove(I[i], S[i], R[i], movementChances[i])
            
            for k in range(0, numPlaces): ##k being the population gaining people from i
                Stemp[i] = Stemp[i] - movementChanges[k][0]
                Stemp[k] = Stemp[k] + movementChanges[k][0]
                
                Itemp[i] = Itemp[i] - movementChanges[k][1]
                Itemp[k] = Itemp[k] + movementChanges[k][1]
                
                Rtemp[i] = Rtemp[i] - movementChanges[k][2]
                Rtemp[k] = Rtemp[k] + movementChanges[k][2]
    
            I[hour+1][i] = Itemp[i]
            S[hour+1][i] = Stemp[i]
            R[hour+1][i] = Rtemp[i]
    

    ##eventually add plotting here, I suppose
    
    Plotter.plotThis22((numpy.zeros(10) + 1),(numpy.zeros(10) - 1)) ##times, S pop, I pop, R pop
    plt.show()
    
    print('done')
    #ended
pass