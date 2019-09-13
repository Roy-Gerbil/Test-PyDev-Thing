'''
Created on Sep. 5, 2019
Last edited on Sep. 12, 2019
@authors: a, h
'''
##IMPORTS

import math
import numpy
import matplotlib.pyplot as plt
import Plotter
import ODEsolver


def setInitialPops(runLength, numPlaces, placePop, infectedFrac): ###S[0][1] is S pop for location 0 at hour 1
    S = numpy.zeros((numPlaces,runLength)) ##susceptible
    I = numpy.zeros((numPlaces,runLength)) ## infected
    R = numpy.zeros((numPlaces,runLength)) ##recovered
    
    for pl in range(0,numPlaces):
        I[pl][0] = numpy.int(placePop[pl]*infectedFrac[pl])
        R[pl][0] = 0
        S[pl][0] = placePop[pl] - I[pl][0]
        
    return (S, I, R)

if __name__ == '__main__':
    
    ##settings
    
    runLength = 24*7 #units of hours, how long the simulation covers
    
    timeStepsPerHour = 80 #timeStepsPerHours each hour (data saved each hour, can't go below 1)
    
    
    
    #Variable Initialization: Populations and constants
    
    places = [["Malmo", 316588, .4, 55.604980, 13.003822], [ "Lund", 91940, 0, 55.704659, 13.191007], ["Copenhagen", 602481, 0, 55.676098, 12.568337], ["Stockholm", 965232, 0, 59.329323, 18.068581]] ##the places, each places has name, inital pop, initial infected fraction
    
    print(numpy.sqrt( (places[0][3]-places[1][3])**2 + (places[0][4]-places[1][4])**2  ))
    ##each place has coordinates (used only for Long-distance travel to calculate very rough travel times)
    vaccinationChancePerHour = 500/places[1][1] ##here, use static rate, made by initially assuming 500 per day created in Lund
    
    ##settings end
     
    numPlaces = len(places)
    
    placePop = numpy.zeros(numPlaces) ##initial population for each place
    infectedFrac = numpy.zeros(numPlaces) ##initially infected

    for i in range(0, numPlaces):
        placePop[i] = places[i][1]
        infectedFrac[i] = places[i][2]
    
    infectionProbPerContact = 0.05 ##probability to infect person per human-human contact
    recovRate = 0.02/24 ## fraction of people per hour
    
    ##not sure if using this one
    humanContactsPerHour = numpy.zeros((numPlaces, 24)) + 0.5 ##average contact one person has each hour, for each place and each hour ##CURRENTLY each hour is identical
    ##should be omega in the paper

    
    ##movement probabilities, movementChance[i][j][k] is fractional probability for 1 person of type i to move from place j to place k (( [0] is S, [1] is I, [2] is R ))
    
    movementChances = numpy.zeros((3, numPlaces, numPlaces, 24))
    
    ###start by assuming that 2000 people move to/from Lund to Malmo per hour on average
    lundMovementChance = 1400/places[1][1]
    
    ###movement between malmo and lund
    movementChances[0][1][0][8] = lundMovementChance
    movementChances[0][0][1][8] = movementChances[0][1][0][8] * places[1][1]/places[0][1] ##making movement chances normalized to population, so that no net exchange of population occurs
    ###movement between malmo and copenhagen
    movementChances[0][0][2][8] = lundMovementChance
    movementChances[0][2][0][8] = movementChances[0][0][2][8] * places[0][1]/places[2][1]
    ###movement between stockholm and lund/malmo
    movementChances[0][3][0][8] = lundMovementChance
    
    
    ###R pop is the same as S pop, I pop difference added later
    
    for pl in range(0, numPlaces):
        for pl2 in range(0, numPlaces):
            movementChances[1][pl][pl2] = movementChances[0][pl][pl2]
            movementChances[2][pl][pl2] = movementChances[0][pl][pl2]
            
            ##now scale movement by time of day, using the sum of two gaussians, peaked (now) at 7:00 and 17:00
            for i in range(0,3):
                for t in range(0,24):
                    movementChances[i][pl][pl2][t] = movementChances[i][pl][pl2][8] * (numpy.exp(-(((t-7)/4)**2)) + numpy.exp(-(((t-17)/4)**2)))
    
    movementChances[1] = movementChances[1] * 2 / 5 ##2/5th chance for an infected person to move
    
    
    ##now long-distance movement chances, which are done using discrete packets rather than the runge-kutta method for simplicity. (currently only between stockholm and other places)
    movementChancesLD = numpy.zeros((3, numPlaces, numPlaces, 24))
    ##between stockholm and malmo
    movementChancesLD[0][3][0][8] = lundMovementChance / 10 ##assume 1/10th of people that go between lund and malmo, say, go between stockholm and malmo
    movementChancesLD[0][0][3][8] = movementChancesLD[0][3][0][8] * places[3][1]/places[0][1]
    ##between stockholm and lund
    movementChancesLD[0][3][1][8] = lundMovementChance / 10 
    movementChancesLD[0][1][3][8] = movementChancesLD[0][3][1][8] * places[3][1]/places[1][1]
    ##between stockholm and copenhagen
    movementChancesLD[0][3][2][8] = lundMovementChance / 10
    movementChancesLD[0][2][3][8] = movementChancesLD[0][3][2][8] * places[3][1]/places[2][1]
    
    for pl in range(0, numPlaces):
        for pl2 in range(0, numPlaces):
            movementChancesLD[1][pl][pl2] = movementChancesLD[0][pl][pl2]
            movementChancesLD[2][pl][pl2] = movementChancesLD[0][pl][pl2]
            
            ##now scale movement by time of day, using the sum of two gaussians, peaked (now) at 7:00 and 17:00
            for i in range(0,3):
                for t in range(0,24):
                    movementChancesLD[i][pl][pl2][t] = movementChancesLD[i][pl][pl2][8] * (numpy.exp(-(((t-7)/4)**2)) + numpy.exp(-(((t-17)/4)**2)))
    
    movementChancesLD[1] = movementChancesLD[1] * 2 / 5 ##2/5th chance for an infected person to move
    
    
    ##The Numbers (in units of 1 person)
    
    S = numpy.zeros((numPlaces,runLength))
    I = numpy.zeros((numPlaces,runLength))
    R = numpy.zeros((numPlaces,runLength))
    
    (S, I, R) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)

    ###Iterate in the RungeKutta, the following is deprecated

    #changes = numpy.zeros((numPlaces, 3)) ##for the iteration, [][0] is S pop, [][1] is I pop, [][2] is R pop
#===============================================================================
#     ###Iterates for set amount of totalTime
#     for hour in range(0, runLength):##iteration of 1 hour, calls for changes in each population due to biological factors, then moves people around
#         
# 
#         ##get population changes
#         changes = ODEsolver.rungeKuttaIterator(I[hour], S[hour], R[hour], timeStepsPerHour, humanContactsPerHour[i] * infectionProbPerContact, recovRate/24, vaccinationChancePerHour) 
#         ## gives population numbers of infected, susceptible, recovered/immune, average human contacts per hour (currently just take any index, ex: humanContactsPerHour[i][0]) * fractional chance to infect a susceptible person per contact, then fractional recovery rate per hour
#         ##changes index 0 = recovered population, 1 = newly infected
#         
#         
#         for i in range(0, numPlaces):##per population, execute changes
# 
#             I[hour+1][i] = I[hour][i] + changes[i][1]
#             S[hour+1][i] = S[hour][i] + changes[i][0]
#             R[hour+1][i] = R[hour][i] + changes[i][2]
#===============================================================================

    #plots here
    plotIndex = 0
    
    ##now a comparison with simplified theory: no recovery, no vaccinations, no movement, only 1 area:
    ##theoretical equation: dS/dt = -B*S*I/N, where B is the infection constant, and N is total population
    ##solved, we get: t_f - t_i = ln[ S_f*(N - S_i) / ( S_i*( N-S_f )) ]
    
    #===========================================================================
    # print('Simplified theory comparison for runtime of  = ' + str(runLength))
    # 
    # (Ss, Is, Rs) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    #  
    # (Ss, Is, Rs) = ODEsolver.rungeKuttaIterator(Ss, Is, Rs, timeStepsPerHour, humanContactsPerHour[0][0] * infectionProbPerContact, recovRate*0, vaccinationChancePerHour*0, movementChances*0)
    #  
    # Plotter.plotThis22(Ss[plotIndex], Is[plotIndex], Rs[plotIndex], 'The Spread of the Plague in Area ' +places[plotIndex][0])
    # plt.show()
    # plt.clf()
    #  
    # print('Using the theory to calculate time passed, it should be: ' + str( (-1 * humanContactsPerHour[0][0] * infectionProbPerContact) * numpy.log( (Ss[0][runLength - 1] * ( (Ss[0][0] + Is[0][0]) - Ss[0][0])) / (Ss[0][0] * ( (Ss[0][0] + Is[0][0]) - Ss[0][runLength - 1] )) )) + ' hours. In the simulation this change was over: ' +str(runLength)+ ' hours.')
    #  
    #  
    # ##now a view of 1 area with recovery and vaccination, but without movement:
    #  
    # print('Simplified runtime of  = ' + str(runLength))
    #  
    # (Ss2, Is2, Rs2) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    #  
    # (Ss2, Is2, Rs2) = ODEsolver.rungeKuttaIterator(Ss2, Is2, Rs2, timeStepsPerHour, humanContactsPerHour[0][0] * infectionProbPerContact, recovRate, vaccinationChancePerHour, movementChances*0)
    #  
    # Plotter.plotThis22Multi(Ss2, Is2, Rs2, 'The Spread of the Plague in Area ' +places[plotIndex][0])
    # plt.show()
    # plt.clf()
    #===========================================================================
     
    
    

    
    ##error estimates, using formula for stepsize of 2h, where y is the value with stepsize of h and u is with stepsize 2h:
    ##  E_n = (y_n - u_n) / (2^m -1), m = h for R-K 4th order method so E_n = (y_n - u_n) / 31
    ##order of error for 1 timeStepsPerHour is O(h^5), so total ~O(h^4)
    
    ##plotting here
    
    
    #(S, I, R) = ODEsolver.rungeKuttaIterator(S, I, R, timeStepsPerHour, humanContactsPerHour[0][0] * infectionProbPerContact, recovRate, vaccinationChancePerHour, movementChances, movementChancesLD)
     
    print('Regular Plot, timeStepsPerHour = '+str(timeStepsPerHour))
    
    Plotter.plotThis22Multi(S, I, R, places, True)
    plt.show()
    plt.clf()
    
    
    
    
    ##now with double the timeStepsPerHour (should be approx ~2^4 times the error)
    
    timeStepsPerHour = timeStepsPerHour * 2
    
    print('Error-Comparison Plot, timeStepsPerHour = '+str(timeStepsPerHour))
    
    (S2, I2, R2) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    #(S2, I2, R2) = ODEsolver.rungeKuttaIterator(S2, I2, R2, timeStepsPerHour, humanContactsPerHour[0][0] * infectionProbPerContact, recovRate, vaccinationChancePerHour, movementChances, movementChancesLD)
    
    Plotter.plotThis22(S2[plotIndex], I2[plotIndex], R2[plotIndex], 'h = 2h: The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    ##now with triple the timeStepsPerHour (should be approx ~2^4 times the error)
    
    timeStepsPerHour = timeStepsPerHour * 3/2
    
    print('Error-Comparison Plot, timeStepsPerHour = '+str(timeStepsPerHour))
    
    (S3, I3, R3) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    #(S3, I3, R3) = ODEsolver.rungeKuttaIterator(S3, I3, R3, timeStepsPerHour, humanContactsPerHour[0][0] * infectionProbPerContact, recovRate, vaccinationChancePerHour, movementChances, movementChancesLD)
    
    Plotter.plotThis22(S3[plotIndex], I3[plotIndex], R3[plotIndex], 'h = 3h: The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    print('Difference in values for endpoints in infected pop: between h and 2h' + str(numpy.abs( I[runLength - 1] - I2[runLength - 1] ) ))
    print('Difference in values for endpoints in infected pop: between 2h and 3h' + str(numpy.abs( I3[runLength - 1] - I2[runLength - 1] ) ))
    print('Difference in values for endpoints in infected pop: between h and 3h' + str(numpy.abs( I[runLength - 1] - I3[runLength - 1] ) ))
    
    
    print('done')
    #ended
pass