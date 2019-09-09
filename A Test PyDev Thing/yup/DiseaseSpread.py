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
    
    ##not sure if using this one
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
    
    changes = numpy.zeros((numPlaces, 3)) ##for the iteration, [][0] is S pop, [][1] is I pop, [][2] is R pop

    
    for i in range(0,numPlaces):
        I[0][i] = placePop[i]*infectedFrac[i]
        R[0][i] = 0
        S[0][i] = placePop[i] - I[i]
        

    ###Iterate
    ##settings
    timeStep = 1/9 #timestep in units of hours
    
    vaccinationsPerHour = numpy.int(500/24) ##assuming 500 per day now
    
    ##settings end
    
    ###Iterates for set amount of totalTime
    for hour in range(0, runLength):##iteration of 1 hour, calls for changes in each population due to biological factors, then moves people around
        

        ##get population changes
        changes = rungeKuttaChange(I[hour], S[hour], R[hour], timeStep, humanContactsPerHour[i] * infectionProbPerContact, recovRate/24, vaccinationsPerHour) 
        ## gives population numbers of infected, susceptible, recovered/immune, average human contacts per hour (currently just take any index, ex: humanContactsPerHour[i][0]) * fractional chance to infect a susceptible person per contact, then fractional recovery rate per hour
        ##changes index 0 = recovered population, 1 = newly infected
        
        
        for i in range(0, numPlaces):##per population, execute changes

            I[hour+1][i] = I[hour][i] + changes[i][1]
            S[hour+1][i] = S[hour][i] + changes[i][0]
            R[hour+1][i] = R[hour][i] + changes[i][2]
    

    
    ##error estimates, using formula for stepsize of 2h, where y is the value with stepsize of h and u is with stepsize 2h:
    ##  E_n = (y_n - u_n) / (2^m -1), m = h for R-K 4th order method so E_n = (y_n - u_n) / 31
    
    ##plotting here
    
    plotIndex = 0
    
    Plotter.plotThis22(numpy.transpose(S)[plotIndex],numpy.transpose(I)[plotIndex], numpy.transpose(R)[plotIndex], plotIndex) ##S pop, I pop, R pop, index/name of location
    plt.show()
    
    print('done')
    #ended
pass