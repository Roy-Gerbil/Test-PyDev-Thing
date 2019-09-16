import matplotlib.pyplot as plt
import numpy

def plotThis22 (yS, yI, yR, places): ##S pop, I pop, R pop, index/name of location
    ts = numpy.zeros(yS.shape[0]) ##an array of the times, could probably optimize by moving this into the main function, but it doesn't matter
    for i in range(0, ts.shape[0] - 1):
        ts[i+1] = ts[i] + 1/24 ## divide by 24 to make units of hours into days
    
    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(ts, yS/1000, 'C1', label='S Pop', linewidth = '3')
    plt.plot(ts, yI/1000, 'C2', label='I Pop', linewidth = '3')
    plt.plot(ts, yR/1000, 'C3', label='R Pop', linewidth = '3')
    plt.plot(ts, (yS+yI+yR)/1000, 'C4', label='Total Pop',  linewidth = '3')
    plt.xlim(0,ts[ts.shape[0] - 1] + 1/24)
    plt.xlabel('Time (days)', fontsize = '13')
    plt.ylabel('Population (${10^{3}}$ People)', fontsize = '13')
    plt.title('Spread of Disease in ' + places[0][0] + ', $\\omega = 0$', fontsize = '17')
    plt.legend()
    
    
def plotThis22Multi (yS, yI, yR, places, plotTotal): ##S pop, I pop, R pop, index/name of location
    ts = numpy.zeros(yS[0].shape[0]) ##an array of the times, could probably optimize by moving this into the main function, but it doesn't matter
    for i in range(0, ts.shape[0] - 1):
        ts[i+1] = ts[i] + 1/24 ## divide by 24 to make units of hours into days
    
    
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    #plt.style.use('dark_background')
    plt.suptitle('Spread of Disease Throughout Some Cities, LD-Movement Included', fontsize=20)
    for i in range(0, 3):
        plt.subplot( (221+i) ) ##currently just 4 at once
        plt.plot(ts, yS[i]/1000, 'C1', label='S Pop', linewidth = '3')
        plt.plot(ts, yI[i]/1000, 'C2', label='I Pop', linewidth = '3')
        plt.plot(ts, yR[i]/1000, 'C3', label='R Pop', linewidth = '3')
        plt.plot(ts, (yR[i]+yI[i]+yS[i])/1000, 'C4', label='Total Pop', linewidth = '3')
        plt.xlabel('Time (days)', fontsize = '13')
        plt.ylabel('Population (${10^{3}}$ People)', fontsize = '13')
        plt.title(places[i][0], fontsize = '17')
        
    #plot total pop
    
    if(plotTotal):
        St = 0
        It = 0
        Rt = 0
        for i in range(0, 3):
            St = yS[i] + St
            It = yI[i] + It
            Rt = yR[i] + Rt
        plt.subplot( (224) )
        plt.plot(ts, St/1000, 'C1', label='S Pop', linewidth = '3')
        plt.plot(ts, It/1000, 'C2', label='I Pop', linewidth = '3')
        plt.plot(ts, Rt/1000, 'C3', label='R Pop', linewidth = '3')
        plt.plot(ts, (Rt+It+St)/1000, 'C4', label='Total Pop', linewidth = '3')
        plt.xlabel('Time (days)', fontsize = '13')
        plt.ylabel('Population (${10^{3}}$ People)', fontsize = '13')
        plt.title('Total Population with LD-Movement', fontsize = '13')
        plt.legend()