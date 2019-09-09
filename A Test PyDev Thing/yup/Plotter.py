import matplotlib.pyplot as plt
import numpy

def plotThis22 (yS, yI, yR, areaname):
    ts = numpy.zeros(yS.shape()[0])
    for i in range(0, ts.shape()[0] - 1):
        ts[i+1] = ts[i] + 1/24
    
    plt.plot(ts, yS, 'b-', label='S Pop')
    plt.plot(ts, yI, 'ot', label='I Pop')
    plt.plot(ts, yR, 'rs', label='R Pop')
    plt.xlabel('Population (${10^{3}}$ People)')
    plt.ylabel('Time (days)')
    plt.title('The Spread of the Plague in Area ' + areaname)
    plt.legend()