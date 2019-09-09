import matplotlib.pyplot as plt
import numpy

def plotThis22 (xs, ys):
    plt.plot(xs, ys, '-')
    plt.xlabel('Population (${10^{3}}$ People)')
    plt.ylabel('Time (hours)')
    plt.title('The Title')