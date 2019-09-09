import matplotlib.pyplot as plt
import numpy

def plotThis22 (ts, yS, yI, yR, areaname):
    plt.plot(ts, yS, 'b-', label='S Pop')
    plt.plot(ts, yI, 'ot', label='I Pop')
    plt.plot(ts, yR, 'rs', label='R Pop')
    plt.xlabel('Population (${10^{3}}$ People)')
    plt.ylabel('Time (hours)')
    plt.title('The Spread of the Plague in Area ' + areaname)
    plt.legend()