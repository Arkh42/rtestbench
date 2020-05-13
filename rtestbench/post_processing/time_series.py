
# Scientific computations
import numpy
import pandas

# Plot library
import matplotlib.pyplot as plt

# String matching
from difflib import SequenceMatcher



# def plot2(*signals, )

def plot(time_data, y_data, title='Time series plot', **kwargs):
    """Plot the time series.

    Assumes that data is a pandas' Series object.
    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    """
    plt.figure()

    plt.plot(time_data, y_data, **kwargs)
    
    plt.xlabel(time_data.name)
    plt.ylabel(y_data.name)
    plt.title(title)
    
    plt.grid(True)

    # plt.show()

def multiplot(time_data, y_data, ylabel, title='Time series plot', **kwargs):
    """Plot the time series of several signals.

    Assumes that y_data is a list of pandas' Series objects sharing the same 'x' axis time_data.
    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    """
    plt.figure()
    legend = list()

    for data in y_data:
        plt.plot(time_data, data)
        legend.append(data.name)

    plt.xlabel(time_data.name)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(legend)

    plt.grid(True)


def remove_offset(y, offset='mean'):
    if offset == 'mean':
        return y - y.mean()
    elif offset == 'first':
        return y - y.iloc[0]

