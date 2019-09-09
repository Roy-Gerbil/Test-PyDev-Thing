import matplotlib.pyplot as plt
import numpy

def plotThis22 (ts, yS, yI, yR):
    plt.plot(ts, yS, '-')
    plt.plot(ts, yI, 'ot')
    plt.plot(ts, yR, 'rs')
    plt.xlabel('Population (${10^{3}}$ People)')
    plt.ylabel('Time (hours)')
    plt.title('The Title')