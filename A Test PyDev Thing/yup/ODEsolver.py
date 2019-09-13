# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-

"""

Spyder Editor



This is a temporary script file.

"""

import numpy



from  scipy import *





places =[[" Malmö",316588], [ "Lund", 91940],  ["Copenhagen", 602481]]

4/11

#Pop



#CityM = [[N11,N12,N13],[N21,N22,N23], [N31,N32,N33]]



numpy.zeros(3)

P_I = 1/11    #Probability that the person at random is infected: assumed that the chance is a quarter of that for a healthy one

P_S = 4/11

P_R = 4/11 



N1 = places[0][1]

N2 = places[1][1]

N3 = places[2][1]



N12 = 2000



N21 = 4000



N13= 2500



N31 = 4200



#Number of initial susceptible in the cities

S1 = 240000 

S2= 480000

S3 = 72000



# Number of initial infected in the cities

I1 = 40000

I2 = 80000

I3 = 8000



#Number of initial reecoved in the cities

R1= N1- I1

R2= N2- I2

R3= N3- I3



T= 20 * 24



T0 = 0 



def setInitialPops(runLength, numPlaces, placePop, infectedFrac): ###S[0][1] is S pop for location 0 at hour 1



    S = numpy.zeros((numPlaces,runLength)) ##susceptible



    I = numpy.zeros((numPlaces,runLength)) ## infected



    R = numpy.zeros((numPlaces,runLength)) ##recovered



    



    for i in range(0,numPlaces):



        I[i][0] = numpy.int(placePop[i]*infectedFrac[i])



        R[i][0] = 0



        S[i][0] = placePop[i] - I[i][0]






def rungeKuttaIterator(Sfull,Ifull,Rfull,timeStepsPerHour,B,A,G,M,MLD,Places): 

    h = 1/timeStepsPerHour

    

    numPlaces = Sfull.shape[0]



    runLength = Sfull.shape[1]

    

    Stemp = numpy.zeros(numPlaces) + 0.0



    Itemp = numpy.zeros(numPlaces) + 0.0



    Rtemp = numpy.zeros(numPlaces) + 0.0


    SLDtemp = 0.0
    
    ILDtemp = 0.0
    
    RLDtemp = 0.0
    

    

    for pl in range(0, numPlaces):



        



        Stemp[pl] = Sfull[pl][0]*1.0



        Itemp[pl] = Ifull[pl][0]*1.0



        Rtemp[pl] = Rfull[pl][0]*1.0




    LDMP = [] #list containing all long distance moving packages
    for hour in range(0, runLength):



        

        for t in range(0, timeStepsPerHour):

            

            
            MovingPackage = [] # Indices [0],[1] and [2] are respectively S, I and R pop. in the packages. Index [3] is destination of the package and [4] is time until the arrival. 
            for pl in range(0, numPlaces): ##The current temp values are stored in the history of the 'actual' values

                SLDtemp = 0.0
    
                ILDtemp = 0.0
    
                RLDtemp = 0.0
    
                # This is where create the Long Distance movement packages.
                for pl2 in range(0,numplaces):
                    
                    for transport in range(0,3):
                        if( transport = 0 ): #AutoMobile Transportation average speed of 100 km/h. 0.5 accounts for 50 % travelling by automobile
                            MovingPackage = [0.5*h*[M[0][pl2][pl][t]],0.5*h*[M[1][pl2][pl][t]], 0.5*h*[M[2][pl2][pl][t]], pl2, numpy.sqrt((places[pl][3]-places[pl2][3])**2 + (places[pl][4]-places[pl2][4])**2  )*98/100]                        
                        if( transport = 1): #Train average speed of 140km/h 
                            MovingPackage = [0.3*h*[M[0][pl2][pl][t]],0.3*h*[M[1][pl2][pl][t]],0.3* h*[M[2][pl2][pl][t]], pl2, numpy.sqrt((places[pl][3]-places[pl2][3])**2 + (places[pl][4]-places[pl2][4])**2  )*140/100]
                        if(transport = 2): # Airplane 400 km/h (making it 200 km/h slower to account for transit to and from the plane)
                            MovingPackage = [0.2*h*[M[0][pl2][pl][t]],0.2*h*[M[1][pl2][pl][t]],0.2* h*[M[2][pl2][pl][t]], pl2, numpy.sqrt((places[pl][3]-places[pl2][3])**2 + (places[pl][4]-places[pl2][4])**2  )*400/100]
                        
                        SLDtemp = SLDtemp - MovingPackage[0]
                        ILDtemp = ILDtemp - MovingPackage[1]
                        RLDtemp = RLDtemp - MovingPackage[2]
                        LDMP.append(MovingPackage)
        
                
                # Runge Kutta for Susceptible 

    

                F1 = h * (- (B * Stemp[pl] * Itemp[pl]/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - G*Stemp[pl])

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):
                                    

                        F1 = F1 + h*((M[0][pl2][pl][t] * Stemp[pl2]) - M[0][pl][pl2][t]*Stemp[pl] M[0][pl][pl2][t]]]) 

                        

                F2 = h * (-(B * (Stemp[pl]+F1/2) * Itemp[pl]/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - G*(Stemp[pl]+F1/2))

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        F2 = F2 + h*(((M[0][pl2][pl][t] * Stemp[pl2]) - M[0][pl][pl2][t]*(Stemp[pl] + F1/2))) 

            

                F3 = h * ((- (B * (Stemp[pl]+F2/2) * Itemp[pl]/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - G*(Stemp[pl]+F2/2))) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        F3 = F3 + h*(((M[0][pl2][pl][t] * Stemp[pl2]) - M[0][pl][pl2][t]*(Stemp[pl] + F2/2))) 

                        

                F4 = h * ((- (B * (Stemp[pl]+F3) * Itemp[pl]/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - G*(Stemp[pl]+F3))) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        F4 = F4 + h*(((M[0][pl2][pl][t] * Stemp[pl2]) - M[0][pl][pl2][t]*(Stemp[pl] + F3))) 

                        

                        
                #Runge Kutta for Infected
                        

                G1 = h * ( (B * Stemp[pl] * Itemp[pl]/(Stemp[pl] + Itemp[pl]+Rtemp[pl]) - A*Itemp[pl] ))

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        G1 = G1 + h*((M[1][pl2][pl][t] * Itemp[pl2]) - M[1][pl][pl2][t]*Itemp[pl]) 

                        

                G2 = h * ((B * Stemp[pl] * (Itemp[pl]+ (G1/2))/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - A*(Itemp[pl]+G1/2))

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        G2 = G2 + h*(((M[1][pl2][pl][t] * Itemp[pl2]) - M[1][pl][pl2][t]*(Itemp[pl] + G1/2))) 

            

                G3 = h * (( (B * Stemp[pl] * (Itemp[pl]+ (G2/2))/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - A*(Itemp[pl]+G2/2))) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        G3 = G3 + h*(((M[1][pl2][pl][t] * Itemp[pl2]) - M[1][pl][pl2][t]*(Itemp[pl] + G2/2))) 

                        

                G4 = h * (( (B * Stemp[pl] * (Itemp[pl]+ G3)/(Stemp[pl] + Itemp[pl]+Rtemp[pl])) - A*(Itemp[pl]+G3))) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        G4 = G4 + h*(((M[0][pl2][pl][t] * Itemp[pl2]) - M[0][pl][pl2][t]*(Itemp[pl] + G3)))  

            

            

                #Runge Kutta for recovered

                K1 = h * ( (G* Stemp[pl])  + A*Itemp[pl]) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        K1 = K1 + h*((M[2][pl2][pl][t] * Rtemp[pl2]) - M[2][pl][pl2][t]*Rtemp[pl])  

                K2 = h * ( (G* Stemp[pl])  + A*Itemp[pl]) 

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        K2 = K2 + h*((M[2][pl2][pl][t] * Rtemp[pl2]) - M[2][pl][pl2][t]*(Rtemp[pl]+(K1/2)))  

                K3 = h * ( (G* Stemp[pl])  + A*Itemp[pl])

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        K3 = K3 + h*((M[2][pl2][pl][t] * Rtemp[pl2]) - M[2][pl][pl2][t]*(Rtemp[pl]+(K2/2)))  

                K4 = h * ( (G* Stemp[pl])  + A*Itemp[pl])

                for pl2 in range(0,numPlaces):

                    if(pl2 !=pl):

                        K4 = K4 + h*((M[2][pl2][pl][t] * Rtemp[pl2]) - M[2][pl][pl2][t]*(Rtemp[pl]+K3))  

                    

               
                
                for l in range(0,len(LDMP)):
                    if( LDMP[l][4]<= 0 and pl = LDMP[l][3]):
                        SLDtemp = SLDtemp + LDMP[l][0]
                        ILDtemp = ILDtemp + LDMP[l][1]
                        RLDtemp = RLDtemp + LDMP[l][2]
                        LDMP.del(l)

                Stemp[pl] = Stemp[pl] + 1/6*(F1 + 2*F2 + 2*F3 + F4) + SLDtemp



                



                Itemp[pl] = Itemp[pl] + 1/6*(G1 + 2*G2 + 2*G3 + G4) + ILDtemp



                



                Rtemp[pl] = Rtemp[pl] + 1/6*(K1 + 2*K2 + 2*K3 + K4) + RLDtemp

                

                
        for l in range(0,len(LDMP)):
            LDMP[l][4] = LDMP[l][4] - 1/timeStepsPerHour
            


        print(hour)

        if(hour!= (runLength-1)): ##because we are adding changes from 0

            for pl in range(0, numPlaces): ##The current temp values are stored in the history of the 'actual' values

    

                #print ('S'+str(pl)+':'+str(Stemp[pl]))

                Sfull[pl][hour+1] = numpy.int(Stemp[pl])

                #print ('I'+str(pl)+':'+str(Itemp[pl]))

                Ifull[pl][hour+1] = numpy.int(Itemp[pl])

                #print ('R'+str(pl)+':'+str(Rtemp[pl]))

                Rfull[pl][hour+1] = numpy.int(Rtemp[pl])
    


    

    return (Sfull, Ifull, Rfull)
