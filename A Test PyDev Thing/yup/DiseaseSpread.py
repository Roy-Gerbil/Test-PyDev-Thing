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


def setInitialPops(runLength, numPlaces, placePop, infectedFrac): ###S[0][1] is S pop for location 0 at hour 1
    S = numpy.zeros((numPlaces,runLength)) ##susceptible
    I = numpy.zeros((numPlaces,runLength)) ## infected
    R = numpy.zeros((numPlaces,runLength)) ##recovered
    
    for pl in range(0,numPlaces):
        I[pl][0] = numpy.int(placePop[pl]*infectedFrac[pl])
        R[pl][0] = 0
        S[pl][0] = placePop[pl] - I[pl][0]

if __name__ == '__main__':
    
    ##settings
    
    runLength = 24*30*6 #units of hours, how long the simulation covers
    
    timeStepsPerHour = 9 #timeStepsPerHours each hour (data saved each hour)
    
    vaccinationsPerHour = numpy.int(500/24) ##assuming 500 per day now
    ##settings end
    
    #Variable Initialization: Populations and constants
    
    places = [["Malmo", 316588, .02], [ "Lund", 91940, 0], ["Copenhagen", 602481, 0]] ##the places, each places has name, inital pop, initial infected fraction
    
    numPlaces = len(places)
    
    placePop = numpy.zeros(numPlaces) ##initial population for each place
    infectedFrac = numpy.zeros(numPlaces) ##initially infected

    for i in range(0, numPlaces):
        placePop[i] = places[i][1]
        infectedFrac[i] = places[i][2]
    
    infectionProbPerContact = 0.05 ##probability to infect person per human-human contact
    recovRate = 0.01/24 ## fraction of people per hour
    
    ##not sure if using this one
    humanContactsPerHour = numpy.zeros((numPlaces, 24)) + 0.5 ##average contact one person has each hour, for each place and each hour ##CURRENTLY each hour is identical
    ##should be omega in the paper

    
    ##movement probabilities, movementChance[i][j][k] is fractional probability for 1 person of type i to move from place j to place k (( [0] is S, [1] is I, [2] is R ))
    movementChances = numpy.zeros((3, numPlaces, numPlaces)) + 0.0001 ##hopefully a good starting chance, somewhat random movement
    movementChances[1] = movementChances[1] / 5 ##1/5th chance for an infected person to move
    
    
    
    
    ##The Numbers (in units of 1 person)
    
    (S, I, R) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)

    ###Iterate in the RungeKutta, the following is deprecated

    #changes = numpy.zeros((numPlaces, 3)) ##for the iteration, [][0] is S pop, [][1] is I pop, [][2] is R pop
#===============================================================================
#     ###Iterates for set amount of totalTime
#     for hour in range(0, runLength):##iteration of 1 hour, calls for changes in each population due to biological factors, then moves people around
#         
# 
#         ##get population changes
#         changes = rungeKuttaChange(I[hour], S[hour], R[hour], timeStepsPerHour, humanContactsPerHour[i] * infectionProbPerContact, recovRate/24, vaccinationsPerHour) 
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

    #new thing
    
    (S, I, R) = rungeKuttaChange(S, I, R, timeStepsPerHour, humanContactsPerHour[0] * infectionProbPerContact, recovRate, vaccinationsPerHour, movementChances)
    

    
    ##error estimates, using formula for stepsize of 2h, where y is the value with stepsize of h and u is with stepsize 2h:
    ##  E_n = (y_n - u_n) / (2^m -1), m = h for R-K 4th order method so E_n = (y_n - u_n) / 31
    ##order of error for 1 timeStepsPerHour is O(h^5), so total ~O(h^4)
    
    ##plotting here
    
    print('Regular Plot, timeStepsPerHour = '+timeStepsPerHour)
    plotIndex = 0
    
    Plotter.plotThis22(S[plotIndex], I[plotIndex], R[plotIndex], 'h = 1h: The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    ##now a comparison with simplified theory: no recovery, no vaccinations, no movement, only 1 area:
    ##theoretical equation: dS/dt = -B*S*I/N, where B is the infection constant, and N is total population
    ##solved, we get: t_f - t_i = ln[ S_f*(N - S_i) / ( S_i*( N-S_f )) ]
    
    print('Simplified theory comparison for runtime of  = ' + runLength)
    
    (Ss, Is, Rs) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    (Ss, Is, Rs) = rungeKuttaChange(Ss, Is, Rs, timeStepsPerHour, humanContactsPerHour[0] * infectionProbPerContact, recovRate*0, vaccinationsPerHour*0, movementChances*0)
    
    Plotter.plotThis22(Ss[plotIndex], Is[plotIndex], Rs[plotIndex], 'The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    print('Using the theory to calculate time passed, it should be: ' + numpy.log( (Ss[0][runLength - 1] * ( (Ss[0][0] + Is[0][0]) - Ss[0][0])) / (Ss[0][0] * ( (Ss[0][0] + Is[0][0]) - Ss[0][runLength - 1] )) ) + ' hours. In the simulation this change was over: ' +runLength+ ' hours.')
    
    ##now a view of 1 area with recovery and vaccination, but without movement:
    
    print('Simplified runtime of  = ' + runLength)
    
    (Ss2, Is2, Rs2) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    (Ss2, Is2, Rs2) = rungeKuttaChange(Ss2, Is2, Rs2, timeStepsPerHour, humanContactsPerHour[0] * infectionProbPerContact, recovRate, vaccinationsPerHour, movementChances*0)
    
    Plotter.plotThis22(Ss2[plotIndex], Is2[plotIndex], Rs2[plotIndex], 'The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    ##now with double the timeStepsPerHour (should be approx ~2^4 times the error)
    
    timeStepsPerHour = timeStepsPerHour * 2
    
    print('Error-Comparison Plot, timeStepsPerHour = '+timeStepsPerHour)
    
    (S2, I2, R2) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    (S2, I2, R2) = rungeKuttaChange(S2, I2, R2, timeStepsPerHour, humanContactsPerHour[0] * infectionProbPerContact, recovRate, vaccinationsPerHour, movementChances)
    
    Plotter.plotThis22(S2[plotIndex], I2[plotIndex], R2[plotIndex], 'h = 2h: The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    ##now with triple the timeStepsPerHour (should be approx ~2^4 times the error)
    
    timeStepsPerHour = timeStepsPerHour * 3/2
    
    print('Error-Comparison Plot, timeStepsPerHour = '+timeStepsPerHour)
    
    (S3, I3, R3) = setInitialPops(runLength, numPlaces, placePop, infectedFrac)
    
    (S3, I3, R3) = rungeKuttaChange(S3, I3, R3, timeStepsPerHour, humanContactsPerHour[0] * infectionProbPerContact, recovRate, vaccinationsPerHour, movementChances)
    
    Plotter.plotThis22(S3[plotIndex], I3[plotIndex], R3[plotIndex], 'h = 3h: The Spread of the Plague in Area ' +places[plotIndex][0])
    plt.show()
    plt.clf()
    
    print('Difference in values for endpoints in infected pop: between h and 2h' + numpy.abs( I[runLength - 1] - I2[runLength - 1] ) )
    print('Difference in values for endpoints in infected pop: between 2h and 3h' + numpy.abs( I3[runLength - 1] - I2[runLength - 1] ) )
    print('Difference in values for endpoints in infected pop: between h and 3h' + numpy.abs( I[runLength - 1] - I3[runLength - 1] ) )
    
    
    print('done')
    #ended
pass