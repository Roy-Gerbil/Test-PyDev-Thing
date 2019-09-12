import matplotlib.pyplot as plt
import numpy

def plotThis22 (yS, yI, yR, plotTitle): ##S pop, I pop, R pop, index/name of location
    ts = numpy.zeros(yS.shape[0]) ##an array of the times, could probably optimize by moving this into the main function, but it doesn't matter
    for i in range(0, ts.shape[0] - 1):
        ts[i+1] = ts[i] + 1/24 ## divide by 24 to make units of hours into days
    
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(ts, yS, 'C1', label='S Pop')
    plt.plot(ts, yI, 'C2', label='I Pop')
    plt.plot(ts, yR, 'C3', label='R Pop')
    plt.xlabel('Time (days)')
    plt.ylabel('Population (${10^{3}}$ People)')
    plt.title(plotTitle)
    plt.legend()
    
    
def plotThis22Multi (yS, yI, yR, places, plotTotal): ##S pop, I pop, R pop, index/name of location
    ts = numpy.zeros(yS[0].shape[0]) ##an array of the times, could probably optimize by moving this into the main function, but it doesn't matter
    for i in range(0, ts.shape[0] - 1):
        ts[i+1] = ts[i] + 1/24 ## divide by 24 to make units of hours into days
    
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    
    
    for i in range(0, yS.shape[0]):
        plt.subplot( (221+i) )
        plt.plot(ts, yS[i]/1000, 'C1', label='S Pop')
        plt.plot(ts, yI[i]/1000, 'C2', label='I Pop')
        plt.plot(ts, yR[i]/1000, 'C3', label='R Pop')
        plt.plot(ts, (yR[i]+yI[i]+yS[i])/1000, 'C4', label='Total Pop')
        plt.xlabel('Time (days)')
        plt.ylabel('Population (${10^{3}}$ People)')
        plt.title(places[i][0])
        
    #plot total pop
    
    if(plotTotal):
        St = 0
        It = 0
        Rt = 0
        for i in range(0, yS.shape[0]):
            St = yS[i] + St
            It = yI[i] + It
            Rt = yR[i] + Rt
        plt.subplot( (224) )
        plt.plot(ts, St/1000, 'C1', label='S Pop')
        plt.plot(ts, It/1000, 'C2', label='I Pop')
        plt.plot(ts, Rt/1000, 'C3', label='R Pop')
        plt.plot(ts, (Rt+It+St)/1000, 'C4', label='Total Pop')
        plt.xlabel('Time (days)')
        plt.ylabel('Population (${10^{3}}$ People)')
        plt.title('Total Population')
        plt.legend()