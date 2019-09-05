import matplotlib.pyplot as plt
import numpy

def createAPlot (xs, ys):
    plt.plot(xs, ys)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('The Title')
    plt.show