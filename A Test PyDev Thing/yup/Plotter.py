import matplotlib.pyplot as plt
import numpy

def plotThis22 (yS, yI, yR, plotTitle): ##S pop, I pop, R pop, index/name of location
    ts = numpy.zeros(yS.shape()[0])
    for i in range(0, ts.shape()[0] - 1):
        ts[i+1] = ts[i] + 1/24
    
    plt.plot(ts, yS, 'C1', label='S Pop')
    plt.plot(ts, yI, 'C2', label='I Pop')
    plt.plot(ts, yR, 'C3', label='R Pop')
    plt.xlabel('Population (${10^{3}}$ People)')
    plt.ylabel('Time (days)')
    plt.title(plotTitle)
    plt.legend()